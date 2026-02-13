# Agent Instructions — TOEFL Speaking Practice

## ⚠️ IMPORTANT: TOEFL 2026 Technical Manual

**ALWAYS refer to `docs/TOEFL-2026-Technical-Manual.pdf` when creating new TOEFL-related materials.**

This is the official TOEFL 2026 Technical Manual and contains critical specifications, rubrics, scoring guidelines, and format requirements. Before creating any new practice materials, questions, rubrics, or features, consult this manual to ensure alignment with official TOEFL standards.

**Difficulty and routing (Reading & Listening):** The manual defines difficulty at **module level**, not per passage/talk. Reading and Listening are multistage adaptive: a routing module leads to either an **easy** or **hard** second module. The **easy** reading module does not contain an academic passage; the **hard** reading module contains one academic passage. The **easy** listening module does not contain an academic lecture; the **hard** listening module contains two academic lectures. The manual does **not** prescribe CEFR or language-difficulty progression for individual academic passages or academic talks. Any CEFR tiers (e.g. Academic Talk A2–C1) or difficulty metadata (e.g. Academic Passage) in this project are for **practice variety only**, not an official TOEFL specification.

## Project Overview

TOEFL Speaking Practice tools. The main files:

- `toefl-listen-repeat-practice.html` — Listen & Repeat practice page (sentence-by-sentence audio playback)
- `toefl-listen-repeat-mock.html` — Mock test mode
- `toefl-build-sentence-practice.html` — Sentence building practice. Data: `data/build-a-sentence-sets.json` (A1–C2 sets, 20 sentences each; one correct order per item).
- `toefl-writing-email-practice.html` — Write an Email. Campus/social situation; 3–4 required bullets; subject + body; 7 min timer; self-review checklist. Data: `data/writing-email-prompts.json` (6 prompts).
- `toefl-writing-academic-discussion-practice.html` — Write for Academic Discussion. Professor question + 2 student posts; response ~100–120 words; 10 min timer; self-review checklist. Data: `data/writing-academic-discussion-prompts.json` (6 prompts).
- `toefl-take-interview-practice.html` — Take an Interview practice (record responses to interviewer questions)
- `toefl-complete-the-words-practice.html` — Complete the Words (C-test). **Strict TOEFL 2026:** first sentence intact; from second sentence every 2nd word: keep `floor(length/2)` chars, delete rest; 10 gaps; punctuation never in blank; one wrong letter = wrong. Data: `data/complete-the-words-passages.json` (20 passages: Tier B2 routing, Tier C1 hard). Features: 3 min countdown per passage (red at 30 s), auto-advance focus, shake on wrong length, per-gap hints after check. Use `?tier=B2` or `?tier=C1` for adaptive practice.
- `toefl-reading-daily-life-practice.html` — Read in Daily Life. Short nonacademic texts (email, menu, notice, text messages, schedule, social media) with 2–3 multiple-choice questions each. Data: `data/read-in-daily-life-passages.json`. See **Read in Daily Life** section below for data format and how to add sets.
- `toefl-reading-academic-passage-practice.html` — Read an Academic Passage. Organised by **academic domain** (Natural Sciences, Social Sciences, Humanities, Arts, Business & Economics, Technology & Engineering). Two passages per domain (Easier + Harder); MC questions. Data: `data/read-academic-passage-passages.json`.
- `toefl-listening-announcement-practice.html` — Listening: Announcement. Campus-style announcements; scripts and MC items embedded in page.
- `toefl-listening-choose-response-practice.html` — Listening: Choose Response. Short dialogues; choose appropriate response; items embedded in page.
- `toefl-listening-academic-talk-practice.html` — Listening: Academic Talk. Short academic lecture/talk; A2–C1 tiers, 2 talks per tier; audio `audio/listening/LT-{A2|B1|B2|C1}-{01|02}.mp3`; MC items and scripts in page (TOEFL 2026 format).
- `docs/lr-question-bank.md` — Master question bank with all 6 Listen & Repeat sets and CEFR levels

## Project Structure

