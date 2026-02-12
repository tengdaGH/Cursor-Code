#!/usr/bin/env python3
"""
Generate Listen & Repeat audio files using the Inworld TTS API.
Synthesizes each sentence individually, then concatenates with silence gaps.

Usage:
  export INWORLD_API_KEY=your_key_here
  python3 generate-audio-inworld.py --set S05 -o LR-S05-lab-safety.mp3
  python3 generate-audio-inworld.py --set S06 -o LR-S06-art-history-renaissance.mp3

Requires: pip install requests  (+ ffmpeg for MP3 conversion)
"""

import argparse
import base64
import io
import os
import struct
import subprocess
import sys
import time
import wave

import requests

# Import voice configuration
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from inworld_voices import get_voice_id_for_lr_set
except ImportError:
    print("Warning: Could not import inworld_voices, using default voice", file=sys.stderr)
    def get_voice_id_for_lr_set(set_id):
        return "Olivia"  # Fallback

# ==================== SENTENCE SETS ====================
S05_SENTENCES = [
    "Good afternoon, and welcome to the biology lab.",
    "Before we begin, I'd like to go over some important safety rules.",
    "Safety goggles must be worn at all times during experiments.",
    "Lab coats are available in the cabinet next to the door.",
    "Never eat or drink anything while you are working in the laboratory.",
    "All chemicals should be handled with gloves to avoid skin contact.",
    "The emergency eyewash station is located right behind the instructor's desk.",
    "If you accidentally spill any chemicals, notify your instructor immediately.",
    "Fire extinguishers are mounted on the wall near both exits of this room.",
    "Make sure you know the location of the nearest emergency exit before starting your work.",
    "Used materials must be disposed of in the designated waste containers, not in the regular trash.",
    "Biological samples should always be stored in sealed containers and clearly labeled with your name.",
    "When using a microscope, make sure the lens is clean before placing your slide on the stage.",
    "Each group is responsible for cleaning their workstation at the end of every lab session.",
    "If the fire alarm goes off during an experiment, turn off all equipment and exit through the nearest door.",
    "You are required to complete the online safety quiz before you will be allowed to participate in any lab activities.",
    "Proper ventilation is essential when working with volatile substances, so always use the fume hood provided.",
    "In the event of a chemical burn, immediately rinse the affected area with cold water for at least fifteen minutes.",
    "All lab reports must follow the standard format outlined in the course syllabus and be submitted by the end of the week.",
    "If you have any questions about today's procedures or the equipment we'll be using, please raise your hand and I'll come over to help.",
]

S06_SENTENCES = [
    "Good morning, everyone, and welcome to Art History 201.",
    "Today we'll be looking at the evolution of painting techniques during the Italian Renaissance.",
    "The Renaissance marked a dramatic shift from the flat, symbolic imagery of the medieval period.",
    "Artists began to experiment with perspective, which allowed them to create a convincing illusion of depth on a flat surface.",
    "One of the earliest examples of linear perspective can be found in Masaccio's fresco, The Holy Trinity.",
    "By using a single vanishing point, Masaccio was able to give the viewer the impression of looking into an actual architectural space.",
    "Another key development was the use of chiaroscuro, a technique that involves strong contrasts between light and dark.",
    "Leonardo da Vinci refined this approach in works like the Mona Lisa, where the soft gradation of tones creates a remarkably lifelike appearance.",
    "It's worth noting that Renaissance painters didn't simply abandon all earlier traditions overnight.",
    "Many continued to work within the framework of religious commissions while gradually incorporating these new naturalistic techniques.",
    "The patronage system played a crucial role in shaping artistic production, as wealthy families like the Medici commissioned works to demonstrate their power and cultural sophistication.",
    "Raphael's School of Athens is often considered one of the finest examples of High Renaissance composition and spatial harmony.",
    "What makes this painting particularly remarkable is the way Raphael arranged dozens of figures within a complex architectural setting without creating a sense of visual clutter.",
    "The introduction of oil paint, which originated in Northern Europe, gave artists far greater control over color blending and surface texture.",
    "Unlike tempera, which dries very quickly, oil paint remains workable for much longer, allowing for subtle adjustments and layered effects.",
    "Titian, one of the leading painters of the Venetian school, exploited this property of oil paint to achieve an extraordinary richness and warmth of color.",
    "It's important to recognize that the technical innovations of the Renaissance did not emerge in isolation but were closely tied to broader intellectual movements, including humanism and the revival of classical learning.",
    "Scholars have argued that the growing emphasis on observation and empirical study in the sciences directly influenced how painters approached the representation of the natural world.",
    "For next week's class, I'd like you to read the chapter on Michelangelo's Sistine Chapel ceiling and think about how it reflects the themes we discussed today.",
    "If anyone would like to explore this topic further, I've placed a list of recommended readings and museum resources on the course website, and I encourage you to take advantage of them before the midterm examination.",
]

