#!/usr/bin/env python3
"""
Generate audio for "Listen to an Announcement" practice questions.
Creates monologic announcements with American accent voice.
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
LEADING_SILENCE = 0.5  # seconds

# Announcement sets - A01 Set (5 announcements)
ANNOUNCEMENTS = {
    "A01-01": {
        "title": "Library Hours Change",
        "context": "Campus Library",
        "voice": VOICE_FEMALE,
        "text": "Good morning, everyone. This is a message from the campus library. We wanted to inform you that starting next Monday, the library will be extending its weekend hours. The library will now be open from 8 AM to 10 PM on Saturdays and Sundays, instead of the previous 9 AM to 6 PM schedule. This change is being made to better accommodate students who prefer to study on weekends. Additionally, the quiet study areas on the third and fourth floors will now be available 24 hours a day, seven days a week, for students who need a quiet place to work. Please note that you will need your student ID card to access the building after regular hours. If you have any questions, please visit the library information desk or check our website. Thank you."
    },
    "A01-02": {
        "title": "Course Registration Reminder",
        "context": "Academic Affairs Office",
        "voice": VOICE_MALE,
        "text": "Attention all students. This is a reminder from the Academic Affairs Office regarding course registration for the upcoming semester. Registration will begin next Monday at 8 AM and will remain open until Friday at 5 PM. Please note that registration is done online through the student portal. You will need your student ID number and password to log in. We strongly recommend that you register as early as possible, as popular courses tend to fill up quickly. If you encounter any technical difficulties during registration, please contact the IT help desk immediately. Additionally, if you need to make changes to your schedule after registration closes, you will need to submit a formal request to your academic advisor. Thank you for your attention."
    },
    "A01-03": {
        "title": "Campus Event Cancellation",
        "context": "Student Activities Office",
        "voice": VOICE_FEMALE,
        "text": "Hello, this is a message from the Student Activities Office. We regret to inform you that the outdoor concert scheduled for this Saturday has been cancelled due to severe weather forecasts. The event will be rescheduled for next Saturday at the same time and location. All tickets purchased for this weekend's event will be valid for the rescheduled date. If you are unable to attend the new date, you can request a full refund by contacting the ticket office before next Wednesday. We apologize for any inconvenience this may cause. For updates and more information, please check the Student Activities website or follow us on social media. Thank you for your understanding."
    },
    "A01-04": {
        "title": "Parking Policy Update",
        "context": "Campus Security",
        "voice": VOICE_MALE,
        "text": "Good afternoon. This is an important announcement from Campus Security regarding parking regulations. Effective immediately, all vehicles parked on campus must display a valid parking permit. Permits can be purchased online through the campus portal or in person at the security office. The cost is fifty dollars per semester. Please note that vehicles without permits will be subject to fines, and repeated violations may result in your vehicle being towed. Additionally, we have designated new parking areas near the science building and the student center to accommodate increased demand. These areas are clearly marked with blue signs. If you have any questions about parking regulations or need assistance purchasing a permit, please visit the security office or call our help line. Thank you."
    },
    "A01-05": {
        "title": "Dining Hall Menu Changes",
        "context": "Campus Dining Services",
        "voice": VOICE_FEMALE,
        "text": "Hello, this is a message from Campus Dining Services. We wanted to let you know about some exciting changes coming to the main dining hall. Starting next week, we will be introducing new vegetarian and vegan options at every meal. These options will be clearly labeled and available at a dedicated station. We have also expanded our salad bar to include more fresh vegetables and fruits. In response to student feedback, we are reducing the use of processed foods and focusing on fresh, locally sourced ingredients whenever possible. Additionally, we will be offering extended hours on weekdays, with the dining hall now open until 9 PM instead of 8 PM. We hope these changes will better serve our diverse student community. If you have any dietary concerns or suggestions, please speak with our dining services manager. Thank you."
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

def generate_audio(announcement_id, announcement_data):
    """Generate audio for a single announcement."""
    print(f"\nGenerating audio for {announcement_id}...")
    print(f"  Title: {announcement_data['title']}")
    print(f"  Voice: {announcement_data['voice']}")
    print(f"  Text length: {len(announcement_data['text'])} characters")
    
    audio_chunks = []
    
    # Add leading silence
    audio_chunks.append(generate_silence(LEADING_SILENCE))
    
    # Synthesize the announcement text
    print(f"  Synthesizing announcement text...")
    audio_data = synthesize_sentence(announcement_data['text'], announcement_data['voice'])
    audio_chunks.append(audio_data)
    
    # Save to file
    output_dir = Path(__file__).parent.parent / 'audio' / 'listening'
    output_dir.mkdir(parents=True, exist_ok=True)
    temp_wav = output_dir / f"LA-{announcement_id}.tmp.wav"
    output_path = output_dir / f"LA-{announcement_id}.mp3"
    
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
    print("Generating audio for 'Listen to an Announcement' questions...")
    print(f"Using API: {API_URL}")
    print(f"Voices: {VOICE_MALE} (male), {VOICE_FEMALE} (female)")
    
    success_count = 0
    total = len(ANNOUNCEMENTS)
    
    for announcement_id, announcement_data in ANNOUNCEMENTS.items():
        if generate_audio(announcement_id, announcement_data):
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"Complete: {success_count}/{total} audio files generated")
    if success_count < total:
        print(f"Failed: {total - success_count} files")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
