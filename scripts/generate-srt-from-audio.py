#!/usr/bin/env python3
"""
Generate SRT subtitle file from audio using OpenAI Whisper.
Each sentence typically has ~1–1.5s silence between them; Whisper segments on natural pauses.

Usage:
  python generate-srt-from-audio.py path/to/audio.mp3
  python generate-srt-from-audio.py LR-S04-dining-hall.mp3 --output LR-S04-dining-hall.srt

Requires: pip install openai-whisper
Also: brew install ffmpeg
"""

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Generate SRT from audio using Whisper")
    parser.add_argument("audio", help="Path to audio file (mp3, wav, flac, etc.)")
    parser.add_argument("-o", "--output", help="Output SRT path (default: same name as audio)")
    parser.add_argument("-m", "--model", default="base.en", help="Whisper model: tiny.en, base.en, small.en, medium.en (default: base.en)")
    parser.add_argument("--language", default="en", help="Language code (default: en)")
    args = parser.parse_args()

    audio_path = Path(args.audio)
    if not audio_path.exists():
        print(f"Error: File not found: {audio_path}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output) if args.output else audio_path.with_suffix(".srt")

    try:
        import whisper
    except ImportError:
        print("Error: Whisper not installed. Run: pip install openai-whisper", file=sys.stderr)
        sys.exit(1)

    print(f"Loading model '{args.model}'...")
    model = whisper.load_model(args.model)

    print(f"Transcribing {audio_path}...")
    result = model.transcribe(
        str(audio_path),
        language=args.language,
        word_timestamps=False,
        verbose=False,
    )

    # Build SRT from segments
    segments = result.get("segments", [])
    if not segments:
        print("Warning: No segments detected. Check audio quality.", file=sys.stderr)
        sys.exit(1)

    def to_srt_time(seconds):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds % 1) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    lines = []
    for i, seg in enumerate(segments, 1):
        start = seg["start"]
        end = seg["end"]
        text = seg["text"].strip()
        if not text:
            continue
        lines.append(f"{i}")
        lines.append(f"{to_srt_time(start)} --> {to_srt_time(end)}")
        lines.append(text)
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved: {output_path} ({len(segments)} segments)")


if __name__ == "__main__":
    main()
