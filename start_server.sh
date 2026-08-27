#!/bin/bash
# AI 学习智库一键启动脚本
cd "$(dirname "$0")"

echo "⚡ 正在生成/刷新最新知识库索引数据..."
python3 build_site_data.py

echo "🚀 启动本地 Web 服务器..."
python3 server.py
