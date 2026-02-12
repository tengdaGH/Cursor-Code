#!/usr/bin/env python3
"""
同步TOEFL练习平台数据到Notion
包括题目、音频文件、工作日志等
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime

# 需要安装: pip install notion-client
try:
    from notion_client import Client
except ImportError:
    print("Error: Please install notion-client: pip install notion-client")
    sys.exit(1)

# 从.env文件加载Notion API密钥
def load_env():
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith('NOTION_API_KEY='):
                    return line.split('=', 1)[1].strip()
    return None

NOTION_API_KEY = load_env() or os.getenv('NOTION_API_KEY')
if not NOTION_API_KEY:
    print("Error: Set NOTION_API_KEY environment variable or add it to .env file")
    print("Get your API key from: https://www.notion.so/my-integrations")
    sys.exit(1)

# Notion数据库ID（需要从Notion页面URL中获取）
# 这些ID会在创建数据库后自动生成
DATABASE_IDS = {
    'questions': '88218505-963f-4b45-b85a-c57a8356f900',  # 题目数据库
    'audio': 'ba5655a1-392d-4db4-9d17-9ac7ea46505a',      # 音频文件数据库
    'worklog': '283d8cc3-2f0b-47f8-8b8d-06517d0a9052',    # 工作日志
    'features': 'e54189bb-400a-4874-9298-c18682694cec'    # 功能模块
}

def init_client():
    """初始化Notion客户端"""
    return Client(auth=NOTION_API_KEY)

def parse_announcement_questions():
    """从HTML文件中解析公告题目"""
    html_path = Path(__file__).parent.parent / 'toefl-listening-announcement-practice.html'
    if not html_path.exists():
        return []
    
    import re
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取ANNOUNCEMENT_SETS数据
    pattern = r'ANNOUNCEMENT_SETS\s*=\s*({.*?});'
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        return []
    
    # 这里简化处理，实际应该用更robust的方法
    questions = []
    # 提取每个announcement的数据
    announcement_pattern = r"id:\s*'([^']+)',\s*title:\s*'([^']+)',\s*context:\s*'([^']+)',\s*audioFile:\s*'([^']+)',\s*text:\s*'([^']+)'"
    for match in re.finditer(announcement_pattern, content):
        ann_id, title, context, audio_file, text = match.groups()
        questions.append({
            'id': ann_id,
            'title': title,
            'context': context,
            'audio_file': audio_file,
            'text': text[:200] + '...' if len(text) > 200 else text
        })
    
    return questions

def sync_announcements_to_notion(client):
    """同步公告题目到Notion"""
    print("\n同步公告题目到Notion...")
    
    questions = parse_announcement_questions()
    db_id = DATABASE_IDS['questions']
    
    for q in questions:
        try:
            # 检查是否已存在
            results = client.databases.query(
                database_id=db_id,
                filter={
                    "property": "题目ID",
                    "title": {
                        "equals": q['id']
                    }
                }
            )
            
            if results['results']:
                print(f"  ⏭️  跳过已存在的题目: {q['id']}")
                continue
            
            # 创建新页面
            client.pages.create(
                parent={"database_id": db_id},
                properties={
                    "题目ID": {"title": [{"text": {"content": q['id']}}]},
                    "题型": {"select": {"name": "Listen to an Announcement"}},
                    "Set编号": {"rich_text": [{"text": {"content": q['id'].split('-')[0]}}]},
                    "主题": {"multi_select": [{"name": "Campus"}]},
                    "状态": {"select": {"name": "已完成"}},
                    "音频文件": {"url": f"https://github.com/your-repo/audio/listening/{q['audio_file']}"}
                }
            )
            print(f"  ✅ 已添加: {q['id']} - {q['title']}")
        except Exception as e:
            print(f"  ❌ 错误 ({q['id']}): {e}")

def sync_audio_files(client):
    """同步音频文件信息到Notion"""
    print("\n同步音频文件到Notion...")
    
    audio_dir = Path(__file__).parent.parent / 'audio' / 'listening'
    if not audio_dir.exists():
        print("  ⚠️  音频目录不存在")
        return
    
    db_id = DATABASE_IDS['audio']
    
    # 查找所有MP3文件
    for audio_file in audio_dir.glob('*.mp3'):
        file_name = audio_file.name
        file_size = audio_file.stat().st_size / 1024  # KB
        
        # 确定题型
        if file_name.startswith('LA-'):
            task_type = "Listen to an Announcement"
            question_id = file_name.replace('LA-', '').replace('.mp3', '')
        elif file_name.startswith('LCR-'):
            task_type = "Listen and Choose a Response"
            question_id = file_name.replace('LCR-', '').replace('.mp3', '')
        elif file_name.startswith('LC-'):
            task_type = "Listen to a Conversation"
            question_id = file_name.replace('LC-', '').replace('.mp3', '')
        else:
            continue
        
        try:
            # 检查是否已存在
            results = client.databases.query(
                database_id=db_id,
                filter={
                    "property": "文件名",
                    "title": {
                        "equals": file_name
                    }
                }
            )
            
            if results['results']:
                print(f"  ⏭️  跳过已存在的文件: {file_name}")
                continue
            
            # 创建新页面
            client.pages.create(
                parent={"database_id": db_id},
                properties={
                    "文件名": {"title": [{"text": {"content": file_name}}]},
                    "文件路径": {"rich_text": [{"text": {"content": str(audio_file.relative_to(Path(__file__).parent.parent))}}]},
                    "关联题目": {"rich_text": [{"text": {"content": question_id}}]},
                    "题型": {"select": {"name": task_type}},
                    "文件大小": {"number": round(file_size, 1)},
                    "状态": {"select": {"name": "已生成"}}
                }
            )
            print(f"  ✅ 已添加: {file_name} ({file_size:.1f} KB)")
        except Exception as e:
            print(f"  ❌ 错误 ({file_name}): {e}")

def add_work_log(client, content, modules=None, status="已完成", priority="中"):
    """添加工作日志"""
    db_id = DATABASE_IDS['worklog']
    
    today = datetime.now().date().iso_format()
    
    try:
        client.pages.create(
            parent={"database_id": db_id},
            properties={
                "工作内容": {"title": [{"text": {"content": content}}]},
                "日期": {
                    "date": {
                        "start": today,
                        "is_datetime": False
                    }
                },
                "功能模块": {
                    "multi_select": [{"name": m} for m in (modules or [])]
                },
                "状态": {"select": {"name": status}},
                "优先级": {"select": {"name": priority}},
                "完成度": {"number": 100 if status == "已完成" else 0}
            }
        )
        print(f"  ✅ 已添加工作日志: {content}")
    except Exception as e:
        print(f"  ❌ 错误: {e}")

def main():
    print("=" * 60)
    print("TOEFL练习平台 - Notion同步工具")
    print("=" * 60)
    
    client = init_client()
    
    # 同步公告题目
    sync_announcements_to_notion(client)
    
    # 同步音频文件
    sync_audio_files(client)
    
    # 添加今日工作日志
    print("\n添加今日工作日志...")
    add_work_log(
        client,
        "创建Listen to an Announcement功能 - 完成5个公告题目和音频生成",
        modules=["Listen to an Announcement"],
        status="已完成"
    )
    
    print("\n" + "=" * 60)
    print("同步完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()
