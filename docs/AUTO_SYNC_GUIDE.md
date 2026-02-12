# 🔄 Notion自动同步指南 - 无需Git

## 🎯 功能说明

这个自动同步服务会在**文件保存时自动同步到Notion**，无需Git commit。只要你在Cursor/VSCode中保存文件，就会自动同步！

## 🚀 快速开始

### 方式1：命令行启动（推荐）

```bash
# 启动自动同步服务
bash scripts/start_auto_sync.sh

# 停止服务
bash scripts/stop_auto_sync.sh
```

### 方式2：在Cursor/VSCode中启动

1. 按 `Cmd+Shift+P` (Mac) 或 `Ctrl+Shift+P` (Windows)
2. 输入 "Tasks: Run Task"
3. 选择 **"Start Auto Sync (File Monitor)"**
4. 服务会在后台运行，监控文件变更

停止服务：
- 选择 **"Stop Auto Sync"** 任务
- 或在终端按 `Ctrl+C`

## 📋 工作原理

### 监控的文件类型

- **HTML文件** (`.html`) - 自动提取题目并同步
  - `toefl-listening-announcement-practice.html`
  - `toefl-listening-choose-response-practice.html`
  - `toefl-listening-conversation-practice.html`

- **音频文件** (`.mp3`) - 自动记录音频信息
  - `audio/listening/LA-*.mp3`
  - `audio/listening/LCR-*.mp3`
  - `audio/listening/LC-*.mp3`

### 同步流程

1. **文件保存** → 检测到文件变更
2. **等待2秒** → 防抖处理（避免频繁同步）
3. **自动解析** → 提取题目/音频信息
4. **同步到Notion** → 更新数据库
5. **显示结果** → 终端显示同步状态

## 💡 使用场景

### 场景1：开发新题目

1. 在HTML文件中添加新题目
2. **保存文件** (Cmd+S / Ctrl+S)
3. 自动同步到Notion题目数据库
4. 老师可以在Notion中立即看到新题目

### 场景2：生成音频文件

1. 运行音频生成脚本
2. 新音频文件保存到 `audio/listening/`
3. 自动同步到Notion音频数据库
4. 自动关联对应的题目ID

### 场景3：修改题目内容

1. 修改HTML文件中的题目
2. **保存文件**
3. 自动更新Notion中的题目信息

## 🎛️ 配置选项

编辑 `scripts/notion_sync_config.json`：

```json
{
  "sync": {
    "watch_paths": [
      "toefl-listening-announcement-practice.html",
      "audio/listening/"
    ],
    "auto_sync_on_save": true,      // 保存时自动同步
    "sync_interval_seconds": 2      // 防抖时间（秒）
  }
}
```

## 📊 监控输出示例

```
============================================================
✅ Notion自动同步服务已启动
============================================================
📝 监控文件变更，自动同步到Notion
🛑 按 Ctrl+C 停止服务
============================================================

👀 监控: /path/to/toefl-listening-announcement-practice.html
👀 监控: /path/to/audio/listening

📝 [14:30:25] 检测到变更: toefl-listening-announcement-practice.html
🔄 [14:30:27] 同步题目文件: toefl-listening-announcement-practice.html
  ✅ 已同步: A01-01 - Library Hours Change
  ✅ 已同步: A01-02 - Course Registration Reminder
✨ 完成！同步了 2 个题目

📝 [14:35:10] 检测到变更: LA-A01-06.mp3
🔄 [14:35:12] 同步音频文件: LA-A01-06.mp3
  ✅ 已同步: LA-A01-06.mp3
```

## 🔧 高级用法

### 后台运行（Daemon模式）

```bash
# 启动后台服务
python3 scripts/notion_auto_sync.py --daemon

# 查看日志
tail -f /tmp/notion_sync.log

# 停止服务
bash scripts/stop_auto_sync.sh
```

### 检查服务状态

```bash
# 检查是否在运行
if [ -f .notion_sync.pid ]; then
    PID=$(cat .notion_sync.pid)
    if ps -p $PID > /dev/null; then
        echo "✅ 服务运行中 (PID: $PID)"
    else
        echo "❌ 服务未运行"
    fi
else
    echo "❌ 服务未运行"
fi
```

## ⚙️ 与Git的区别

| 特性 | Git同步 | 自动同步 |
|------|---------|----------|
| 触发方式 | Git commit | 文件保存 |
| 需要提交 | ✅ 是 | ❌ 否 |
| 实时性 | 延迟（需commit） | 即时（保存即同步） |
| 工作日志 | 自动记录commit | 不记录（仅同步数据） |
| 适用场景 | 代码版本管理 | 实时数据同步 |

## 🎯 最佳实践

### 1. 开发时保持服务运行

```bash
# 开始工作时启动
bash scripts/start_auto_sync.sh

# 结束工作时停止（可选）
bash scripts/stop_auto_sync.sh
```

### 2. 保存文件后检查同步

- 查看终端输出确认同步成功
- 在Notion中验证数据是否正确

### 3. 批量修改时

- 可以暂时停止服务
- 完成所有修改后启动服务
- 或手动运行 `python3 scripts/notion_sync.py --sync-all`

## ❓ 常见问题

### Q: 服务启动失败？
A: 
1. 检查虚拟环境：`source .venv/bin/activate`
2. 检查依赖：`pip list | grep watchdog`
3. 检查API Key：确认 `.env` 文件中有 `NOTION_API_KEY`

### Q: 文件保存了但没有同步？
A:
1. 确认服务正在运行
2. 检查文件路径是否在监控列表中
3. 查看终端输出是否有错误信息

### Q: 同步太频繁？
A: 
- 调整 `sync_interval_seconds` 增加防抖时间
- 或使用手动同步模式

### Q: 如何只同步特定文件？
A:
- 修改 `notion_sync_config.json` 中的 `watch_paths`
- 只添加需要监控的文件路径

## 🔄 与Git同步结合使用

可以同时使用两种方式：

- **自动同步**：文件保存时立即同步（实时）
- **Git同步**：Git commit时记录工作日志（版本管理）

两者互补，互不冲突！
