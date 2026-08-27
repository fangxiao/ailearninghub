#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版多头注意力示意图
"""

from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs('mermaid', exist_ok=True)

try:
    font_title = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 22)
    font_med = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 16)
    font_small = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 13)
except:
    font_title = ImageFont.load_default()
    font_med = ImageFont.load_default()
    font_small = ImageFont.load_default()

# ============ Figure: 简化版多头同时思考示意图 ============
width, height = 700, 350
img = Image.new('RGB', (width, height), '#FFFFFF')
draw = ImageDraw.Draw(img)

draw.text((200, 8), "多头注意力：多个小脑子同时分析", font=font_title, fill='#333')

# 中央：输入句子
draw.rounded_rectangle([200, 50, 500, 95], radius=8, fill='#e3f2fd', outline='#1976d2', width=2)
draw.text((230, 62), "小明在公园遇到了小红，她正在喂鸽子", font=font_small, fill='#1565c0')

# 三个小脑子 - 横向排列
brain_y = 200
brain_colors = [('#1976d2', '蓝色脑子'), ('#388e3c', '绿色脑子'), ('#f57c00', '橙色脑子')]
brain_x_positions = [100, 300, 500]

for i, ((color, label), x) in enumerate(zip(brain_colors, brain_x_positions)):
    # 脑子圆圈
    draw.ellipse([x, brain_y, x+120, brain_y+80], fill=color, outline='#333', width=2)
    draw.text((x+35, brain_y+25), f"脑子{i+1}", font=font_med, fill='white')

    # 连接线 - 从输入到脑子
    draw.line([(350, 95), (x+60, brain_y)], fill='#999', width=2)

# 三个脑子的分析结果
results = [
    "找人物关系\n小明↔小红",
    "理解动作\n喂鸽子",
    "理解场景\n在公园"
]

for i, (result, x) in enumerate(zip(results, brain_x_positions)):
    # 结果框
    draw.rounded_rectangle([x-10, brain_y+95, x+130, brain_y+175], radius=6, fill='#fff8e1', outline='#ffa000', width=1)
    lines = result.split('\n')
    draw.text((x+10, brain_y+105), lines[0], font=font_small, fill='#333')
    draw.text((x+10, brain_y+125), lines[1], font=font_small, fill='#666')

    # 从脑子到结果的连线
    draw.line([(x+60, brain_y+80), (x+60, brain_y+95)], fill='#999', width=2)

# 底部：合起来理解
draw.rounded_rectangle([200, brain_y+195, 500, brain_y+255], radius=8, fill='#e8f5e9', outline='#4caf50', width=2)
draw.text((230, brain_y+210), "所有信息合在一起 → 完整理解这句话", font=font_med, fill='#2e7d32')

# 箭头从三个结果指向底部
for x in brain_x_positions:
    draw.line([(x+60, brain_y+175), (350, brain_y+195)], fill='#4caf50', width=2)

img.save('mermaid/10-simple-multi-head.png')
print("简化版多头注意力示意图已保存到 mermaid/10-simple-multi-head.png")