#!/usr/bin/env python3
"""
Cursor <-> Notion 自动同步系统
支持文件监控、Git hooks、定期同步等功能
"""

import os
import json
import sys
import re
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

try:
    from notion_client import Client
except ImportError:
    print("Error: Please install notion-client: pip install notion-client")
    sys.exit(1)

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    print("Warning: watchdog not installed. File watching disabled.")
    print("Install with: pip install watchdog")

# 配置加载
CONFIG_PATH = Path(__file__).parent / 'notion_sync_config.json'
CONFIG = {}

def load_config():
    """加载配置文件"""
    global CONFIG
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            CONFIG = json.load(f)
    else:
        print(f"Warning: Config file not found at {CONFIG_PATH}")
        CONFIG = {}

def load_env():
    """从.env文件加载API密钥"""
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

load_config()

# Notion客户端
client = Client(auth=NOTION_API_KEY)

# 数据库ID
DB_IDS = CONFIG.get('notion', {}).get('database_ids', {})

class NotionSyncer:
    """Notion同步器"""
    
    def __init__(self):
        self.client = client
        self.db_ids = DB_IDS
    
    @staticmethod
    def get_instance():
        """获取单例实例"""
        if not hasattr(NotionSyncer, '_instance'):
            NotionSyncer._instance = NotionSyncer()
        return NotionSyncer._instance
    
    def parse_html_questions(self, html_path: Path, question_type: str) -> List[Dict]:
        """从HTML文件解析题目数据"""
        if not html_path.exists():
            return []
        
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        questions = []
        
        if question_type == "announcement":
            # 解析公告题目
            pattern = r"id:\s*['\"]([^'\"]+)['\"],\s*title:\s*['\"]([^'\"]+)['\"],\s*context:\s*['\"]([^'\"]+)['\"],\s*audioFile:\s*['\"]([^'\"]+)['\"],\s*text:\s*['\"]([^'\"]+)['\"]"
            for match in re.finditer(pattern, content):
                q_id, title, context, audio_file, text = match.groups()
                questions.append({
                    'id': q_id,
                    'title': title,
                    'context': context,
                    'audio_file': audio_file,
                    'text': text,
                    'type': 'Listen to an Announcement',
                    'set_id': q_id.split('-')[0]
                })
        
        elif question_type == "choose_response":
            # 解析选择回应题目
            # 更复杂的解析逻辑
            pattern = r'"id":\s*["\']([^"\']+)["\'],\s*"topic":\s*["\']([^"\']+)["\'],\s*"difficulty":\s*["\']([^"\']+)["\']'
            for match in re.finditer(pattern, content):
                q_id, topic, difficulty = match.groups()
                questions.append({
                    'id': q_id,
                    'topic': topic,
                    'difficulty': difficulty,
                    'type': 'Listen and Choose a Response',
                    'set_id': q_id.split('-')[0]
                })
        
        return questions
    
    def sync_question(self, question: Dict, question_type: str) -> bool:
        """同步单个题目到Notion"""
        db_id = self.db_ids.get('questions')
        if not db_id:
            return False
        
        try:
            # 检查是否已存在
            results = self.client.databases.query(
                database_id=db_id,
                filter={
                    "property": "题目ID",
                    "title": {
                        "equals": question['id']
                    }
                }
            )
            
            if results['results']:
                # 更新现有页面
                page_id = results['results'][0]['id']
                self.client.pages.update(
                    page_id=page_id,
                    properties={
                        "最后更新": {"last_edited_time": datetime.now().iso_format()}
                    }
                )
                return False  # 已存在，跳过
            
            # 创建新页面
            properties = {
                "题目ID": {"title": [{"text": {"content": question['id']}}]},
                "题型": {"select": {"name": question['type']}},
                "Set编号": {"rich_text": [{"text": {"content": question.get('set_id', '')}}]},
                "状态": {"select": {"name": "已完成"}}
            }
            
            if 'difficulty' in question:
                properties["难度"] = {"select": {"name": question['difficulty']}}
            
            if 'topic' in question:
                topics = question['topic'].split(',') if isinstance(question['topic'], str) else question['topic']
                properties["主题"] = {"multi_select": [{"name": t.strip()} for t in topics]}
            
            if 'audio_file' in question:
                properties["音频文件"] = {"url": f"file://{question['audio_file']}"}
            
            self.client.pages.create(
                parent={"database_id": db_id},
                properties=properties
            )
            return True
            
        except Exception as e:
            print(f"  ❌ 错误同步题目 {question['id']}: {e}")
            return False
    
    def sync_audio_file(self, audio_path: Path) -> bool:
        """同步音频文件到Notion"""
        db_id = self.db_ids.get('audio')
        if not db_id:
            return False
        
        file_name = audio_path.name
        file_size = audio_path.stat().st_size / 1024  # KB
        
        # 确定题型和题目ID
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
            return False
        
        try:
            # 检查是否已存在
            results = self.client.databases.query(
                database_id=db_id,
                filter={
                    "property": "文件名",
                    "title": {
                        "equals": file_name
                    }
                }
            )
            
            if results['results']:
                return False  # 已存在
            
            # 创建新页面
            self.client.pages.create(
                parent={"database_id": db_id},
                properties={
                    "文件名": {"title": [{"text": {"content": file_name}}]},
                    "文件路径": {"rich_text": [{"text": {"content": str(audio_path.relative_to(Path(__file__).parent.parent))}}]},
                    "关联题目": {"rich_text": [{"text": {"content": question_id}}]},
                    "题型": {"select": {"name": task_type}},
                    "文件大小": {"number": round(file_size, 1)},
                    "状态": {"select": {"name": "已生成"}}
                }
            )
            return True
            
        except Exception as e:
            print(f"  ❌ 错误同步音频 {file_name}: {e}")
            return False
    
    def add_work_log(self, content: str, modules: List[str] = None, 
                     status: str = "已完成", priority: str = "中") -> bool:
        """添加工作日志"""
        db_id = self.db_ids.get('worklog')
        if not db_id:
            return False
        
        today = datetime.now().date().iso_format()
        
        try:
            self.client.pages.create(
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
            return True
        except Exception as e:
            print(f"  ❌ 错误添加工作日志: {e}")
            return False
    
    def sync_all(self):
        """同步所有数据"""
        print("=" * 60)
        print("开始同步到Notion...")
        print("=" * 60)
        
        root = Path(__file__).parent.parent
        
        # 同步题目
        print("\n📚 同步题目...")
        for parser_name, parser_config in CONFIG.get('parsers', {}).items():
            html_file = root / parser_config['file']
            if html_file.exists():
                questions = self.parse_html_questions(html_file, parser_name)
                for q in questions:
                    if self.sync_question(q, parser_name):
                        print(f"  ✅ {q['id']} - {q.get('title', '')}")
        
        # 同步音频文件
        print("\n🎵 同步音频文件...")
        audio_dir = root / 'audio' / 'listening'
        if audio_dir.exists():
            for audio_file in audio_dir.glob('*.mp3'):
                if self.sync_audio_file(audio_file):
                    print(f"  ✅ {audio_file.name}")
        
        print("\n" + "=" * 60)
        print("同步完成！")
        print("=" * 60)


class FileWatcher(FileSystemEventHandler):
    """文件监控处理器"""
    
    def __init__(self, syncer: NotionSyncer):
        self.syncer = syncer
        self.debounce_time = 2.0  # 防抖时间（秒）
        self.pending_files = {}
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # 只处理相关文件
        if file_path.suffix == '.html' or file_path.suffix == '.mp3':
            self.pending_files[file_path] = datetime.now()
            print(f"📝 检测到文件变更: {file_path.name}")
    
    def process_pending(self):
        """处理待同步的文件"""
        now = datetime.now()
        to_sync = []
        
        for file_path, timestamp in list(self.pending_files.items()):
            if (now - timestamp).total_seconds() >= self.debounce_time:
                to_sync.append(file_path)
                del self.pending_files[file_path]
        
        for file_path in to_sync:
            if file_path.suffix == '.html':
                # 同步题目
                print(f"🔄 同步题目文件: {file_path.name}")
                # 这里可以调用同步逻辑
            elif file_path.suffix == '.mp3':
                # 同步音频
                print(f"🔄 同步音频文件: {file_path.name}")
                self.syncer.sync_audio_file(file_path)


def watch_files(syncer: NotionSyncer):
    """监控文件变更"""
    if not WATCHDOG_AVAILABLE:
        print("Error: watchdog not available. Cannot watch files.")
        return
    
    root = Path(__file__).parent.parent
    event_handler = FileWatcher(syncer)
    observer = Observer()
    
    # 监控配置的路径
    watch_paths = CONFIG.get('sync', {}).get('watch_paths', [])
    for path_str in watch_paths:
        watch_path = root / path_str
        if watch_path.exists():
            observer.schedule(event_handler, str(watch_path.parent), recursive=True)
            print(f"👀 监控: {watch_path}")
    
    observer.start()
    print("\n✅ 文件监控已启动 (按 Ctrl+C 停止)")
    
    try:
        import time
        while True:
            event_handler.process_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()


def create_git_hook():
    """创建Git hook来自动记录工作日志"""
    git_dir = Path(__file__).parent.parent / '.git'
    if not git_dir.exists():
        print("⚠️  不是Git仓库，跳过Git hook创建")
        return
    
    hooks_dir = git_dir / 'hooks'
    hooks_dir.mkdir(exist_ok=True)
    
    post_commit_hook = hooks_dir / 'post-commit'
    
    hook_content = f"""#!/bin/bash
# 自动同步Git commit到Notion工作日志

cd "{Path(__file__).parent.parent}"
python3 scripts/notion_sync.py --git-commit "$(git log -1 --pretty=format:'%s')"
"""
    
    with open(post_commit_hook, 'w') as f:
        f.write(hook_content)
    
    os.chmod(post_commit_hook, 0o755)
    print("✅ Git hook已创建: .git/hooks/post-commit")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Cursor <-> Notion 同步工具')
    parser.add_argument('--sync-all', action='store_true', help='同步所有数据')
    parser.add_argument('--watch', action='store_true', help='监控文件变更')
    parser.add_argument('--git-commit', type=str, help='从Git commit消息创建工作日志')
    parser.add_argument('--setup-git-hook', action='store_true', help='设置Git hook')
    
    args = parser.parse_args()
    
    syncer = NotionSyncer()
    
    if args.setup_git_hook:
        create_git_hook()
    
    if args.git_commit:
        # 从Git commit创建工作日志
        syncer.add_work_log(
            content=args.git_commit,
            modules=["系统优化"],
            status="已完成"
        )
    
    if args.sync_all:
        syncer.sync_all()
    
    if args.watch:
        watch_files(syncer)
    
    if not any([args.sync_all, args.watch, args.git_commit, args.setup_git_hook]):
        # 默认行为：同步所有
        syncer.sync_all()


if __name__ == '__main__':
    main()
