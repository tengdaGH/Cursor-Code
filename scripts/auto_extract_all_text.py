#!/usr/bin/env python3
"""
Automatically extract text from all question images and update the question bank.

This script:
1. Reads all images from docs/academic-discussion/images/
2. Extracts text using OCR
3. Parses Professor Question and Student Posts
4. Updates the question bank file automatically
"""

import sys
import re
from pathlib import Path
from datetime import datetime

try:
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

PROJECT_ROOT = Path(__file__).parent.parent
IMAGES_DIR = PROJECT_ROOT / "docs" / "academic-discussion" / "images"
BANK_FILE = PROJECT_ROOT / "docs" / "academic-discussion-question-bank.md"


def extract_text_ocr(image_path):
    """Extract text from image using OCR."""
    if not OCR_AVAILABLE:
        return None
    
    try:
        image = Image.open(image_path)
        # Try English first
        text = pytesseract.image_to_string(image, lang='eng')
        # If result is too short, try with Chinese
        if len(text.strip()) < 100:
            try:
                text_cn = pytesseract.image_to_string(image, lang='chi_sim+eng')
                if len(text_cn.strip()) > len(text.strip()):
                    text = text_cn
            except:
                pass
        return text.strip()
    except Exception as e:
        print(f"    Error: {e}")
        return None


