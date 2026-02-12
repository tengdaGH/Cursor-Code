#!/usr/bin/env python3
"""
Generate audio for "Listen to an Academic Talk" practice (A2–C1 tiers, 2 talks per tier).

VOICE DIRECTION (context of usage for Inworld):
- These are short academic lectures for TOEFL listening practice. The speaker is a professor
  or instructor addressing students. Delivery should be clear, at a moderate pace, with
  natural emphasis on key terms—not rushed, not monotone. Think "engaged lecturer" not
  "announcer." We achieve this by:
  1. Casting the most fitting voice per talk (see inworld_voices.ACADEMIC_TALK_VOICES).
  2. Synthesizing sentence-by-sentence and inserting brief pauses (0.35s) so prosody is
     natural and phrase-boundaries are clear.
  3. Optional: slightly slower speaking rate for clarity (if API supports it).

Usage:
  export INWORLD_API_KEY=your_key
  python3 scripts/generate-academic-talk-audio.py

Output: audio/listening/LT-{tier}-{01|02}.mp3 (e.g. LT-A2-01.mp3, LT-C1-02.mp3).
Requires: requests, ffmpeg
"""

import os
import re
import sys
import time
import wave
import base64
import subprocess
from pathlib import Path

import requests

# Load API key from .env
def load_env():
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.startswith("INWORLD_API_KEY="):
                    return line.split("=", 1)[1].strip()
    return None

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from inworld_voices import get_voice_id_for_academic_talk
except ImportError:
    def get_voice_id_for_academic_talk(talk_id):
        return "Carter"

API_KEY = load_env() or os.getenv("INWORLD_API_KEY")
if not API_KEY:
    print("Error: Set INWORLD_API_KEY or add to .env")
    sys.exit(1)

API_URL = "https://api.inworld.ai/tts/v1/voice"
MODEL_ID = "inworld-tts-1.5-mini"
SAMPLE_RATE = 48000
LEADING_SILENCE = 0.5   # seconds before first sentence
PAUSE_BETWEEN_SENTENCES = 0.35  # seconds (natural lecture pacing)

