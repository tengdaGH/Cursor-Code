---
name: toefl-item-review
description: ETS-style review of TOEFL practice items (MC, C-test, Build a Sentence, Listening). Use when reviewing test items, varying key positions, fixing flawed options, or adding item sets. Log all edits in docs/item-review-log.md.
---

# TOEFL Item Review

Apply when reviewing or editing any TOEFL practice items in this project. Ensures one correct answer per item, key balance, and consistent documentation.

## Where item data lives

| Type | Location |
|------|----------|
| Read in Daily Life | `data/read-in-daily-life-passages.json` |
| Build a Sentence | `data/build-a-sentence-sets.json` |
| Complete the Words | `data/complete-the-words-passages.json` (+ cefr-sets) |
| Listening (Announcement, Choose Response, Conversation) | Scripts and MC items embedded in respective `.html` files |

## Review checklist (MC items)

- **Key balance:** Within a passage/set, vary correct answer position (no same key for all questions). Reorder options and update `correct` index.
- **Flawed options:** Remove non-parallel options (e.g. two values in one option), length cues, or grammar giveaways. Replace with one plausible distractor.
- **Stems:** Add "According to the [text/email/notice/announcement/conversation]" for factual items where appropriate.
- **Explanations:** Tie to source ("The text states…"). Keep concise.

## Review checklist (Build a Sentence)

- **Single correct order:** No ambiguous items (e.g. "He asked whether she…" vs "She asked whether he…"). Replace with unambiguous wording (e.g. "The boss asked whether she…").
- **Proper nouns:** Use capitalized forms in fragments where displayed (e.g. Monday, March).
- **Possessives:** Store as one fragment (e.g. `committee's`) not split (`committee`, `'s`).

## Review checklist (C-test / Complete the Words)

- **Gap rules:** First sentence intact; from sentence 2, every 2nd word; keep floor(length/2) chars; 10 gaps max; punctuation never in blank.
- **Passage text:** Fix typos (e.g. "Earth's surface", "researcher's own", "one's own"). Possessives must be correct in source text.

## Log every change

1. **Central log:** Append one row per logical change to `docs/item-review-log.md` under the correct section (Read in Daily Life, Build a Sentence, Complete the Words, Listening: Announcement, Listening: Choose Response, Listening: Conversation).
2. **Row format:** Date | Set/Item ID | Change type (review / edit / add / remove) | Details.
3. **Data files:** Ensure `meta.reviewLogRef: "docs/item-review-log.md"` and a short `meta.reviewLog` summary entry in the JSON. HTML practice pages: keep the REVIEW LOG comment after `<body>` pointing to the log.

## Reference

- Full edit history: `docs/item-review-log.md`
- Session summary and data map: `docs/SESSION_SUMMARY_2026-02-13.md`
- Doc index: `docs/README.md`
- Project and item-log instructions: `AGENTS.md`
