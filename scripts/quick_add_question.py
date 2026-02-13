#!/usr/bin/env python3
"""
Quick helper script to add a question to the question bank.

Usage:
    python3 scripts/quick_add_question.py
    
This will prompt you to enter:
1. Question ID (e.g., D07)
2. Question title/short description
3. Category
4. Source
5. Professor Question text
6. Student Post 1 (author + text)
7. Student Post 2 (author + text)

Then it will format and append to the question bank file.
"""

import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
BANK_FILE = PROJECT_ROOT / "docs" / "academic-discussion-question-bank.md"


def get_input(prompt, default=None):
    """Get user input with optional default."""
    if default:
        response = input(f"{prompt} [{default}]: ").strip()
        return response if response else default
    return input(f"{prompt}: ").strip()


def add_question_to_bank():
    """Interactive function to add a question."""
    print("\n" + "="*60)
    print("Add New Academic Discussion Question")
    print("="*60 + "\n")
    
    # Get question details
    q_id = get_input("Question ID (e.g., D07)")
    if not q_id.startswith('D'):
        q_id = 'D' + q_id.lstrip('D')
    
    title = get_input("Question title/short description")
    category = get_input("Category", "Other")
    source = get_input("Source (OG/Real/Practice)", "Practice")
    image_name = f"d{q_id[1:]}-{title.lower().replace(' ', '-').replace('?', '').replace('？', '')[:30]}.png"
    
    print("\n" + "-"*60)
    print("Professor Question:")
    print("(Paste the question text, press Enter twice when done)")
    question_lines = []
    while True:
        line = input()
        if not line and question_lines:
            break
        if line:
            question_lines.append(line)
    professor_question = ' '.join(question_lines).strip()
    
    print("\n" + "-"*60)
    print("Student Post 1:")
    author1 = get_input("Author name")
    print("Post text (press Enter twice when done):")
    post1_lines = []
    while True:
        line = input()
        if not line and post1_lines:
            break
        if line:
            post1_lines.append(line)
    post1_text = ' '.join(post1_lines).strip()
    
    print("\n" + "-"*60)
    print("Student Post 2:")
    author2 = get_input("Author name")
    print("Post text (press Enter twice when done):")
    post2_lines = []
    while True:
        line = input()
        if not line and post2_lines:
            break
        if line:
            post2_lines.append(line)
    post2_text = ' '.join(post2_lines).strip()
    
    # Format the question entry
    entry = f"""
### {q_id} - {title} ({source})
**Category:** {category}  
**Source:** {source}  
**Image:** `images/{image_name}`

**Professor Question:**
{professor_question}

**Student Posts:**
- **{author1}:** {post1_text}
- **{author2}:** {post2_text}

**Notes:** 
- [待添加]

**Status:** ⏳

---
"""
    
    # Read current bank file
    with open(BANK_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find insertion point (before "## Statistics")
    if "## Statistics" in content:
        insertion_point = content.find("## Statistics")
        new_content = content[:insertion_point] + entry + "\n" + content[insertion_point:]
    else:
        # Append at the end
        new_content = content.rstrip() + "\n" + entry
    
    # Write back
    with open(BANK_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("\n" + "="*60)
    print("✅ Question added successfully!")
    print(f"   ID: {q_id}")
    print(f"   Title: {title}")
    print(f"   Image: {image_name}")
    print(f"\n   Next steps:")
    print(f"   1. Copy image to: docs/academic-discussion/images/{image_name}")
    print(f"   2. Review the entry in: {BANK_FILE}")
    print(f"   3. Change status to ✅ when verified")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        add_question_to_bank()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