```
/
├── *.html                    # Main practice pages (entry points)
├── AGENTS.md                 # This file — AI agent instructions
├── .cursor/skills/           # Project skills (e.g. toefl-item-review)
├── .gitignore
├── audio/
│   ├── lr/                  # Listen & Repeat audio files
│   │   ├── LR-S01-*.mp3
│   │   ├── LR-S01-*.srt
│   │   └── ... (S02-S06)
│   └── interview/           # Interview practice audio files
│       └── TI-*-Q*.mp3
├── data/                     # JSON data for practice
│   ├── build-a-sentence-sets.json   # A1–C2 sets, 20 sentences each
│   ├── complete-the-words-passages.json
│   ├── complete-the-words-cefr-sets.json
│   ├── read-in-daily-life-passages.json
│   ├── read-academic-passage-passages.json
│   ├── writing-email-prompts.json          # 6 Write an Email prompts (situation + bullets)
│   └── writing-academic-discussion-prompts.json   # 6 Academic Discussion prompts (question + 2 posts)
├── docs/                     # Documentation and reference materials
│   ├── item-review-log.md    # Detailed item/set edit & ETS review log (maintainers only)
│   ├── SESSION_SUMMARY_2026-02-13.md  # Recent session: reviews, Build a Sentence, log setup
│   ├── README.md             # Documentation index (this folder)
│   ├── lr-question-bank.md
│   ├── design-system-reference.md
│   └── TOEFL-2026-Technical-Manual.pdf  # Official TOEFL 2026 Technical Manual — ALWAYS REFER TO THIS
└── scripts/                  # Audio generation and SRT tools
    ├── docs_maintenance.py    # Periodic validation of docs/logs/skill (run every 12h)
    ├── com.nyk.docs-maintenance.plist.template  # launchd template for 12h schedule
    ├── generate-audio-inworld.py
    ├── generate-interview-audio.py
    ├── generate-srt-silence.py
    ├── inworld_voices.py     # Voice configuration and assignments
    ├── verify-voice-ids.py    # Script to verify voice IDs from API
    └── ...
```

## Item & set edit / review log

**When you add, edit, or review any test items or item sets**, record it in **`docs/item-review-log.md`**:

- One row per logical change (one item edit, one set-level decision).
- Columns: Date | Set/Item ID | Change type (review / edit / add / remove) | Details.
- Each item type (Read in Daily Life, Build a Sentence, Listening, Complete the Words) has its own section.

Data files use `meta.reviewLogRef: "docs/item-review-log.md"` and optional `meta.reviewLog` summary; the full detail lives in the central log. HTML practice pages have a short comment pointing to the log. Users never see the log.

**Project skill:** `.cursor/skills/toefl-item-review/SKILL.md` encodes ETS-style item review (key balance, flawed options, stems, logging). Use when reviewing or editing test items.

**Periodic maintenance:** To validate docs, review-log refs, and skill every 12 hours, see `docs/MAINTENANCE_SCHEDULE.md` and `scripts/docs_maintenance.py`. Schedule via launchd (Mac) or cron.

## Learnings & practices (from item review work)

- **Key balance:** Vary correct answer position within each passage/set (reorder options, update `correct` index) so no two questions share the same key.
- **One correct answer:** Build a Sentence and C-test items must have a single correct response; fix ambiguous wording (e.g. pronoun swaps).
- **Source attribution:** Use "According to the [text/announcement/academic talk]…" in stems for factual MC items.
- **Log everything:** Every substantive item/set change goes in `docs/item-review-log.md`; keep data-file `meta.reviewLog` and HTML comments in sync.
- **Listening scripts:** All three listening types keep full scripts and MC items in the same HTML file (no separate JSON).

## File Naming Convention

```
Audio:  LR-S{XX}-{scenario-slug}.mp3
SRT:    LR-S{XX}-{scenario-slug}.srt
```

| Set | File slug              | CEFR  | Scenario                              | Status    |
|-----|------------------------|-------|---------------------------------------|-----------|
| S01 | bookstore-tour         | A2-B1 | Campus Bookstore Tour                 | Done      |
| S02 | museum-tour            | B1-B2 | Natural History Museum Tour           | Done      |
| S03 | orientation-academic   | B2-C1 | University Orientation                | Done      |
| S04 | dining-hall            | A2-B1 | Campus Dining Hall Tour               | Done      |
| S05 | lab-safety             | B1-B2 | Biology Lab Safety Orientation        | Done      |
| S06 | art-history-renaissance| B2-C1 | Art History Lecture                    | Done      |

