#!/usr/bin/env python3
"""
Fix incomplete extractions by re-processing with better parsing logic.
"""

import sys
import re
from pathlib import Path

try:
    from Cocoa import NSURL
    from Vision import VNImageRequestHandler, VNRecognizeTextRequest
    VISION_AVAILABLE = True
except ImportError:
    VISION_AVAILABLE = False


def extract_all_text_vision(image_path):
    """Extract ALL text from image using Vision framework."""
    if not VISION_AVAILABLE:
        return None
    
    try:
        image_url = NSURL.fileURLWithPath_(str(image_path))
        handler = VNImageRequestHandler.alloc().initWithURL_options_(image_url, None)
        request = VNRecognizeTextRequest.alloc().init()
        request.setRecognitionLevel_(1)  # Accurate mode
        
        handler.performRequests_error_([request], None)
        observations = request.results()
        
        if not observations:
            return None
        
        # Get all text, preserving order
        all_text = []
        for obs in observations:
            candidates = obs.topCandidates_(1)
            if candidates and len(candidates) > 0:
                text = candidates[0].string()
                all_text.append(text)
        
        return '\n'.join(all_text)
    
    except Exception as e:
        return None


def parse_discussion_improved(text):
    """Improved parsing that handles various formats."""
    if not text or len(text.strip()) < 50:
        return None
    
    # Clean up text
    lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 2]
    
    # Find question - look for lines with ? that are complete sentences
    question = None
    question_end = 0
    
    for i, line in enumerate(lines):
        # Skip header lines
        if any(word in line.lower() for word in ['toefl', 'volume', 'writing', 'question', 'help', 'next']):
            continue
        
        if '?' in line:
            # Check if it's a complete question
            if len(line) > 30 and any(word in line.lower() for word in 
                ['do you', 'should', 'think', 'believe', 'what', 'why', 'how', 'would', 'could', 'is', 'are']):
                question = line
                question_end = i
                break
    
    # If no question with ?, try to find longest line that might be a question
    if not question:
        for i, line in enumerate(lines):
            if any(word in line.lower() for word in ['toefl', 'volume', 'writing']):
                continue
            if len(line) > 60:
                question = line
                question_end = i
                break
    
    if not question:
        return None
    
    # Find student posts - look for names or paragraphs after question
    remaining = lines[question_end + 1:]
    posts = []
    
    # Pattern 1: Name: text
    name_pattern = re.compile(r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*:?\s*(.*)$')
    
    current_author = None
    current_text = []
    
    for line in remaining:
        # Skip UI elements
        if any(word in line.lower() for word in ['toefl', 'volume', 'writing', 'question', 'help', 'next', 'previous']):
            continue
        
        match = name_pattern.match(line)
        if match:
            name = match.group(1).strip()
            # Valid name: 1-2 words, starts with capital
            if len(name.split()) <= 2 and name[0].isupper() and len(name) > 2:
                # Save previous
                if current_author and current_text:
                    post_text = ' '.join(current_text).strip()
                    if len(post_text) > 15:
                        posts.append({
                            'author': current_author,
                            'text': post_text
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
            elif len(posts) < 2 and len(line) > 30:
                # Might be a post without clear name
                posts.append({
                    'author': f'Student{len(posts)+1}',
                    'text': line
                })
    
    # Save last post
    if current_author and current_text:
        post_text = ' '.join(current_text).strip()
        if len(post_text) > 15:
            posts.append({
                'author': current_author,
                'text': post_text
            })
    
    # If still don't have 2 posts, try to find paragraphs
    if len(posts) < 2:
        # Look for long paragraphs
        all_remaining = ' '.join(remaining)
        if len(all_remaining) > 100:
            # Try to split into 2 parts
            sentences = re.split(r'[.!?]\s+', all_remaining)
            if len(sentences) >= 4:
                mid = len(sentences) // 2
                post1_text = '. '.join(sentences[:mid]) + '.'
                post2_text = '. '.join(sentences[mid:])
                
                if len(post1_text) > 30 and len(post2_text) > 30:
                    posts = [
                        {'author': 'Student1', 'text': post1_text},
                        {'author': 'Student2', 'text': post2_text}
                    ]
    
    if len(posts) < 2:
        return None
    
    return {
        'question': question,
        'posts': posts[:2]
    }


def update_question(q_id, parsed):
    """Update question in bank file."""
    bank_file = Path(__file__).parent.parent / "docs" / "academic-discussion-question-bank.md"
    
    with open(bank_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the question block
    pattern = f'(### {re.escape(q_id)}[^#]+?\\*\\*Professor Question:\\*\\*\\s*\\n)(.*?)(\\s*\\n\\*\\*Student Posts:\\*\\*\\s*\\n-\\s+\\*\\*\\[Author1\\]:\\*\\*\\s*)(.*?)(\\s*\\n-\\s+\\*\\*\\[Author2\\]:\\*\\*\\s*)(.*?)(\\s*\\n\\*\\*Notes:)'
    
    def replacer(m):
        return (
            m.group(1) + parsed['question'] + 
            m.group(3) + parsed['posts'][0]['text'] +
            m.group(5) + parsed['posts'][1]['text'] +
            m.group(7)
        )
    
    new_content = re.sub(pattern, replacer, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(bank_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False


def main():
    if not VISION_AVAILABLE:
        print("Vision framework not available")
        return
    
    bank_file = Path(__file__).parent.parent / "docs" / "academic-discussion-question-bank.md"
    images_dir = Path(__file__).parent.parent / "docs" / "academic-discussion" / "images"
    
    with open(bank_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find questions that need fixing (incomplete or placeholder)
    need_fixing = []
    for i in range(7, 94):
        q_id = f"D{i:02d}"
        pattern = f'### {re.escape(q_id)}.*?\\*\\*Professor Question:\\*\\*\\s*\\n(.*?)\\n\\*\\*Student Posts:'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            q_text = match.group(1)
            # Check if incomplete (too short, has placeholder, or missing ?)
            if ('[待从截图提取]' in q_text or 
                len(q_text.strip()) < 30 or 
                (len(q_text.strip()) < 100 and '?' not in q_text)):
                need_fixing.append(q_id)
    
    print(f"Found {len(need_fixing)} questions needing fixes")
    print("="*60 + "\n")
    
    fixed = 0
    failed = 0
    
    for q_id in need_fixing:
        q_num = q_id[1:]
        matches = list(images_dir.glob(f'd{q_num}-*.png'))
        
        if not matches:
            print(f"{q_id}: ⚠️  No image")
            failed += 1
            continue
        
        img_file = matches[0]
        print(f"{q_id}: {img_file.name[:50]}...", end=' ')
        
        # Extract all text
        text = extract_all_text_vision(img_file)
        if not text:
            print("❌ No text")
            failed += 1
            continue
        
        # Parse with improved logic
        parsed = parse_discussion_improved(text)
        if not parsed or len(parsed['posts']) < 2:
            print(f"❌ Parse failed")
            failed += 1
            continue
        
        # Update
        if update_question(q_id, parsed):
            print(f"✅ Fixed")
            fixed += 1
        else:
            print("⚠️  Update failed")
            failed += 1
    
    print("\n" + "="*60)
    print(f"✅ Fixed: {fixed}")
    print(f"❌ Failed: {failed}")
    print("="*60)


if __name__ == "__main__":
    main()
