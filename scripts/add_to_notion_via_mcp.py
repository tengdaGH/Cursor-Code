#!/usr/bin/env python3
"""
通过Cursor MCP工具添加数据到Notion的辅助脚本
生成可以直接在Cursor中使用的命令
"""

import json
from pathlib import Path
from datetime import datetime

def generate_notion_commands():
    """生成Notion添加命令"""
    
    # 读取数据
    data_file = Path(__file__).parent / 'notion_sync_data.json'
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    commands = []
    
    # 工作日志
    today = datetime.now().date().isoformat()
    work_log = f"""
工作日志 - {today}

## 完成的工作

### 1. Listen to an Announcement功能
- ✅ HTML练习页面 (toefl-listening-announcement-practice.html)
- ✅ 5个公告题目 (A01-01到A01-05)
- ✅ 5个音频文件 (LA-A01-01到LA-A01-05)
- ✅ 更新主页链接

### 2. Notion同步系统
- ✅ 4个数据库结构
- ✅ 文件监控脚本
- ✅ 同步脚本
- ✅ 文档和指南

## 统计数据
- 题目: 5个
- 音频文件: 5个 (约2.5 MB)
- 代码文件: 14个
- 文档文件: 8个

## 符合TOEFL 2026标准
✅ 学术环境公告
✅ 每个公告2个问题
✅ 单声道格式
✅ 美式口音
"""
    
    commands.append({
        'type': 'worklog',
        'content': work_log,
        'properties': {
            '工作内容': f'创建Listen to an Announcement功能 - 完成5个公告题目和音频生成，创建Notion同步系统',
            '日期': today,
            '功能模块': ['Listen to an Announcement', '系统优化'],
            '状态': '已完成',
            '优先级': '高',
            '完成度': 100
        }
    })
    
    # 题目数据
    for q in data['questions']:
        commands.append({
            'type': 'question',
            'content': q['content'],
            'properties': q['properties']
        })
    
    # 音频数据
    for a in data['audio']:
        commands.append({
            'type': 'audio',
            'properties': a['properties']
        })
    
    return commands

def main():
    """生成命令列表"""
    commands = generate_notion_commands()
    
    print("=" * 60)
    print("Notion数据添加命令")
    print("=" * 60)
    print(f"\n总共需要添加: {len(commands)} 条数据")
    print(f"  - 工作日志: 1条")
    print(f"  - 题目: {len([c for c in commands if c['type'] == 'question'])}条")
    print(f"  - 音频文件: {len([c for c in commands if c['type'] == 'audio'])}条")
    print("\n" + "=" * 60)
    print("💡 提示: 告诉AI助手逐个添加这些数据到Notion")
    print("=" * 60)
    
    # 保存为JSON供参考
    output_file = Path(__file__).parent / 'notion_add_commands.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(commands, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 命令已保存到: {output_file}")

if __name__ == '__main__':
    main()
