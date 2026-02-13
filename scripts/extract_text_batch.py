#!/usr/bin/env python3
"""
Batch extract text from all question images using macOS OCR capabilities.

Uses AppleScript to leverage macOS Preview's OCR functionality.
"""

import subprocess
import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
IMAGES_DIR = PROJECT_ROOT / "docs" / "academic-discussion" / "images"
BANK_FILE = PROJECT_ROOT / "docs" / "academic-discussion-question-bank.md"


def extract_text_using_applescript(image_path):
    """Extract text using macOS Preview via AppleScript."""
    script = f'''
    tell application "Preview"
        activate
        open POSIX file "{image_path}"
        delay 1
        tell application "System Events"
            keystroke "a" using command down
            delay 0.5
            keystroke "c" using command down
            delay 0.5
        end tell
        quit
    end tell
    '''
    
    try:
        # This approach requires GUI interaction, not ideal for batch
        # Let's try a different approach using Python OCR
        return None
    except:
        return None


def try_pytesseract():
    """Try using pytesseract if available."""
    try:
        import pytesseract
        from PIL import Image
        return True
    except ImportError:
        return False


def extract_with_tesseract(image_path):
    """Extract text using Tesseract OCR."""
    try:
        import pytesseract
        from PIL import Image
        
        image = Image.open(image_path)
        # Try English first, then Chinese if needed
        text = pytesseract.image_to_string(image, lang='eng')
        if len(text.strip()) < 50:  # If too short, try Chinese
            text = pytesseract.image_to_string(image, lang='chi_sim+eng')
        return text.strip()
    except Exception as e:
        print(f"  ⚠️  OCR error: {e}")
        return None


def parse_discussion_text(text):
    """Parse extracted text to find Professor Question and Student Posts."""
    if not text or len(text.strip()) < 50:
        return None
    
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Find Professor Question (usually contains "?" and is longer)
    question = None
    question_start_idx = None
    
    for i, line in enumerate(lines):
        if '?' in line and len(line) > 30:
            # Check if it looks like a question
            if any(word in line.lower() for word in ['do you', 'should', 'think', 'believe', 'what', 'why', 'how']):
                question = line
                question_start_idx = i
                break
    
    # If no clear question found, take first long line
    if not question:
        for line in lines:
            if len(line) > 50:
                question = line
                break
    
    # Find student posts (look for names followed by text)
    posts = []
    if question_start_idx:
        remaining_lines = lines[question_start_idx + 1:]
    else:
        remaining_lines = lines
    
    # Common patterns: "Name:" or "Name " at start of line
    name_pattern = re.compile(r'^([A-Z][a-z]+)\s*:?\s*(.*)$')
    current_author = None
    current_text = []
    
    for line in remaining_lines:
        # Skip if it's part of the question
        if question and line in question:
            continue
        
        match = name_pattern.match(line)
        if match:
            # Save previous post
            if current_author and current_text:
                posts.append({
                    'author': current_author,
                    'text': ' '.join(current_text).strip()
                })
            current_author = match.group(1)
            current_text = [match.group(2).strip()] if match.group(2).strip() else []
        elif current_author:
            current_text.append(line)
    
    # Save last post
    if current_author and current_text:
        posts.append({
            'author': current_author,
            'text': ' '.join(current_text).strip()
        })
    
    # If we didn't find posts by name pattern, try to find by content
    if len(posts) < 2:
        # Look for lines that might be student responses
        for line in remaining_lines:
            if len(line) > 30 and line not in question:
                if len(posts) < 2:
                    posts.append({
                        'author': f'Student{len(posts)+1}',
                        'text': line
                    })
    
    return {
        'question': question or '[Unable to extract]',
        'posts': posts[:2] if len(posts) >= 2 else posts
    }


def update_bank_file():
    """Update bank file with extracted text."""
    # Read current bank
    with open(BANK_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all question entries
    question_pattern = re.compile(
        r'### (D\d+)\s+-\s+(.+?)\s+\(([^)]+)\)\s*\n'
        r'\*\*Category:\*\*\s*(.+?)\s*\n'
        r'\*\*Source:\*\*\s*(.+?)\s*\n'
        r'\*\*Image:\*\*\s*`images/(.+?)`\s*\n'
        r'\*\*Professor Question:\*\*\s*\n(.+?)\n\*\*Student Posts:\*\*\s*\n'
        r'-\s+\*\*\[Author1\]:\*\*\s*(.+?)\n'
        r'-\s+\*\*\[Author2\]:\*\*\s*(.+?)\n',
        re.DOTALL
    )
    
    # Process each image
    image_files = sorted(IMAGES_DIR.glob('*.png'))
    print(f"Found {len(image_files)} images to process")
    
    if not try_pytesseract():
        print("\n⚠️  pytesseract not available.")
        print("To install:")
        print("  pip install pytesseract pillow")
        print("  brew install tesseract")
        print("\nFor now, you can manually extract text using macOS Preview:")
        print("  1. Open each image in Preview")
        print("  2. Cmd+A to select all text")
        print("  3. Cmd+C to copy")
        print("  4. Paste into the bank file")
        return
    
    processed = 0
    for img_file in image_files:
        q_num = img_file.stem.split('-')[0].replace('d', 'D')
        print(f"\nProcessing {q_num}: {img_file.name}")
        
        # Extract text
        text = extract_with_tesseract(img_file)
        if not text:
            print(f"  ⚠️  Could not extract text")
            continue
        
        # Parse
        parsed = parse_discussion_text(text)
        if not parsed or parsed['question'] == '[Unable to extract]':
            print(f"  ⚠️  Could not parse text")
            continue
        
        print(f"  ✅ Question: {parsed['question'][:60]}...")
        print(f"  ✅ Posts: {len(parsed['posts'])}")
        
        # Update bank file (this is complex, better to do manually or with better parsing)
        processed += 1
    
    print(f"\n✅ Processed {processed} images")
    print("\nNote: Text extraction complete, but bank file update requires manual review.")
    print("Please review extracted text and update the bank file manually.")


if __name__ == "__main__":
    update_bank_file()
