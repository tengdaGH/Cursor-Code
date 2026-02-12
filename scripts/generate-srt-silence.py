#!/usr/bin/env python3
"""
Generate SRT from audio using ffmpeg silence detection.
Use when you have ~1–1.5s silence between sentences and know the sentence text.

Usage:
  python generate-srt-silence.py audio.mp3 sentences.txt -o output.srt
  python generate-srt-silence.py audio.mp3 --set S04 -o output.srt

Requires: ffmpeg
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

# Sentences from lr-question-bank.md (S04 Campus Dining Hall)
S04_SENTENCES = [
    "Hi there, welcome to the dining hall.",
    "We serve breakfast, lunch, and dinner.",
    "Breakfast starts at seven thirty every morning.",
    "You can pick up a tray at the entrance.",
    "The salad bar is on your left when you walk in.",
    "Hot meals are served at the counter straight ahead.",
    "Today's special is grilled chicken with roasted vegetables.",
    "All drinks are included with your meal plan.",
    "You can refill your water bottle at the station over there.",
    "Please return your tray to the drop-off area when you're done.",
    "We have a vegetarian section with fresh options every day.",
    "If you have any food allergies, please check the labels on each dish.",
    "The dessert table is next to the beverage station near the window.",
    "We try to use locally grown ingredients whenever they are available.",
    "Students with a meal plan can eat here up to three times a day.",
    "Guest passes can be purchased at the front desk for five dollars each.",
    "The dining hall gets really busy around noon, so you might want to come a little earlier.",
    "On weekends, we offer a special brunch menu from ten in the morning until two in the afternoon.",
    "If you have any suggestions about the menu, there's a feedback box right next to the exit.",
    "We hope you enjoy your meals here, and please don't hesitate to ask the staff if you need anything at all.",
]

SENTENCE_SETS = {"S04": S04_SENTENCES}


def run_silencedetect(audio_path: str, silence_duration: float = 1.0, noise_dB: float = -30) -> list:
    """Run ffmpeg silencedetect and return list of (silence_start, silence_end)."""
    cmd = [
        "ffmpeg", "-i", audio_path,
        "-af", f"silencedetect=noise={noise_dB}dB:d={silence_duration}",
        "-f", "null", "-",
        "-nostats", "-loglevel", "info"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    stderr = (result.stderr or "") + (result.stdout or "")

    silences = []
    for line in stderr.splitlines():
        m = re.search(r"silence_start: ([\d.]+)", line)
        if m:
            silences.append({"start": float(m.group(1)), "end": None})
            continue
        m = re.search(r"silence_end: ([\d.]+)", line)
        if m and silences and silences[-1]["end"] is None:
            silences[-1]["end"] = float(m.group(1))

    return [s for s in silences if s["end"] is not None]


def silences_to_speech_segments(silences: list, total_duration: float, has_leading_silence: bool = True) -> list:
    """
    Convert silence periods to speech segments using midpoints of silence gaps.

    Key idea: use the MIDPOINT of each silence gap as the boundary between
    sentences. This avoids clipping the tail of the previous sentence or the
    onset of the next sentence.

    has_leading_silence: True if the audio starts with silence before sentence 1.
                         False if sentence 1 starts right at the beginning.
    """
    if not silences:
        return [{"start": 0.0, "end": total_duration}]

    segments = []

    if has_leading_silence and len(silences) >= 2:
        # First silence is leading silence; skip it.
        # Sentence 1 starts at midpoint of first silence gap.
        # Sentence boundaries use midpoints of subsequent silences.
        for i in range(len(silences) - 1):
            mid_start = (silences[i]["start"] + silences[i]["end"]) / 2
            mid_end = (silences[i + 1]["start"] + silences[i + 1]["end"]) / 2
            if mid_end - mid_start > 0.1:
                segments.append({"start": mid_start, "end": mid_end})
        # Last sentence: from midpoint of last silence to end of file
        mid_last = (silences[-1]["start"] + silences[-1]["end"]) / 2
        if total_duration - mid_last > 0.1:
            segments.append({"start": mid_last, "end": total_duration})
    else:
        # No leading silence: sentence 1 starts at 0
        first_mid = (silences[0]["start"] + silences[0]["end"]) / 2
        segments.append({"start": 0.0, "end": first_mid})
        for i in range(len(silences) - 1):
            mid_start = (silences[i]["start"] + silences[i]["end"]) / 2
            mid_end = (silences[i + 1]["start"] + silences[i + 1]["end"]) / 2
            if mid_end - mid_start > 0.1:
                segments.append({"start": mid_start, "end": mid_end})
        # Last sentence: from midpoint of last silence to end of file
        mid_last = (silences[-1]["start"] + silences[-1]["end"]) / 2
        if total_duration - mid_last > 0.1:
            segments.append({"start": mid_last, "end": total_duration})

    return segments


def get_audio_duration(audio_path: str) -> float:
    """Get audio duration in seconds using ffprobe."""
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", audio_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip()) if result.returncode == 0 else 0.0


def to_srt_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main():
    parser = argparse.ArgumentParser(description="Generate SRT from audio using silence detection")
    parser.add_argument("audio", help="Path to audio file")
    parser.add_argument("--set", "-s", choices=list(SENTENCE_SETS), help="Use predefined sentence set (e.g. S04)")
    parser.add_argument("--sentences", "-t", help="Path to text file with one sentence per line (alternative to --set)")
    parser.add_argument("-o", "--output", help="Output SRT path")
    parser.add_argument("--silence-duration", type=float, default=0.8, help="Min silence duration in seconds (default: 0.8)")
    parser.add_argument("--noise-db", type=float, default=-40, help="Noise threshold in dB (default: -40)")
    parser.add_argument("--no-leading-silence", action="store_true", help="Audio starts immediately with sentence 1 (no silence before it)")
    args = parser.parse_args()

    audio_path = Path(args.audio)
    if not audio_path.exists():
        print(f"Error: File not found: {audio_path}", file=sys.stderr)
        sys.exit(1)

    if args.set:
        sentences = SENTENCE_SETS[args.set]
    elif args.sentences:
        sentences = Path(args.sentences).read_text(encoding="utf-8").strip().split("\n")
        sentences = [s.strip() for s in sentences if s.strip()]
    else:
        print("Error: Use --set S04 or --sentences path/to/file.txt", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output) if args.output else audio_path.with_suffix(".srt")

    print("Getting audio duration...")
    duration = get_audio_duration(str(audio_path))
    if duration <= 0:
        print("Error: Could not get audio duration", file=sys.stderr)
        sys.exit(1)

    print(f"Detecting silences (duration >= {args.silence_duration}s)...")
    silences = run_silencedetect(str(audio_path), args.silence_duration, args.noise_db)
    print(f"Found {len(silences)} silence periods")

    has_leading = not args.no_leading_silence
    segments = silences_to_speech_segments(silences, duration, has_leading_silence=has_leading)

    # Match segments to sentences (take first N segments)
    n = min(len(segments), len(sentences))
    if n < len(sentences):
        print(f"Warning: Only {n} segments for {len(sentences)} sentences", file=sys.stderr)

    lines = []
    for i in range(n):
        seg = segments[i]
        text = sentences[i]
        lines.append(f"{i + 1}")
        lines.append(f"{to_srt_time(seg['start'])} --> {to_srt_time(seg['end'])}")
        lines.append(text)
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved: {output_path} ({n} segments)")


if __name__ == "__main__":
    main()
