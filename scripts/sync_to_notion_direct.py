#!/usr/bin/env python3
"""
直接同步内容到Notion页面
使用MCP工具或Notion API
"""

import json
import sys
from pathlib import Path

# 读取Markdown内容
def read_markdown_content():
    """读取要同步的Markdown内容"""
    md_file = Path(__file__).parent.parent / "docs" / "NOTION_AI_READABLE.md"
    if not md_file.exists():
        print(f"错误: 找不到文件 {md_file}")
        return None
    return md_file.read_text(encoding='utf-8')

def main():
    """主函数"""
    content = read_markdown_content()
    if not content:
        sys.exit(1)
    
    print("=" * 60)
    print("Notion同步内容已准备好")
    print("=" * 60)
    print("\n请执行以下操作之一：")
    print("\n1. 在Notion页面中，点击右上角的'...'菜单")
    print("2. 选择'Import' → 'Markdown'")
    print("3. 选择文件: docs/NOTION_AI_READABLE.md")
    print("\n或者：")
    print("1. 打开 docs/NOTION_AI_READABLE.md")
    print("2. 复制全部内容")
    print("3. 在Notion页面中粘贴")
    print("\n" + "=" * 60)
    
    # 输出前500字符作为预览
    print("\n内容预览（前500字符）：")
    print("-" * 60)
    print(content[:500])
    print("...")
    print("-" * 60)

if __name__ == "__main__":
    main()