def parse_discussion_text(text):
    """Parse OCR text to extract Professor Question and Student Posts."""
    if not text or len(text.strip()) < 50:
        return None
    
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Find Professor Question (usually contains "?" and is a complete sentence)
    question = None
    question_end_idx = 0
    
    for i, line in enumerate(lines):
        if '?' in line and len(line) > 30:
            # Check if it looks like a question
            question_words = ['do you', 'should', 'think', 'believe', 'what', 'why', 'how', 
                            'would', 'could', 'is', 'are', 'does', 'will']
            if any(word in line.lower() for word in question_words):
                question = line
                question_end_idx = i
                break
    
    # If no clear question, take first long line
    if not question:
        for i, line in enumerate(lines):
            if len(line) > 50 and ('?' in line or line.endswith('?')):
                question = line
                question_end_idx = i
                break
    
    if not question:
        return None
    
    # Find student posts
    posts = []
    remaining_lines = lines[question_end_idx + 1:]
    
    # Pattern: Name followed by colon or space, then text
    name_pattern = re.compile(r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*:?\s*(.*)$')
    
    current_author = None
    current_text = []
    
    for line in remaining_lines:
        # Skip empty or very short lines
        if len(line) < 5:
            continue
        
        # Check if line starts with a name
        match = name_pattern.match(line)
        if match:
            name = match.group(1).strip()
            # Common student names (Alex, Sam, Jordan, etc.)
            if len(name.split()) <= 2 and name[0].isupper():
                # Save previous post
                if current_author and current_text:
                    posts.append({
                        'author': current_author,
                        'text': ' '.join(current_text).strip()
                    })
                current_author = name
                rest = match.group(2).strip()
                current_text = [rest] if rest else []
            else:
                # Not a name, continue current post
                if current_author:
                    current_text.append(line)
        else:
            # Continue current post or start new if we have enough content
            if current_author:
                current_text.append(line)
            elif len(posts) < 2 and len(line) > 20:
                # Might be a student post without clear name
                posts.append({
                    'author': f'Student{len(posts)+1}',
                    'text': line
                })
    
    # Save last post
    if current_author and current_text:
        posts.append({
            'author': current_author,
            'text': ' '.join(current_text).strip()
        })
    
    # Ensure we have 2 posts
    if len(posts) < 2:
        # Try to split remaining text into posts
        all_remaining = ' '.join(remaining_lines)
        if len(all_remaining) > 100:
            # Split roughly in half
            mid = len(all_remaining) // 2
            # Find a good split point (sentence end)
            for i in range(mid-50, mid+50):
                if i < len(all_remaining) and all_remaining[i] in '.!?':
                    posts = [
                        {'author': 'Student1', 'text': all_remaining[:i+1].strip()},
                        {'author': 'Student2', 'text': all_remaining[i+1:].strip()}
                    ]
                    break
    
    return {
        'question': question,
        'posts': posts[:2] if len(posts) >= 2 else posts
    }


def update_bank_file():
    """Update bank file with extracted text."""
    if not OCR_AVAILABLE:
        print("❌ OCR libraries not available.")
        print("\nTo install:")
        print("  pip install pytesseract pillow")
        print("  brew install tesseract")
        return False
    
    # Read bank file
    print(f"Reading bank file: {BANK_FILE}")
    with open(BANK_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all question entries that need text extraction
    pattern = r'(### D\d+\s+-[^\n]+\n.*?\*\*Professor Question:\*\*\s*\n)\[待从截图提取\](\s*\n\*\*Student Posts:\*\*\s*\n-\s+\*\*\[Author1\]:\*\*\s*)\[待从截图提取\](\s*\n-\s+\*\*\[Author2\]:\*\*\s*)\[待从截图提取\]'
    
    matches = list(re.finditer(pattern, content, re.DOTALL))
    print(f"Found {len(matches)} questions needing text extraction")
    
    if not matches:
        print("No questions found that need text extraction.")
        return True
    
    # Process each image
    image_files = sorted(IMAGES_DIR.glob('d*.png'))
    print(f"Found {len(image_files)} images to process\n")
    
    updated_count = 0
    failed_count = 0
    
    for img_file in image_files:
        # Extract question number from filename
        q_num_match = re.search(r'd(\d+)', img_file.stem)
        if not q_num_match:
            continue
        
        q_num = int(q_num_match.group(1))
        q_id = f"D{q_num:02d}"
        
        print(f"Processing {q_id}: {img_file.name}")
        
        # Extract text
        text = extract_text_ocr(img_file)
        if not text:
            print(f"  ⚠️  Could not extract text")
            failed_count += 1
            continue
        
        # Parse
        parsed = parse_discussion_text(text)
        if not parsed or not parsed['question'] or len(parsed['posts']) < 2:
            print(f"  ⚠️  Could not parse (Question: {bool(parsed and parsed.get('question'))}, Posts: {len(parsed['posts']) if parsed else 0})")
            failed_count += 1
            continue
        
        # Find and replace in content - use a function to avoid group reference issues
        def replace_func(match):
            return (
                match.group(1) + parsed['question'] + 
                match.group(2) + parsed['posts'][0]['text'] +
                match.group(3) + parsed['posts'][1]['text']
            )
        
        question_pattern = f'(### {re.escape(q_id)}[^#]+?\\*\\*Professor Question:\\*\\*\\s*\\n)\\[待从截图提取\\](\\s*\\n\\*\\*Student Posts:\\*\\*\\s*\\n-\\s+\\*\\*\\[Author1\\]:\\*\\*\\s*)\\[待从截图提取\\](\\s*\\n-\\s+\\*\\*\\[Author2\\]:\\*\\*\\s*)\\[待从截图提取\\]'
        
        new_content = re.sub(question_pattern, replace_func, content, flags=re.DOTALL)
        
        if new_content != content:
            content = new_content
            print(f"  ✅ Extracted: Q={len(parsed['question'])} chars, Posts={len(parsed['posts'])}")
            updated_count += 1
        else:
            print(f"  ⚠️  Pattern not found in bank file")
            failed_count += 1
    
    # Write updated content
    if updated_count > 0:
        with open(BANK_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n✅ Updated {updated_count} questions in bank file")
        print(f"⚠️  Failed: {failed_count} questions")
        return True
    else:
        print(f"\n⚠️  No questions were updated")
        return False


if __name__ == "__main__":
    print("="*60)
    print("Automatic Text Extraction from Images")
    print("="*60 + "\n")
    
    try:
        success = update_bank_file()
        if success:
            print("\n✅ Text extraction complete!")
            print("\nNext steps:")
            print("1. Review extracted text in the bank file")
            print("2. Fix any errors manually")
            print("3. Run: python3 scripts/convert-question-bank-to-json.py")
        else:
            print("\n⚠️  Text extraction had issues. Please review.")
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
