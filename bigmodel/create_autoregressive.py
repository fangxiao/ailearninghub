#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自回归生成过程示意图
"""

from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs('mermaid', exist_ok=True)

try:
    font_title = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 18)
    font_med = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 14)
    font_small = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 12)
except:
    font_title = ImageFont.load_default()
    font_med = ImageFont.load_default()
    font_small = ImageFont.load_default()

# ============ 自回归生成过程 ============
width, height = 750, 380
img = Image.new('RGB', (width, height), '#FFFFFF')
draw = ImageDraw.Draw(img)

draw.text((220, 10), "自回归生成：一个字一个字预测", font=font_title, fill='#333')

# 步骤展示
steps = [
    ("输入", "今天天气", '#e3f2fd', '#1565c0'),
    ("预测", "很(30%) 好(20%) 不错(15%)", '#fff8e1', '#f57c00'),
    ("选择", "很", '#e8f5e9', '#2e7d32'),
]

y_start = 50
for i, (label, content, bg, text_color) in enumerate(steps):
    y = y_start + i * 80
    draw.rounded_rectangle([50, y, 200, y+60], radius=8, fill=bg, outline=text_color, width=2)
    draw.text((80, y+10), label, font=font_med, fill=text_color)
    draw.text((70, y+35), content[:15], font=font_small, fill='#333')

# 箭头
for i in range(2):
    y = y_start + i * 80 + 30
    draw.polygon([(210, y), (230, y-10), (230, y+10)], fill='#999')
    draw.line([(230, y), (260, y)], fill='#999', width=2)

# 循环箭头说明
draw.rounded_rectangle([280, 50, 700, 290], radius=10, fill='#f5f5f5', outline='#ddd', width=1)
draw.text((300, 60), "生成过程：", font=font_med, fill='#333')

# 展示每一步
examples = [
    "Step 1: 输入='今天天气' → 预测下一个 → 选'很'",
    "Step 2: 输入='今天天气很' → 预测下一个 → 选'好'",
    "Step 3: 输入='今天天气很好' → 预测下一个 → 选'，'",
    "Step 4: 输入='今天天气很好，' → 预测下一个 → 选'适合'",
    "...",
    "最终输出：今天天气很好，适合出门散步",
]

for i, ex in enumerate(examples):
    y = 90 + i * 30
    draw.text((300, y), ex, font=font_small, fill='#666')

# 底部说明
draw.rounded_rectangle([50, 320, 700, 370], radius=8, fill='#fff3e0', outline='#ffa000', width=1)
draw.text((70, 330), "关键点：", font=font_med, fill='#f57c00')
draw.text((70, 350), "每生成一个字，这个字就加入输入，用来预测下一个字——这就是\"自回归\"", font=font_small, fill='#666')

img.save('mermaid/13-autoregressive-generation.png')
print("自回归生成示意图已保存")

import base64
with open('mermaid/13-autoregressive-generation.png', 'rb') as f:
    img_data = base64.b64encode(f.read()).decode('utf-8')
print(f"Base64长度: {len(img_data)}")