SENTENCE_SETS = {"S05": S05_SENTENCES, "S06": S06_SENTENCES}

# ==================== CONFIG ====================
API_URL = "https://api.inworld.ai/tts/v1/voice"
MODEL_ID = "inworld-tts-1.5-mini"
SAMPLE_RATE = 48000
SILENCE_DURATION = 1.5  # seconds between sentences
LEADING_SILENCE = 2.0   # seconds before first sentence


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


def generate_silence(duration_sec):
    """Generate raw PCM silence (16-bit mono)."""
    num_samples = int(SAMPLE_RATE * duration_sec)
    return b'\x00\x00' * num_samples


def combine_to_wav(audio_chunks, output_wav):
    """Combine raw PCM chunks into a WAV file."""
    with wave.open(output_wav, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(SAMPLE_RATE)
        for chunk in audio_chunks:
            wf.writeframes(chunk)


def wav_to_mp3(wav_path, mp3_path):
    """Convert WAV to MP3 using ffmpeg."""
    subprocess.run([
        "ffmpeg", "-y", "-i", wav_path,
        "-codec:a", "libmp3lame", "-qscale:a", "2",
        mp3_path
    ], capture_output=True, check=True)


def main():
    parser = argparse.ArgumentParser(description="Generate LR audio via Inworld TTS")
    parser.add_argument("--set", "-s", required=True, choices=list(SENTENCE_SETS),
                        help="Sentence set to generate (S05 or S06)")
    parser.add_argument("-o", "--output", required=True, help="Output MP3 path")
    args = parser.parse_args()

    api_key = os.getenv("INWORLD_API_KEY")
    if not api_key:
        print("Error: Set INWORLD_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    # Get voice ID for this set
    voice_id = get_voice_id_for_lr_set(args.set)
    print(f"Using voice: {voice_id} for set {args.set}")

    sentences = SENTENCE_SETS[args.set]
    audio_chunks = []

    # Leading silence
    audio_chunks.append(generate_silence(LEADING_SILENCE))

    for i, text in enumerate(sentences):
        print(f"  [{i+1}/{len(sentences)}] {text[:60]}...")
        try:
            pcm = synthesize_sentence(text, api_key, voice_id)
            audio_chunks.append(pcm)
        except Exception as e:
            print(f"  ERROR on sentence {i+1}: {e}", file=sys.stderr)
            sys.exit(1)

        # Add silence between sentences (not after the last one)
        if i < len(sentences) - 1:
            audio_chunks.append(generate_silence(SILENCE_DURATION))

        # Small delay to avoid rate limiting
        time.sleep(0.3)

    # Save as WAV then convert to MP3
    wav_path = args.output.replace('.mp3', '.wav')
    print(f"Combining {len(sentences)} sentences into WAV...")
    combine_to_wav(audio_chunks, wav_path)

    print(f"Converting to MP3...")
    wav_to_mp3(wav_path, args.output)

    # Clean up WAV
    os.remove(wav_path)

    print(f"Done! Saved: {args.output}")


if __name__ == "__main__":
    main()
