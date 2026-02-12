# 🔄 Cursor ↔ Notion 同步工作流

## 🎯 工作方式

由于Cursor已经集成了Notion MCP工具，我们可以通过以下方式实现同步：

### 方式1：文件监控 + 手动同步（推荐）

1. **启动文件监控**：
   ```bash
   bash scripts/start_auto_sync.sh
   ```

2. **正常开发**：
   - 在HTML文件中添加/修改题目
   - 保存文件 (Cmd+S)
   - 文件监控会自动记录变更

3. **查看待同步文件**：
   ```bash
   python3 scripts/check_sync_status.py
   ```

4. **通过Cursor同步**：
   - 告诉AI助手："同步这些文件到Notion"
   - AI会使用MCP工具自动添加到Notion

### 方式2：直接告诉AI同步

当你完成工作后，直接告诉AI：
- "把我刚才修改的题目同步到Notion"
- "同步所有公告题目到Notion"
- "添加今日工作日志到Notion"

AI会直接使用MCP工具操作Notion，无需API Key！

## 📋 当前状态

### 已准备的数据

✅ **题目数据** (5个公告题目):
- A01-01: Library Hours Change
- A01-02: Course Registration Reminder  
- A01-03: Campus Event Cancellation
- A01-04: Parking Policy Update
- A01-05: Dining Hall Menu Changes

✅ **音频文件** (5个):
- LA-A01-01.mp3 到 LA-A01-05.mp3

✅ **Notion数据库**:
- 📚 题目数据库
- 🎵 音频文件数据库
- 📝 工作日志
- 🔧 功能模块

## 🚀 开始使用

### 步骤1：启动文件监控

```bash
bash scripts/start_auto_sync.sh
```

### 步骤2：开始工作

- 正常开发，保存文件
- 文件变更会自动记录

### 步骤3：同步到Notion

告诉AI助手：
```
"请把我刚才修改的文件同步到Notion"
```

或查看待同步列表：
```bash
python3 scripts/check_sync_status.py
```

## 💡 最佳实践

1. **开发时**：
   - 保持文件监控运行
   - 正常保存文件
   - 定期告诉AI同步

2. **完成工作后**：
   - 查看待同步文件
   - 告诉AI："同步所有变更到Notion"
   - 在Notion中验证数据

3. **Review时**：
   - 在Notion中查看题目
   - 修改状态（待审核 → 已完成）
   - 添加review意见

## 🎉 优势

- ✅ 无需API Key配置
- ✅ 使用Cursor内置的MCP工具
- ✅ AI助手直接操作Notion
- ✅ 文件变更自动追踪
- ✅ 灵活的手动同步控制
