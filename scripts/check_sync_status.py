#!/usr/bin/env python3
"""
检查待同步的文件状态
"""

import json
from pathlib import Path
from datetime import datetime

def check_status():
    """检查同步状态"""
    log_file = Path(__file__).parent.parent / '.notion_sync_pending.json'
    
    if not log_file.exists():
        print("ℹ️  暂无待同步的文件")
        return
    
    with open(log_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("=" * 60)
    print("📋 待同步文件列表")
    print("=" * 60)
    print(f"最后更新: {data.get('last_update', 'N/A')}")
    print(f"变更文件数: {len(data.get('changed_files', []))}")
    print("\n变更的文件:")
    
    for i, file_path in enumerate(data.get('changed_files', []), 1):
        file_obj = Path(__file__).parent.parent / file_path
        if file_obj.exists():
            size = file_obj.stat().st_size
            print(f"  {i}. {file_path} ({size/1024:.1f} KB)")
        else:
            print(f"  {i}. {file_path} (文件不存在)")
    
    print("\n" + "=" * 60)
    print("💡 提示: 这些文件已准备好同步到Notion")
    print("   可以通过Cursor的MCP工具手动同步，或运行同步脚本")
    print("=" * 60)

if __name__ == '__main__':
    check_status()