# All 8 talks: id, title, context, text (must match toefl-listening-academic-talk-practice.html)
ACADEMIC_TALKS = [
    {
        "id": "A2-01",
        "title": "The Four Seasons",
        "context": "Science class",
        "text": "Hello, everyone. Today we will talk about the four seasons: spring, summer, autumn, and winter. Why do we have different seasons? The main reason is that the Earth is tilted. When your part of the Earth is tilted toward the Sun, you get more sunlight and it is warmer. That is summer. When your part is tilted away from the Sun, you get less sunlight and it is colder. That is winter. In spring and autumn, we are in between, so the weather is mild. In the north, summer is usually from June to August. Winter is from December to February. In spring, flowers grow and leaves come back. In autumn, leaves turn red and yellow and fall from the trees. So the tilt of the Earth and the way it moves around the Sun give us our seasons.",
    },
    {
        "id": "A2-02",
        "title": "A Day at School",
        "context": "Orientation",
        "text": "Good morning. I will tell you what a typical day at our school looks like. School starts at eight thirty. First, you go to your classroom. The teacher checks your name. Then you have three lessons in the morning. Each lesson is forty-five minutes. At twelve o'clock we have lunch. You can eat in the cafeteria or bring your own food. After lunch, you have two more lessons. School finishes at three fifteen. On Monday and Wednesday, you can stay for sports or music. Those activities start at half past three. You need to bring a notebook, a pen, and your books every day. If you have questions, ask your teacher or go to the office. Thank you.",
    },
    {
        "id": "B1-01",
        "title": "How Libraries Work",
        "context": "Library orientation",
        "text": "Today I will explain how the library works. To borrow a book, you need a library card. You can get one at the desk. You show your card, and we give you the book. You can keep most books for two weeks. If you need more time, you can renew them online or in person. If you return a book after the due date, you pay a fine. The fine is usually a small amount per day. We also have computers you can use for free. You can search for books on our website. If the book you want is in another building, we can bring it here for you. That is called a reserve. It takes one or two days. Do you have any questions?",
    },
    {
        "id": "B1-02",
        "title": "Why We Have Weekends",
        "context": "Social studies class",
        "text": "Why do we have weekends? A weekend is usually Saturday and Sunday. In the past, many people worked six days a week. Then laws changed. Workers wanted more rest and time with their families. So in many countries, Saturday and Sunday became free days. That gave people two days to relax, do hobbies, or go out. Schools and offices are closed. Shops may be open. Today we take weekends for granted, but they are a result of social change. Some countries have different days off. For example, in some places Friday and Saturday are the weekend. The idea is the same: a regular break from work or school.",
    },
    {
        "id": "B2-01",
        "title": "Photosynthesis and Light",
        "context": "Biology class",
        "text": "Good morning. Today I want to talk briefly about how plants use light to make food. This process is called photosynthesis. In photosynthesis, plants take in carbon dioxide from the air and water from the soil. They use energy from sunlight to convert these into glucose, which is a type of sugar, and they release oxygen as a byproduct. The key part of the plant where this happens is the chloroplast. Inside the chloroplast you find chlorophyll, the green pigment that absorbs light. So when we say plants are green, it is because chlorophyll reflects green light and absorbs mainly red and blue. Without enough light, photosynthesis slows down, which is why plants grown in dim conditions often look pale or weak. Understanding this process is essential for topics like agriculture and climate, because plants absorb a lot of the carbon dioxide we produce.",
    },
    {
        "id": "B2-02",
        "title": "Roman Aqueducts",
        "context": "History class",
        "text": "Today we will look at one of the Romans' greatest engineering achievements: the aqueduct. Aqueducts were structures designed to bring fresh water from distant sources into cities. The Romans did not invent the idea of moving water through channels, but they built aqueducts on a scale that had never been seen before. Some of their aqueducts ran for dozens of miles. The key to their success was the use of a slight downward slope over the whole distance. Gravity did the work; water flowed from the source to the city without pumps. The channels were often covered to keep the water clean and to reduce evaporation. When the path had to cross a valley, the Romans built arches to support the channel at the right height. Many of these arches are still standing today. The water supplied public fountains, baths, and sometimes private homes, and it was crucial for the growth and health of Roman cities.",
    },
    {
        "id": "C1-01",
        "title": "Climate Feedback Loops",
        "context": "Environmental science",
        "text": "In this lecture I want to introduce the concept of feedback loops in the climate system. A feedback loop is when a change in one part of the system leads to more change in the same direction. Take the ice-albedo effect. Ice and snow reflect a lot of sunlight back into space. When global temperatures rise, ice melts and exposes darker ocean or land. Those surfaces absorb more heat, so temperatures rise further. That is a positive feedback: warming leads to more warming. Another example is water vapour. Warmer air holds more moisture, and water vapour is a greenhouse gas, so more vapour can amplify the initial warming. Not all feedbacks are positive. For instance, more plant growth in some regions might take up more carbon dioxide. But the net effect of the main feedbacks is to amplify climate change. Understanding these mechanisms is critical for predicting how the climate will respond to rising emissions.",
    },
    {
        "id": "C1-02",
        "title": "Historical Causation",
        "context": "History seminar",
        "text": "Today we are going to discuss how historians explain major changes in history. It is tempting to point to a single event—a battle, a law, a discovery—and say that it caused everything that followed. But historians usually argue that big changes have multiple causes. Economic conditions, ideas, technology, and chance all play a role. For example, the rise of industrialisation in Europe depended on new machines, but also on access to raw materials, labour, capital, and political stability. No one factor alone is sufficient. Historians also distinguish between short-term and long-term causes. A revolution might be triggered by a specific crisis, but the causes may have built up over decades. So when you read or write history, look for several causes and how they interact, rather than a single turning point.",
    },
]


