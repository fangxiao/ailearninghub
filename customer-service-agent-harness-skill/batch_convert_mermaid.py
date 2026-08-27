#!/usr/bin/env python3
"""批量转换 Mermaid 图为 base64 图片 - v2 自动修复 Unicode 问题"""

import re
import os
import base64
import urllib.request
import time
from pathlib import Path

BASE_DIR = '/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent-harness-skill'
OUTPUT_DIR = '/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent-harness-skill/公众号版'


def is_ascii_diagram(content):
    """检查是否是 ASCII 字符画（非 Mermaid 代码）"""
    ascii_patterns = ['┌', '│', '└', '─', '┘', '┐', '┤', '├', '▼', '▲']
    return any(p in content for p in ascii_patterns)


def sanitize_mermaid(code):
    """修复 Mermaid 代码中的问题字符（仅处理 Unicode，不移除引号）"""
    code = code.replace('→', '->')
    code = code.replace('←', '<-')
    code = code.replace('↑', '^')
    code = code.replace('↓', 'v')
    code = code.replace('｜', '|')
    code = code.replace('＂', '"')
    code = code.replace('\u3000', ' ')
    code = re.sub(r'[ \t]+$', '', code, flags=re.MULTILINE)
    return code


def sanitize_mermaid_strict(code):
    """更激进的修复（用于降级重试）"""
    code = sanitize_mermaid(code)
    code = re.sub(r'\|"([^"]*)"\|', r'|\1|', code)
    return code


def generate_mermaid_image(mmd_code):
    """将 Mermaid 代码转换为 base64 PNG"""
    encoded = base64.urlsafe_b64encode(mmd_code.encode('utf-8')).decode('utf-8')
    url = f"https://mermaid.ink/img/{encoded}?type=png&bgColor=ffffff"

    for attempt in range(3):
        try:
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'image/png'}
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = resp.read()
                if len(data) > 100 and data[:8] == b'\x89PNG\r\n\x1a\n':
                    return base64.b64encode(data).decode('utf-8')
                else:
                    print(f"    Attempt {attempt+1}: Invalid response ({len(data)} bytes)")
        except Exception as e:
            print(f"    Attempt {attempt+1}: {e}")
            time.sleep(1)

    return None


def process_html_file(html_path):
    """处理单个 HTML 文件"""
    filename = os.path.basename(html_path)
    print(f"\n{'='*60}")
    print(f"Processing: {filename}")
    print(f"{'='*60}")

    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    img_count = 0

    pattern = r'<(?:p|div) class="diagram-title">([^<]+)</(?:p|div)>\s*<div class="mermaid">\s*(.*?)\s*</div>'

    matches = list(re.finditer(pattern, content, re.DOTALL))
    print(f"  Found {len(matches)} Mermaid blocks")

    for match in matches:
        title = match.group(1).strip()
        mmd_code = match.group(2).strip()

        if is_ascii_diagram(mmd_code):
            print(f"  [SKIP] ASCII diagram: {title[:50]}")
            continue

        print(f"  [CONVERT] {title[:50]}...")

        sanitized_code = sanitize_mermaid(mmd_code)
        b64_data = generate_mermaid_image(sanitized_code)

        if not b64_data:
            print(f"    Retrying with strict sanitization...")
            strict_code = sanitize_mermaid_strict(mmd_code)
            if strict_code != sanitized_code:
                b64_data = generate_mermaid_image(strict_code)

        if b64_data:
            img_tag = (
                f'<p class="diagram-title">{title}</p>\n'
                f'<img src="data:image/png;base64,{b64_data}" '
                f'alt="{title}" style="max-width:100%;height:auto;'
                f'display:block;margin:20px auto;border-radius:8px;">'
            )
            content = content.replace(match.group(0), img_tag)
            img_count += 1
            print(f"    [OK] {len(b64_data)} chars base64")
        else:
            print(f"    [FAIL] Keeping original Mermaid code")

    content = re.sub(
        r'<script\s+src="https://cdn\.jsdelivr\.net/npm/mermaid[^"]*"\s*></script>',
        '',
        content
    )
    content = re.sub(
        r'<script>mermaid\.initialize\([^)]*\);</script>',
        '',
        content
    )
    content = re.sub(
        r'<div class="mermaid">',
        '<div style="text-align:center;margin:20px;background:#fafafa;padding:20px;border-radius:8px;">',
        content
    )

    output_path = os.path.join(OUTPUT_DIR, filename)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  Saved: {output_path}")
    print(f"  Converted: {img_count} images")
    return img_count


def main():
    html_files = sorted([
        f for f in os.listdir(BASE_DIR)
        if f.endswith('.html') and '公众号版' not in f
    ])

    print(f"Found {len(html_files)} HTML files to process")
    total_images = 0

    for html_file in html_files:
        html_path = os.path.join(BASE_DIR, html_file)
        count = process_html_file(html_path)
        total_images += count

    print(f"\n{'='*60}")
    print(f"DONE! Converted {total_images} Mermaid diagrams to base64 images")
    print(f"Output: {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
