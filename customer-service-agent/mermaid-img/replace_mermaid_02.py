#!/usr/bin/env python3
import base64
import re

base_dir = '/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/mermaid-img'

# 读取图片的base64
png_file = f'{base_dir}/diagram02_1.png'
with open(png_file, 'rb') as f:
    data = base64.b64encode(f.read()).decode()
img_tag = f'<img src="data:image/png;base64,{data}" alt="图1" style="max-width:100%;height:auto;display:block;margin:20px auto;">'

# 读取HTML文件
html_file = '/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/客服Agent实战系列-02.html'
with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# 替换mermaid图表为base64图片
pattern = r'<p class="diagram-title">图1：System Prompt 在对话中的位置</p>\s*<div class="mermaid">.*?</div>'
html = re.sub(pattern, f'<p class="diagram-title">图1：System Prompt 在对话中的位置</p>\n{img_tag}', html, flags=re.DOTALL)

# 移除mermaid脚本
html = re.sub(r'<script src="https://cdn\.jsdelivr\.net/npm/mermaid@10/dist/mermaid\.min\.js"></script>\s*<script>mermaid\.initialize\(\{startOnLoad:true,theme:[^}]+\}\);</script>', '', html)

# 保存
output_file = '/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/客服Agent实战系列-02-公众号版.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Generated: {output_file}")
print(f"Size: {len(html)} bytes")