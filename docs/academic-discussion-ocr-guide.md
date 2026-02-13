# OCR 文字提取使用指南

## 方法1：使用 Python OCR 脚本（推荐）

### 安装依赖

```bash
# 安装 Python 库（如果系统限制，使用虚拟环境）
python3 -m venv venv
source venv/bin/activate
pip install pytesseract pillow

# Tesseract OCR 已安装（/opt/homebrew/bin/tesseract）
```

### 使用方法

**处理单个题目：**
```bash
python3 scripts/extract_text_from_images.py "/Users/tengda/Downloads/学术讨论写作/Automation"
```

**批量处理所有题目：**
```bash
python3 scripts/extract_text_from_images.py "/Users/tengda/Downloads/学术讨论写作/" --all
```

结果会保存到：`docs/academic-discussion/ocr_results.jsonl`

---

## 方法2：使用 macOS 自带 OCR（简单快速）

macOS 的预览（Preview）和截图工具支持 OCR：

1. **打开截图**：双击图片文件
2. **选择文字**：Cmd+A 全选，或直接拖选文字
3. **复制**：Cmd+C
4. **粘贴到题库**：粘贴到 `docs/academic-discussion-question-bank.md`

**优点：**
- 无需安装
- 识别准确度高
- 支持中英文

**步骤：**
1. 打开题目文件夹中的图片（通常是题目名称命名的.png文件）
2. 在预览中，文字会自动可选
3. 复制文字，粘贴到题库文件

---

## 方法3：手动录入模板

如果 OCR 效果不好，可以手动录入。使用以下模板：

```markdown
### D07 - Automation (Practice)
**Category:** Technology  
**Source:** Practice  
**Image:** `images/d07-automation.png`

**Professor Question:**
[从截图中复制粘贴教授问题]

**Student Posts:**
- **[Author1]:** [从截图中复制粘贴第一个学生回复]
- **[Author2]:** [从截图中复制粘贴第二个学生回复]

**Notes:** 
- [可选：任何备注]

**Status:** ⏳
```

---

## 推荐工作流程

### 快速批量处理（推荐）

1. **使用 macOS 预览 OCR**：
   - 打开每个题目的主图片（通常是题目名称命名的.png）
   - Cmd+A 全选文字
   - Cmd+C 复制
   - 直接粘贴到题库文件

2. **整理格式**：
   - 分离 Professor Question 和 Student Posts
   - 添加分类和来源标签
   - 复制图片到 `docs/academic-discussion/images/`

3. **批量转换**：
   - 每完成10题，运行转换脚本
   - `python3 scripts/convert-question-bank-to-json.py`

---

## 图片命名规范

复制截图到 `docs/academic-discussion/images/` 时，使用以下命名：

- `d07-automation.png`
- `d08-early-adopter.png`
- `d09-switching-jobs.png`
- ...

格式：`d{编号}-{简短名称}.png`

---

## 常见问题

**Q: OCR 识别不准确怎么办？**
A: 使用 macOS 预览的 OCR，通常比 Python OCR 更准确。

**Q: 图片中有中文和英文混合？**
A: macOS 预览可以同时识别中英文，直接复制即可。

**Q: 如何快速处理大量题目？**
A: 
1. 批量打开图片（选中多个，空格预览）
2. 逐个复制文字
3. 使用模板快速格式化

---

*最后更新：2026-02-13*
