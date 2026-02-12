# 🚀 Notion同步快速开始指南

## ✅ 已完成
- ✅ Python虚拟环境已创建
- ✅ Python依赖已安装（notion-client, watchdog）
- ✅ Git hook脚本已准备
- ✅ 同步脚本已就绪

## 📋 下一步：配置Notion API Key

### 步骤1：获取Notion API Key

1. 访问：https://www.notion.so/my-integrations
2. 点击 **"+ New integration"**
3. 填写信息：
   - **Name**: TOEFL Practice Sync
   - **Type**: Internal
   - **Associated workspace**: 选择你的工作区
4. 点击 **"Submit"**
5. 复制 **"Internal Integration Token"**（以 `secret_` 开头）

### 步骤2：添加API Key到项目

编辑 `.env` 文件，添加：

```bash
NOTION_API_KEY=secret_你的API密钥
```

### 步骤3：连接Integration到Notion页面

1. 打开你的Notion页面：https://www.notion.so/3055eb7be7e480a19e19fd360181d918
2. 点击右上角 **"..."** → **"Connections"**
3. 搜索并添加你的integration（名称：TOEFL Practice Sync）

### 步骤4：测试连接

```bash
# 激活虚拟环境
source .venv/bin/activate

# 测试同步（会显示连接状态）
python3 scripts/notion_sync.py --sync-all

# 退出虚拟环境
deactivate
```

## 🎯 开始使用

### 首次同步（导入所有现有数据）

```bash
source .venv/bin/activate
python3 scripts/notion_sync.py --sync-all
deactivate
```

这会同步：
- ✅ 所有公告题目（A01-01 到 A01-05）
- ✅ 所有音频文件（LA-*.mp3, LCR-*.mp3, LC-*.mp3）
- ✅ 创建今日工作日志

### 文件监控模式（实时同步）

```bash
source .venv/bin/activate
python3 scripts/notion_sync.py --watch
# 按 Ctrl+C 停止
deactivate
```

### Git自动记录工作日志

设置完成后，每次git commit会自动记录：

```bash
git commit -m "完成新功能开发"
# 自动记录到Notion工作日志！
```

## 📊 检查同步结果

1. 打开Notion页面：https://www.notion.so/3055eb7be7e480a19e19fd360181d918
2. 查看各个数据库：
   - 📚 题目数据库 - 应该看到5个公告题目
   - 🎵 音频文件数据库 - 应该看到所有音频文件
   - 📝 工作日志 - 应该看到今日的工作记录

## 🔧 在Cursor中使用

1. 按 `Cmd+Shift+P` (Mac) 或 `Ctrl+Shift+P` (Windows)
2. 输入 "Tasks: Run Task"
3. 选择：
   - **Sync to Notion** - 手动同步
   - **Watch Files & Sync to Notion** - 文件监控模式

## ❓ 常见问题

### Q: API Key在哪里找？
A: https://www.notion.so/my-integrations → 创建integration → 复制token

### Q: 如何知道数据库ID？
A: 打开Notion数据库，URL格式：`https://www.notion.so/workspace/数据库ID?v=视图ID`
   复制32位十六进制ID（带连字符）

### Q: 同步失败怎么办？
A: 
1. 检查 `.env` 文件中的API Key是否正确
2. 确认在Notion页面中已连接integration
3. 检查 `scripts/notion_sync_config.json` 中的数据库ID是否正确

### Q: 如何手动添加工作日志？
A: 
```bash
source .venv/bin/activate
python3 scripts/notion_sync.py --git-commit "工作内容描述"
deactivate
```

## 📞 需要帮助？

查看详细文档：`docs/NOTION_SYNC_SETUP.md`
