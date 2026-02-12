# Cursor <-> Notion 同步系统设置指南

## 🎯 功能概述

这个同步系统实现了Cursor代码库与Notion数据库之间的自动同步，包括：

- ✅ **自动同步题目数据**：从HTML文件提取题目并同步到Notion
- ✅ **自动同步音频文件**：监控音频文件变更并记录到Notion
- ✅ **文件监控**：实时监控文件变更并自动同步
- ✅ **Git集成**：Git commit自动记录为工作日志
- ✅ **批量同步**：一次性同步所有数据

## 🚀 快速开始

### 1. 安装依赖

```bash
# 运行设置脚本（会自动安装依赖）
bash scripts/setup_notion_sync.sh

# 或手动安装
pip3 install notion-client watchdog
```

### 2. 配置Notion API Key

1. 访问 https://www.notion.so/my-integrations
2. 创建新的integration
3. 复制API token
4. 在 `.env` 文件中添加：
   ```
   NOTION_API_KEY=your_notion_api_key_here
   ```
5. 在Notion页面中连接integration：
   - 打开你的Notion页面
   - 点击右上角 "..." → "Connections"
   - 添加你的integration

### 3. 配置数据库ID

编辑 `scripts/notion_sync_config.json`，确保数据库ID正确：

```json
{
  "notion": {
    "database_ids": {
      "questions": "你的题目数据库ID",
      "audio": "你的音频数据库ID",
      "worklog": "你的工作日志数据库ID",
      "features": "你的功能模块数据库ID"
    }
  }
}
```

**如何获取数据库ID**：
- 打开Notion数据库页面
- URL格式：`https://www.notion.so/workspace/数据库ID?v=视图ID`
- 复制URL中的数据库ID（32位十六进制字符串，带连字符）

## 📖 使用方法

### 方法1：手动同步（推荐用于首次导入）

```bash
# 同步所有数据到Notion
python3 scripts/notion_sync.py --sync-all
```

### 方法2：文件监控模式（实时同步）

```bash
# 启动文件监控，自动同步变更
python3 scripts/notion_sync.py --watch
```

这个模式会：
- 监控HTML文件变更，自动同步题目
- 监控音频文件变更，自动同步音频信息
- 按Ctrl+C停止监控

### 方法3：Git集成（自动记录工作日志）

```bash
# 设置Git hook（只需运行一次）
python3 scripts/notion_sync.py --setup-git-hook

# 之后每次git commit都会自动记录到Notion工作日志
git commit -m "完成新功能开发"
```

### 方法4：在Cursor/VSCode中使用

1. 按 `Cmd+Shift+P` (Mac) 或 `Ctrl+Shift+P` (Windows)
2. 输入 "Tasks: Run Task"
3. 选择：
   - **Sync to Notion** - 手动同步所有数据
   - **Watch Files & Sync to Notion** - 启动文件监控
   - **Setup Notion Sync** - 运行设置脚本

## 🔧 配置文件说明

### `notion_sync_config.json`

```json
{
  "notion": {
    "database_ids": {
      "questions": "...",  // 题目数据库ID
      "audio": "...",      // 音频数据库ID
      "worklog": "...",    // 工作日志数据库ID
      "features": "..."    // 功能模块数据库ID
    }
  },
  "sync": {
    "watch_paths": [      // 监控的文件路径
      "toefl-listening-announcement-practice.html",
      "audio/listening/"
    ],
    "auto_sync_on_save": true,      // 保存时自动同步
    "auto_log_git_commits": true,   // Git commit自动记录
    "sync_interval_seconds": 300    // 同步间隔（秒）
  },
  "parsers": {
    "announcement": {
      "file": "toefl-listening-announcement-practice.html",
      "pattern": "ANNOUNCEMENT_SETS"
    }
  }
}
```

## 📝 工作流程建议

### 日常开发流程

1. **开始工作时**：
   ```bash
   # 启动文件监控（可选）
   python3 scripts/notion_sync.py --watch &
   ```

2. **完成题目后**：
   - 保存HTML文件
   - 如果开启了监控，会自动同步
   - 或手动运行：`python3 scripts/notion_sync.py --sync-all`

3. **生成音频后**：
   - 音频文件会自动被检测并同步
   - 或手动运行同步命令

4. **提交代码时**：
   - Git hook会自动记录commit消息到工作日志
   - 或手动添加：
     ```bash
     python3 scripts/notion_sync.py --git-commit "完成的功能描述"
     ```

### Review流程

1. **老师review题目**：
   - 在Notion题目数据库中查看新题目
   - 修改状态：待审核 → 已完成/待修改
   - 在页面中添加review意见

2. **检查同步状态**：
   - 查看音频数据库，确认所有音频都已同步
   - 查看工作日志，了解开发进度

## 🐛 故障排除

### 问题1：API Key错误

```
Error: Set NOTION_API_KEY environment variable
```

**解决**：
- 检查 `.env` 文件是否存在
- 确认API Key格式正确
- 确认在Notion中已连接integration

### 问题2：数据库ID错误

```
Error: Invalid database ID
```

**解决**：
- 检查 `notion_sync_config.json` 中的数据库ID
- 确认数据库ID格式正确（32位十六进制，带连字符）
- 确认integration有访问权限

### 问题3：文件监控不工作

```
Warning: watchdog not installed
```

**解决**：
```bash
pip3 install watchdog
```

### 问题4：Git hook不执行

**解决**：
1. 确认Git hook文件存在：`.git/hooks/post-commit`
2. 确认文件有执行权限：`chmod +x .git/hooks/post-commit`
3. 手动测试：`bash .git/hooks/post-commit`

## 🔄 同步策略

### 实时同步（推荐）
- 使用 `--watch` 模式
- 文件保存后自动同步
- 适合频繁开发时使用

### 定时同步
- 设置cron job或定时任务
- 定期运行 `--sync-all`
- 适合批量处理

### 手动同步
- 需要时手动运行同步命令
- 完全控制同步时机
- 适合review和测试

## 📊 数据映射

### 题目数据映射

| HTML字段 | Notion字段 | 说明 |
|---------|-----------|------|
| id | 题目ID | 唯一标识符 |
| type | 题型 | Listen to an Announcement等 |
| set_id | Set编号 | A01, R01等 |
| difficulty | 难度 | Easy/Medium/Hard |
| topic | 主题 | Campus/Academic等 |
| audio_file | 音频文件 | 文件路径 |

### 音频文件映射

| 文件命名 | 题型 | 题目ID提取 |
|---------|------|-----------|
| LA-*.mp3 | Listen to an Announcement | LA-A01-01 → A01-01 |
| LCR-*.mp3 | Listen and Choose a Response | LCR-R01-01 → R01-01 |
| LC-*.mp3 | Listen to a Conversation | LC-C01-01 → C01-01 |

## 🎯 最佳实践

1. **首次使用**：
   - 先运行 `--sync-all` 同步现有数据
   - 检查Notion中的数据是否正确

2. **日常开发**：
   - 使用 `--watch` 模式自动同步
   - 定期检查Notion确保数据同步

3. **代码提交**：
   - 使用有意义的commit消息
   - Git hook会自动记录到工作日志

4. **数据维护**：
   - 定期检查Notion数据库
   - 清理重复或错误的数据
   - 更新题目状态

## 📞 支持

如有问题，请：
1. 检查日志输出
2. 查看配置文件
3. 测试Notion API连接
4. 联系项目维护者
