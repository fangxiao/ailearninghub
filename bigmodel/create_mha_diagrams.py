#!/usr/bin/env python3
"""Create diagrams for 大模型原理系列-04 多头注意力"""

from PIL import Image, ImageDraw, ImageFont
import os

# Create mermaid directory if not exists
os.makedirs('mermaid', exist_ok=True)

# Font setup
font_path = '/System/Library/Fonts/Helvetica.ttc'
font_title = ImageFont.truetype(font_path, 16)
font_med = ImageFont.truetype(font_path, 13)
font_small = ImageFont.truetype(font_path, 11)

# ============ Figure 1: Single vs Multi-Head Attention ============
width1, height1 = 750, 400
img1 = Image.new('RGB', (width1, height1), '#FFFFFF')
draw1 = ImageDraw.Draw(img1)

draw1.text((220, 5), "单头注意力 vs 多头注意力", font=font_title, fill='#333')

# Left side: Single head
draw1.rounded_rectangle([20, 40, 360, 380], radius=12, fill='#f5f5f5', outline='#ddd', width=2)
draw1.text((140, 50), "单头注意力", font=font_med, fill='#333')

# Draw single attention box
draw1.rounded_rectangle([60, 90, 320, 200], radius=10, fill='#e3f2fd', outline='#1976d2', width=2)
draw1.text((150, 100), "Self-Attention", font=font_med, fill='#1565c0')
draw1.text((80, 130), "Q, K, V → Attention", font=font_small, fill='#333')
draw1.text((80, 155), "一个视角", font=font_small, fill='#666')

# Show limitation
draw1.rounded_rectangle([60, 220, 320, 360], radius=10, fill='#ffebee', outline='#d32f2f', width=2)
draw1.text((130, 230), "局限性", font=font_med, fill='#d32f2f')
draw1.text((80, 260), "• 只能学一种模式", font=font_small, fill='#333')
draw1.text((80, 285), "• 语法/语义难以兼顾", font=font_small, fill='#333')
draw1.text((80, 310), "• 无法区分多义词", font=font_small, fill='#333')
draw1.text((80, 335), '  如"苹果"=水果/公司', font=font_small, fill='#666')

# Arrow
arrow_x = 390
draw1.polygon([(arrow_x, 200), (arrow_x - 15, 180), (arrow_x - 15, 220)], fill='#999')
draw1.text((arrow_x - 30, 170), "不够", font=font_small, fill='#666')

# Right side: Multi-head
draw1.rounded_rectangle([390, 40, 730, 380], radius=12, fill='#f5f5f5', outline='#ddd', width=2)
draw1.text((500, 50), "多头注意力", font=font_med, fill='#333')

# Draw multiple heads
colors_heads = ['#e91e63', '#9c27b0', '#3f51b5', '#009688', '#ff9800', '#4caf50', '#00bcd4', '#ff5722']
head_labels = ['头1\n语法', '头2\n语义', '头3\n词性', '头4\n实体',
              '头5\n指代', '头6\n关系', '头7\n位置', '头8\n情感']

for i, (color, label) in enumerate(zip(colors_heads, head_labels)):
    row = i // 4
    col = i % 4
    x = 410 + col * 75
    y = 90 + row * 80
    draw1.rounded_rectangle([x, y, x + 65, y + 65], radius=8, fill=color, outline='#333', width=1)
    draw1.text((x + 10, y + 20), label, font=font_small, fill='#fff')

# Merge arrow
draw1.polygon([(560, 255), (545, 235), (575, 235)], fill='#666')
draw1.polygon([(560, 255), (545, 275), (575, 275)], fill='#666')
draw1.rounded_rectangle([510, 265, 610, 300], radius=8, fill='#e8f5e9', outline='#2e7d32', width=2)
draw1.text((520, 275), "Concat", font=font_small, fill='#2e7d32')

# Advantage box
draw1.rounded_rectangle([390, 320, 730, 380], radius=10, fill='#e8f5e9', outline='#2e7d32', width=2)
draw1.text((500, 330), "优势", font=font_med, fill='#2e7d32')
draw1.text((400, 355), "• 每个头学不同模式", font=font_small, fill='#333')

img1.save('mermaid/07-single-vs-multi-head.png')
print("Figure 1 saved: mermaid/07-single-vs-multi-head.png")

# ============ Figure 2: Vector Split and Concatenation ============
width2, height2 = 750, 350
img2 = Image.new('RGB', (width2, height2), '#FFFFFF')
draw2 = ImageDraw.Draw(img2)

draw2.text((200, 5), "向量拆分与拼接过程", font=font_title, fill='#333')

