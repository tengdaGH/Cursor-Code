#!/usr/bin/env python3
"""
简化的文件监控服务 - 检测文件变更并生成同步清单
无需API Key，通过Cursor MCP工具手动同步
"""

import time
import json
from pathlib import Path
from datetime import datetime
from typing import Set, Dict, List

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("Error: Please install watchdog: pip install watchdog")
    sys.exit(1)

class FileChangeTracker(FileSystemEventHandler):
    """文件变更追踪器"""
    
    def __init__(self):
        self.changed_files: Set[Path] = set()
        self.change_log: List[Dict] = []
        
    def on_modified(self, event):
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        if file_path.suffix in ['.html', '.mp3']:
            self.changed_files.add(file_path)
            self.change_log.append({
                'time': datetime.now().isoformat(),
                'file': str(file_path.relative_to(Path(__file__).parent.parent)),
                'action': 'modified'
            })
            print(f"📝 [{datetime.now().strftime('%H:%M:%S')}] 检测到变更: {file_path.name}")
    
    def on_created(self, event):
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        if file_path.suffix == '.mp3':
            self.changed_files.add(file_path)
            self.change_log.append({
                'time': datetime.now().isoformat(),
                'file': str(file_path.relative_to(Path(__file__).parent.parent)),
                'action': 'created'
            })
            print(f"➕ [{datetime.now().strftime('%H:%M:%S')}] 新文件: {file_path.name}")
    
    def save_changes(self):
        """保存变更记录"""
        log_file = Path(__file__).parent.parent / '.notion_sync_pending.json'
        data = {
            'last_update': datetime.now().isoformat(),
            'changed_files': [str(f.relative_to(Path(__file__).parent.parent)) for f in self.changed_files],
            'change_log': self.change_log[-20:]  # 保留最近20条记录
        }
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return log_file
    
    def clear(self):
        """清空变更记录"""
        self.changed_files.clear()
        self.change_log.clear()

def start_watching():
    """启动文件监控"""
    root = Path(__file__).parent.parent
    tracker = FileChangeTracker()
    observer = Observer()
    
    # 监控关键路径
    watch_paths = [
        root / 'toefl-listening-announcement-practice.html',
        root / 'toefl-listening-choose-response-practice.html',
        root / 'toefl-listening-conversation-practice.html',
        root / 'audio' / 'listening'
    ]
    
    for watch_path in watch_paths:
        if watch_path.exists():
            if watch_path.is_file():
                observer.schedule(tracker, str(watch_path.parent), recursive=False)
            else:
                observer.schedule(tracker, str(watch_path), recursive=True)
            print(f"👀 监控: {watch_path}")
    
    observer.start()
    
    print("\n" + "=" * 60)
    print("✅ 文件监控已启动")
    print("=" * 60)
    print("📝 检测到文件变更时会自动记录")
    print("💡 变更记录保存在: .notion_sync_pending.json")
    print("🛑 按 Ctrl+C 停止")
    print("=" * 60 + "\n")
    
    try:
        last_save = time.time()
        while True:
            time.sleep(5)  # 每5秒保存一次变更记录
            if time.time() - last_save > 5:
                if tracker.changed_files:
                    log_file = tracker.save_changes()
                    print(f"💾 [{datetime.now().strftime('%H:%M:%S')}] 已保存变更记录: {len(tracker.changed_files)} 个文件")
                last_save = time.time()
    except KeyboardInterrupt:
        # 最后保存一次
        if tracker.changed_files:
            log_file = tracker.save_changes()
            print(f"\n💾 已保存变更记录到: {log_file}")
        observer.stop()
    
    observer.join()
    print("\n🛑 监控已停止")

if __name__ == '__main__':
    start_watching()
