# 🚀 快速开始 - 自动同步（无需Git）

## ✨ 功能

**文件保存时自动同步到Notion，无需Git commit！**

只要你在Cursor中保存文件，就会自动同步到Notion。

## 🎯 三步开始

### 1. 配置Notion API Key（如果还没配置）

编辑 `.env` 文件，添加：
```
NOTION_API_KEY=secret_你的API密钥
```

### 2. 启动自动同步服务

```bash
bash scripts/start_auto_sync.sh
```

### 3. 开始工作！

现在你只需要：
- ✅ 在HTML文件中添加/修改题目
- ✅ **保存文件** (Cmd+S)
- ✅ 自动同步到Notion！

## 📝 使用示例

### 添加新题目

1. 打开 `toefl-listening-announcement-practice.html`
2. 添加新题目到 `ANNOUNCEMENT_SETS`
3. **保存文件** (Cmd+S)
4. 终端显示：`✅ 已同步: A01-06 - New Announcement`
5. 在Notion中立即看到新题目！

### 生成音频文件

1. 运行音频生成脚本
2. 新文件保存到 `audio/listening/LA-A01-06.mp3`
3. 自动同步到Notion音频数据库
4. 自动关联题目ID

## 🛑 停止服务

```bash
bash scripts/stop_auto_sync.sh
```

或在终端按 `Ctrl+C`

## 🎛️ 在Cursor中使用

1. 按 `Cmd+Shift+P`
2. 输入 "Tasks: Run Task"
3. 选择 **"Start Auto Sync (File Monitor)"**

停止：选择 **"Stop Auto Sync"**

## 📊 监控的文件

- ✅ HTML文件：`toefl-listening-*.html`
- ✅ 音频文件：`audio/listening/*.mp3`

## 💡 提示

- 服务会在后台运行，不影响你的工作
- 文件保存后2秒内自动同步（防抖）
- 终端会显示同步状态
- 可以随时停止/启动服务

## ❓ 问题？

查看详细文档：`docs/AUTO_SYNC_GUIDE.md`
