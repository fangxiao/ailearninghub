#!/usr/bin/env bash
# ==============================================================================
# 🚀 快速建站与自媒体全流程技能 (Claude Code / Antigravity 官方一键安装脚本)
# 支持一键安装:
# 1. quick-site-builder (3分钟极速独立建站)
# 2. independent-knowledge-base-publisher (知识库发布与SEO)
# 3. wechat-official-account (微信公众号100%保真排版)
# ==============================================================================

set -e

REPO_URL="https://raw.githubusercontent.com/fangxiao/ailearninghub/main/.agents/skills"
TARGET_DIR="$HOME/.claude/skills"

echo "================================================================="
echo " 📦 正在为您的 Claude Code 安装【快速建站与自媒体全流程技能包】..."
echo "================================================================="

mkdir -p "$TARGET_DIR/quick-site-builder"
mkdir -p "$TARGET_DIR/independent-knowledge-base-publisher"
mkdir -p "$TARGET_DIR/wechat-official-account"

# 1. 下载 quick-site-builder
echo "⏳ 正在拉取 quick-site-builder ..."
curl -fsSL "$REPO_URL/quick-site-builder/SKILL.md" -o "$TARGET_DIR/quick-site-builder/SKILL.md"

# 2. 下载 independent-knowledge-base-publisher
echo "⏳ 正在拉取 independent-knowledge-base-publisher ..."
curl -fsSL "$REPO_URL/independent-knowledge-base-publisher/SKILL.md" -o "$TARGET_DIR/independent-knowledge-base-publisher/SKILL.md"

# 3. 下载 wechat-official-account
echo "⏳ 正在拉取 wechat-official-account ..."
curl -fsSL "$REPO_URL/wechat-official-account/SKILL.md" -o "$TARGET_DIR/wechat-official-account/SKILL.md"

echo "================================================================="
echo " 🎉 安装成功！已生效至: $TARGET_DIR"
echo ""
echo " 💡 现在打开终端输入 'claude'，即可直接对话使用："
echo "   • '用 quick-site-builder 帮我新建一个技术知识库'"
echo "   • '用 wechat-official-account 帮我把文章排版成公众号专用版'"
echo "================================================================="
