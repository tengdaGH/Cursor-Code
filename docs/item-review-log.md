# Item & Item-Set Edit / Review Log

**Purpose:** Keep a detailed, chronological record of all item- and set-level edits and ETS-style reviews. Not shown to users; for maintainers and future item writers.

**How to use:** Append new entries at the bottom under the appropriate section. Use the format below. When doing an ETS-style review, log each substantive change (flawed option fix, key position change, stem wording, new set, etc.).

**Session summary:** For a high-level summary of the 2026-02-13 review and Build a Sentence work, see `docs/SESSION_SUMMARY_2026-02-13.md`. Documentation index: `docs/README.md`.

### Review status (as of 2026-02-13)

| Item type | Data / location | Reviewed | Notes |
|-----------|-----------------|----------|--------|
| Read in Daily Life | `data/read-in-daily-life-passages.json` | Yes | Key balance, stems, flawed option fix. |
| Build a Sentence | `data/build-a-sentence-sets.json` | Yes | A1–C2 sets added; ambiguous item fixed. |
| Complete the Words | `data/complete-the-words-passages.json` | Yes | Passage typos; gap rules verified. |
| Listening: Announcement | `toefl-listening-announcement-practice.html` | Yes | Key balance, stems. |
| Listening: Choose Response | `toefl-listening-choose-response-practice.html` | Yes | No edits needed. |
| Listening: Conversation | (removed from TOEFL 2026 format; file retained for reference) | — | — |
| Listening: Academic Talk | `toefl-listening-academic-talk-practice.html` | Yes | A2–C1 tiers, 2 talks each; key balance, stems. |
| Reading: Academic Passage | `data/read-academic-passage-passages.json` | Yes | R01 set, 2 passages; key balance, stems. |
| Writing: Write an Email | `data/writing-email-prompts.json` | Added 2026-02-13 | 6 prompts (E01–E06); situation + 3–4 bullets; 7 min. |
| Writing: Academic Discussion | `data/writing-academic-discussion-prompts.json` | Added 2026-02-13 | 6 prompts (D01–D06); professor Q + 2 posts; 10 min. |

---

## Log format (for each entry)

- **Date:** YYYY-MM-DD
- **Item type / Source:** e.g. Read in Daily Life, Build a Sentence, Listening Announcement
- **Set / Passage / Item ID:** e.g. D02, D02-03, A1, R01-01
- **Change type:** `review` | `edit` | `add` | `remove`
- **Details:** What was changed and why (option text, key, stem, explanation, etc.)

---

## Read in Daily Life  
**Data:** `data/read-in-daily-life-passages.json`

| Date       | Set/Item   | Change type | Details |
|------------|------------|-------------|---------|
| 2026-02-13 | D02-03     | edit        | Q: juice price. Option D was `"$1.50 and $2.00"` (non-parallel, two values). Replaced with `"$3.00"`. Stem updated to "According to the menu, how much is the juice?" |
| 2026-02-13 | D02-04     | edit        | Q2 key varied: reordered options so key moved from B to C. Stem: "According to the sign, what are you not allowed to bring into the library?" |
| 2026-02-13 | D03-01     | edit        | Q2 key varied to A; stem "According to the email, what should students do if they did not get the message?" |
| 2026-02-13 | D03-02     | edit        | Q2 key varied to D; stem "According to the schedule, how much is a ticket for someone under 16?" |
| 2026-02-13 | D03-03     | edit        | Q2 key varied to A; stem "According to the email, what will happen if it rains?" |
| 2026-02-13 | D03-05     | edit        | Q2 key varied to A; stem "According to the notice, where can you get food on Monday?" |
| 2026-02-13 | D04-01     | edit        | Q2 key varied to A; stem "According to the email, when was the order delivered?" |
| 2026-02-13 | D04-04     | edit        | Q2 key varied to A; stem "According to the notice, when must you pay?" |
| 2026-02-13 | D04-05     | edit        | Q2 key varied to A; stem "According to the post, what does the £15 fee include?" |
| 2026-02-13 | D05-03     | edit        | Q2 key varied to C; stem "According to the email, what should the team do with documentation for now?" |
| 2026-02-13 | D05-04     | edit        | Q2 key varied to A; stem "According to the notice, what can you request regarding your data?" |
| 2026-02-13 | D06-01     | edit        | Q2 key varied to A (was same as Q1 key C). Stem "According to the text, what are staff and contractors required to do?" |
| 2026-02-13 | D06-03     | edit        | Q2 key varied to A (was same as Q1 key B). Stem "According to the notice, what is a quorum?" |
| 2026-02-13 | D06-04     | edit        | Q2 key varied to C; stem "According to the email, how long is the offer valid?" |
| 2026-02-13 | D06-05     | edit        | Q2 key varied to A; stem "According to the notice, what happens to late submissions?" |
| 2026-02-13 | (multiple)  | edit        | Explanations tightened: tied to source ("The text/notice/email states..."). D06-01, D06-03 policy/governance explanations clarified. |

