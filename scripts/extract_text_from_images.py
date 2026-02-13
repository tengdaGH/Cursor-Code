#!/usr/bin/env python3
"""
Extract text from Academic Discussion question screenshots using OCR.

Usage:
    python3 scripts/extract_text_from_images.py "/path/to/question/folder"
    
Or process all questions:
    python3 scripts/extract_text_from_images.py "/Users/tengda/Downloads/学术讨论写作/" --all
"""

import sys
import os
from pathlib import Path
import json

try:
    from PIL import Image
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("Warning: pytesseract or PIL not installed. Install with:")
    print("  pip install pytesseract pillow")
    print("  brew install tesseract  # macOS")


def extract_text_from_image(image_path):
    """Extract text from an image using OCR."""
    if not OCR_AVAILABLE:
        return None
    
    try:
        image = Image.open(image_path)
        # Use English + Chinese OCR
        text = pytesseract.image_to_string(image, lang='eng+chi_sim')
        return text.strip()
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None


def find_best_image(folder_path):
    """Find the best image file in a folder (prefer .png with question name)."""
    folder = Path(folder_path)
    images = []
    
    # Look for images
    for ext in ['.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG']:
        images.extend(list(folder.glob(f'*{ext}')))
    
    if not images:
        return None
    
    # Prefer files with question name (folder name)
    folder_name = folder.name
    for img in images:
        if folder_name.lower() in img.stem.lower():
            return img
    
    # Otherwise return the largest file (likely highest quality)
    return max(images, key=lambda p: p.stat().st_size)


def parse_discussion_text(ocr_text):
    """Parse OCR text to extract Professor Question and Student Posts."""
    lines = [line.strip() for line in ocr_text.split('\n') if line.strip()]
    
    # Try to find Professor Question (usually starts with "Professor:" or question mark)
    question_start = None
    for i, line in enumerate(lines):
        if 'professor' in line.lower() or '?' in line:
            question_start = i
            break
    
    if question_start is None:
        question_start = 0
    
    # Extract question (usually ends before student names)
    question_lines = []
    for i in range(question_start, len(lines)):
        line = lines[i]
        # Stop if we see common student name patterns
        if any(name in line.lower() for name in ['alex', 'sam', 'jordan', 'casey', 'riley', 'morgan']):
            break
        question_lines.append(line)
    
    question = ' '.join(question_lines).replace('Professor:', '').replace('Professor', '').strip()
    
    # Find student posts (look for names followed by text)
    posts = []
    current_author = None
    current_text = []
    
    for line in lines:
        # Check if line starts with a name (common patterns)
        potential_name = None
        for name in ['Alex', 'Sam', 'Jordan', 'Casey', 'Riley', 'Morgan', 'Taylor', 'Jamie', 
                     'Quinn', 'Avery', 'Parker', 'Skyler', 'Chris', 'Pat', 'Lee', 'Kim']:
            if line.startswith(name + ':') or line.startswith(name + ':'):
                potential_name = name
                break
        
        if potential_name:
            # Save previous post if exists
            if current_author:
                posts.append({
                    'author': current_author,
                    'text': ' '.join(current_text).strip()
                })
            current_author = potential_name
            current_text = [line.split(':', 1)[1].strip() if ':' in line else '']
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
        'posts': posts[:2]  # Only take first 2 posts
    }


def process_question_folder(folder_path, output_file=None):
    """Process a single question folder and extract text."""
    folder = Path(folder_path)
    
    if not folder.is_dir():
        print(f"Error: {folder_path} is not a directory")
        return None
    
    print(f"\nProcessing: {folder.name}")
    print("-" * 60)
    
    # Find best image
    image_file = find_best_image(folder)
    if not image_file:
        print("  ❌ No image found")
        return None
    
    print(f"  📷 Using image: {image_file.name}")
    
    # Extract text
    print("  🔍 Extracting text...")
    ocr_text = extract_text_from_image(image_file)
    
    if not ocr_text:
        print("  ❌ Failed to extract text")
        return None
    
    # Parse text
    print("  📝 Parsing discussion...")
    parsed = parse_discussion_text(ocr_text)
    
    # Display results
    print(f"\n  ✅ Professor Question:")
    print(f"     {parsed['question'][:100]}...")
    print(f"\n  ✅ Student Posts ({len(parsed['posts'])}):")
    for post in parsed['posts']:
        print(f"     - {post['author']}: {post['text'][:60]}...")
    
    # Save to file if requested
    if output_file:
        result = {
            'folder': folder.name,
            'image': str(image_file),
            'ocr_text': ocr_text,
            'parsed': parsed
        }
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')
    
    return parsed


def main():
    """Main function."""
    if not OCR_AVAILABLE:
        print("\n❌ OCR libraries not available.")
        print("\nTo install:")
        print("  1. Install Tesseract OCR:")
        print("     brew install tesseract  # macOS")
        print("     # or download from: https://github.com/tesseract-ocr/tesseract")
        print("\n  2. Install Python libraries:")
        print("     pip install pytesseract pillow")
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 scripts/extract_text_from_images.py <question_folder>")
        print("  python3 scripts/extract_text_from_images.py <parent_folder> --all")
        sys.exit(1)
    
    target_path = Path(sys.argv[1])
    process_all = '--all' in sys.argv
    
    if process_all:
        # Process all question folders
        output_file = Path(__file__).parent.parent / 'docs' / 'academic-discussion' / 'ocr_results.jsonl'
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        if output_file.exists():
            output_file.unlink()  # Clear previous results
        
        folders = [d for d in target_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
        folders.sort()
        
        print(f"Found {len(folders)} question folders")
        print(f"Output: {output_file}")
        print("\nProcessing all questions...")
        
        for folder in folders:
            try:
                process_question_folder(folder, output_file)
            except KeyboardInterrupt:
                print("\n\n⚠️  Interrupted by user")
                break
            except Exception as e:
                print(f"\n❌ Error processing {folder.name}: {e}")
                continue
        
        print(f"\n✅ Done! Results saved to: {output_file}")
    else:
        # Process single folder
        result = process_question_folder(target_path)
        if result:
            print("\n✅ Extraction complete!")
            print("\nYou can now add this to the question bank manually or use the parsed data.")


if __name__ == "__main__":
    main()