def split_sentences(text):
    """Split text into sentences (rough: . ! ? and trim). Keeps phrases after colons/semicolons attached when reasonable."""
    text = text.strip()
    if not text:
        return []
    # Split on sentence-ending punctuation followed by space or end
    parts = re.split(r'(?<=[.!?])\s+', text)
    return [p.strip() for p in parts if p.strip()]


def synthesize_sentence(text, voice_id):
    """Call Inworld TTS for one sentence. Returns raw PCM (16-bit mono)."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {API_KEY}",
    }
    audio_config = {
        "audio_encoding": "LINEAR16",
        "sample_rate_hertz": SAMPLE_RATE,
    }
    payload = {
        "text": text,
        "voice_id": voice_id,
        "model_id": MODEL_ID,
        "audio_config": audio_config,
    }
    resp = requests.post(API_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    result = resp.json()
    audio_bytes = base64.b64decode(result["audioContent"])
    if len(audio_bytes) > 44 and audio_bytes[:4] == b"RIFF":
        audio_bytes = audio_bytes[44:]
    return audio_bytes


def generate_silence(duration_seconds):
    """Raw PCM silence (16-bit mono)."""
    n = int(SAMPLE_RATE * duration_seconds)
    return b"\x00\x00" * n


def combine_to_wav(chunks, wav_path):
    """Write list of PCM chunks to WAV file."""
    with wave.open(str(wav_path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        for ch in chunks:
            wf.writeframes(ch)


def wav_to_mp3(wav_path, mp3_path):
    """Convert WAV to MP3 with ffmpeg."""
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(wav_path),
            "-codec:a", "libmp3lame", "-qscale:a", "2",
            str(mp3_path),
        ],
        capture_output=True,
        check=True,
    )


def generate_talk(talk):
    """Generate one academic talk: sentence-by-sentence with pauses."""
    talk_id = talk["id"]
    title = talk["title"]
    text = talk["text"]
    voice_id = get_voice_id_for_academic_talk(talk_id)

    print(f"\n[{talk_id}] {title}")
    print(f"  Voice: {voice_id}  (context: {talk['context']})")

    sentences = split_sentences(text)
    print(f"  Sentences: {len(sentences)}")

    chunks = []
    chunks.append(generate_silence(LEADING_SILENCE))

    for i, sent in enumerate(sentences):
        print(f"    [{i+1}/{len(sentences)}] {sent[:55]}...")
        try:
            pcm = synthesize_sentence(sent, voice_id)
            chunks.append(pcm)
        except requests.RequestException as e:
            print(f"    ERROR: {e}")
            if hasattr(e, "response") and e.response is not None and hasattr(e.response, "text"):
                print(e.response.text[:500])
            raise
        if i < len(sentences) - 1:
            chunks.append(generate_silence(PAUSE_BETWEEN_SENTENCES))
        time.sleep(0.25)  # rate limit

    out_dir = Path(__file__).parent.parent / "audio" / "listening"
    out_dir.mkdir(parents=True, exist_ok=True)
    file_id = talk_id.replace("-", "")  # A2-01 -> A201? No: we need LT-A2-01.mp3
    # talk_id is already "A2-01", "B2-02" etc. Output: LT-A2-01.mp3
    base = f"LT-{talk_id}"
    wav_path = out_dir / f"{base}.tmp.wav"
    mp3_path = out_dir / f"{base}.mp3"

    combine_to_wav(chunks, wav_path)
    wav_to_mp3(wav_path, mp3_path)
    wav_path.unlink()
    size_kb = mp3_path.stat().st_size / 1024
    print(f"  ✓ {mp3_path.name} ({size_kb:.1f} KB)")
    return True


def main():
    print("Academic Talk audio — voice-directed lecture delivery")
    print("Context: TOEFL listening; clear, moderate pace; sentence-by-sentence for natural prosody.")
    print(f"API: {API_URL}")

    ok = 0
    for talk in ACADEMIC_TALKS:
        try:
            if generate_talk(talk):
                ok += 1
        except Exception as e:
            print(f"  FAILED: {e}")
    print(f"\nDone: {ok}/{len(ACADEMIC_TALKS)} files generated.")


if __name__ == "__main__":
    main()