## How to Add a New Practice Set

### Step 1: Generate SRT from Audio

Use `scripts/generate-srt-silence.py` (requires `ffmpeg`).

**How it works:**
1. Runs ffmpeg `silencedetect` to find silence gaps between sentences
2. Uses the **midpoint** of each silence gap as the boundary between sentences
3. This avoids clipping the beginning or end of any sentence
4. Pairs detected segments with known sentence text from the question bank

**Important parameters:**
- `--noise-db -40` — Silence threshold (default, works well for TTS audio)
- `--silence-duration 0.8` — Minimum silence length to count as a gap (default)
- `--no-leading-silence` — Use if the audio starts immediately with sentence 1 (no silence before it)

**For sets with sentence text already in the script:**

```bash
python3 scripts/generate-srt-silence.py audio/lr/LR-S04-dining-hall.mp3 --set S04 -o audio/lr/LR-S04-dining-hall.srt
```

**For new sets not in the script, use a text file (one sentence per line):**

```bash
python3 scripts/generate-srt-silence.py audio/lr/LR-S05-lab-safety.mp3 --sentences S05-sentences.txt -o audio/lr/LR-S05-lab-safety.srt
```

**To add a new set to the script:** Add the sentences array to `SENTENCE_SETS` in `scripts/generate-srt-silence.py`.

### Step 2: Rename the Audio File

TTS tools export files with long names like `Inworld_inworld-tts-1.5-mini_Olivia_02-12-2026 22-34-55.mp3`. Rename to match the convention:

```bash
mv "original-tts-filename.mp3" audio/lr/LR-S05-lab-safety.mp3
```

### Step 3: Add Set to the Practice Page

Edit `toefl-listen-repeat-practice.html`:

1. **Enable the dropdown option:** Find the `<select id="setSelect">` and remove `disabled` from the option.

2. **Add the data to `PRACTICE_SETS`:** Add a new entry after the last set:

```javascript
S05: {
  label: 'S05 — Lab Safety (B1-B2)',
  audioFile: 'audio/lr/LR-S05-lab-safety.mp3',
  sentences: parseSentences([
    { text: "...", start: "HH:MM:SS,mmm", end: "HH:MM:SS,mmm" },
    // ... 20 sentences, timestamps from the SRT file
  ])
}
```

3. **Copy timestamps from the SRT file.** Each SRT entry maps to one `{ text, start, end }` object.

### Step 4: Verify

Open the page in a browser. Switch to the new set. Play each sentence — make sure no words are clipped at the start or end.

## Audio Characteristics

- TTS-generated audio with ~1.5s silence between sentences
- Some audio files have leading silence (1–2s before sentence 1), some don't
- No trailing silence after the last sentence
- The midpoint-based boundary method handles both cases

### Accent Preferences

**IMPORTANT:** For all TOEFL practice audio generation:
- **Prioritize American accents** (primary)
- British and Australian accents are acceptable as additional options
- This aligns with TOEFL's focus on North American English pronunciation and intonation patterns

### Voice Configuration

Voice assignments are managed in `scripts/inworld_voices.py`. This file maps voice names to Inworld API voice IDs and assigns appropriate voices to each practice set based on content type.

**Preferred Voices:**
- **Female:** Ashley, Deborah, Sarah
- **Male:** Dennis, Mark
- **Male Admin/Prof:** Edward, Craig (British), Carter

**Voice Assignments:**

Listen & Repeat Sets:
- S01 (Bookstore Tour): Ashley — friendly tour guide
- S02 (Museum Tour): Deborah — tour guide
- S03 (University Orientation): Edward — academic administrator (Dr. Chen)
- S04 (Dining Hall): Sarah — friendly staff member
- S05 (Lab Safety): Carter — instructor/professor
- S06 (Art History): Craig — professor/lecturer (British accent)

