#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多头注意力可视化图
"""

from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs('mermaid', exist_ok=True)

try:
    font_title = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 20)
    font_med = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 14)
    font_small = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 12)
except:
    font_title = ImageFont.load_default()
    font_med = ImageFont.load_default()
    font_small = ImageFont.load_default()

# ============ 多头注意力可视化 ============
width, height = 750, 450
img = Image.new('RGB', (width, height), '#FFFFFF')
draw = ImageDraw.Draw(img)

draw.text((230, 8), "多头注意力：多个头同时分析", font=font_title, fill='#333')

# 输入向量
draw.rounded_rectangle([250, 40, 500, 80], radius=8, fill='#e3f2fd', outline='#1976d2', width=2)
draw.text((300, 52), "输入向量 X", font=font_med, fill='#1565c0')

# Q, K, V 投影
draw.rounded_rectangle([100, 110, 200, 150], radius=6, fill='#ffecb3', outline='#ffa000', width=1)
draw.text((115, 120), "W^Q", font=font_small, fill='#333')
draw.rounded_rectangle([280, 110, 380, 150], radius=6, fill='#ffecb3', outline='#ffa000', width=1)
draw.text((295, 120), "W^K", font=font_small, fill='#333')
draw.rounded_rectangle([460, 110, 560, 150], radius=6, fill='#ffecb3', outline='#ffa000', width=1)
draw.text((475, 120), "W^V", font=font_small, fill='#333')

# 箭头从输入到Q,K,V
for x in [150, 330, 510]:
    draw.line([(375, 80), (x, 110)], fill='#999', width=2)

# 8个头的 Attention
head_labels = [
    ("头1: 语法", '#e3f2fd', '#1565c0'),
    ("头2: 语义", '#f3e5f5', '#7b1fa2'),
    ("头3: 位置", '#e8f5e9', '#2e7d32'),
    ("头4: 指代", '#fff3e0', '#e65100'),
    ("头5: 关系", '#fce4ec', '#c2185b'),
    ("头6: 依存", '#e0f7fa', '#00838f'),
    ("头7: 实体", '#fbe9e7', '#4e342e'),
    ("头8: 语义", '#f1f8e9', '#558b2f'),
]

head_y_start = 175
head_spacing = 28

for i, (label, bg, text_color) in enumerate(head_labels):
    y = head_y_start + i * head_spacing
    draw.rounded_rectangle([120, y, 220, y+22], radius=4, fill=bg, outline=text_color, width=1)
    draw.text((130, y+4), label, font=font_small, fill=text_color)

# Q,K,V 到 各个头的连线
for i in range(8):
    y = head_y_start + i * head_spacing + 11
    draw.line([(200, 130), (120, y)], fill='#ccc', width=1)
    draw.line([(380, 130), (120, y)], fill='#ccc', width=1)
    draw.line([(560, 130), (120, y)], fill='#ccc', width=1)

# Concat
draw.rounded_rectangle([280, 200, 470, 350], radius=10, fill='#fff8e1', outline='#ffa000', width=2)
draw.text((320, 210), "Concat", font=font_med, fill='#333')
draw.text((300, 235), "把所有头的输出", font=font_small, fill='#666')
draw.text((300, 255), "拼接在一起", font=font_small, fill='#666')

# 从8个头到Concat
for i in range(8):
    y = head_y_start + i * head_spacing + 11
    draw.line([(220, y), (280, 275)], fill='#ffa000', width=1)

# W^O
draw.rounded_rectangle([530, 250, 620, 300], radius=6, fill='#c8e6c9', outline='#388e3c', width=2)
draw.text((535, 265), "W^O", font=font_med, fill='#2e7d32')
draw.line([(470, 275), (530, 275)], fill='#388e3c', width=2)

# 输出
draw.rounded_rectangle([530, 330, 680, 370], radius=6, fill='#e3f2fd', outline='#1976d2', width=2)
draw.text((540, 340), "MultiHead Output", font=font_small, fill='#1565c0')
draw.line([(620, 300), (605, 330)], fill='#1976d2', width=2)

# 底部说明
draw.rounded_rectangle([100, 395, 650, 440], radius=8, fill='#f5f5f5', outline='#ddd', width=1)
draw.text((120, 400), "每个头独立学习不同类型的信息：语法结构、词义、指代关系、位置关系等", font=font_small, fill='#666')
draw.text((120, 418), "最后把所有头的理解合起来，得到更全面、更准确的分析结果", font=font_small, fill='#666')

img.save('mermaid/10-multi-head-attention.png')
print("多头注意力可视化图已保存")

import base64
with open('mermaid/10-multi-head-attention.png', 'rb') as f:
    img_data = base64.b64encode(f.read()).decode('utf-8')
print(f"Base64长度: {len(img_data)}")