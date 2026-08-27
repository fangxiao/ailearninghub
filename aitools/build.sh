#!/usr/bin/env bash
# 公众号文章一键构建：markdown → 公众号 HTML（modern 主题）→ 统一品牌色 → 预览
#
# 用法:
#   bash build.sh <文章.md> [品牌色, 默认 #2C6E9B]
#
# 说明:
#   - 转换用 baoyu-markdown-to-html（modern 主题 + 指定主色）
#   - modern 主题把 H2 下边框、引用块左边框写死成固定暖色 #E4B1A0，
#     EXTEND.md 在该版本不生效，所以用 sed 统一替换成品牌色
#   - 生成的 .html 与 .md 同目录；图片（如 diagram/）会被转换器拷贝引用
set -euo pipefail

MD="${1:-}"
if [ -z "$MD" ]; then
  echo "用法: bash build.sh <文章.md> [品牌色, 默认 #2C6E9B]"
  exit 1
fi
COLOR="${2:-#2C6E9B}"

SKILL=/Users/admin/.claude/skills/baoyu-markdown-to-html/scripts/main.ts
DIR=$(cd "$(dirname "$MD")" && pwd)
BASE=$(basename "$MD" .md)
OUT="$DIR/$BASE.html"

echo "→ 转换: $MD"
echo "  主题=modern  主色=$COLOR"
npx -y bun "$SKILL" "$MD" --theme modern --color "$COLOR" --font-size 16 --keep-title

echo "→ 统一边框/引用色为 $COLOR (替换 #E4B1A0)"
sed -i '' "s/#E4B1A0/$COLOR/g" "$OUT"

echo "→ 注入公众号样式微调（间距 / 代码块）"
python3 - "$OUT" <<'PY'
import sys
CSS = '''<style>
/* 公众号样式微调：间距与代码块 */
body { line-height: 1.8 !important; }
.container { padding: 22px 20px !important; border-radius: 16px !important; }
.p { line-height: 1.8 !important; letter-spacing: 0 !important; word-break: break-word !important; font-size: 16px !important; margin: 16px 0 !important; color: #2b2b2b !important; }
.h1 { letter-spacing: 0 !important; line-height: 1.4 !important; margin: 0 0 22px !important; font-size: 22px !important; }
.h2 { letter-spacing: 0 !important; line-height: 1.5 !important; padding: 0 0 8px !important; margin: 30px auto 14px !important; font-size: 19px !important; }
.h3 { letter-spacing: 0 !important; line-height: 1.5 !important; margin: 22px auto 10px !important; font-size: 17px !important; color: #2C6E9B !important; }
.ul, .ol { line-height: 1.8 !important; padding-left: 1.6em !important; margin: 14px 0 !important; color: #2b2b2b !important; }
.listitem { display: block !important; margin: 8px 0 !important; }
code.codespan { background: rgba(27,31,35,0.06) !important; color: #d14 !important; padding: 2px 6px !important; border-radius: 4px !important; font-size: 90% !important; word-break: break-word !important; }
code[class^="language-"] { display: block !important; white-space: pre-wrap !important; word-break: break-word !important; background: #f6f8fa !important; border: 1px solid #eaecef !important; border-radius: 8px !important; padding: 14px 16px !important; font-size: 13.5px !important; line-height: 1.6 !important; margin: 16px 0 !important; overflow-x: auto !important; color: #24292e !important; }
pre { background: #f6f8fa !important; border: 1px solid #eaecef !important; border-radius: 8px !important; padding: 14px 16px !important; margin: 16px 0 !important; overflow-x: auto !important; }
pre code { background: none !important; border: none !important; padding: 0 !important; }
</style>'''
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
if '<!-- wechat-style-injected -->' not in s:
    s = s.replace('</head>', '<!-- wechat-style-injected -->' + CSS + '\n</head>', 1)
    open(p, 'w', encoding='utf-8').write(s)
PY

echo "→ 清理本次 build 产生的 .bak 备份"
rm -f "${OUT}.bak-"* 2>/dev/null || true

echo "→ 预览: $OUT"
open "$OUT"
echo "完成。"
