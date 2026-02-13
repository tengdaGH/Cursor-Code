#!/usr/bin/env python3
"""
Compare source folders, question bank, JSON, and practice page.

Compares:
1. Source folders in /Users/tengda/Downloads/学术讨论写作/
2. Markdown question bank (docs/academic-discussion-question-bank.md)
3. JSON prompts file (data/writing-academic-discussion-prompts.json)
4. HTML practice page (toefl-writing-academic-discussion-practice.html)
"""

import json
import re
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path(__file__).parent.parent
SOURCE_DIR = Path("/Users/tengda/Downloads/学术讨论写作")
BANK_FILE = PROJECT_ROOT / "docs" / "academic-discussion-question-bank.md"
JSON_FILE = PROJECT_ROOT / "data" / "writing-academic-discussion-prompts.json"
HTML_FILE = PROJECT_ROOT / "toefl-writing-academic-discussion-practice.html"


def get_source_folders():
    """Get all question folders from source directory."""
    if not SOURCE_DIR.exists():
        return []
    
    folders = []
    for item in SOURCE_DIR.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            # Skip non-question folders
            if item.name not in ['1.ico'] and '微信截图' not in item.name:
                folders.append(item.name)
    
    return sorted(folders)


def get_markdown_questions():
    """Extract question IDs and titles from Markdown bank."""
    if not BANK_FILE.exists():
        return {}
    
    questions = {}
    with open(BANK_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all question headers
    pattern = r'^###\s+(D\d+)\s+-\s+(.+?)\s+\(([^)]+)\)'
    matches = re.finditer(pattern, content, re.MULTILINE)
    
    for match in matches:
        q_id = match.group(1)
        title = match.group(2).strip()
        source = match.group(3).strip()
        questions[q_id] = {
            'title': title,
            'source': source,
            'id': q_id
        }
    
    return questions


def get_json_questions():
    """Get questions from JSON file."""
    if not JSON_FILE.exists():
        return {}
    
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions = {}
    for prompt in data.get('prompts', []):
        q_id = prompt.get('id')
        questions[q_id] = {
            'id': q_id,
            'shortDesc': prompt.get('shortDesc', ''),
            'shortDescEn': prompt.get('shortDescEn', ''),
            'category': prompt.get('category', ''),
            'question': prompt.get('question', '')[:50] + '...' if len(prompt.get('question', '')) > 50 else prompt.get('question', ''),
            'posts_count': len(prompt.get('posts', []))
        }
    
    return questions


def get_html_questions():
    """Extract question IDs from HTML practice page."""
    # HTML page loads questions from JSON via fetch, so it should match JSON
    # We'll check if the HTML references the JSON file correctly
    if not HTML_FILE.exists():
        return set()
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if HTML references the JSON file
    json_ref = 'writing-academic-discussion-prompts.json' in content
    
    # Since HTML loads from JSON dynamically, return empty set
    # and note that it should match JSON
    return set()  # HTML loads dynamically from JSON


def normalize_title(title):
    """Normalize title for comparison."""
    # Remove special characters, normalize spaces
    title = re.sub(r'[？?]', '', title)
    title = re.sub(r'\s+', ' ', title)
    title = title.strip()
    return title.lower()


def compare():
    """Compare all sources."""
    print("=" * 80)
    print("学术讨论题目对比报告")
    print("=" * 80)
    print()
    
    # Get data from all sources
    source_folders = get_source_folders()
    md_questions = get_markdown_questions()
    json_questions = get_json_questions()
    html_ids = get_html_questions()
    
    print(f"📁 源文件夹数量: {len(source_folders)}")
    print(f"📝 Markdown题库题目数: {len(md_questions)}")
    print(f"📄 JSON文件题目数: {len(json_questions)}")
    print(f"🌐 HTML页面: 动态加载JSON文件（应包含 {len(json_questions)} 个题目）")
    print()
    
    # Get all IDs
    md_ids = set(md_questions.keys())
    json_ids = set(json_questions.keys())
    
    # Find missing IDs
    print("=" * 80)
    print("缺失的题目")
    print("=" * 80)
    
    missing_in_json = md_ids - json_ids
    missing_in_md = json_ids - md_ids
    # HTML loads from JSON, so it should match JSON
    missing_in_html = set()  # HTML dynamically loads from JSON
    
    if missing_in_json:
        print(f"\n❌ JSON中缺失的题目 ({len(missing_in_json)}):")
        for q_id in sorted(missing_in_json, key=lambda x: int(x[1:])):
            print(f"   - {q_id}: {md_questions[q_id]['title']}")
    
    if missing_in_md:
        print(f"\n❌ Markdown中缺失的题目 ({len(missing_in_md)}):")
        for q_id in sorted(missing_in_md, key=lambda x: int(x[1:])):
            print(f"   - {q_id}: {json_questions[q_id]['shortDesc']}")
    
    # Check if HTML references JSON correctly
    html_refs_json = False
    if HTML_FILE.exists():
        with open(HTML_FILE, 'r', encoding='utf-8') as f:
            html_content = f.read()
            html_refs_json = 'writing-academic-discussion-prompts.json' in html_content
    
    if html_refs_json:
        print(f"\n✅ HTML页面正确引用了JSON文件")
    else:
        print(f"\n⚠️  HTML页面可能未正确引用JSON文件")
    
    if not missing_in_json and not missing_in_md and not missing_in_html:
        print("\n✅ 所有题目ID都一致！")
    
    # Check for gaps in ID sequence
    print()
    print("=" * 80)
    print("ID序列检查")
    print("=" * 80)
    
    all_ids = sorted(md_ids | json_ids, key=lambda x: int(x[1:]))
    if all_ids:
        first_id = int(all_ids[0][1:])
        last_id = int(all_ids[-1][1:])
        expected_ids = set(f"D{i:02d}" for i in range(first_id, last_id + 1))
        missing_ids = expected_ids - (md_ids | json_ids)
        
        if missing_ids:
            print(f"\n⚠️  缺失的ID序列 ({len(missing_ids)}):")
            for q_id in sorted(missing_ids, key=lambda x: int(x[1:])):
                print(f"   - {q_id}")
        else:
            print(f"\n✅ ID序列连续 (D{first_id:02d} - D{last_id:02d})")
    
    # Compare source folders with questions
    print()
    print("=" * 80)
    print("源文件夹与题目对比")
    print("=" * 80)
    
    # Create mapping from titles to IDs
    title_to_id = {}
    for q_id, q_data in md_questions.items():
        normalized = normalize_title(q_data['title'])
        title_to_id[normalized] = q_id
    
    unmatched_folders = []
    matched_folders = []
    
    for folder in source_folders:
        normalized_folder = normalize_title(folder)
        matched = False
        for title, q_id in title_to_id.items():
            if normalized_folder in title or title in normalized_folder:
                matched_folders.append((folder, q_id, title))
                matched = True
                break
        
        if not matched:
            unmatched_folders.append(folder)
    
    print(f"\n✅ 匹配的文件夹: {len(matched_folders)}")
    print(f"❓ 未匹配的文件夹: {len(unmatched_folders)}")
    
    if unmatched_folders:
        print("\n未匹配的文件夹列表:")
        for folder in unmatched_folders[:20]:  # Show first 20
            print(f"   - {folder}")
        if len(unmatched_folders) > 20:
            print(f"   ... 还有 {len(unmatched_folders) - 20} 个")
    
    # Summary
    print()
    print("=" * 80)
    print("总结")
    print("=" * 80)
    print(f"""
✅ JSON文件: {len(json_questions)} 个题目
✅ Markdown题库: {len(md_questions)} 个题目
✅ HTML页面: {len(html_ids)} 个题目
✅ 源文件夹: {len(source_folders)} 个文件夹

{"⚠️  发现不一致，请检查上述差异" if (missing_in_json or missing_in_md or missing_in_html or missing_ids) else "✅ 所有数据源一致！"}
    """)
    
    return {
        'source_folders': len(source_folders),
        'md_questions': len(md_questions),
        'json_questions': len(json_questions),
        'html_questions': len(html_ids),
        'missing_in_json': list(missing_in_json),
        'missing_in_md': list(missing_in_md),
        'missing_in_html': list(missing_in_html),
        'missing_ids': list(missing_ids) if 'missing_ids' in locals() else [],
        'unmatched_folders': unmatched_folders
    }


if __name__ == "__main__":
    compare()
