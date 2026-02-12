#!/usr/bin/env python3
"""
使用MCP工具直接同步数据到Notion（无需API Key）
通过Cursor的MCP集成直接操作Notion
"""

import json
import re
from pathlib import Path
from datetime import datetime

# Notion数据库ID（从之前的创建结果中获取）
DATABASE_IDS = {
    'questions': '88218505-963f-4b45-b85a-c57a8356f900',
    'audio': 'ba5655a1-392d-4db4-9d17-9ac7ea46505a',
    'worklog': '283d8cc3-2f0b-47f8-8b8d-06517d0a9052',
    'features': 'e54189bb-400a-4874-9298-c18682694cec'
}

def parse_announcement_html():
    """从HTML文件解析公告题目"""
    html_path = Path(__file__).parent.parent / 'toefl-listening-announcement-practice.html'
    if not html_path.exists():
        return []
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    announcements = []
    
    # 提取ANNOUNCEMENT_SETS数据
    pattern = r"id:\s*['\"]([^'\"]+)['\"],\s*title:\s*['\"]([^'\"]+)['\"],\s*context:\s*['\"]([^'\"]+)['\"],\s*audioFile:\s*['\"]([^'\"]+)['\"],\s*text:\s*['\"]([^'\"]+)['\"]"
    
    for match in re.finditer(pattern, content):
        ann_id, title, context, audio_file, text = match.groups()
        
        # 提取问题
        questions_pattern = r"questions:\s*\[(.*?)\]"
        questions_match = re.search(questions_pattern, content[content.find(match.group(0)):content.find(match.group(0))+2000])
        
        questions_text = ""
        if questions_match:
            # 提取问题文本
            q_pattern = r"text:\s*['\"]([^'\"]+)['\"]"
            questions = re.findall(q_pattern, questions_match.group(1))
            questions_text = "\n\n**Questions**:\n" + "\n".join([f"{i+1}. {q}" for i, q in enumerate(questions[:2])])
        
        announcements.append({
            'id': ann_id,
            'title': title,
            'context': context,
            'audio_file': audio_file,
            'text': text,
            'questions': questions_text,
            'set_id': ann_id.split('-')[0]
        })
    
    return announcements

def generate_notion_pages():
    """生成Notion页面数据"""
    announcements = parse_announcement_html()
    
    # 生成题目页面
    question_pages = []
    for ann in announcements:
        content = f"""## {ann['title']}

**Context**: {ann['context']}

**Announcement Text**:

{ann['text']}
{ann['questions']}
"""
        
        question_pages.append({
            'database': 'questions',
            'properties': {
                '题目ID': ann['id'],
                '题型': 'Listen to an Announcement',
                'Set编号': ann['set_id'],
                '主题': ['Campus'],
                '难度': 'Medium',
                '状态': '已完成',
                '音频文件': f"file://{ann['audio_file']}"
            },
            'content': content
        })
    
    # 生成音频文件页面
    audio_pages = []
    audio_dir = Path(__file__).parent.parent / 'audio' / 'listening'
    if audio_dir.exists():
        for audio_file in audio_dir.glob('LA-*.mp3'):
            file_name = audio_file.name
            file_size = audio_file.stat().st_size / 1024  # KB
            question_id = file_name.replace('LA-', '').replace('.mp3', '')
            
            audio_pages.append({
                'database': 'audio',
                'properties': {
                    '文件名': file_name,
                    '文件路径': str(audio_file.relative_to(Path(__file__).parent.parent)),
                    '关联题目': question_id,
                    '题型': 'Listen to an Announcement',
                    '文件大小': round(file_size, 1),
                    '状态': '已生成'
                }
            })
    
    return {
        'questions': question_pages,
        'audio': audio_pages
    }

def main():
    """主函数 - 生成同步数据"""
    print("=" * 60)
    print("生成Notion同步数据")
    print("=" * 60)
    
    pages = generate_notion_pages()
    
    print(f"\n📚 题目数据: {len(pages['questions'])} 条")
    print(f"🎵 音频数据: {len(pages['audio'])} 条")
    
    # 保存为JSON文件，供MCP工具使用
    output_file = Path(__file__).parent / 'notion_sync_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 数据已保存到: {output_file}")
    print("\n💡 提示: 这些数据可以通过MCP工具直接添加到Notion")
    print("=" * 60)

if __name__ == '__main__':
    main()
