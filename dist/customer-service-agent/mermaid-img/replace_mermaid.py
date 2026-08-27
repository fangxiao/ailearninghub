#!/usr/bin/env python3
import base64
import re

base_dir = '/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/mermaid-img'

# 读取所有图片的base64
images = []
for i in range(1, 4):  # 只有3个图
    png_file = f'{base_dir}/diagram{i}.png'
    with open(png_file, 'rb') as f:
        data = base64.b64encode(f.read()).decode()
    images.append(f'<img src="data:image/png;base64,{data}" alt="图{i}" style="max-width:100%;height:auto;display:block;margin:20px auto;">')

# 读取HTML文件
html_file = '/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/客服Agent实战系列-01.html'
with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# 替换mermaid图表为base64图片
# 图1
pattern1 = r'<p class="diagram-title">图1：客服Agent核心架构</p>\s*<div class="mermaid">.*?</div>'
html = re.sub(pattern1, f'<p class="diagram-title">图1：客服Agent核心架构</p>\n{images[0]}', html, flags=re.DOTALL)

# 图2
pattern2 = r'<p class="diagram-title">图2：数据流转过程</p>\s*<div class="mermaid">.*?</div>'
html = re.sub(pattern2, f'<p class="diagram-title">图2：数据流转过程</p>\n{images[1]}', html, flags=re.DOTALL)

# 图3
pattern3 = r'<p class="diagram-title">图3：快速验证流程</p>\s*<div class="mermaid">.*?</div>'
html = re.sub(pattern3, f'<p class="diagram-title">图3：快速验证流程</p>\n{images[2]}', html, flags=re.DOTALL)

# 移除mermaid脚本
html = re.sub(r'<script src="https://cdn\.jsdelivr\.net/npm/mermaid@10/dist/mermaid\.min\.js"></script>\s*<script>mermaid\.initialize\(\{startOnLoad:true,theme:[^}]+\}\);</script>', '', html)

# 保存
output_file = '/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/客服Agent实战系列-01-公众号版.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Generated: {output_file}")
