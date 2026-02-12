# Documentation Index

Quick reference for key docs in this folder. Not shown to end users.

---

## TOEFL 2026 & item quality

| File | Purpose |
|------|---------|
| **TOEFL-2026-Technical-Manual.pdf** | Official TOEFL 2026 spec. Consult when creating or reviewing practice materials, rubrics, or item types. |
| **item-review-log.md** | Detailed item/set edit and ETS-style review log. One row per change; sections by item type. Maintainers only. |
| **SESSION_SUMMARY_2026-02-13.md** | Summary of recent session: item reviews, Build a Sentence sets, review log setup, UI fixes. |

---

## Practice content & question banks

| File | Purpose |
|------|---------|
| **lr-question-bank.md** | Listen & Repeat: all 6 sets, sentences, CEFR levels. |
| **listen-choose-response-plan.md** | Plan/reference for Listen & Choose Response. |
| **complete-the-words-end-user-findings.md** | C-test user feedback and findings. |

---

## Design & sync

| File | Purpose |
|------|---------|
| **design-system-reference.md** | UI/design system reference. |
| **NOTION_AI_READABLE.md**, **NOTION_SYNC_*** | Notion sync and content docs. |
| **AUTO_SYNC_GUIDE.md**, **SYNC_WORKFLOW.md** | Sync workflows. |

---

## Where item data lives

- **Read in Daily Life:** `data/read-in-daily-life-passages.json`
- **Build a Sentence:** `data/build-a-sentence-sets.json`
- **Complete the Words:** `data/complete-the-words-passages.json`, `data/complete-the-words-cefr-sets.json`
- **Listening (Announcement, Choose Response, Academic Talk):** scripts and MC items embedded in respective `.html` files.
- **Reading: Academic Passage:** `data/read-academic-passage-passages.json`

When editing items, update **`docs/item-review-log.md`** (see AGENTS.md). Project skill **`.cursor/skills/toefl-item-review/SKILL.md`** encodes the ETS-style review checklist and logging steps.

| File | Purpose |
|------|---------|
| **MAINTENANCE_SCHEDULE.md** | How to run docs/logs validation every 12 hours (script, launchd, cron). |
