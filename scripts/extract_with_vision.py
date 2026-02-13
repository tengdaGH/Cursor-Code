#!/usr/bin/env python3
"""
Extract text using macOS Vision framework (same as Preview app uses).
This should be more accurate than Tesseract.
"""

import sys
import re
from pathlib import Path

try:
    from Cocoa import NSURL
    from Vision import VNImageRequestHandler, VNRecognizeTextRequest
    import objc
    VISION_AVAILABLE = True
except ImportError as e:
    VISION_AVAILABLE = False
    print(f"Vision framework not available: {e}")


def extract_text_vision(image_path):
    """Extract text using macOS Vision framework."""
    if not VISION_AVAILABLE:
        return None
    
    try:
        image_url = NSURL.fileURLWithPath_(str(image_path))
        
        # Create request handler
        handler = VNImageRequestHandler.alloc().initWithURL_options_(image_url, None)
        
        # Create text recognition request - use accurate mode
        request = VNRecognizeTextRequest.alloc().init()
        request.setRecognitionLevel_(1)  # 0=fast, 1=accurate (same as Preview)
        
        # Perform request - use None for error parameter
        success = handler.performRequests_error_([request], None)
        
        if not success:
            return None
        
        # Extract text from results
        observations = request.results()
        if not observations:
            return None
        
        text_lines = []
        for observation in observations:
            candidates = observation.topCandidates_(1)
            if candidates and len(candidates) > 0:
                text = candidates[0].string()
                text_lines.append(text)
        
        return '\n'.join(text_lines)
    
    except Exception as e:
        print(f"  Vision OCR error: {e}")
        import traceback
        traceback.print_exc()
        return None


def parse_discussion_text(text):
    """Parse extracted text."""
    if not text or len(text.strip()) < 50:
        return None
    
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # Find question (line with ?)
    question = None
    question_idx = 0
    for i, line in enumerate(lines):
        if '?' in line and len(line) > 30:
            question = line
            question_idx = i
            break
    
    if not question:
        # Try to find any long line that might be a question
        for line in lines:
            if len(line) > 50:
                question = line
                break
    
    if not question:
        return None
    
    # Find student posts
    posts = []
    remaining = lines[question_idx + 1:] if question_idx > 0 else lines
    
    # Look for names followed by text
    name_pattern = re.compile(r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*:?\s*(.*)$')
    
    current_author = None
    current_text = []
    
    for line in remaining:
        if len(line) < 5:
            continue
        
        match = name_pattern.match(line)
        if match:
            name = match.group(1).strip()
            # Check if it's a valid name (1-2 words, capitalized)
            if len(name.split()) <= 2 and name[0].isupper():
                # Save previous
                if current_author and current_text:
                    posts.append({
                        'author': current_author,
                        'text': ' '.join(current_text).strip()
                    })
                current_author = name
                rest = match.group(2).strip()
                current_text = [rest] if rest else []
            else:
                if current_author:
                    current_text.append(line)
        else:
            if current_author:
                current_text.append(line)
    
    # Save last post
    if current_author and current_text:
        posts.append({
            'author': current_author,
            'text': ' '.join(current_text).strip()
        })
    
    # If we don't have 2 posts, try to find them another way
    if len(posts) < 2:
        # Look for paragraphs that might be student posts
        all_text = ' '.join(remaining)
        if len(all_text) > 100:
            # Try to split by common patterns
            parts = re.split(r'(?:^|\n)([A-Z][a-z]+\s*:?\s*)', all_text, flags=re.MULTILINE)
            if len(parts) >= 3:
                for i in range(1, len(parts), 2):
                    if i + 1 < len(parts):
                        author = parts[i].strip().rstrip(':').strip()
                        text = parts[i+1].strip()
                        if len(text) > 20:
                            posts.append({'author': author, 'text': text})
                            if len(posts) >= 2:
                                break
    
    if len(posts) < 2:
        return None
    
    return {
        'question': question,
        'posts': posts[:2]
    }


def update_question_in_bank(q_id, parsed):
    """Update one question in bank file."""
    bank_file = Path(__file__).parent.parent / "docs" / "academic-discussion-question-bank.md"
    
    with open(bank_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match the question block
    pattern = (
        f'(### {re.escape(q_id)}[^#]+?\\*\\*Professor Question:\\*\\*\\s*\\n)'
        r'\[待从截图提取\]'
        r'(\s*\n\*\*Student Posts:\*\*\s*\n-\s+\*\*\[Author1\]:\*\*\s*)'
        r'\[待从截图提取\]'
        r'(\s*\n-\s+\*\*\[Author2\]:\*\*\s*)'
        r'\[待从截图提取\]'
    )
    
    def replacer(m):
        return (
            m.group(1) + parsed['question'] + 
            m.group(2) + parsed['posts'][0]['text'] +
            m.group(3) + parsed['posts'][1]['text']
        )
    
    new_content = re.sub(pattern, replacer, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(bank_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False


def main():
    if not VISION_AVAILABLE:
        print("❌ Vision framework not available")
        return
    
    # Find failed questions
    bank_file = Path(__file__).parent.parent / "docs" / "academic-discussion-question-bank.md"
    images_dir = Path(__file__).parent.parent / "docs" / "academic-discussion" / "images"
    
    with open(bank_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find questions that need extraction
    failed_ids = []
    for i in range(7, 94):
        q_id = f"D{i:02d}"
        pattern = f'### {re.escape(q_id)}.*?\\*\\*Professor Question:\\*\\*\\s*\\n(.*?)\\n\\*\\*Student Posts:'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            q_text = match.group(1)
            if '[待从截图提取]' in q_text or len(q_text.strip()) < 20:
                failed_ids.append(q_id)
    
    print(f"Found {len(failed_ids)} questions needing extraction")
    print("="*60 + "\n")
    
    success = 0
    failed = 0
    
    for q_id in failed_ids:
        q_num = q_id[1:]
        # Find image file
        pattern = f'd{q_num}-*.png'
        matches = list(images_dir.glob(pattern))
        
        if not matches:
            print(f"{q_id}: ⚠️  No image found")
            failed += 1
            continue
        
        img_file = matches[0]
        print(f"{q_id}: {img_file.name[:50]}...", end=' ')
        
        # Extract text
        text = extract_text_vision(img_file)
        if not text:
            print("❌ No text")
            failed += 1
            continue
        
        # Parse
        parsed = parse_discussion_text(text)
        if not parsed or len(parsed['posts']) < 2:
            print(f"❌ Parse failed (Q={bool(parsed)}, P={len(parsed['posts']) if parsed else 0})")
            failed += 1
            continue
        
        # Update bank
        if update_question_in_bank(q_id, parsed):
            print(f"✅ Q={len(parsed['question'])} chars")
            success += 1
        else:
            print("⚠️  Update failed")
            failed += 1
    
    print("\n" + "="*60)
    print(f"✅ Success: {success}")
    print(f"❌ Failed: {failed}")
    print("="*60)


if __name__ == "__main__":
    main()
