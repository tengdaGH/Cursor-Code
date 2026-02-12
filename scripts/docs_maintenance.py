#!/usr/bin/env python3
"""
Periodic docs & logs maintenance: validate structure, refs, and write last-run stamp.
Run via cron/launchd every 12 hours. Does not edit item-review-log or skills content.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Project root (parent of scripts/)
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DOCS = ROOT / "docs"
SKILLS = ROOT / ".cursor" / "skills"
LAST_RUN_FILE = DOCS / ".maintenance-last-run.txt"

# Data files that must have meta.reviewLogRef
DATA_FILES_WITH_REVIEW = [
    "read-in-daily-life-passages.json",
    "read-academic-passage-passages.json",
    "build-a-sentence-sets.json",
    "complete-the-words-passages.json",
]

# HTML practice pages that should contain REVIEW LOG comment and item-review-log ref
HTML_PRACTICE_PAGES = [
    "toefl-reading-daily-life-practice.html",
    "toefl-reading-academic-passage-practice.html",
    "toefl-build-sentence-practice.html",
    "toefl-complete-the-words-practice.html",
    "toefl-listening-announcement-practice.html",
    "toefl-listening-choose-response-practice.html",
    "toefl-listening-academic-talk-practice.html",
]

# Required docs
REQUIRED_DOCS = [
    "docs/item-review-log.md",
    "docs/README.md",
]


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    # 1. Data files: valid JSON + reviewLogRef
    for name in DATA_FILES_WITH_REVIEW:
        path = ROOT / "data" / name
        if not path.exists():
            warnings.append(f"Data file missing: {name}")
            continue
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            meta = data.get("meta") or {}
            if meta.get("reviewLogRef") != "docs/item-review-log.md":
                errors.append(f"{name}: meta.reviewLogRef missing or wrong")
        except json.JSONDecodeError as e:
            errors.append(f"{name}: invalid JSON — {e}")

    # 2. HTML pages: contain REVIEW LOG and item-review-log
    for name in HTML_PRACTICE_PAGES:
        path = ROOT / name
        if not path.exists():
            warnings.append(f"HTML missing: {name}")
            continue
        text = path.read_text(encoding="utf-8")
        if "REVIEW LOG" not in text or "item-review-log.md" not in text:
            errors.append(f"{name}: missing REVIEW LOG comment or item-review-log.md reference")

    # 3. Required docs exist
    for rel in REQUIRED_DOCS:
        if not (ROOT / rel).exists():
            errors.append(f"Missing: {rel}")

    # 4. Skill exists
    skill_path = SKILLS / "toefl-item-review" / "SKILL.md"
    if not skill_path.exists():
        warnings.append(".cursor/skills/toefl-item-review/SKILL.md not found")

    # Write last-run stamp
    status = "FAIL" if errors else ("WARN" if warnings else "OK")
    lines = [
        f"status={status}",
        f"errors={len(errors)}",
        f"warnings={len(warnings)}",
    ]
    if errors:
        lines.append("")
        lines.extend("error: " + e for e in errors)
    if warnings:
        lines.append("")
        lines.extend("warning: " + w for w in warnings)
    try:
        LAST_RUN_FILE.parent.mkdir(parents=True, exist_ok=True)
        LAST_RUN_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    except OSError:
        pass  # non-fatal

    # Log to stderr for cron
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    if warnings:
        for w in warnings:
            print("warning:", w, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