Interview Practice Sets:
- PT1 (Work-Life Balance): Edward — Research Study interviewer (Dr. Williams)
- SC1 (Scholarship Application): Craig — Professor Adams (British academic)
- OA1 (Outdoor Activities): Edward — Research Study interviewer (Dr. Chen)
- CL1 (Campus Life): Sarah — Student Survey interviewer (Ms. Thompson)
- ZJ1 (真题 2026-01-21): Sarah — Graduate Researcher (Health and Habits)

**To verify voice IDs:**
```bash
export INWORLD_API_KEY=your_key_here
python3 scripts/verify-voice-ids.py
```

This will list all available voices from the Inworld API. Update `scripts/inworld_voices.py` if any voice IDs need correction.

## State Persistence

The practice page saves `currentSetId` and `currentSentenceIndex` to `localStorage` (key: `toefl-lr-practice-state`). Students return to where they left off on refresh.

## Timecode Quality Notes

- **S04, S05, S06** use the improved midpoint-based SRT generation (best quality)
- **S01, S02, S03** were manually created with tighter boundaries — may clip sentence tails slightly
- When regenerating S01–S03, run the silence script against their audio files to get midpoint-based timecodes

---

## Write for Academic Discussion Practice

### Overview

`toefl-writing-academic-discussion-practice.html` provides practice for the TOEFL Academic Discussion writing task. Students read a professor's question and two student posts, then write their own response.

### Question Bank

- **Source:** `docs/academic-discussion-question-bank.md` (Markdown format, 92 questions)
- **JSON Data:** `data/writing-academic-discussion-prompts.json` (92 questions)
- **Images:** `docs/academic-discussion/images/` (86 images)

### Question Processing Status

✅ **Complete:** All 92 questions (D01-D93, D72 missing) have been:
- Extracted from screenshots using macOS Vision Framework OCR
- Parsed and entered into the question bank
- Converted to JSON format
- Added to the practice page dropdown menu

**Dropdown Format:** `D07 — Automation` or `D08 — Being An Early Adopter`

### Adding New Questions

1. **Add to question bank:** Edit `docs/academic-discussion-question-bank.md`
2. **Convert to JSON:** Run `python3 scripts/convert-question-bank-to-json.py`
3. **Test:** Open `toefl-writing-academic-discussion-practice.html` and verify the new question appears

### Processing Scripts

- `scripts/batch_process_questions.py` - Batch create question framework
- `scripts/extract_with_vision.py` - Vision OCR extraction
- `scripts/fix_incomplete_extractions.py` - Fix incomplete extractions
- `scripts/fix_student_posts.py` - Fix student post parsing
- `scripts/convert-question-bank-to-json.py` - Convert Markdown to JSON

---

## Take an Interview Practice

### Overview

`toefl-take-interview-practice.html` simulates a TOEFL Speaking interview. The student listens to an interviewer question (audio auto-plays), then records a 60-second spoken response. After all 4 questions, a review phase shows playback of all recordings with an ETS-style self-evaluation rubric.

### Task context (official format)

On the real TOEFL test, the Interview task **begins with a short context screen** before any question: the test-taker is told they have agreed to take part in a research study (or similar situation), and that they will have a short online interview with a researcher who will ask questions. This matches ETS/TOEFL Essentials style (e.g. *"You have agreed to take part in a research study about urban life. You will have a short online interview with a researcher. The researcher will ask you some questions. Please answer the interviewer's questions."*). In our app, the **intro phase** shows this as the **scenario** (task context) card; each set's `scenario` field should be this kind of context paragraph. See official test demos and the TOEFL 2026 Technical Manual for exact wording.

### Interview Sets

| Set ID | Slug | Scenario | Interviewer |
|--------|------|----------|-------------|
| PT1 | Work-Life Balance | Research Study | Dr. Williams |
| SC1 | Scholarship Application | Interview | Professor Adams |
| OA1 | Outdoor Activities | Research Study | Dr. Chen |
| CL1 | Campus Life | Student Survey | Ms. Thompson |
| ZJ1 | 真题 2026年1月21日 | Health and Habits (Research) | Graduate Researcher |

### Audio File Naming

```
audio/interview/TI-{SetID}-Q{N}.mp3
```

Example: `audio/interview/TI-PT1-Q1.mp3` — Practice Test 1, Question 1

