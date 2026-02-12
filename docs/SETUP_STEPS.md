# 🎯 Notion自动同步 - 逐步设置指南

## ✅ 当前状态检查

- ✅ Python虚拟环境已创建
- ✅ Python依赖已安装
- ⚠️  Notion API Key需要配置

## 📝 设置步骤

### 步骤1：获取Notion API Key

1. **打开浏览器，访问**：
   ```
   https://www.notion.so/my-integrations
   ```

2. **点击 "+ New integration"** 按钮

3. **填写信息**：
   - **Name**: `TOEFL Practice Sync`
   - **Type**: 选择 `Internal`
   - **Associated workspace**: 选择你的工作区

4. **点击 "Submit"**

5. **复制API Token**：
   - 找到 "Internal Integration Token"
   - 点击 "Show" 或 "Copy"
   - Token格式：`secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - **重要：复制这个token，下一步需要用到**

---

### 步骤2：添加API Key到项目

**方法A：在Cursor中编辑**

1. 在Cursor中打开 `.env` 文件
2. 添加新的一行：
   ```
   NOTION_API_KEY=secret_你刚才复制的token
   ```
3. 保存文件 (Cmd+S)

**方法B：命令行添加**

运行以下命令（替换YOUR_TOKEN为你的实际token）：
```bash
echo "NOTION_API_KEY=secret_YOUR_TOKEN" >> .env
```

---

### 步骤3：连接Integration到Notion页面

1. **打开你的Notion页面**：
   ```
   https://www.notion.so/3055eb7be7e480a19e19fd360181d918
   ```

2. **点击页面右上角的 "..."** (三个点)

3. **选择 "Connections"** (连接)

4. **搜索并添加你的integration**：
   - 搜索框输入：`TOEFL Practice Sync`
   - 点击你的integration名称
   - 确认连接

---

### 步骤4：测试连接

运行测试命令：

```bash
source .venv/bin/activate
python3 scripts/notion_sync.py --sync-all
deactivate
```

**预期结果**：
- ✅ 如果看到 "同步完成！" 说明连接成功
- ❌ 如果看到错误，检查：
  - API Key是否正确
  - Integration是否已连接到页面
  - 数据库ID是否正确

---

### 步骤5：启动自动同步服务

**启动服务**：
```bash
bash scripts/start_auto_sync.sh
```

**你会看到**：
```
============================================================
✅ Notion自动同步服务已启动
============================================================
📝 监控文件变更，自动同步到Notion
🛑 按 Ctrl+C 停止服务
============================================================

👀 监控: toefl-listening-announcement-practice.html
👀 监控: audio/listening
```

**现在服务正在运行！**

---

### 步骤6：测试自动同步

1. **打开一个HTML文件**（如 `toefl-listening-announcement-practice.html`）

2. **做一个小修改**（比如添加一个空格）

3. **保存文件** (Cmd+S 或 Ctrl+S)

4. **查看终端输出**，应该看到：
   ```
   📝 [时间] 检测到变更: toefl-listening-announcement-practice.html
   🔄 [时间] 同步题目文件: ...
   ✅ 已同步: ...
   ```

5. **检查Notion**，新数据应该已经同步！

---

## 🎉 完成！

现在你的自动同步系统已经设置完成：

- ✅ 文件保存时自动同步到Notion
- ✅ 无需Git commit
- ✅ 实时同步

## 🛑 停止服务

当不需要同步时，可以停止服务：

```bash
bash scripts/stop_auto_sync.sh
```

或在运行服务的终端按 `Ctrl+C`

## 📞 需要帮助？

如果遇到问题，检查：
1. API Key是否正确
2. Integration是否已连接
3. 虚拟环境是否激活
4. 查看错误信息
