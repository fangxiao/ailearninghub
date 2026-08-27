#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
嵌入Encoder-Decoder图片到HTML
"""

import base64

with open('mermaid/11-encoder-decoder.png', 'rb') as f:
    img_data = base64.b64encode(f.read()).decode('utf-8')
base64_img = f"data:image/png;base64,{img_data}"

with open('大模型原理系列-05.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

html_content = html_content.replace('PLACEHOLDER_ENCODER_DECODER', base64_img)

with open('大模型原理系列-05.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("图片已嵌入HTML")