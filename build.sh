#!/bin/bash

# 获取脚本所在的目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 进入 frontend 目录
cd "$SCRIPT_DIR/frontend" || exit

# 执行构建
rm -rf dist
npm run build-only

# 复制构建结果
rm -rf "$SCRIPT_DIR/frontend_dist"
cp -r dist "$SCRIPT_DIR/frontend_dist/"

# 回到脚本所在目录
cd "$SCRIPT_DIR" || exit

# 清理先前的构建
rm -rf ./dist
rm -rf ./build
rm ./main.spec

# 使用 pyinstaller 构建
pyinstaller main.py --onefile --distpath ./dist \
    --add-data "$SCRIPT_DIR/frontend_dist:frontend_dist" \
    --add-data "$SCRIPT_DIR/config.json5:." \
    --add-data "$SCRIPT_DIR/icon.png:." \
    --exclude-module PyQt5 --exclude-module PyQt6 \
    --exclude-module PySide2 --exclude-module PySide6 \
    --name bangumium --noconsole --icon="$SCRIPT_DIR/icon.png"