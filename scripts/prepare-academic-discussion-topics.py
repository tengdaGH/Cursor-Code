#!/usr/bin/env python3
"""
Helper script to prepare Academic Discussion topics for processing.

Scans the source folder and:
1. Lists all topics
2. Copies images to project folder
3. Generates a processing checklist
"""

import os
import shutil
from pathlib import Path

SOURCE_DIR = Path("/Users/tengda/Downloads/学术讨论写作/")
TARGET_IMAGES_DIR = Path(__file__).parent.parent / "docs" / "academic-discussion" / "images"
BANK_FILE = Path(__file__).parent.parent / "docs" / "academic-discussion-question-bank.md"

def get_topic_folders():
    """Get all topic folders."""
    folders = []
    for item in SOURCE_DIR.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            folders.append(item.name)
    return sorted(folders)

def find_best_image(folder_path):
    """Find the best image file in a folder (prefer .png with topic name)."""
    folder_name = folder_path.name
    images = []
    
    for ext in ['.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.JPEG']:
        # Try exact match with folder name
        exact_match = folder_path / f"{folder_name}{ext}"
        if exact_match.exists():
            return exact_match
        
        # List all images
        for img in folder_path.glob(f"*{ext}"):
            if img.name != '.DS_Store':
                images.append(img)
    
    # Prefer .png files, then files with folder name in filename
    if images:
        png_files = [img for img in images if img.suffix.lower() == '.png']
        if png_files:
            return png_files[0]
        return images[0]
    
    return None

def copy_image(source_path, topic_name, index):
    """Copy image to target directory with standardized name."""
    if not source_path or not source_path.exists():
        return None
    
    # Create safe filename
    safe_name = topic_name.replace('？', '').replace('？', '').replace(' ', '-').replace('/', '-')
    safe_name = ''.join(c for c in safe_name if c.isalnum() or c in '-_')
    target_name = f"d{index+7:02d}-{safe_name[:30]}{source_path.suffix.lower()}"
    target_path = TARGET_IMAGES_DIR / target_name
    
    try:
        shutil.copy2(source_path, target_path)
        return target_name
    except Exception as e:
        print(f"Error copying {source_path}: {e}")
        return None

def generate_topic_list():
    """Generate topic list for processing."""
    topics = get_topic_folders()
    
    print(f"Found {len(topics)} topics")
    print("\nTopic list:")
    for i, topic in enumerate(topics, 1):
        folder_path = SOURCE_DIR / topic
        image = find_best_image(folder_path)
        image_name = copy_image(image, topic, i-1) if image else None
        
        print(f"{i:2d}. {topic}")
        if image_name:
            print(f"    Image: {image_name}")
        else:
            print(f"    Image: ⚠️  Not found")
    
    return topics

def main():
    """Main function."""
    # Ensure target directory exists
    TARGET_IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("Academic Discussion Topics Preparation")
    print("=" * 60)
    print(f"Source: {SOURCE_DIR}")
    print(f"Target images: {TARGET_IMAGES_DIR}")
    print()
    
    topics = generate_topic_list()
    
    print(f"\n✅ Processed {len(topics)} topics")
    print(f"📁 Images copied to: {TARGET_IMAGES_DIR}")
    print(f"\nNext step: Extract text from images and add to question bank")

if __name__ == "__main__":
    main()
