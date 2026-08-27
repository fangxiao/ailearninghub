#!/usr/bin/env python3
"""为公众号版文章添加代码语法高亮 - 使用内联样式"""

import re
import os
from pathlib import Path
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer, TextLexer
from pygments.util import ClassNotFound
from pygments.formatters import HtmlFormatter

INPUT_DIR = '/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent-harness-skill/公众号版'


def detect_language(code_content):
    """根据代码内容猜测语言"""
    if re.search(r'def\s+\w+|import\s+\w+|from\s+\w+\s+import|class\s+\w+|self\.', code_content):
        return 'python'
    if re.search(r'\bconst\b|\bfunction\b|\bvar\b|=>|console\.log|require\(', code_content):
        return 'javascript'
    if re.search(r'#include|using namespace|std::|\bint main\b', code_content):
        return 'cpp'
    if re.search(r'\.select\(|\.from\(|\.where\(|SELECT|INSERT|UPDATE|DELETE|CREATE TABLE', code_content, re.IGNORECASE):
        return 'sql'
    if re.search(r'[│├──└──├─]', code_content):
        return 'structure'
    if re.search(r'^\s*#\s+.+|^\s*if\s+.+|^\s*for\s+.+|^\s*print\s+', code_content, re.MULTILINE):
        return 'bash'
    return 'text'


def build_style_map(formatter):
    """从 formatter 构建 class -> inline style 映射"""
    style_defs = formatter.get_style_defs()
    style_map = {}

    class_pattern = r'\.([a-zA-Z0-9_]+)\s*\{([^}]+)\}'
    for match in re.finditer(class_pattern, style_defs):
        cls_name = match.group(1)
        css_props = match.group(2).strip()
        declarations = []
        for decl in css_props.split(';'):
            decl = decl.strip()
            if decl and ':' in decl:
                key, value = decl.split(':', 1)
                key = key.strip()
                value = value.strip()
                if not key.startswith('/*') and value:
                    declarations.append(f'{key}: {value}')
        if declarations:
            style_map[cls_name] = '; '.join(declarations)

    return style_map


def apply_inline_styles(html_content, style_map):
    """将 CSS class 替换为内联样式"""
    def replace_span(match):
        classes = match.group(1).split()
        content = match.group(2)
        styles = []
        for cls in classes:
            if cls in style_map:
                styles.append(style_map[cls])
        if styles:
            return f'<span style="{"; ".join(styles)}">{content}</span>'
        return match.group(0)

    return re.sub(r'<span class="([^"]+)">(.*?)</span>', replace_span, html_content, flags=re.DOTALL)


def highlight_code_inline(code_content, lang=None):
    """对代码进行语法高亮并返回带内联样式的 HTML"""
    if lang is None:
        lang = detect_language(code_content)

    if lang == 'structure':
        return code_content.replace('│', '<span style="color:#8b949e">│</span>')

    if lang == 'text':
        return code_content

    try:
        lexer = get_lexer_by_name(lang)
    except ClassNotFound:
        try:
            lexer = guess_lexer(code_content)
        except ClassNotFound:
            return code_content

    formatter = HtmlFormatter(style='monokai', nowrap=True)
    highlighted = highlight(code_content, lexer, formatter)

    style_map = build_style_map(formatter)
    result = apply_inline_styles(highlighted, style_map)

    return result


def process_html_file(html_path):
    """处理单个 HTML 文件"""
    filename = os.path.basename(html_path)
    print(f"Processing: {filename}")

    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 支持多种代码块格式：
    # 1. <pre><code>代码</code></pre>
    # 2. <pre><div class="code-header">...</div><code>代码</code></pre>
    # 3. <pre>\n<div class="code-header">\n...\n</div>\n<code>\n代码\n</code>\n</pre>
    pattern1 = r'<pre><code>(.*?)</code></pre>'
    pattern2 = r'<pre>\s*<div class="code-header">.*?</div>\s*<code>(.*?)</code>\s*</pre>'

    code_stats = {'highlighted': 0, 'styled': 0}

    def replace_code(match):
        code = match.group(1)
        lang = detect_language(code)
        highlighted = highlight_code_inline(code, lang)

        lang_label_map = {
            'python': 'Python',
            'javascript': 'JavaScript',
            'cpp': 'C++',
            'sql': 'SQL',
            'bash': 'Bash',
            'structure': 'Structure',
            'text': 'Text',
        }
        lang_label = lang_label_map.get(lang, lang.upper())

        new_block = (
            f'<pre style="margin:16px 0;border-radius:8px;overflow:hidden;'
            f'box-shadow:0 2px 8px rgba(0,0,0,0.1);">'
            f'<div style="display:block;height:32px;padding:8px 16px;'
            f'background:#1e2433;color:#8b949e;font-size:12px;'
            f'font-family:monospace;text-transform:uppercase;'
            f'border-bottom:1px solid #2d3748;">'
            f'{lang_label}'
            f'</div>'
            f'<code style="display:block;padding:16px 20px;color:#e2e8f0;'
            f'background:#2d3748;font-family:monospace;font-size:13px;'
            f'line-height:1.6;overflow-x:auto;white-space:pre;">{highlighted}</code>'
            f'</pre>'
        )

        code_stats['highlighted'] += 1
        return new_block

    # 先处理带code-header的，再处理普通的
    content = re.sub(pattern2, replace_code, content, flags=re.DOTALL)
    content = re.sub(pattern1, replace_code, content, flags=re.DOTALL)

    if content != original_content:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Styled: {code_stats['highlighted']} code blocks")
    else:
        print(f"  No changes needed")


def main():
    html_files = sorted([
        f for f in os.listdir(INPUT_DIR)
        if f.endswith('.html')
    ])

    print(f"Found {len(html_files)} HTML files")

    for html_file in html_files:
        html_path = os.path.join(INPUT_DIR, html_file)
        process_html_file(html_path)

    print(f"\nDone! Code highlighting added.")


if __name__ == '__main__':
    main()
