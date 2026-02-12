# 📝 添加到Notion的详细说明

## 🎯 目标
将所有今天的工作内容同步到Notion，包括：
- 📚 5个题目
- 🎵 5个音频文件记录
- 📝 工作日志
- 🔧 功能模块状态

## 🚀 最佳方案：使用Cursor AI助手

由于Cursor已经集成了Notion MCP工具，**最简单的方式是直接告诉AI助手添加**：

### 步骤1：添加工作日志

告诉AI：
```
"在Notion工作日志数据库中添加一条记录：
- 工作内容：创建Listen to an Announcement功能 - 完成5个公告题目和音频生成，创建Notion同步系统
- 日期：2026-02-12
- 功能模块：Listen to an Announcement, 系统优化
- 状态：已完成
- 优先级：高
- 完成度：100%"
```

### 步骤2：添加题目（逐个添加）

告诉AI：
```
"在Notion题目数据库中添加题目A01-01：
- 题目ID：A01-01
- 题型：Listen to an Announcement
- Set编号：A01
- 主题：Campus
- 难度：Medium
- 状态：已完成
- 音频文件：audio/listening/LA-A01-01.mp3

题目内容：
标题：Library Hours Change
Context：Campus Library
公告文本：[完整的公告文本]
问题：[2个问题和选项]"
```

重复这个步骤添加A01-02到A01-05。

### 步骤3：添加音频文件（批量添加）

告诉AI：
```
"在Notion音频文件数据库中添加以下5个文件：
1. LA-A01-01.mp3 (511.5 KB) - 关联题目A01-01
2. LA-A01-02.mp3 (481.8 KB) - 关联题目A01-02
3. LA-A01-03.mp3 (464.7 KB) - 关联题目A01-03
4. LA-A01-04.mp3 (534.0 KB) - 关联题目A01-04
5. LA-A01-05.mp3 (569.9 KB) - 关联题目A01-05

所有文件的：
- 题型：Listen to an Announcement
- 状态：已生成
- 文件路径：audio/listening/[文件名]"
```

### 步骤4：更新功能模块

告诉AI：
```
"在Notion功能模块数据库中添加或更新：
- 功能名称：Listen to an Announcement
- 文件路径：toefl-listening-announcement-practice.html
- 状态：已完成
- 题目数量：5
- 音频数量：5"
```

## 📋 快速方式：一次性添加

告诉AI：
```
"请帮我将今天的所有工作内容添加到Notion：
1. 添加工作日志（已完成Listen to an Announcement功能）
2. 添加5个公告题目（A01-01到A01-05）
3. 添加5个音频文件记录
4. 更新功能模块状态

详细数据在 scripts/notion_sync_data.json 和 docs/TODAY_WORK_SUMMARY.md 中"
```

AI会读取这些文件并批量添加到Notion。

## 💡 推荐工作流

### 日常使用
1. **完成工作后**：告诉AI "添加工作日志：今天完成了..."
2. **添加题目后**：告诉AI "把这个题目添加到Notion"
3. **生成音频后**：告诉AI "把这个音频文件添加到Notion"

### 批量同步
1. 告诉AI："同步所有公告题目到Notion"
2. AI会读取HTML文件，提取所有题目，批量添加

## 📊 数据文件位置

- **题目数据**: `scripts/notion_sync_data.json`
- **工作总结**: `docs/TODAY_WORK_SUMMARY.md`
- **命令列表**: `scripts/notion_add_commands.json`

## ✅ 验证

添加完成后，在Notion中检查：
1. 工作日志数据库 - 应该有今天的记录
2. 题目数据库 - 应该有5个题目
3. 音频文件数据库 - 应该有5个文件
4. 功能模块数据库 - 应该有Listen to an Announcement记录