Each set has 4 questions (e.g. 5 sets → 20 audio files). 真题 sets (ZJ*) use exam date in the label (e.g. 2026年1月21日).

### Generating Interview Audio

Use `scripts/generate-interview-audio.py` (requires Inworld TTS API key):

```bash
export INWORLD_API_KEY=your_key_here
python3 scripts/generate-interview-audio.py
```

This generates all 16 MP3 files in `audio/interview/`.

**Note:** When configuring TTS voices, prioritize American accents (British/Australian as secondary options) to match TOEFL standards.

### Generating Academic Talk Audio

Use `scripts/generate-academic-talk-audio.py` (requires Inworld TTS API key):

```bash
export INWORLD_API_KEY=your_key_here
python3 scripts/generate-academic-talk-audio.py
```

This generates all 8 MP3 files in `audio/listening/` (LT-A2-01, LT-A2-02, LT-B1-01, … LT-C1-02). **Voice direction:** The script tells Inworld the context of usage (TOEFL academic lecture; clear, moderate pace) and uses sentence-by-sentence synthesis with short pauses for natural prosody. Voice casting is in `scripts/inworld_voices.py` under `ACADEMIC_TALK_VOICES` (e.g. Sarah for A2, Carter for B2 biology, Craig for history/seminar).

### How to Add a New Interview Set

1. **Add the set data to `INTERVIEW_SETS`** in `toefl-take-interview-practice.html`:

```javascript
XX1: {
  label: 'Set N — Topic Name (Context)',
  icon: '🎤',
  scenario: 'Description of the interview context...',
  interviewerName: 'Dr. Name',
  interviewerRole: 'Role',
  questions: [
    {
      type: 'Personal / Factual',
      text: 'Question text...',
      audioFile: 'audio/interview/TI-XX1-Q1.mp3',
      timeLimit: 60
    },
    // ... 4 questions total
  ]
}
```

2. **Generate the audio files** — either add the questions to `scripts/generate-interview-audio.py` and re-run (outputs to `audio/interview/`), or manually place MP3 files in `audio/interview/` with the correct naming.

3. The dropdown is auto-populated from `INTERVIEW_SETS` — no manual HTML changes needed.

### Question Progression Pattern

Each interview follows a 4-question arc with increasing cognitive demand:

1. **Personal / Factual** — describe your experience
2. **Personal + Opinion** — relate experience to a broader topic
3. **Opinion + Argument** — evaluate a policy or claim
4. **Opinion + Prediction** — speculate about the future

### Features

- **Auto-play interviewer audio** — question audio plays automatically when advancing
- **60-second recording timer** with visual countdown ring
- **Recording saved in-memory** — persists within the session (lost on page refresh)
- **Review phase** — replay all recordings, self-evaluate on 4 ETS rubric dimensions
- **State persistence** — `localStorage` saves current set and question index (key: `toefl-interview-practice-state`)
- **Microphone permission** — requires `http://` (not `file://`); serves via `python3 -m http.server 8000`

---

## Writing (Write an Email / Write for Academic Discussion)

**TOEFL 2026 (Technical Manual):** Writing section has Build a Sentence, Write an Email, and Write for Academic Discussion. Integrated Writing is removed.

### Write an Email

- **Practice page:** `toefl-writing-email-practice.html`
- **Data:** `data/writing-email-prompts.json` — `prompts[]` with `id`, `situation`, `bullets[]` (3–4 items), `timeLimitMinutes` (7), `wordTarget` (130).
- **To add a prompt:** Append to `prompts` in the JSON; dropdown and timer/word target are driven by the data.

### Write for Academic Discussion

- **Practice page:** `toefl-writing-academic-discussion-practice.html`
- **Data:** `data/writing-academic-discussion-prompts.json` — `prompts[]` with `id`, `question`, `posts[]` (each `author`, `text`), `timeLimitMinutes` (10), `wordTarget` (120).
- **To add a prompt:** Append to `prompts` in the JSON; professor question and two student posts required.

Both pages include an optional countdown timer, word count, and self-review checklist (no auto-scoring). Log item/set changes in `docs/item-review-log.md`.

---

## Read in Daily Life

