#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scaling Law示意图
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

# ============ Scaling Law曲线 ============
width, height = 750, 400
img = Image.new('RGB', (width, height), '#FFFFFF')
draw = ImageDraw.Draw(img)

draw.text((250, 10), "Scaling Law: 幂律关系", font=font_title, fill='#333')

# 坐标轴
draw.line([(80, 350), (700, 350)], fill='#333', width=2)  # X轴
draw.line([(80, 350), (80, 50)], fill='#333', width=2)    # Y轴

# X轴标签
draw.text((350, 360), "参数量 / 数据量 / 计算量", font=font_small, fill='#666')
draw.text((80, 360), "小", font=font_small, fill='#666')
draw.text((650, 360), "大", font=font_small, fill='#666')

# Y轴标签
draw.text((30, 200), "损失", font=font_small, fill='#666')
draw.text((30, 80), "高", font=font_small, fill='#666')
draw.text((30, 330), "低", font=font_small, fill='#666')

# 绘制幂律曲线（损失随规模增加而下降）
points = []
for i in range(50):
    x = 100 + i * 12
    # 幂律曲线：L = a * N^(-b)
    y = 80 + 250 * (1 - (i / 50) ** 0.5)
    points.append((x, y))

# 绘制曲线
for i in range(len(points) - 1):
    draw.line([points[i], points[i+1]], fill='#1976d2', width=3)

# 标注关键点
draw.ellipse([(150, 280), (160, 290)], fill='#e91e63', outline='#c2185b', width=2)
draw.text((170, 275), "GPT-2 (1.5B)", font=font_small, fill='#e91e63')

draw.ellipse([(350, 180), (360, 190)], fill='#e91e63', outline='#c2185b', width=2)
draw.text((370, 175), "GPT-3 (175B)", font=font_small, fill='#e91e63')

draw.ellipse([(550, 120), (560, 130)], fill='#e91e63', outline='#c2185b', width=2)
draw.text((570, 115), "GPT-4 (万亿级)", font=font_small, fill='#e91e63')

# 说明框
draw.rounded_rectangle([100, 50, 400, 120], radius=8, fill='#fff8e1', outline='#ffa000', width=1)
draw.text((120, 60), "幂律关系：", font=font_med, fill='#f57c00')
draw.text((120, 80), "规模增加10倍 → 损失下降固定比例", font=font_small, fill='#666')
draw.text((120, 100), "效果提升可预测！", font=font_small, fill='#4caf50')

img.save('mermaid/14-scaling-law.png')
print("Scaling Law示意图已保存")

import base64
with open('mermaid/14-scaling-law.png', 'rb') as f:
    img_data = base64.b64encode(f.read()).decode('utf-8')
print(f"Base64长度: {len(img_data)}")