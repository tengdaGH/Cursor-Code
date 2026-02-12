#!/usr/bin/env python3
"""
Notion自动同步服务 - 文件保存时自动同步，无需Git
后台运行，监控文件变更并自动同步到Notion
"""

import os
import sys
import time
import signal
from pathlib import Path
from datetime import datetime
from typing import Set

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("Error: Please install watchdog: pip install watchdog")
    sys.exit(1)

# 导入同步器
sys.path.insert(0, str(Path(__file__).parent))
try:
    from notion_sync import NotionSyncer, load_config, CONFIG
    load_config()  # 确保配置已加载
except ImportError as e:
    print(f"Error: Cannot import notion_sync: {e}")
    print("Make sure notion_sync.py is in the same directory")
    sys.exit(1)

class AutoSyncHandler(FileSystemEventHandler):
    """文件变更处理器 - 自动同步到Notion"""
    
    def __init__(self, syncer: NotionSyncer):
        self.syncer = syncer
        self.pending_files: Set[Path] = set()
        self.last_sync_time = {}
        self.debounce_seconds = 2  # 防抖时间：2秒内多次变更只同步一次
        
    def should_sync(self, file_path: Path) -> bool:
        """判断是否应该同步"""
        now = time.time()
        
        # 检查是否在防抖时间内
        if file_path in self.last_sync_time:
            elapsed = now - self.last_sync_time[file_path]
            if elapsed < self.debounce_seconds:
                return False
        
        self.last_sync_time[file_path] = now
        return True
    
    def on_modified(self, event):
        """文件修改事件"""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # 只处理相关文件
        if file_path.suffix in ['.html', '.mp3']:
            if self.should_sync(file_path):
                self.pending_files.add(file_path)
                print(f"📝 [{datetime.now().strftime('%H:%M:%S')}] 检测到变更: {file_path.name}")
    
    def on_created(self, event):
        """文件创建事件"""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # 只处理音频文件
        if file_path.suffix == '.mp3':
            if self.should_sync(file_path):
                self.pending_files.add(file_path)
                print(f"➕ [{datetime.now().strftime('%H:%M:%S')}] 新文件: {file_path.name}")
    
    def sync_pending(self):
        """同步待处理的文件"""
        if not self.pending_files:
            return
        
        files_to_sync = list(self.pending_files)
        self.pending_files.clear()
        
        for file_path in files_to_sync:
            try:
                if file_path.suffix == '.html':
                    self.sync_html_file(file_path)
                elif file_path.suffix == '.mp3':
                    self.sync_audio_file(file_path)
            except Exception as e:
                print(f"❌ 同步失败 {file_path.name}: {e}")
    
    def sync_html_file(self, file_path: Path):
        """同步HTML文件中的题目"""
        print(f"🔄 [{datetime.now().strftime('%H:%M:%S')}] 同步题目文件: {file_path.name}")
        
        # 确定题目类型
        if 'announcement' in file_path.name.lower():
            question_type = 'announcement'
        elif 'choose-response' in file_path.name.lower():
            question_type = 'choose_response'
        elif 'conversation' in file_path.name.lower():
            question_type = 'conversation'
        else:
            return
        
        # 解析并同步题目
        questions = self.syncer.parse_html_questions(file_path, question_type)
        synced_count = 0
        
        for q in questions:
            if self.syncer.sync_question(q, question_type):
                synced_count += 1
                print(f"  ✅ 已同步: {q['id']} - {q.get('title', '')}")
        
        if synced_count > 0:
            print(f"✨ 完成！同步了 {synced_count} 个题目")
        else:
            print(f"ℹ️  无新题目需要同步")
    
    def sync_audio_file(self, file_path: Path):
        """同步音频文件"""
        print(f"🔄 [{datetime.now().strftime('%H:%M:%S')}] 同步音频文件: {file_path.name}")
        
        if self.syncer.sync_audio_file(file_path):
            print(f"  ✅ 已同步: {file_path.name}")
        else:
            print(f"  ℹ️  已存在或跳过: {file_path.name}")


class AutoSyncService:
    """自动同步服务"""
    
    def __init__(self):
        self.syncer = NotionSyncer()
        self.observer = None
        self.running = False
        
    def start(self):
        """启动监控服务"""
        root = Path(__file__).parent.parent
        
        # 创建事件处理器
        event_handler = AutoSyncHandler(self.syncer)
        
        # 创建观察者
        self.observer = Observer()
        
        # 监控配置的路径
        watch_paths = CONFIG.get('sync', {}).get('watch_paths', [])
        watched_count = 0
        
        for path_str in watch_paths:
            watch_path = root / path_str
            if watch_path.exists():
                if watch_path.is_file():
                    # 监控文件所在目录
                    self.observer.schedule(event_handler, str(watch_path.parent), recursive=False)
                else:
                    # 监控目录
                    self.observer.schedule(event_handler, str(watch_path), recursive=True)
                watched_count += 1
                print(f"👀 监控: {watch_path}")
        
        if watched_count == 0:
            print("⚠️  没有找到要监控的路径，使用默认路径")
            # 默认监控项目根目录
            self.observer.schedule(event_handler, str(root), recursive=True)
        
        # 启动监控
        self.observer.start()
        self.running = True
        
        print("\n" + "=" * 60)
        print("✅ Notion自动同步服务已启动")
        print("=" * 60)
        print("📝 监控文件变更，自动同步到Notion")
        print("🛑 按 Ctrl+C 停止服务")
        print("=" * 60 + "\n")
        
        # 处理同步循环
        try:
            while self.running:
                event_handler.sync_pending()
                time.sleep(1)  # 每秒检查一次待同步文件
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """停止监控服务"""
        if self.observer:
            self.observer.stop()
            self.observer.join()
        self.running = False
        print("\n\n🛑 服务已停止")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Notion自动同步服务 - 文件保存时自动同步')
    parser.add_argument('--daemon', action='store_true', help='后台运行（daemon模式）')
    parser.add_argument('--pid-file', type=str, default='.notion_sync.pid', help='PID文件路径')
    
    args = parser.parse_args()
    
    service = AutoSyncService()
    
    if args.daemon:
        # Daemon模式（后台运行）
        import daemon
        import daemon.pidfile
        
        pid_path = Path(__file__).parent.parent / args.pid_file
        
        with daemon.DaemonContext(
            pidfile=daemon.pidfile.PIDLockFile(str(pid_path)),
            stdout=open('/tmp/notion_sync.log', 'w'),
            stderr=open('/tmp/notion_sync_error.log', 'w')
        ):
            service.start()
    else:
        # 前台运行
        service.start()


if __name__ == '__main__':
    main()