**TOEFL 2026 (Technical Manual II-3):** Short, nonacademic texts (15–150 words) with 2–3 multiple-choice questions per passage. Text types: poster, sign/notice, menu, social media post, webpage, schedule, email, text messages, ads, news article, form, invoice, receipt.

### File and data

- **Practice page:** `toefl-reading-daily-life-practice.html`
- **Data file:** `data/read-in-daily-life-passages.json`

### Data format

```json
{
  "meta": { "format": "TOEFL 2026 Read in Daily Life", "rules": "..." },
  "sets": {
    "D01": {
      "label": "Set 1 — Mixed Daily Life",
      "passages": [
        {
          "id": "D01-01",
          "type": "email",
          "title": "Email from Building Management",
          "from": "...",
          "to": "...",
          "subject": "...",
          "date": "...",
          "content": "Body text...",
          "wordCount": 95,
          "difficulty": "B1",
          "questions": [
            {
              "text": "What is the main purpose of this email?",
              "options": ["Option A text", "Option B text", "Option C text", "Option D text"],
              "correct": 0,
              "explanation": "Why the answer is correct."
            }
          ]
        }
      ]
    }
  }
}
```

### Passage types and fields

- **`type`** (required): `email` | `text_messages` | `menu` | `schedule` | `social_media` | `notice` | `plain`
- **`email`:** `from`, `to`, `subject`, `date`, `content` (body)
- **`text_messages`:** `messages`: `[{ "sender": "Name", "text": "..." }]` (no `content`)
- **`menu`** / **`schedule`:** `content` (plain text, line breaks preserved)
- **`social_media`:** `author`, `date`, `content`
- **`notice`** / **`plain`:** `content`
- **`questions`:** `options` array of strings; `correct` is 0-based index of the correct option.

### How to add a new set

1. Open `data/read-in-daily-life-passages.json`.
2. Add a new key under `sets`, e.g. `"D02": { "label": "Set 2 — ...", "passages": [ ... ] }`.
3. Each passage must have `id`, `type`, `title`, and `questions` (each question: `text`, `options`, `correct`, `explanation`).
4. The set selector on the practice page is populated from `sets`; no HTML changes needed.
5. Optional: use `?shuffle=false` in the URL to disable shuffling of passages.

### State persistence

The practice page saves `setId`, `index`, `results`, and `answers` to `localStorage` (key: `toefl-reading-daily-life-state`).

---

## Inline Gap Input Style (Proven Pattern)

When rendering fill-in-the-blank gaps inline with passage text, use this approach:

### Structure
```html
<span class="word-gap">
  visiblePrefix
  <span class="gap-slot">
    <span class="gap-underscores">___</span>  <!-- N real _ chars -->
    <input style="width: calc(Nch + N*2+6 px)">
  </span>
  suffix
</span>
```

### Key CSS Rules
- **`.gap-slot`**: `display: inline-block; position: relative; vertical-align: baseline; line-height: 0; background: #e5e7eb; border-radius: 3px;`
- **`.gap-underscores`**: `position: absolute; top:0; left:0; right:0; bottom:0;` — same monospace font, font-size, line-height, letter-spacing, and padding as the input. `color: #aaa; pointer-events: none;`
- **`input`**: `position: relative; background: transparent;` — monospace font (`'SF Mono', Menlo, Monaco, Consolas, 'Courier New', monospace`), `font-size: 16px; line-height: 1.3; letter-spacing: 2px; padding: 2px 3px;`
- **Width**: `calc(N * 1ch + N * 2px + 6px)` — N chars + N×letter-spacing + horizontal padding

### Why This Works
1. **No vertical alignment issues** — `line-height: 0` on wrapper prevents it from disrupting text flow; `vertical-align: baseline` aligns with surrounding text
2. **1:1 underscore-to-letter mapping** — real `_` characters in monospace font, same metrics as input, so each underscore sits directly under its letter
3. **Visible individual underscores** — `letter-spacing: 2px` on both layers prevents adjacent `_` from merging into one long line
4. **Input is transparent** — typed letters paint on top of underscores; grey background comes from `.gap-slot`
5. **State styling** — correct/incorrect classes go on `.gap-slot` (changes background + hides underscores via `visibility: hidden`)
