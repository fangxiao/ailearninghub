#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BPE分词示意图
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

# ============ BPE分词示例 ============
width, height = 750, 400
img = Image.new('RGB', (width, height), '#FFFFFF')
draw = ImageDraw.Draw(img)

draw.text((250, 10), "BPE分词：英文单词怎么切", font=font_title, fill='#333')

# 常用词示例
draw.rounded_rectangle([50, 50, 350, 180], radius=10, fill='#e3f2fd', outline='#1976d2', width=2)
draw.text((80, 60), "常用词（整个作为1个Token）", font=font_med, fill='#1565c0')
draw.text((80, 90), "hello", font=font_med, fill='#333')
draw.ellipse([80, 115, 150, 145], fill='#4caf50', outline='#2e7d32', width=2)
draw.text((95, 122), "Token", font=font_small, fill='white')
draw.text((80, 155), "出现频率高 → 整体学习", font=font_small, fill='#666')

# 生僻词示例
draw.rounded_rectangle([400, 50, 700, 180], radius=10, fill='#fff8e1', outline='#ffa000', width=2)
draw.text((430, 60), "生僻词（拆成多个Token）", font=font_med, fill='#f57c00')
draw.text((430, 90), "tokenization", font=font_med, fill='#333')

# 拆分展示
draw.rounded_rectangle([430, 115, 500, 145], fill='#c8e6c9', outline='#2e7d32', width=1)
draw.text((440, 122), "token", font=font_small, fill='#2e7d32')
draw.rounded_rectangle([510, 115, 570, 145], fill='#c8e6c9', outline='#2e7d32', width=1)
draw.text((518, 122), "ize", font=font_small, fill='#2e7d32')
draw.rounded_rectangle([580, 115, 660, 145], fill='#c8e6c9', outline='#2e7d32', width=1)
draw.text((590, 122), "tion", font=font_small, fill='#2e7d32')

draw.text((430, 155), "出现频率低 → 拆开学习", font=font_small, fill='#666')

# 分割线
draw.line([(50, 200), (700, 200)], fill='#e0e0e0', width=1)

# 中文字示例
draw.text((80, 215), "中文分词示例", font=font_title, fill='#333')

draw.rounded_rectangle([50, 250, 350, 340], radius=10, fill='#f3e5f5', outline='#7b1fa2', width=2)
draw.text((80, 260), "方式一：基于字", font=font_med, fill='#7b1fa2')
draw.text((80, 290), "今天天气很好", font=font_med, fill='#333')
draw.text((80, 320), "今/天/天/气/很/好 = 6个Token", font=font_small, fill='#666')

draw.rounded_rectangle([400, 250, 700, 340], radius=10, fill='#e8f5e9', outline='#2e7d32', width=2)
draw.text((430, 260), "方式二：基于词（混合）", font=font_med, fill='#2e7d32')
draw.text((430, 290), "今天天气很好", font=font_med, fill='#333')
draw.text((430, 320), "今天/天气/很好 = 3个Token", font=font_small, fill='#666')

img.save('mermaid/12-bpe-tokenization.png')
print("BPE分词示意图已保存")

import base64
with open('mermaid/12-bpe-tokenization.png', 'rb') as f:
    img_data = base64.b64encode(f.read()).decode('utf-8')
print(f"Base64长度: {len(img_data)}")