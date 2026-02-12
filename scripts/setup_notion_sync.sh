#!/bin/bash
# Cursor <-> Notion 同步系统设置脚本

set -e

echo "=========================================="
echo "Cursor <-> Notion 同步系统设置"
echo "=========================================="

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 需要Python 3"
    exit 1
fi

# 检查虚拟环境
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    echo ""
    echo "📦 创建Python虚拟环境..."
    python3 -m venv "$VENV_DIR"
fi

# 激活虚拟环境并安装依赖
echo ""
echo "📦 安装Python依赖..."
source "$VENV_DIR/bin/activate"
pip install notion-client watchdog --quiet
deactivate

# 检查.env文件
ENV_FILE=".env"
if [ ! -f "$ENV_FILE" ]; then
    echo ""
    echo "⚠️  .env文件不存在，正在创建..."
    touch "$ENV_FILE"
    echo "# Notion API Key" >> "$ENV_FILE"
    echo "NOTION_API_KEY=your_notion_api_key_here" >> "$ENV_FILE"
    echo ""
    echo "请编辑 .env 文件，添加你的 Notion API Key"
    echo "获取API Key: https://www.notion.so/my-integrations"
fi

# 设置Git hook
echo ""
echo "🔧 设置Git hook..."
source "$VENV_DIR/bin/activate"
python3 scripts/notion_sync.py --setup-git-hook
deactivate

# 测试连接
echo ""
echo "🧪 测试Notion连接..."
source "$VENV_DIR/bin/activate"
if python3 -c "
import sys
sys.path.insert(0, 'scripts')
from notion_sync import NotionSyncer
syncer = NotionSyncer()
print('✅ Notion连接成功')
" 2>/dev/null; then
    echo "✅ Notion连接成功"
else
    echo "❌ Notion连接失败，请检查API Key"
fi
deactivate

echo ""
echo "=========================================="
echo "设置完成！"
echo "=========================================="
echo ""
echo "使用方法："
echo "  1. 激活虚拟环境: source .venv/bin/activate"
echo "  2. 同步所有数据: python3 scripts/notion_sync.py --sync-all"
echo "  3. 监控文件变更: python3 scripts/notion_sync.py --watch"
echo "  4. 手动添加工作日志: python3 scripts/notion_sync.py --git-commit '工作内容'"
echo "  5. 退出虚拟环境: deactivate"
echo ""
