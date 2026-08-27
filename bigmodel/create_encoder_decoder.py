#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Encoder-Decoder 架构示意图
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

# ============ Encoder-Decoder 架构图 ============
width, height = 750, 400
img = Image.new('RGB', (width, height), '#FFFFFF')
draw = ImageDraw.Draw(img)

draw.text((220, 8), "Transformer: 编码器与解码器", font=font_title, fill='#333')

# ============ 左侧：Encoder（蓝色） ============
# Encoder 标签
draw.text((60, 45), "Encoder", font=font_med, fill='#1565c0')
draw.text((60, 62), "(理解脑)", font=font_small, fill='#666')

# 输入
draw.rounded_rectangle([60, 95, 280, 135], radius=8, fill='#e3f2fd', outline='#1976d2', width=2)
draw.text((100, 105), "Hello, world!", font=font_med, fill='#1565c0')
draw.text((100, 125), "输入句子", font=font_small, fill='#666')

# Encoder 层
for i in range(3):
    y = 155 + i * 50
    draw.rounded_rectangle([60, y, 280, y+40], radius=6, fill='#bbdefb', outline='#1976d2', width=1)
    draw.text((100, y+12), f"Layer {i+1}: Self-Attention + FFN", font=font_small, fill='#1565c0')

# Encoder 输出
draw.rounded_rectangle([60, 320, 280, 360], radius=6, fill='#e3f2fd', outline='#1976d2', width=2)
draw.text((90, 330), "Context Vectors", font=font_small, fill='#1565c0')
draw.text((90, 348), "（语义向量）", font=font_small, fill='#666')

# ============ 中间：连接线 ============
# Encoder 到 Decoder 的箭头
draw.text((305, 185), "语义向量", font=font_small, fill='#666')
draw.text((305, 200), "传递", font=font_small, fill='#666')
draw.polygon([(295, 220), (285, 205), (305, 205)], fill='#999')
draw.line([(280, 220), (350, 220)], fill='#999', width=2)
draw.polygon([(350, 220), (365, 210), (365, 230)], fill='#999')

# ============ 右侧：Decoder（绿色） ============
# Decoder 标签
draw.text((400, 45), "Decoder", font=font_med, fill='#2e7d32')
draw.text((400, 62), "(生成脑)", font=font_small, fill='#666')

# 输入（Shifted）
draw.rounded_rectangle([400, 95, 620, 135], radius=8, fill='#e8f5e9', outline='#388e3c', width=2)
draw.text((430, 105), "<BOS> 你", font=font_med, fill='#2e7d32')
draw.text((430, 125), "已生成 + 输入嵌入", font=font_small, fill='#666')

# Decoder 层
for i in range(3):
    y = 155 + i * 50
    draw.rounded_rectangle([400, y, 620, y+40], radius=6, fill='#c8e6c9', outline='#388e3c', width=1)
    if i == 1:
        draw.text((420, y+12), f"Layer {i+1}: Masked SA + Cross Attention", font=font_small, fill='#2e7d32')
    else:
        draw.text((420, y+12), f"Layer {i+1}: Self-Attention + FFN", font=font_small, fill='#2e7d32')

# Decoder 输出
draw.rounded_rectangle([400, 320, 620, 360], radius=6, fill='#e8f5e9', outline='#388e3c', width=2)
draw.text((430, 330), "Output Probabilities", font=font_small, fill='#2e7d32')
draw.text((430, 348), "（下一个词的分布）", font=font_small, fill='#666')

# ============ 底部：生成过程 ============
draw.rounded_rectangle([100, 380, 650, 420], radius=8, fill='#fff8e1', outline='#ffa000', width=1)
draw.text((120, 390), "生成过程：", font=font_small, fill='#333')
draw.text((200, 390), "你 -> 好好 -> 你好好 -> 你好好， -> 你好好，世 -> ... -> 你好，世界！", font=font_small, fill='#666')

img.save('mermaid/11-encoder-decoder.png')
print("Encoder-Decoder架构图已保存")

import base64
with open('mermaid/11-encoder-decoder.png', 'rb') as f:
    img_data = base64.b64encode(f.read()).decode('utf-8')
print(f"Base64长度: {len(img_data)}")