---

## Build a Sentence  
**Data:** `data/build-a-sentence-sets.json`

| Date       | Set/Item   | Change type | Details |
|------------|------------|-------------|---------|
| 2026-02-13 | (original) | edit        | Item 18: fragment `"monday"` → `"Monday"` (proper noun). Item 20: `"march"` → `"March"`. |
| 2026-02-13 | (original) | edit        | Item 11: Ambiguous (two correct orders: "He asked whether she..." / "She asked whether he..."). Replaced with "The boss asked whether she could help with the project." Single correct order. |
| 2026-02-13 | A1–C2      | add         | New sets A1, A2, B1, B2, C1, C2 created; 20 sentences each (120 items). CEFR-aligned grammar/vocabulary; each item has single correct word order. |
| 2026-02-13 | C1         | edit        | Possessives as single fragment: candidate's, committee's, project's, director's (no split "candidate" + "'s"). |

---

## Complete the Words (C-test)  
**Data:** `data/complete-the-words-passages.json`, `data/complete-the-words-cefr-sets.json`

| Date       | Set/Item | Change type | Details |
|------------|----------|-------------|---------|
| 2026-02-13 | B2-08    | edit        | Passage text: "Earth surface" → "Earth's surface" (possessive). |
| 2026-02-13 | C1-02    | edit        | Passage text: "researcher own" → "researcher's own" (possessive). |
| 2026-02-13 | C1-08    | edit        | Passage text: "one own" → "one's own" (possessive). |
| 2026-02-13 | (set)    | review      | Verified: gaps derived from every 2nd word (sentence 2+), floor(len/2) chars kept, 10 gaps max, punctuation stripped from blank. No further edits. |

---

## Listening: Announcement  
**Data:** Embedded in `toefl-listening-announcement-practice.html`  
**Script/items:** `ANNOUNCEMENT_SETS[*].announcements[].text`, `.questions[]`

| Date       | Set/Item | Change type | Details |
|------------|----------|-------------|---------|
| 2026-02-13 | A01-02   | edit        | Q2 key varied from B to A (reordered options). Stem: "According to the announcement, what does the speaker recommend students do?" |
| 2026-02-13 | A01-03   | edit        | Q2 key varied from B to A. Stem Q1: "According to the announcement, why was the concert cancelled?" |
| 2026-02-13 | A01-04   | edit        | Q2 key varied from B to A. |
| 2026-02-13 | A01-05   | edit        | Q2 key varied from B to A. Stem Q1: "According to the announcement, what change is being made to the dining hall menu?" |
| 2026-02-13 | A01-03   | edit        | Q2 stem: "According to the announcement, what should students do if they cannot attend the rescheduled event?" |
| 2026-02-13 | A01-05   | edit        | Q2 stem: "According to the announcement, what is one reason mentioned for these changes?" |

---

## Listening: Choose Response  
**Data:** Embedded in `toefl-listening-choose-response-practice.html`  
**Script/items:** `QUESTION_SETS[*].questions[].dialogue`, `.options[]`, `.correct`

| Date       | Set/Item | Change type | Details |
|------------|----------|-------------|---------|
| 2026-02-13 | (set)    | review      | Key distribution checked: R01 mostly A, R02 B, R03 C, R04 D, later sets mixed. No same-key runs; options and stems reviewed; no edits required. |

---

## Listening: Conversation *(removed from TOEFL 2026 format)*  
**Data:** Was in `toefl-listening-conversation-practice.html`. Conversation task type is not part of TOEFL 2026; page kept in repo but unlinked from index.

