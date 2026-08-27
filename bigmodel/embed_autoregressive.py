#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
嵌入自回归生成图片到HTML
"""

import base64

with open('mermaid/13-autoregressive-generation.png', 'rb') as f:
    img_data = base64.b64encode(f.read()).decode('utf-8')
base64_img = f"data:image/png;base64,{img_data}"

with open('大模型原理系列-07.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

html_content = html_content.replace('PLACEHOLDER_AUTOREGRESSIVE', base64_img)

with open('大模型原理系列-07.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("图片已嵌入HTML")