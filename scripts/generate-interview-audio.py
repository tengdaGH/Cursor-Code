#!/usr/bin/env python3
"""
Generate Take an Interview audio prompts using the Inworld TTS API.
Each question is a separate MP3 file.

Usage:
  export INWORLD_API_KEY=your_key_here
  python3 scripts/generate-interview-audio.py [--set SET_ID]

  If --set SET_ID is given, only that set is generated (e.g. --set ZJ1).
"""

import base64
import os
import subprocess
import sys
import time
import wave
from pathlib import Path

import requests


def load_env():
    """Load INWORLD_API_KEY from project root .env if present."""
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        with open(env_path, "r") as f:
            for line in f:
                if line.startswith("INWORLD_API_KEY="):
                    return line.split("=", 1)[1].strip()
    return None

# Import voice configuration
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from inworld_voices import get_voice_id_for_interview_set
except ImportError:
    print("Warning: Could not import inworld_voices, using default voice", file=sys.stderr)
    def get_voice_id_for_interview_set(set_id):
        return "Olivia"  # Fallback

# ==================== CONFIG ====================
API_URL = "https://api.inworld.ai/tts/v1/voice"
MODEL_ID = "inworld-tts-1.5-mini"
SAMPLE_RATE = 48000
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "audio", "interview")

# ==================== INTERVIEW QUESTIONS ====================
INTERVIEW_SETS = {
    "PT1": {
        "label": "Practice Test 1 — Work-Life Balance",
        "questions": [
            "Thank you for participating. Today, I'd like to ask you some questions about your work-life balance. First, can you share one or two strategies that you use that you think are effective in managing your work-life balance?",
            "I see. Many companies are now developing programs to help employees manage work-life balance. Would programs like this affect your interest in working for a particular company? Why or why not?",
            "Interesting. Some companies also offer flexible working hours or remote work options to help employees achieve a better work-life balance, but they are concerned that these options would reduce employee attention to tasks or engagement in the workplace. Do you think such programs are a good strategy for companies? Why or why not?",
            "Good points. Lastly, looking to the future, do you think people's attitudes towards work-life balance will change? For example, do you think people will prioritize personal life over work, or work over personal life? Explain your thoughts.",
        ]
    },
    "SC1": {
        "label": "Set 2 — Scholarship Application",
        "questions": [
            "Welcome, and thank you for applying for this scholarship. To start, could you tell me a little about your academic background and what you are currently studying?",
            "That's great. What made you choose this particular field of study, and what do you hope to achieve with your degree in the future?",
            "I see. Some people believe that financial support, like scholarships, should be based purely on academic performance, while others think it should also consider factors like community involvement and leadership. What is your view on this?",
            "That's an interesting perspective. Finally, how do you think higher education will change in the next ten years? For example, do you think online learning will become more common than traditional classroom learning? Why or why not?",
        ]
    },
    "OA1": {
        "label": "Set 3 — Outdoor Activities",
        "questions": [
            "Thanks for joining us today. I'd like to ask you about outdoor activities. First, what kinds of outdoor recreational activities do you enjoy, and how often do you participate in them?",
            "That sounds interesting. Some people say outdoor activities are important for maintaining good physical and mental health. Based on your own experience, would you agree with that? Can you give me an example?",
            "I see. In many cities, local governments are investing money in building parks, hiking trails, and sports facilities. However, some people argue that this money would be better spent on other public services, like healthcare or education. What do you think about this?",
            "That's a thoughtful answer. Looking ahead, do you think technology, for example, virtual reality or fitness apps, will change the way people engage in outdoor activities? Will people spend more or less time outdoors in the future? Explain your reasoning.",
        ]
    },
    "CL1": {
        "label": "Set 4 — Campus Life",
        "questions": [
            "Thank you for taking the time to participate in this survey. First, can you describe a typical day for you on campus? For example, what activities do you usually do between classes?",
            "That's helpful. Which campus resource or facility do you find most useful, and why? It could be the library, student center, gym, or anything else.",
            "Interesting. Some universities are considering reducing the number of in-person student services and moving them online to cut costs. For example, academic advising and counseling sessions would be conducted through video calls instead of face-to-face meetings. Do you think this is a good idea? Why or why not?",
            "Good points. Finally, how do you think the university campus experience will change for students in the next five to ten years? Do you think campuses will still play an important role in students' lives, or will more learning happen remotely? Explain your thoughts.",
        ]
    },
    "ZJ1": {
        "label": "真题 — 2026年1月21日 考试 (Health and Habits)",
        "questions": [
            "First, do you have any specific routines or practices you use to maintain your physical health? If so, what are they?",
            "Can you describe any eating choices or habits that you follow to stay healthy? Give details to explain it.",
            "If you could make one important change to your diet or exercise habits to stay healthy, what would it be? Why would you make that choice?",
            "Some people believe that mental health is just as equally important as physical health. Do you agree or disagree with this viewpoint? Why?",
        ]
    }
}