| Date       | Set/Item | Change type | Details |
|------------|----------|-------------|---------|
| 2026-02-13 | C01-01   | edit        | Q2 key varied from A to B (reordered options). Stems: added "According to the conversation," for source attribution. |
| 2026-02-13 | (format) | remove      | Listen to a Conversation removed from app navigation and docs as not in TOEFL 2026 format. |

---

## Listening: Academic Talk  
**Data:** Embedded in `toefl-listening-academic-talk-practice.html`  
**Script/items:** `ACADEMIC_TALK_SETS[*].talks[].text`, `.questions[]`  
**Sets:** A2, B1, B2, C1 (2 talks per tier; audio: `audio/listening/LT-{tier}-{01|02}.mp3`).

| Date       | Set/Item | Change type | Details |
|------------|----------|-------------|---------|
| 2026-02-13 | A2, B1, B2, C1 | add         | Four CEFR tiers added; 2 lectures per tier (A2-01/02, B1-01/02, B2-01/02, C1-01/02). Stems use "According to the talk" for factual Q2s. |
| 2026-02-13 | B2-01     | edit        | Q2 key varied from A to B (reordered options) so Q1 and Q2 do not share the same key. |
| 2026-02-13 | (set)     | review      | Key balance checked across all 8 talks; explanations tied to source. |

---

## Reading: Academic Passage  
**Data:** `data/read-academic-passage-passages.json`  
**Structure:** Sets by **academic domain** (dropdown). Six domains: Natural Sciences (NATSCI), Social Sciences (SOCSCI), Humanities (HUM), Arts (ARTS), Business & Economics (BUS), Technology & Engineering (TECH). Each domain has 2 passages: one Easier, one Harder. Passage: id, title, topic, content, wordCount, difficulty (Easier/Harder), questions[] (text, options[], correct index, explanation).

| Date       | Set/Item | Change type | Details |
|------------|----------|-------------|---------|
| 2026-02-13 | R01      | add         | Set R01 added with 2 passages: R01-01 The Water Cycle (Earth science), R01-02 The Printing Press (History). 4 questions each; stems use "According to the passage" where factual. |
| 2026-02-13 | R01-01   | edit        | Q3 key varied from C to A (reordered options so "In the ocean" is A) to avoid same key as Q2. |
| 2026-02-13 | (set)    | review      | Key balance checked; explanations tied to passage. |
| 2026-02-13 | (all)    | add         | Reorganised by academic domain: 6 domains, 2 passages each (Easier + Harder). NATSCI (Water Cycle, Plate Tectonics), SOCSCI (Group Decisions, Cognitive Dissonance), HUM (Printing Press, Historical Causation), ARTS (Renaissance Perspective, Impressionism), BUS (Supply and Demand, Externalities), TECH (Batteries, Renewable Grid). Dropdown shows domain names. |
| 2026-02-13 | (all)    | review      | Full item review: key balance varied within each passage (no same key for consecutive questions); reordered options where needed; stems use "According to the passage" for factual items; explanations tied to source; no flawed-option issues. |

---

## Writing: Write an Email  
**Data:** `data/writing-email-prompts.json`  
**Structure:** `prompts[]`: id, situation, bullets[], timeLimitMinutes (7), wordTarget (130). No auto-scoring; self-review checklist on page.

| Date       | Set/Item | Change type | Details |
|------------|----------|-------------|---------|
| 2026-02-13 | E01–E06  | add         | 6 prompts added: library hours (E01), bookstore order (E02), review session (E03), roommate (E04), sponsorship (E05), missed deadline (E06). Each has situation + 3 bullets, 7 min, 130-word target. |

---

## Writing: Write for Academic Discussion  
**Data:** `data/writing-academic-discussion-prompts.json`  
**Structure:** `prompts[]`: id, question, posts[] (author, text), timeLimitMinutes (10), wordTarget (120). No auto-scoring; self-review checklist on page.

| Date       | Set/Item | Change type | Details |
|------------|----------|-------------|---------|
| 2026-02-13 | D01–D06  | add         | 6 prompts added: required outside major (D01), group vs individual (D02), cars/transport (D03), financial literacy (D04), gap year (D05), books vs video (D06). Professor question + 2 student posts each; 10 min, ~120 words. |

---

*Add new entries at the bottom of the relevant section. Keep one row per logical change (one item edit, or one set-level decision) so the log stays searchable.*
