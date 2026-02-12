#!/usr/bin/env python3
"""
Verify Inworld TTS Voice IDs

This script queries the Inworld API to list all available voices
and helps verify that the voice IDs in inworld_voices.py are correct.

Usage:
  export INWORLD_API_KEY=your_key_here
  python3 scripts/verify-voice-ids.py
"""

import os
import sys
import base64
import requests

API_URL = "https://api.inworld.ai/tts/v1/voices?filter=language=en"

def main():
    api_key = os.getenv("INWORLD_API_KEY")
    if not api_key:
        print("Error: Set INWORLD_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    headers = {
        "Authorization": f"Basic {api_key}"
    }

    try:
        resp = requests.get(API_URL, headers=headers, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        
        print("=" * 60)
        print("Available Inworld TTS Voices (English)")
        print("=" * 60)
        print()
        
        voices = result.get("voices", [])
        if not voices:
            print("No voices found.")
            return
        
        # Group by tags if available
        female_voices = []
        male_voices = []
        other_voices = []
        
        for voice in voices:
            voice_id = voice.get("voiceId", "")
            display_name = voice.get("displayName", "")
            description = voice.get("description", "")
            tags = voice.get("tags", [])
            
            voice_info = {
                "id": voice_id,
                "name": display_name,
                "desc": description,
                "tags": tags
            }
            
            if "female" in [t.lower() for t in tags]:
                female_voices.append(voice_info)
            elif "male" in [t.lower() for t in tags]:
                male_voices.append(voice_info)
            else:
                other_voices.append(voice_info)
        
        if female_voices:
            print("FEMALE VOICES:")
            print("-" * 60)
            for v in female_voices:
                print(f"  Voice ID: {v['id']:15} | {v['name']}")
                print(f"    Description: {v['desc']}")
                if v['tags']:
                    print(f"    Tags: {', '.join(v['tags'])}")
                print()
        
        if male_voices:
            print("MALE VOICES:")
            print("-" * 60)
            for v in male_voices:
                print(f"  Voice ID: {v['id']:15} | {v['name']}")
                print(f"    Description: {v['desc']}")
                if v['tags']:
                    print(f"    Tags: {', '.join(v['tags'])}")
                print()
        
        if other_voices:
            print("OTHER VOICES:")
            print("-" * 60)
            for v in other_voices:
                print(f"  Voice ID: {v['id']:15} | {v['name']}")
                print(f"    Description: {v['desc']}")
                if v['tags']:
                    print(f"    Tags: {', '.join(v['tags'])}")
                print()
        
        print("=" * 60)
        print("\nTo verify your preferred voices, check if these IDs exist:")
        print("  Female: Ashley, Deborah, Sarah")
        print("  Male: Dennis, Mark")
        print("  Male Admin/Prof: Edward, Craig, Carter")
        print()
        
    except Exception as e:
        print(f"Error querying API: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