def synthesize_sentence(text, api_key, voice_id):
    """Call Inworld TTS API for a single sentence. Returns raw PCM audio bytes."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {api_key}"
    }
    data = {
        "text": text,
        "voice_id": voice_id,
        "model_id": MODEL_ID,
        "audio_config": {
            "audio_encoding": "LINEAR16",
            "sample_rate_hertz": SAMPLE_RATE
        }
    }
    resp = requests.post(API_URL, headers=headers, json=data, timeout=30)
    resp.raise_for_status()
    result = resp.json()
    audio_bytes = base64.b64decode(result["audioContent"])
    # Strip WAV header if present
    if len(audio_bytes) > 44 and audio_bytes[:4] == b'RIFF':
        audio_bytes = audio_bytes[44:]
    return audio_bytes


def pcm_to_wav(pcm_bytes, wav_path):
    """Write raw PCM bytes to a WAV file."""
    with wave.open(wav_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(pcm_bytes)


def wav_to_mp3(wav_path, mp3_path):
    """Convert WAV to MP3 using ffmpeg."""
    subprocess.run([
        "ffmpeg", "-y", "-i", wav_path,
        "-codec:a", "libmp3lame", "-qscale:a", "2",
        mp3_path
    ], capture_output=True, check=True)


def main():
    api_key = load_env() or os.getenv("INWORLD_API_KEY")
    if not api_key:
        print("Error: Set INWORLD_API_KEY environment variable or add it to .env", file=sys.stderr)
        sys.exit(1)

    only_set = None
    if len(sys.argv) > 1 and sys.argv[1] == "--set" and len(sys.argv) > 2:
        only_set = sys.argv[2]
        if only_set not in INTERVIEW_SETS:
            print(f"Error: Unknown set ID '{only_set}'. Choose from: {list(INTERVIEW_SETS.keys())}", file=sys.stderr)
            sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    sets_to_run = {k: v for k, v in INTERVIEW_SETS.items() if only_set is None or k == only_set}
    total = sum(len(s["questions"]) for s in sets_to_run.values())
    count = 0

    for set_id, set_data in sets_to_run.items():
        # Get voice ID for this interview set
        voice_id = get_voice_id_for_interview_set(set_id)
        print(f"\n=== {set_data['label']} ===")
        print(f"Using voice: {voice_id}")
        
        for qi, text in enumerate(set_data["questions"]):
            count += 1
            q_num = qi + 1
            filename = f"TI-{set_id}-Q{q_num}"
            mp3_path = os.path.join(OUTPUT_DIR, f"{filename}.mp3")
            wav_path = os.path.join(OUTPUT_DIR, f"{filename}.wav")

            print(f"  [{count}/{total}] Q{q_num}: {text[:60]}...")

            try:
                pcm = synthesize_sentence(text, api_key, voice_id)
                pcm_to_wav(pcm, wav_path)
                wav_to_mp3(wav_path, mp3_path)
                os.remove(wav_path)
                print(f"         -> {mp3_path}")
            except Exception as e:
                print(f"  ERROR: {e}", file=sys.stderr)
                sys.exit(1)

            # Small delay to avoid rate limiting
            time.sleep(0.5)

    print(f"\nDone! Generated {count} audio files in {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
