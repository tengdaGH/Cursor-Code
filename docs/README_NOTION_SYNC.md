# 🔄 Cursor ↔ Notion 同步系统

## ✅ 已完成设置

1. ✅ **Notion数据库已创建**：
   - 📚 题目数据库
   - 🎵 音频文件数据库
   - 📝 工作日志
   - 🔧 功能模块

2. ✅ **文件监控脚本已准备**
3. ✅ **数据解析脚本已创建**

## 🎯 最简单的工作方式

### **直接告诉AI助手同步！**

由于Cursor已经集成了Notion MCP工具，**最简单的方式就是直接告诉我同步**：

```
"把我刚才修改的题目同步到Notion"
"同步所有公告题目到Notion"
"添加今日工作日志到Notion"
```

我会直接使用MCP工具操作Notion，**无需任何API Key配置**！

## 📋 工作流程

### 日常开发

1. **正常开发**：
   - 在HTML文件中添加/修改题目
   - 生成音频文件
   - 保存文件

2. **告诉AI同步**：
   - "把我刚才修改的题目同步到Notion"
   - "同步所有公告题目"
   - "添加工作日志：今天完成了..."

3. **AI自动处理**：
   - 解析文件内容
   - 提取题目/音频信息
   - 添加到Notion数据库
   - 显示同步结果

### Review流程

1. **在Notion中查看**：
   - 打开Notion页面
   - 查看题目数据库
   - Review题目内容

2. **修改状态**：
   - 在Notion中修改题目状态
   - 添加review意见

3. **更新代码**：
   - 根据review修改代码
   - 告诉AI："更新Notion中的题目状态"

## 🛠️ 可选：文件监控

如果你想追踪文件变更，可以启动文件监控：

```bash
# 启动监控
bash scripts/start_auto_sync.sh

# 查看待同步文件
python3 scripts/check_sync_status.py

# 停止监控
Ctrl+C 或 bash scripts/stop_auto_sync.sh
```

监控会记录文件变更，然后你可以告诉我同步这些文件。

## 📊 当前数据状态

### 已准备的题目数据

- ✅ A01-01: Library Hours Change
- ✅ A01-02: Course Registration Reminder
- ✅ A01-03: Campus Event Cancellation
- ✅ A01-04: Parking Policy Update
- ✅ A01-05: Dining Hall Menu Changes

### 已准备的音频文件

- ✅ LA-A01-01.mp3 到 LA-A01-05.mp3

## 💡 使用示例

### 示例1：添加新题目后同步

```
你: "我刚刚在HTML文件中添加了新题目A01-06，请同步到Notion"
AI: [解析文件] [提取题目] [添加到Notion] ✅ 完成！
```

### 示例2：生成音频后同步

```
你: "我生成了新的音频文件LA-A01-06.mp3，请同步到Notion"
AI: [读取文件信息] [添加到音频数据库] ✅ 完成！
```

### 示例3：添加工作日志

```
你: "添加工作日志：今天完成了Listen to an Announcement功能的5个题目"
AI: [添加到工作日志数据库] ✅ 完成！
```

## 🎉 优势

- ✅ **无需API Key**：使用Cursor内置的MCP工具
- ✅ **即时同步**：告诉AI即可，立即处理
- ✅ **智能解析**：AI自动提取和格式化数据
- ✅ **灵活控制**：你想同步什么就同步什么
- ✅ **无需配置**：开箱即用

## 📞 需要帮助？

直接告诉我：
- "帮我同步..."
- "添加...到Notion"
- "更新Notion中的..."

我会立即处理！
