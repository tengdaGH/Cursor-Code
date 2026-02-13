#!/usr/bin/env python3
"""
Simplified version: Extract text and update bank file one by one.
"""

import sys
import re
from pathlib import Path

try:
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

PROJECT_ROOT = Path(__file__).parent.parent
IMAGES_DIR = PROJECT_ROOT / "docs" / "academic-discussion" / "images"
BANK_FILE = PROJECT_ROOT / "docs" / "academic-discussion-question-bank.md"


def extract_text(image_path):
    """Extract text from image."""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang='eng')
        return text.strip()
    except Exception as e:
        return None


def parse_text(text):
    """Simple parsing."""
    if not text or len(text) < 50:
        return None
    
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # Find question (line with ?)
    question = None
    for line in lines:
        if '?' in line and len(line) > 30:
            question = line
            break
    
    if not question:
        return None
    
    # Find posts (look for names)
    posts = []
    name_pattern = re.compile(r'^([A-Z][a-z]+)\s*:?\s*(.*)$')
    
    for i, line in enumerate(lines):
        match = name_pattern.match(line)
        if match and len(match.group(1).split()) <= 2:
            # Found a name, collect text until next name or end
            author = match.group(1)
            post_text = [match.group(2)] if match.group(2).strip() else []
            
            # Collect following lines until next name
            for j in range(i+1, len(lines)):
                next_match = name_pattern.match(lines[j])
                if next_match and len(next_match.group(1).split()) <= 2:
                    break
                post_text.append(lines[j])
            
            posts.append({
                'author': author,
                'text': ' '.join(post_text).strip()
            })
            
            if len(posts) >= 2:
                break
    
    if len(posts) < 2:
        return None
    
    return {
        'question': question,
        'posts': posts[:2]
    }


def update_one_question(q_id, parsed):
    """Update one question in bank file."""
    with open(BANK_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the question block
    pattern = f'(### {re.escape(q_id)}[^#]+?\\*\\*Professor Question:\\*\\*\\s*\\n)\\[待从截图提取\\](\\s*\\n\\*\\*Student Posts:\\*\\*\\s*\\n-\\s+\\*\\*\\[Author1\\]:\\*\\*\\s*)\\[待从截图提取\\](\\s*\\n-\\s+\\*\\*\\[Author2\\]:\\*\\*\\s*)\\[待从截图提取\\]'
    
    def replacer(m):
        return (
            m.group(1) + parsed['question'] + 
            m.group(2) + parsed['posts'][0]['text'] +
            m.group(3) + parsed['posts'][1]['text']
        )
    
    new_content = re.sub(pattern, replacer, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(BANK_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False


def main():
    if not OCR_AVAILABLE:
        print("OCR not available")
        return
    
    images = sorted(IMAGES_DIR.glob('d*.png'))
    print(f"Processing {len(images)} images...\n")
    
    success = 0
    failed = 0
    
    for img_file in images:
        # Get question ID
        q_match = re.search(r'd(\d+)', img_file.stem)
        if not q_match:
            continue
        
        q_num = int(q_match.group(1))
        q_id = f"D{q_num:02d}"
        
        print(f"{q_id}: {img_file.name[:50]}...", end=' ')
        
        # Extract
        text = extract_text(img_file)
        if not text:
            print("❌ No text")
            failed += 1
            continue
        
        # Parse
        parsed = parse_text(text)
        if not parsed:
            print("❌ Parse failed")
            failed += 1
            continue
        
        # Update
        if update_one_question(q_id, parsed):
            print(f"✅ Q={len(parsed['question'])}")
            success += 1
        else:
            print("⚠️ Update failed")
            failed += 1
    
    print(f"\n✅ Success: {success}")
    print(f"❌ Failed: {failed}")


if __name__ == "__main__":
    main()
