# Generate SRT Timecodes from Audio

Automatic SRT generation using **OpenAI Whisper**. Works well when there's ~1–1.5s silence between sentences.

## One-time setup

```bash
# 1. Install ffmpeg (required)
brew install ffmpeg

# 2. Create a virtual environment and install Whisper
cd "/Users/tengda/Cursor Code"
python3 -m venv .venv
source .venv/bin/activate
pip install openai-whisper
```

## Usage

### Option A: Python script (recommended)

```bash
cd "/Users/tengda/Cursor Code"
source .venv/bin/activate   # if using venv
python3 scripts/generate-srt-from-audio.py LR-S04-dining-hall.mp3
# Output: LR-S04-dining-hall.srt

# Custom output path
python3 scripts/generate-srt-from-audio.py audio.mp3 -o output.srt

# Faster model (less accurate): tiny.en
# Better accuracy (slower): small.en or medium.en
python3 scripts/generate-srt-from-audio.py audio.mp3 -m small.en
```

### Option B: Whisper CLI directly

```bash
whisper your-audio.mp3 --model base.en --language en --output_format srt
```

## Model sizes

| Model    | Speed   | Accuracy | Use when            |
|----------|---------|----------|---------------------|
| tiny.en  | Fastest | Lower    | Quick test          |
| base.en  | Fast    | Good     | Default, balanced   |
| small.en | Medium  | Better   | Clear speech        |
| medium.en| Slower  | Best     | Complex vocabulary  |

## Tips

- Whisper segments on natural pauses; 1–1.5s silence between sentences works well
- If segments are wrong, you may need to merge/split manually or try a larger model
- Output text may differ slightly from your script (e.g. "Centre" vs "Center"); you can edit the SRT after generation
