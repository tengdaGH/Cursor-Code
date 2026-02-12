# Session Summary — 2026-02-13

**Purpose:** Summary of item review, Build a Sentence sets, UI fixes, and documentation work completed in this session. For future reference and handoff.

---

## 1. ETS-style item review (all test item types)

### Read in Daily Life
- **Data:** `data/read-in-daily-life-passages.json`
- **Changes:** Flawed option D02-03 (juice: "$1.50 and $2.00" → "$3.00"); key position varied within every passage so no two questions share the same key; stems updated with "According to the [text/email/notice/menu…]"; explanations tied to source.
- **Log:** `docs/item-review-log.md` (Read in Daily Life section)

### Build a Sentence
- **Data:** `data/build-a-sentence-sets.json`
- **Changes:** Grammar/caps (Monday, March); ambiguous item 11 (he/she swap) replaced with "The boss asked whether she could help with the project"; A1–C2 sets added (20 sentences each, 120 items); possessives as single fragment (e.g. committee's).
- **Log:** `docs/item-review-log.md` (Build a Sentence section)

### Complete the Words (C-test)
- **Data:** `data/complete-the-words-passages.json`
- **Changes:** Passage typos: B2-08 "Earth's surface", C1-02 "researcher's own", C1-08 "one's own". Gap rules verified (10 gaps, punctuation not in blank).
- **Log:** `docs/item-review-log.md` (Complete the Words section)

### Listening: Announcement
- **Data:** Embedded in `toefl-listening-announcement-practice.html`
- **Changes:** Key balance (A01-02 through A01-05: Q2 key varied from B to A); stems updated with "According to the announcement" where missing.
- **Log:** `docs/item-review-log.md` (Listening: Announcement section)

### Listening: Choose Response
- **Data:** Embedded in `toefl-listening-choose-response-practice.html`
- **Changes:** None. Key distribution and options reviewed; no edits required.
- **Log:** `docs/item-review-log.md` (Listening: Choose Response section)

### Listening: Conversation
- **Data:** Embedded in `toefl-listening-conversation-practice.html`
- **Changes:** C01-01 Q2 key varied from A to B; "According to the conversation," added to all five question stems.
- **Log:** `docs/item-review-log.md` (Listening: Conversation section)

---

## 2. Build a Sentence: A1–C2 sets and practice page

- **New data:** `data/build-a-sentence-sets.json` — six CEFR sets (A1, A2, B1, B2, C1, C2), 20 sentences each.
- **Practice page:** `toefl-build-sentence-practice.html`
  - Set selector in header (dropdown); data loaded via `fetch('data/build-a-sentence-sets.json')`.
  - State persistence: `localStorage` key `toefl-build-sentence-state` (setId, index, results, elapsedSeconds).
  - New Practice / Retry mistakes use current set; full set state saved only when not in retry mode.
- **UI:** Set dropdown moved to centre of header (between title and progress/timer); `.header-right` flex and `flex-shrink: 0` for layout.

---

## 3. Review log system (for maintainers)

- **Central log:** `docs/item-review-log.md` — detailed item/set edit and ETS review log (one row per change).
- **Data files:** Each item data file has `meta.reviewLogRef: "docs/item-review-log.md"` and optional `meta.reviewLog` summary.
- **HTML pages:** Each practice page has an HTML comment after `<body>` pointing to the log (users do not see it).
- **AGENTS.md:** New section "Item & set edit / review log" instructs agents to update the central log when adding/editing/reviewing items.

---

## 4. Documentation and references

| Document | Purpose |
|----------|---------|
| `docs/item-review-log.md` | Item- and set-level edit/review history (maintainers only) |
| `docs/TOEFL-2026-Technical-Manual.pdf` | Official TOEFL 2026 spec — consult for new materials |
| `docs/SESSION_SUMMARY_2026-02-13.md` | This summary (session work for future reference) |
| `AGENTS.md` | Project overview, structure, item log instructions, file naming |

---

## 5. Data and page reference

| Item type | Data / script location | Practice page |
|-----------|------------------------|---------------|
| Read in Daily Life | `data/read-in-daily-life-passages.json` | `toefl-reading-daily-life-practice.html` |
| Build a Sentence | `data/build-a-sentence-sets.json` | `toefl-build-sentence-practice.html` |
| Complete the Words | `data/complete-the-words-passages.json`, `data/complete-the-words-cefr-sets.json` | `toefl-complete-the-words-practice.html` |
| Listening: Announcement | Embedded in HTML (`ANNOUNCEMENT_SETS`) | `toefl-listening-announcement-practice.html` |
| Listening: Choose Response | Embedded in HTML (`QUESTION_SETS`) | `toefl-listening-choose-response-practice.html` |
| Listening: Conversation | Embedded in HTML (`CONVERSATION_SETS`) | `toefl-listening-conversation-practice.html` |

---

---

## 6. Skill and learnings

- **Project skill added:** `.cursor/skills/toefl-item-review/SKILL.md` — ETS-style item review checklist (key balance, flawed options, stems, single correct order, C-test rules) and requirement to log all changes in `docs/item-review-log.md`.
- **AGENTS.md updated:** "Learnings & practices" section and project structure now reference the skill and the above practices for future agents.
