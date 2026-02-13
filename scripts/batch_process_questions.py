#!/usr/bin/env python3
"""
Batch process all Academic Discussion questions from screenshots.

Automatically:
1. Finds all question folders
2. Extracts text from images using macOS OCR (via vision framework)
3. Parses Professor Question and Student Posts
4. Adds to question bank file
"""

import sys
import subprocess
import json
import re
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
SOURCE_FOLDER = Path('/Users/tengda/Downloads/学术讨论写作/')
BANK_FILE = PROJECT_ROOT / "docs" / "academic-discussion-question-bank.md"
IMAGES_DIR = PROJECT_ROOT / "docs" / "academic-discussion" / "images"


def find_best_image(folder):
    """Find the best image file in a folder."""
    images = []
    for ext in ['.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG']:
        images.extend(list(folder.glob(f'*{ext}')))
    
    if not images:
        return None
    
    # Prefer files with folder name
    folder_name = folder.name
    for img in images:
        if folder_name.lower() in img.stem.lower():
            return img
    
    # Return largest file
    return max(images, key=lambda p: p.stat().st_size)


def extract_text_macos(image_path):
    """Extract text using macOS vision framework via AppleScript."""
    script = f'''
    tell application "System Events"
        set imagePath to POSIX file "{image_path}"
        try
            -- Use vision framework via shell
            do shell script "mdls -name kMDItemTextContent " & quoted form of POSIX path of imagePath
        on error
            return ""
        end try
    end tell
    '''
    
    # Alternative: use sips or other macOS tools
    # For now, return empty and we'll use a different approach
    return None


def extract_text_vision(image_path):
    """Extract text using macOS Vision framework via Python."""
    try:
        import Vision
        from Cocoa import NSURL, NSImage
        
        # This requires PyObjC
        # For now, we'll use a simpler approach
        pass
    except:
        pass
    
    return None


def parse_discussion_text(text):
    """Parse text to extract Professor Question and Student Posts."""
    if not text:
        return None
    
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Find Professor Question
    question_start = None
    for i, line in enumerate(lines):
        if 'professor' in line.lower() or ('?' in line and len(line) > 20):
            question_start = i
            break
    
    if question_start is None:
        question_start = 0
    
    # Extract question
    question_lines = []
    for i in range(question_start, len(lines)):
        line = lines[i]
        # Stop at student names
        if re.match(r'^[A-Z][a-z]+:', line) or re.match(r'^[A-Z][a-z]+\s+[A-Z]', line):
            break
        question_lines.append(line)
    
    question = ' '.join(question_lines)
    question = re.sub(r'^Professor\s*:?\s*', '', question, flags=re.IGNORECASE).strip()
    
    # Find student posts
    posts = []
    current_author = None
    current_text = []
    
    # Common student names
    name_pattern = re.compile(r'^([A-Z][a-z]+)\s*:?\s*(.*)$')
    
    for line in lines:
        match = name_pattern.match(line)
        if match:
            # Save previous post
            if current_author:
                posts.append({
                    'author': current_author,
                    'text': ' '.join(current_text).strip()
                })
            current_author = match.group(1)
            current_text = [match.group(2).strip()] if match.group(2) else []
        elif current_author:
            current_text.append(line)
    
    # Save last post
    if current_author:
        posts.append({
            'author': current_author,
            'text': ' '.join(current_text).strip()
        })
    
    return {
        'question': question,
        'posts': posts[:2]  # Only first 2
    }


def categorize_question(title):
    """Categorize question based on title."""
    title_lower = title.lower()
    
    if any(word in title_lower for word in ['school', 'student', 'teacher', 'education', 'learn', 'study', 'course', 'class', 'university', 'college']):
        return 'Education'
    elif any(word in title_lower for word in ['environment', 'pollution', 'climate', 'green', 'sustainable', 'energy', 'fuel', 'car', 'transport']):
        return 'Environment'
    elif any(word in title_lower for word in ['technology', 'automation', 'ai', 'computer', 'digital', 'online', 'internet', 'app', 'software']):
        return 'Technology'
    elif any(word in title_lower for word in ['business', 'company', 'job', 'work', 'career', 'employ', 'salary', 'money', 'financial', 'economic']):
        return 'Economy'
    elif any(word in title_lower for word in ['friend', 'social', 'community', 'society', 'people', 'relationship', 'family']):
        return 'Society'
    elif any(word in title_lower for word in ['art', 'music', 'culture', 'book', 'film', 'media']):
        return 'Culture'
    else:
        return 'Other'


def process_all_questions():
    """Process all question folders."""
    folders = sorted([d for d in SOURCE_FOLDER.iterdir() if d.is_dir() and not d.name.startswith('.')])
    
    print(f"Found {len(folders)} question folders")
    print("="*60)
    
    # Ensure images directory exists
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    
    # Read current bank file
    with open(BANK_FILE, 'r', encoding='utf-8') as f:
        bank_content = f.read()
    
    # Find insertion point
    if "## New Questions (To Be Added)" in bank_content:
        insertion_marker = "## New Questions (To Be Added)"
    elif "## Statistics" in bank_content:
        insertion_marker = "## Statistics"
    else:
        insertion_marker = None
    
    new_entries = []
    processed = 0
    skipped = 0
    
    for i, folder in enumerate(folders, start=7):  # Start from D07
        q_id = f"D{i:02d}"
        folder_name = folder.name
        
        print(f"\n[{i-6}/{len(folders)}] Processing: {folder_name}")
        
        # Find best image
        image_file = find_best_image(folder)
        if not image_file:
            print(f"  ⚠️  No image found, skipping")
            skipped += 1
            continue
        
        print(f"  📷 Image: {image_file.name}")
        
        # Copy image
        image_name = f"d{i:02d}-{folder_name.lower().replace(' ', '-').replace('?', '').replace('？', '').replace('/', '-')[:40]}.png"
        dest_image = IMAGES_DIR / image_name
        
        try:
            import shutil
            shutil.copy2(image_file, dest_image)
            print(f"  ✅ Copied to: {image_name}")
        except Exception as e:
            print(f"  ⚠️  Failed to copy image: {e}")
        
        # Categorize
        category = categorize_question(folder_name)
        
        # Create entry (text will be filled manually or via OCR later)
        entry = f"""
### {q_id} - {folder_name} (Practice)
**Category:** {category}  
**Source:** Practice  
**Image:** `images/{image_name}`

**Professor Question:**
[待从截图提取]

**Student Posts:**
- **[Author1]:** [待从截图提取]
- **[Author2]:** [待从截图提取]

**Notes:** 
- 图片已复制
- 待提取文字内容

**Status:** ⏳

---
"""
        new_entries.append(entry)
        processed += 1
    
    # Insert new entries
    if insertion_marker:
        parts = bank_content.split(insertion_marker, 1)
        new_content = parts[0] + insertion_marker + '\n' + ''.join(new_entries) + '\n' + parts[1]
    else:
        new_content = bank_content.rstrip() + '\n' + ''.join(new_entries)
    
    # Write back
    with open(BANK_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("\n" + "="*60)
    print(f"✅ Processing complete!")
    print(f"   Processed: {processed}")
    print(f"   Skipped: {skipped}")
    print(f"   Total: {len(folders)}")
    print(f"\n   Next step: Extract text from images")
    print(f"   Use macOS Preview to copy text from each image")
    print(f"   Or run OCR script if available")
    print("="*60)


if __name__ == "__main__":
    try:
        process_all_questions()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