# Input vector
draw2.rounded_rectangle([20, 50, 180, 300], radius=10, fill='#e3f2fd', outline='#1976d2', width=2)
draw2.text((55, 60), "输入向量", font=font_med, fill='#1565c0')
draw2.text((40, 95), "[x₁, x₂, x₃, ..., x₅₁₂]", font=font_small, fill='#333')
draw2.text((60, 130), "维度=512", font=font_small, fill='#666')

# Arrow
draw2.polygon([(200, 175), (185, 155), (215, 155)], fill='#999')

# Split arrow text
draw2.text((165, 175), "拆分", font=font_small, fill='#666')

# Split into 8 heads
draw2.text((230, 50), "拆分为8个头 (每头64维)", font=font_med, fill='#333')

for i in range(8):
    row = i // 4
    col = i % 4
    x = 230 + col * 125
    y = 85 + row * 85
    draw2.rounded_rectangle([x, y, x + 110, y + 70], radius=8, fill=colors_heads[i], outline='#333', width=1)
    draw2.text((x + 25, y + 25), f"头{i+1}", font=font_med, fill='#fff')

# Arrow down
draw2.polygon([(375, 270), (360, 250), (390, 250)], fill='#999')

# Concatenate
draw2.text((330, 275), "拼接", font=font_small, fill='#666')

# Output
draw2.rounded_rectangle([230, 290, 700, 330], radius=10, fill='#e8f5e9', outline='#2e7d32', width=2)
draw2.text((400, 300), "Concat(head₁, head₂, ..., head₈) × Wᵒ → 输出", font=font_med, fill='#2e7d32')

img2.save('mermaid/08-vector-split-concat.png')
print("Figure 2 saved: mermaid/08-vector-split-concat.png")

# ============ Figure 3: Multi-Head Attention Flow ============
width3, height3 = 750, 320
img3 = Image.new('RGB', (width3, height3), '#FFFFFF')
draw3 = ImageDraw.Draw(img3)

draw3.text((220, 5), "多头注意力计算流程", font=font_title, fill='#333')

# Step 1: Input
draw3.rounded_rectangle([20, 50, 150, 120], radius=10, fill='#e3f2fd', outline='#1976d2', width=2)
draw3.text((50, 60), "输入X", font=font_med, fill='#1565c0')
draw3.text((35, 85), "序列向量", font=font_small, fill='#333')

# Arrow 1
draw3.polygon([(165, 85), (150, 65), (180, 65)], fill='#999')
draw3.text((140, 95), "×W", font=font_small, fill='#666')

# Step 2: Q, K, V for each head
draw3.text((200, 50), "每个头独立计算Q、K、V", font=font_med, fill='#333')

for i in range(4):
    x = 200 + i * 135
    draw3.rounded_rectangle([x, 75, x + 120, 140], radius=8, fill=colors_heads[i], outline='#333', width=1)
    draw3.text((x + 35, 90), f"头{i+1}", font=font_small, fill='#fff')
    draw3.text((x + 25, 115), "Qᵢ, Kᵢ, Vᵢ", font=font_small, fill='#fff')

# Arrow 2
draw3.polygon([(355, 200), (340, 180), (370, 180)], fill='#999')
draw3.text((325, 210), "Attention", font=font_small, fill='#666')

# Step 3: Attention per head
draw3.text((200, 160), "每个头独立计算注意力", font=font_med, fill='#333')

for i in range(4):
    x = 200 + i * 135
    draw3.rounded_rectangle([x, 185, x + 120, 250], radius=8, fill=colors_heads[i+4], outline='#333', width=1)
    draw3.text((x + 30, 200), f"头{i+5}", font=font_small, fill='#fff')
    draw3.text((x + 25, 220), "headᵢ", font=font_small, fill='#fff')

# Arrow 3
draw3.polygon([(545, 200), (530, 180), (560, 180)], fill='#999')
draw3.text((515, 210), "Concat", font=font_small, fill='#666')

# Step 4: Concat
draw3.rounded_rectangle([580, 185, 730, 250], radius=10, fill='#e8f5e9', outline='#2e7d32', width=2)
draw3.text((620, 200), "拼接", font=font_med, fill='#2e7d32')
draw3.text((600, 225), "× Wᵒ", font=font_small, fill='#2e7d32')

img3.save('mermaid/09-mha-flow.png')
print("Figure 3 saved: mermaid/09-mha-flow.png")

print("\nAll diagrams created successfully!")
print("Files:")
print("  - mermaid/07-single-vs-multi-head.png")
print("  - mermaid/08-vector-split-concat.png")
print("  - mermaid/09-mha-flow.png")