#!/usr/bin/env python3
"""
Generate audio for R03 questions only (Set 3 — Service & Social).
"""

import os
import sys
import requests
import base64
import wave
import struct
import subprocess
from pathlib import Path

# Load API key from .env file
def load_env():
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith('INWORLD_API_KEY='):
                    return line.split('=', 1)[1].strip()
    return None

API_KEY = load_env() or os.getenv('INWORLD_API_KEY')
if not API_KEY:
    print("Error: Set INWORLD_API_KEY environment variable or add it to .env file")
    sys.exit(1)

API_URL = "https://api.inworld.ai/tts/v1/voice"
VOICE_FEMALE = "Olivia"  # American female
VOICE_MALE = "Dennis"    # American male
MODEL_ID = "inworld-tts-1.5-mini"
SAMPLE_RATE = 48000
PAUSE_BETWEEN_TURNS = 0.8  # seconds
LEADING_SILENCE = 0.5  # seconds

# R03 Set - Service & Social (30 questions)
QUESTIONS = {
    "R03-01": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'd like to order a coffee, please."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "What size would you like?"}
        ]
    },
    "R03-02": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "Happy birthday! I hope you have a wonderful day."},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "Thank you so much! That's very kind of you."}
        ]
    },
    "R03-03": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'd like to book a hotel room for next weekend."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "How many nights will you be staying?"}
        ]
    },
    "R03-04": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I really enjoyed the movie we saw together last night."},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "I'm glad you liked it! I thought it was great too."}
        ]
    },
    "R03-05": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "Excuse me, do you accept credit cards?"},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Yes, we accept all major credit cards."}
        ]
    },
    "R03-06": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I heard you're moving to a new apartment. How exciting!"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "Yes, I'm really looking forward to it. The new place is much closer to campus."}
        ]
    },
    "R03-07": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'd like to return this item. It's defective."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Do you have your receipt with you?"}
        ]
    },
    "R03-08": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "Congratulations on your graduation!"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "Thank you! I can't believe it's finally here."}
        ]
    },
    "R03-09": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'd like to schedule a haircut appointment."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "What day works best for you?"}
        ]
    },
    "R03-10": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I wanted to thank you for helping me move last weekend. I really appreciate it."},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "You're welcome! I was happy to help. How are you settling into the new place?"}
        ]
    },
    "R03-11": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "Do you have this shirt in a larger size?"},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Let me check for you. What size are you looking for?"}
        ]
    },
    "R03-12": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I'm so sorry I forgot to call you back yesterday."},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "That's okay. I understand you've been busy."}
        ]
    },
    "R03-13": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'd like to exchange this for a different color."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Sure. What color would you prefer?"}
        ]
    },
    "R03-14": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I hope you feel better soon!"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "Thank you! I'm starting to feel a bit better already."}
        ]
    },
    "R03-15": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'm not happy with the service I received. The food took over an hour to arrive."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "I sincerely apologize for the delay. Let me speak with the manager about this."}
        ]
    },
    "R03-16": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I wanted to let you know that I got accepted into graduate school!"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "That's fantastic news! Congratulations!"}
        ]
    },
    "R03-17": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "Can I pay with cash?"},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Of course. Cash is accepted."}
        ]
    },
    "R03-18": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I'm really sorry I couldn't attend your presentation yesterday."},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "That's all right. I understand you had other commitments."}
        ]
    },
    "R03-19": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'd like to make a complaint about my recent order."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "I'm sorry to hear that. Can you tell me what happened?"}
        ]
    },
    "R03-20": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I wanted to apologize for my comment at the meeting. It was inappropriate."},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "I appreciate you saying that. We can move past this."}
        ]
    },
    "R03-21": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "Is this item on sale?"},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Yes, it's 30% off this week."}
        ]
    },
    "R03-22": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I heard you got promoted! That's amazing!"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "Thank you! I'm really excited about the new role."}
        ]
    },
    "R03-23": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'd like to cancel my subscription."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "I can help with that. Can I have your account number?"}
        ]
    },
    "R03-24": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I wanted to thank you for being so supportive during my job search. Your advice really helped."},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "I'm so glad I could help! How is everything going now?"}
        ]
    },
    "R03-25": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "Do you offer delivery?"},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Yes, we deliver within a 5-mile radius."}
        ]
    },
    "R03-26": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I'm really sorry I forgot your birthday. I feel terrible about it."},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "Don't worry about it. I know you've been busy lately."}
        ]
    },
    "R03-27": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "I'd like to upgrade my phone plan."},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "What features are you looking for in the upgrade?"}
        ]
    },
    "R03-28": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I wanted to apologize for not responding to your messages. I've been dealing with some personal issues."},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "I understand. Is everything okay now?"}
        ]
    },
    "R03-29": {
        "topic": "Service",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_MALE, "text": "Can I get a refund for this purchase?"},
            {"speaker": "speaker2", "voice": VOICE_FEMALE, "text": "Do you have the receipt with you?"}
        ]
    },
    "R03-30": {
        "topic": "Social",
        "dialogue": [
            {"speaker": "speaker1", "voice": VOICE_FEMALE, "text": "I wanted to thank you for helping me prepare for my interview. Your tips were really helpful!"},
            {"speaker": "speaker2", "voice": VOICE_MALE, "text": "You're welcome! I'm glad I could help. How did it go?"}
        ]
    }
}

