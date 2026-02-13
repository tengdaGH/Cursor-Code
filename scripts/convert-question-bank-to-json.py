#!/usr/bin/env python3
"""
Convert Academic Discussion Question Bank (Markdown) to JSON.

Reads from: docs/academic-discussion-question-bank.md
Writes to: data/writing-academic-discussion-prompts.json

Preserves existing questions (D01-D06) and adds new ones from the bank.
"""

import json
import re
import sys
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
BANK_FILE = PROJECT_ROOT / "docs" / "academic-discussion-question-bank.md"
JSON_FILE = PROJECT_ROOT / "data" / "writing-academic-discussion-prompts.json"


def parse_question_bank(md_content):
    """Parse Markdown question bank and extract questions."""
    questions = []
    
    # Split by question headers (### D{ID})
    question_blocks = re.split(r'\n###\s+(D\d+)', md_content)
    
    # First block is content before first question, skip it
    for i in range(1, len(question_blocks), 2):
        if i + 1 >= len(question_blocks):
            break
            
        q_id = question_blocks[i]
        content = question_blocks[i + 1]
        
        # Extract title
        title_match = re.search(r'-\s+(.+?)\s+\(([^)]+)\)', content)
        if not title_match:
            continue
        title = title_match.group(1).strip()
        source = title_match.group(2).strip()
        
        # Extract category
        category_match = re.search(r'\*\*Category:\*\*\s*(.+?)\s*\n', content)
        category = category_match.group(1).strip() if category_match else "other"
        
        # Extract source tag
        source_match = re.search(r'\*\*Source:\*\*\s*(.+?)\s*\n', content)
        source_tag = source_match.group(1).strip() if source_match else source
        
        # Extract image (optional)
        image_match = re.search(r'\*\*Image:\*\*\s*(.+?)\s*\n', content)
        image = image_match.group(1).strip() if image_match else None
        
        # Extract professor question (everything between "Professor Question:" and "Student Posts:")
        question_match = re.search(
            r'\*\*Professor Question:\*\*\s*\n(.*?)\n\*\*Student Posts:\*\*',
            content,
            re.DOTALL
        )
        if not question_match:
            continue
        question = question_match.group(1).strip()
        
        # Extract student posts
        # Look for Author1 and Author2 posts
        # Format: - **[Author1]:** or - **Author1:** followed by content (may be on next line)
        post1_match = re.search(
            r'-\s+\*\*\[?Author1\]?:\*\*\s*\n?(.*?)(?=\n-\s+\*\*\[?Author2\]?:\*\*|\n\*\*Notes:\*\*|\n\*\*Status:\*\*|\n---|\Z)',
            content,
            re.DOTALL
        )
        post1 = post1_match.group(1).strip() if post1_match else ""
        
        post2_match = re.search(
            r'-\s+\*\*\[?Author2\]?:\*\*\s*\n?(.*?)(?=\n\*\*Notes:\*\*|\n\*\*Status:\*\*|\n---|\Z)',
            content,
            re.DOTALL
        )
        post2 = post2_match.group(1).strip() if post2_match else ""
        
        # Extract author names from posts if present, otherwise use defaults
        # Check if post starts with a name pattern (e.g., "Alex: text" or "Alex text")
        author1_match = re.match(r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*:?\s*(.*)$', post1, re.DOTALL)
        if author1_match and len(author1_match.group(2).strip()) > 0:
            author1 = author1_match.group(1)
            post1 = author1_match.group(2).strip()
        else:
            # Check if it's a real name pattern at the start
            name_pattern = re.match(r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(.+)$', post1, re.DOTALL)
            if name_pattern and len(name_pattern.group(2).strip()) > 10:  # Reasonable length check
                author1 = name_pattern.group(1)
                post1 = name_pattern.group(2).strip()
            else:
                author1 = "Student1"
        
        author2_match = re.match(r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*:?\s*(.*)$', post2, re.DOTALL)
        if author2_match and len(author2_match.group(2).strip()) > 0:
            author2 = author2_match.group(1)
            post2 = author2_match.group(2).strip()
        else:
            name_pattern = re.match(r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+(.+)$', post2, re.DOTALL)
            if name_pattern and len(name_pattern.group(2).strip()) > 10:
                author2 = name_pattern.group(1)
                post2 = name_pattern.group(2).strip()
            else:
                author2 = "Student2"
        
        # Extract short description from title
        short_desc = title.split(' - ')[-1] if ' - ' in title else title
        
        questions.append({
            "id": q_id,
            "question": question,
            "posts": [
                {"author": author1, "text": post1},
                {"author": author2, "text": post2}
            ],
            "timeLimitMinutes": 10,
            "wordTarget": 120,
            "category": category.lower(),
            "source": source_tag,
            "shortDesc": short_desc,
            "shortDescEn": short_desc  # Can be customized later
        })
    
    return questions


def load_existing_json():
    """Load existing JSON file."""
    if not JSON_FILE.exists():
        return {
            "meta": {
                "format": "TOEFL 2026 Write for Academic Discussion",
                "rules": "Read professor's question and two student posts; write your own post (~100–120+ words) that contributes to the discussion with reasons or examples. ~10 min.",
                "reviewLogRef": "docs/item-review-log.md"
            },
            "prompts": []
        }
    
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def is_question_valid(q):
    """Check if a question has valid content."""
    # Check if question field is too short or looks incomplete
    if not q.get("question") or len(q["question"]) < 20:
        return False
    
    # Check if question looks like a fragment (starts with lowercase or ends abruptly)
    question = q["question"].strip()
    if question[0].islower() or question.endswith(("?", ":", ".", ",")) and len(question) < 50:
        # Might be incomplete, but check if it's a valid short question
        if len(question) < 30:
            return False
    
    # Check if posts are valid
    posts = q.get("posts", [])
    if len(posts) < 2:
        return False
    
    # Check if post text contains markdown headers (indicates parsing error)
    for post in posts:
        text = post.get("text", "")
        if "###" in text or "**Category:**" in text or "**Professor Question:**" in text:
            return False
    
    return True


def merge_questions(existing_data, new_questions, verbose=False):
    """Merge new questions with existing ones, updating invalid ones."""
    # Create a dict of new questions by ID
    new_questions_dict = {q["id"]: q for q in new_questions}
    
    # Process existing questions
    merged = []
    updated_count = 0
    kept_count = 0
    
    for existing_q in existing_data.get("prompts", []):
        q_id = existing_q["id"]
        
        # If new version exists
        if q_id in new_questions_dict:
            new_q = new_questions_dict[q_id]
            existing_valid = is_question_valid(existing_q)
            new_valid = is_question_valid(new_q)
            
            # Always prefer new version if:
            # 1. Existing is invalid
            # 2. New is valid and existing is invalid
            # 3. New question is longer (more complete)
            # 4. New posts are longer (more complete)
            
            should_update = False
            reason = ""
            
            if not existing_valid:
                should_update = True
                reason = "existing invalid"
            elif new_valid and not existing_valid:
                should_update = True
                reason = "new valid, existing invalid"
            elif new_valid and len(new_q.get("question", "")) > len(existing_q.get("question", "")):
                # Update if new question is longer (even slightly)
                should_update = True
                reason = f"new question longer ({len(new_q.get('question', ''))} vs {len(existing_q.get('question', ''))} chars)"
            elif new_valid:
                # Check if posts are better
                new_posts_total = sum(len(p.get("text", "")) for p in new_q.get("posts", []))
                existing_posts_total = sum(len(p.get("text", "")) for p in existing_q.get("posts", []))
                if new_posts_total > existing_posts_total * 1.2:
                    should_update = True
                    reason = f"new posts longer ({new_posts_total} vs {existing_posts_total} chars)"
            
            if should_update:
                merged.append(new_q)
                updated_count += 1
                if verbose:
                    print(f"  ✓ Updating {q_id}: {reason}")
            else:
                merged.append(existing_q)
                kept_count += 1
                if verbose and not existing_valid:
                    print(f"  ⚠ Keeping {q_id} (both invalid, keeping existing)")
        else:
            # Keep existing if no new version
            merged.append(existing_q)
            kept_count += 1
    
    # Add new questions that don't exist yet
    existing_ids = {p["id"] for p in merged}
    new_count = 0
    for q in new_questions:
        if q["id"] not in existing_ids:
            merged.append(q)
            new_count += 1
            if verbose:
                print(f"  + Adding new question {q['id']}")
    
    # Sort by ID
    merged.sort(key=lambda x: int(x["id"][1:]) if x["id"][1:].isdigit() else 999)
    
    if verbose:
        print(f"\n  Updated: {updated_count}, Kept: {kept_count}, New: {new_count}")
    
    return merged


def main():
    """Main conversion function."""
    if not BANK_FILE.exists():
        print(f"Error: Question bank file not found: {BANK_FILE}")
        sys.exit(1)
    
    # Read question bank
    print(f"Reading question bank from: {BANK_FILE}")
    with open(BANK_FILE, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Parse questions
    print("Parsing questions from Markdown...")
    new_questions = parse_question_bank(md_content)
    
    if not new_questions:
        print("Warning: No questions found in the bank file.")
        print("Make sure questions follow the template format.")
        sys.exit(1)
    
    print(f"Found {len(new_questions)} questions in bank.")
    
    # Load existing JSON
    print(f"Loading existing JSON from: {JSON_FILE}")
    existing_data = load_existing_json()
    existing_count = len(existing_data.get("prompts", []))
    print(f"Existing questions: {existing_count}")
    
    # Merge
    print("Merging questions...")
    all_questions = merge_questions(existing_data, new_questions, verbose=True)
    
    # Update data
    existing_data["prompts"] = all_questions
    
    # Write JSON
    print(f"Writing {len(all_questions)} questions to: {JSON_FILE}")
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Success!")
    print(f"   Total questions: {len(all_questions)}")
    print(f"   Existing: {existing_count}")
    print(f"   New: {len(all_questions) - existing_count}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
