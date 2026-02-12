#!/bin/bash
# 启动Notion自动同步服务

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_DIR="$PROJECT_ROOT/.venv"
PID_FILE="$PROJECT_ROOT/.notion_sync.pid"

# 检查虚拟环境
if [ ! -d "$VENV_DIR" ]; then
    echo "❌ 错误: 虚拟环境不存在，请先运行: bash scripts/setup_notion_sync.sh"
    exit 1
fi

# 激活虚拟环境
source "$VENV_DIR/bin/activate"

# 检查是否已在运行
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "⚠️  服务已在运行 (PID: $OLD_PID)"
        echo "   停止服务: bash scripts/stop_auto_sync.sh"
        exit 1
    else
        rm -f "$PID_FILE"
    fi
fi

# 启动服务
echo "🚀 启动文件监控服务..."
cd "$PROJECT_ROOT"
python3 scripts/file_watcher_simple.py
