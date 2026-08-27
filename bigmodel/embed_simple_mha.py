#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将简化版多头注意力图片嵌入HTML
"""

import base64
import re

# 读取图片并转为base64
with open('mermaid/10-simple-multi-head.png', 'rb') as f:
    img_data = base64.b64encode(f.read()).decode('utf-8')
base64_img = f"data:image/png;base64,{img_data}"

# 读取HTML文件
with open('大模型原理系列-04.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 检查是否已经嵌入过（避免重复嵌入）
if 'data:image/png;base64,data:image/png;base64,' in html_content:
    # 修复重复的前缀
    html_content = html_content.replace('data:image/png;base64,data:image/png;base64,', 'data:image/png;base64,')
    print("已修复重复前缀")

# 如果还没有嵌入，则替换占位符
if 'PLACEHOLDER_SIMPLE_MHA' in html_content:
    html_content = html_content.replace('PLACEHOLDER_SIMPLE_MHA', base64_img)
    print("已嵌入图片")
elif base64_img not in html_content:
    # 找到img标签并替换
    pattern = r'<img src="[^"]*" alt="多头同时思考示意"'
    replacement = f'<img src="{base64_img}" alt="多头同时思考示意"'
    html_content = re.sub(pattern, replacement, html_content)
    print("已替换图片")

# 保存
with open('大模型原理系列-04.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("完成")