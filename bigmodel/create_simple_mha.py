#!/usr/bin/env python3
"""Create simpler diagrams for 大模型原理系列-04 多头注意力"""

from PIL import Image, ImageDraw, ImageFont
import os
import base64

os.makedirs('mermaid', exist_ok=True)

font_path = '/System/Library/Fonts/Helvetica.ttc'
font_title = ImageFont.truetype(font_path, 16)
font_med = ImageFont.truetype(font_path, 13)
font_small = ImageFont.truetype(font_path, 11)

# ============ Figure 1: Single Eye vs Multiple Eyes ============
width1, height1 = 700, 300
img1 = Image.new('RGB', (width1, height1), '#FFFFFF')
draw1 = ImageDraw.Draw(img1)

draw1.text((250, 10), "一只眼睛 vs 多只眼睛", font=font_title, fill='#333')

# Left: single eye
draw1.rounded_rectangle([50, 60, 320, 270], radius=12, fill='#fff5f5', outline='#e0e0e0', width=2)
draw1.ellipse([160, 100, 210, 150], fill='#999', outline='#666')
draw1.text((140, 160), "单眼视角", font=font_med, fill='#333')
draw1.text((100, 190), "• 平面画面", font=font_small, fill='#666')
draw1.text((100, 215), "• 没有立体感", font=font_small, fill='#666')
draw1.text((100, 240), "• 容易看漏重点", font=font_small, fill='#f44336')

# Arrow
draw1.polygon([(350, 165), (330, 145), (370, 145)], fill='#999')
draw1.text((330, 170), "→", font=font_med, fill='#999')

# Right: multiple eyes
draw1.rounded_rectangle([380, 60, 650, 270], radius=12, fill='#f5fff5', outline='#e0e0e0', width=2)

# Draw multiple eyes
for i, (x, y, c) in enumerate([(420, 100, '#1976d2'), (480, 100, '#388e3c'), (540, 100, '#f57c00')]):
    draw1.ellipse([x, y, x+50, y+50], fill=c, outline='#333')
    draw1.text((x+5, y+60), f"眼睛{i+1}", font=font_small, fill='#333')

draw1.text((440, 165), "多头视角", font=font_med, fill='#333')
draw1.text((400, 195), "• 立体画面", font=font_small, fill='#666')
draw1.text((400, 220), "• 全面观察", font=font_small, fill='#666')
draw1.text((400, 245), "• 不容易漏重点", font=font_small, fill='#4caf50')

img1.save('mermaid/10-single-vs-multi-eye.png')
print("Figure 1 saved: mermaid/10-single-vs-multi-eye.png")

# ============ Figure 2: 8 Brains Analyzing One Sentence ============
width2, height2 = 700, 350
img2 = Image.new('RGB', (width2, height2), '#FFFFFF')
draw2 = ImageDraw.Draw(img2)

draw2.text((200, 10), "8个脑袋同时分析一句话", font=font_title, fill='#333')

# Sentence
draw2.rounded_rectangle([150, 45, 550, 80], radius=8, fill='#e3f2fd', outline='#1976d2', width=2)
draw2.text((180, 55), ""小明在公园遇到了小红，她正在喂鸽子"", font=font_small, fill='#1565c0')

# 8 brains
colors = ['#e91e63', '#9c27b0', '#3f51b5', '#009688', '#ff9800', '#4caf50', '#00bcd4', '#ff5722']
tasks = [
    "谁和谁说话",
    ""她"指谁",
    "在哪里",
    "在做什么",
    "动作承受者",
    "词的关系",
    "谁在何地",
    "整句故事"
]

for i, (color, task) in enumerate(zip(colors, tasks)):
    row = i // 4
    col = i % 4
    x = 50 + col * 165
    y = 110 + row * 100

    draw2.rounded_rectangle([x, y, x+150, y+85], radius=10, fill=color, outline='#333', width=1)
    draw2.text((x+50, y+15), f"脑袋{i+1}", font=font_med, fill='#fff')
    draw2.text((x+15, y+50), task, font=font_small, fill='#fff')

# Result arrow
draw2.polygon([(350, 310), (330, 290), (370, 290)], fill='#4caf50')
draw2.rounded_rectangle([200, 300, 500, 340], radius=8, fill='#e8f5e9', outline='#4caf50', width=2)
draw2.text((260, 312), "合起来 = 完整理解", font=font_med, fill='#2e7d32')

img2.save('mermaid/11-eight-brains.png')
print("Figure 2 saved: mermaid/11-eight-brains.png")

# Embed into HTML
with open('大模型原理系列-04.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('mermaid/10-single-vs-multi-eye.png', 'rb') as f:
    fig1_b64 = base64.b64encode(f.read()).decode()

with open('mermaid/11-eight-brains.png', 'rb') as f:
    fig2_b64 = base64.b64encode(f.read()).decode()

html = html.replace('PLACEHOLDER_MHA_VS_SINGLE', fig1_b64)
html = html.replace('PLACEHOLDER_MHA_SPLIT', fig2_b64)

with open('大模型原理系列-04.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("\nImages embedded successfully!")
print("Updated: 大模型原理系列-04.html")