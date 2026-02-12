#!/bin/bash
# 停止Notion自动同步服务

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PID_FILE="$PROJECT_ROOT/.notion_sync.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "ℹ️  服务未运行"
    exit 0
fi

PID=$(cat "$PID_FILE")

if ps -p "$PID" > /dev/null 2>&1; then
    echo "🛑 停止服务 (PID: $PID)..."
    kill "$PID"
    rm -f "$PID_FILE"
    echo "✅ 服务已停止"
else
    echo "ℹ️  服务未运行"
    rm -f "$PID_FILE"
fi