def synthesize_sentence(text, voice_id):
    """Call Inworld TTS API for a single sentence. Returns raw PCM audio bytes."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {API_KEY}"
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
    try:
        resp = requests.post(API_URL, headers=headers, json=data, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        audio_bytes = base64.b64decode(result["audioContent"])
        # Strip WAV header if present
        if len(audio_bytes) > 44 and audio_bytes[:4] == b'RIFF':
            audio_bytes = audio_bytes[44:]
        return audio_bytes
    except requests.exceptions.RequestException as e:
        print(f"Error synthesizing '{text[:50]}...': {e}")
        if hasattr(e, 'response') and hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        raise

def generate_silence(duration_seconds):
    """Generate raw PCM silence (16-bit mono)."""
    num_samples = int(SAMPLE_RATE * duration_seconds)
    return b'\x00\x00' * num_samples

def combine_to_wav(audio_chunks, output_wav):
    """Combine raw PCM chunks into a WAV file."""
    import wave
    with wave.open(str(output_wav), 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(SAMPLE_RATE)
        for chunk in audio_chunks:
            wf.writeframes(chunk)

def wav_to_mp3(wav_path, mp3_path):
    """Convert WAV to MP3 using ffmpeg."""
    import subprocess
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", str(wav_path),
            "-codec:a", "libmp3lame", "-qscale:a", "2",
            str(mp3_path)
        ], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error converting to MP3: {e.stderr.decode()}")
        return False
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please install ffmpeg.")
        return False

def generate_audio(question_id, dialogue_data):
    """Generate audio for a single dialogue."""
    print(f"\nGenerating audio for {question_id}...")
    
    audio_chunks = []
    
    # Add leading silence
    audio_chunks.append(generate_silence(LEADING_SILENCE))
    
    # Synthesize each turn
    for i, turn in enumerate(dialogue_data["dialogue"]):
        print(f"  Synthesizing: {turn['speaker']} - '{turn['text'][:50]}...'")
        audio_data = synthesize_sentence(turn['text'], turn['voice'])
        audio_chunks.append(audio_data)
        
        # Add pause between turns (except after last turn)
        if i < len(dialogue_data["dialogue"]) - 1:
            audio_chunks.append(generate_silence(PAUSE_BETWEEN_TURNS))
    
    # Save to file
    output_dir = Path(__file__).parent.parent / 'audio' / 'listening'
    output_dir.mkdir(parents=True, exist_ok=True)
    temp_wav = output_dir / f"LCR-{question_id}.tmp.wav"
    output_path = output_dir / f"LCR-{question_id}.mp3"
    
    # Combine into WAV
    combine_to_wav(audio_chunks, temp_wav)
    
    # Convert to MP3
    if wav_to_mp3(temp_wav, output_path):
        temp_wav.unlink()  # Remove temp file
        file_size = output_path.stat().st_size / 1024  # KB
        print(f"  ✓ Saved: {output_path} ({file_size:.1f} KB)")
        return True
    else:
        return False

def main():
    print("Generating audio for R03 'Listen and Choose a Response' questions...")
    print(f"Using API: {API_URL}")
    print(f"Voices: {VOICE_MALE} (male), {VOICE_FEMALE} (female)")
    
    success_count = 0
    total = len(QUESTIONS)
    
    for question_id, dialogue_data in QUESTIONS.items():
        if generate_audio(question_id, dialogue_data):
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"Complete: {success_count}/{total} audio files generated")
    if success_count < total:
        print(f"Failed: {total - success_count} files")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
