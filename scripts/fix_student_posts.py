#!/usr/bin/env python3
"""
Fix incomplete student posts by re-extracting and better parsing.
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


def extract_all_text(image_path):
    """Extract all text using Vision."""
    if not VISION_AVAILABLE:
        return None
    
    try:
        image_url = NSURL.fileURLWithPath_(str(image_path))
        handler = VNImageRequestHandler.alloc().initWithURL_options_(image_url, None)
        request = VNRecognizeTextRequest.alloc().init()
        request.setRecognitionLevel_(1)
        
        handler.performRequests_error_([request], None)
        observations = request.results()
        
        if not observations:
            return None
        
        all_text = []
        for obs in observations:
            candidates = obs.topCandidates_(1)
            if candidates:
                all_text.append(candidates[0].string())
        
        return '\n'.join(all_text)
    except:
        return None


def find_student_posts_improved(text):
    """Better algorithm to find student posts."""
    if not text:
        return None
    
    lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 2]
    
    # Skip header lines
    filtered_lines = []
    for line in lines:
        if any(word in line.lower() for word in ['toefl', 'volume', 'writing', 'question', 'help', 'next', 'previous', 'hide time']):
            continue
        if len(line) < 5:
            continue
        filtered_lines.append(line)
    
    # Find student names (common patterns)
    name_pattern = re.compile(r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*:?\s*(.*)$')
    
    posts = []
    current_author = None
    current_text = []
    
    for i, line in enumerate(filtered_lines):
        match = name_pattern.match(line)
        if match:
            name = match.group(1).strip()
            # Check if it's a valid name
            if (len(name.split()) <= 2 and 
                name[0].isupper() and 
                len(name) > 2 and 
                name.lower() not in ['question', 'writing', 'help', 'next', 'previous']):
                
                # Save previous post
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
    
    # Save last post
    if current_author and current_text:
        post_text = ' '.join(current_text).strip()
        if len(post_text) > 15:
            posts.append({
                'author': current_author,
                'text': post_text
            })
    
    # If we have posts but less than 2, try to find more
    if len(posts) == 1:
        # Look for another post after the first one
        first_post_end = None
        for i, line in enumerate(filtered_lines):
            if posts[0]['author'].lower() in line.lower():
                first_post_end = i
                break
        
        if first_post_end:
            # Look for another name after first post
            for i in range(first_post_end + 5, min(len(filtered_lines), first_post_end + 20)):
                match = name_pattern.match(filtered_lines[i])
                if match:
                    name = match.group(1).strip()
                    if len(name.split()) <= 2 and name[0].isupper():
                        # Found second author
                        post_text_parts = []
                        for j in range(i+1, min(len(filtered_lines), i+15)):
                            if name_pattern.match(filtered_lines[j]):
                                break
                            if len(filtered_lines[j]) > 5:
                                post_text_parts.append(filtered_lines[j])
                        
                        if post_text_parts:
                            posts.append({
                                'author': name,
                                'text': ' '.join(post_text_parts).strip()
                            })
                        break
    
    return posts[:2] if len(posts) >= 2 else None


def update_student_posts(q_id, posts):
    """Update student posts in bank file."""
    bank_file = Path(__file__).parent.parent / "docs" / "academic-discussion-question-bank.md"
    
    with open(bank_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match student posts section
    pattern = (
        f'(### {re.escape(q_id)}[^#]+?\\*\\*Student Posts:\\*\\*\\s*\\n-\\s+\\*\\*\\[Author1\\]:\\*\\*\\s*)'
        r'.*?'
        r'(\s*\n-\s+\*\*\[Author2\]:\*\*\s*)'
        r'.*?'
        r'(\s*\n\*\*Notes:)'
    )
    
    def replacer(m):
        return (
            m.group(1) + posts[0]['text'] +
            m.group(2) + posts[1]['text'] +
            m.group(3)
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
    
    # Find questions with incomplete posts
    incomplete = []
    for i in range(7, 94):
        q_id = f"D{i:02d}"
        pattern = f'### {re.escape(q_id)}.*?\\*\\*Student Posts:\\*\\*\\s*\\n-.*?\\*\\*\\[Author1\\]:\\*\\*\\s*(.*?)\\n-.*?\\*\\*\\[Author2\\]:\\*\\*\\s*(.*?)\\n'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            p1 = match.group(1)
            p2 = match.group(2)
            if ('[待从截图提取]' in p1 or '[待从截图提取]' in p2 or 
                len(p1.strip()) < 20 or len(p2.strip()) < 20):
                incomplete.append(q_id)
    
    print(f"Found {len(incomplete)} questions with incomplete posts")
    print("="*60 + "\n")
    
    fixed = 0
    failed = 0
    
    for q_id in incomplete:
        q_num = q_id[1:]
        matches = list(images_dir.glob(f'd{q_num}-*.png'))
        
        if not matches:
            print(f"{q_id}: ⚠️  No image")
            failed += 1
            continue
        
        img_file = matches[0]
        print(f"{q_id}: {img_file.name[:45]}...", end=' ')
        
        # Extract text
        text = extract_all_text(img_file)
        if not text:
            print("❌ No text")
            failed += 1
            continue
        
        # Find posts
        posts = find_student_posts_improved(text)
        if not posts or len(posts) < 2:
            print(f"❌ Posts not found ({len(posts) if posts else 0})")
            failed += 1
            continue
        
        # Update
        if update_student_posts(q_id, posts):
            print(f"✅ Fixed ({posts[0]['author']}, {posts[1]['author']})")
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
