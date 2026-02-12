#!/usr/bin/env python3
"""
Generate conversation audio files using the Inworld TTS API.
Creates dialogues with two speakers (male and female, both American accents).

Usage:
  export INWORLD_API_KEY=your_key_here
  python3 scripts/generate-conversation-audio.py --conversation C01-01 -o audio/listening/LC-C01-01.mp3
"""

import argparse
import base64
import os
import subprocess
import sys
import time
import wave

import requests

# ==================== CONFIG ====================
API_URL = "https://api.inworld.ai/tts/v1/voice"
# American voices: Olivia (female), Dennis (male)
VOICE_FEMALE = "Olivia"  # American female voice
VOICE_MALE = "Dennis"    # American male voice
MODEL_ID = "inworld-tts-1.5-mini"
SAMPLE_RATE = 48000
PAUSE_BETWEEN_TURNS = 0.8  # seconds between speaker turns
LEADING_SILENCE = 1.0       # seconds before conversation starts

# ==================== CONVERSATION DEFINITIONS ====================
CONVERSATIONS = {
    "C01-01": {
        "title": "Finding a Piano to Practice",
        "topic": "Education",
        "turns": [
            {"speaker": "student", "voice": VOICE_MALE, "text": "Uh, I almost forgot to return the keys to the music practice room. Uh, it's been a long day."},
            {"speaker": "administrator", "voice": VOICE_FEMALE, "text": "Okay, thanks. You know, very soon that's not gonna be an issue anymore. The school is planning to distribute electronic key cards to students, so you won't have to pick up and drop off the key every time you use the practice rooms."},
            {"speaker": "student", "voice": VOICE_MALE, "text": "Oh, that'll be good. But what would really make life easier would be if it were possible to use a room earlier in the day. I can never get anything before 9 in the evening."},
            {"speaker": "administrator", "voice": VOICE_FEMALE, "text": "Really? Why's that?"},
            {"speaker": "student", "voice": VOICE_MALE, "text": "So, if you're not getting a degree in music, which I'm not, the only times practice rooms are available to you are early in the morning and late in the evening. My major course of study is biology, so I have lab classes and they're early in the morning, so I don't have a lot of energy left when I finally do get to practice."},
            {"speaker": "administrator", "voice": VOICE_FEMALE, "text": "Well, you aren't the first to complain about lack of availability. You know, now that the weather's been better, I often hear students just practicing outside in the courtyard."},
            {"speaker": "student", "voice": VOICE_MALE, "text": "Yeah, but they're not playing pianos."},
            {"speaker": "administrator", "voice": VOICE_FEMALE, "text": "Ah, that's true. But doesn't every resident hall have a piano in the lounge area?"},
            {"speaker": "student", "voice": VOICE_MALE, "text": "Yeah, but when people are studying, which is a lot of the time, I don't think my playing would be much appreciated. Besides, you know, you usually want some privacy to practice in a quiet, soundproofed place."},
            {"speaker": "administrator", "voice": VOICE_FEMALE, "text": "Well, I think there actually may be some good news on the way, but it wouldn't go into effect until at least next year, as you said, students in the music department get priority on using the rooms."},
            {"speaker": "student", "voice": VOICE_MALE, "text": "Right?"},
            {"speaker": "administrator", "voice": VOICE_FEMALE, "text": "But tell me, are you currently taking private music lessons?"},
            {"speaker": "student", "voice": VOICE_MALE, "text": "Yeah?"},
            {"speaker": "administrator", "voice": VOICE_FEMALE, "text": "Well, they're considering giving students from other departments an incentive to sign up for lessons with instructors from our department, so if you study with one of our people, it'd give you priority on the rooms, equal to that of the music students. Well, that's the plan anyway."},
            {"speaker": "student", "voice": VOICE_MALE, "text": "Seriously? because my instructor, Eric Miller, actually is one of your graduate students."},
            {"speaker": "administrator", "voice": VOICE_FEMALE, "text": "Good. Plus, we're hoping we'll be able to increase the hours for open on the weekends, that'd make things more convenient too."},
            {"speaker": "student", "voice": VOICE_MALE, "text": "All sounds promising! Oh, well, I have your ear. I should mention that the piano in room 220 really needs tuning."},
            {"speaker": "administrator", "voice": VOICE_FEMALE, "text": "Ah, really? Someone comes in every few months to retune them all."},
            {"speaker": "student", "voice": VOICE_MALE, "text": "Well, that one needs to be serviced again, trust me."},
        ]
    }
}


def synthesize_sentence(text, voice_id, api_key):
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
    parser = argparse.ArgumentParser(description="Generate conversation audio via Inworld TTS")
    parser.add_argument("--conversation", "-c", required=True, choices=list(CONVERSATIONS),
                        help="Conversation ID to generate (e.g., C01-01)")
    parser.add_argument("-o", "--output", required=True, help="Output MP3 path")
    args = parser.parse_args()

    api_key = os.getenv("INWORLD_API_KEY")
    if not api_key:
        print("Error: Set INWORLD_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    conversation = CONVERSATIONS[args.conversation]
    audio_chunks = []

    # Leading silence
    audio_chunks.append(generate_silence(LEADING_SILENCE))

    print(f"Generating conversation: {conversation['title']}")
    print(f"Total turns: {len(conversation['turns'])}")

    for i, turn in enumerate(conversation['turns']):
        speaker_name = turn['speaker']
        voice_id = turn['voice']
        text = turn['text']
        print(f"  [{i+1}/{len(conversation['turns'])}] {speaker_name} ({voice_id}): {text[:60]}...")
        
        try:
            pcm = synthesize_sentence(text, voice_id, api_key)
            audio_chunks.append(pcm)
        except Exception as e:
            print(f"  ERROR on turn {i+1}: {e}", file=sys.stderr)
            sys.exit(1)

        # Add pause between turns (not after the last one)
        if i < len(conversation['turns']) - 1:
            audio_chunks.append(generate_silence(PAUSE_BETWEEN_TURNS))

        # Small delay to avoid rate limiting
        time.sleep(0.3)

    # Ensure output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Save as WAV then convert to MP3
    wav_path = args.output.replace('.mp3', '.wav')
    print(f"Combining {len(conversation['turns'])} turns into WAV...")
    combine_to_wav(audio_chunks, wav_path)

    print(f"Converting to MP3...")
    wav_to_mp3(wav_path, args.output)

    # Clean up WAV
    os.remove(wav_path)

    print(f"Done! Saved: {args.output}")


if __name__ == "__main__":
    main()
