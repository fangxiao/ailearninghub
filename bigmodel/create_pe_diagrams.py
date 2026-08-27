#!/usr/bin/env python3
"""Create positional encoding diagrams using PIL."""

from PIL import Image, ImageDraw, ImageFont
import math

# Get font
font_path = "/System/Library/Fonts/STHeiti Medium.ttc"

# ============ Figure 1: Positional Encoding Waveform ============
width, height = 700, 400
img1 = Image.new('RGB', (width, height), '#FFFFFF')
draw1 = ImageDraw.Draw(img1)

font_title = ImageFont.truetype(font_path, 22)
font_med = ImageFont.truetype(font_path, 16)
font_small = ImageFont.truetype(font_path, 13)

# Title
draw1.text((150, 10), "位置编码波形图（不同位置的sin值）", font=font_title, fill='#333')

# Axes
margin = 60
plot_x1, plot_x2 = margin, width - margin
plot_y1, plot_y2 = 80, height - 60
mid_y = (plot_y1 + plot_y2) // 2

# Y axis
draw1.line([(margin, plot_y1), (margin, plot_y2)], fill='#333', width=2)
# X axis
draw1.line([(margin, mid_y), (width - margin, mid_y)], fill='#ccc', width=1)

# Y labels
draw1.text((20, plot_y1 - 5), "1", font=font_small, fill='#666')
draw1.text((15, mid_y - 5), "0", font=font_small, fill='#666')
draw1.text((10, plot_y2 - 5), "-1", font=font_small, fill='#666')

# X labels
positions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
for pos in positions:
    x = plot_x1 + (pos / 9) * (plot_x2 - plot_x1)
    draw1.text((x - 5, mid_y + 10), str(pos), font=font_small, fill='#666')

# Draw sine waves for different dimensions (different frequencies)
colors = ['#e91e63', '#2196f3', '#4caf50', '#ff9800', '#9c27b0']
labels = ['维度0(高频)', '维度2(中高频)', '维度4(中频)', '维度6(中低频)', '维度8(低频)']
frequencies = [1.0, 0.5, 0.25, 0.125, 0.0625]

for i, (freq, color, label) in enumerate(zip(frequencies, colors, labels)):
    points = []
    for pos in range(100):
        x = plot_x1 + (pos / 99) * (plot_x2 - plot_x1)
        sin_val = math.sin(pos * freq * 0.5)
        y = mid_y - sin_val * (plot_y2 - mid_y - 20)
        points.append((x, y))
    
    for j in range(len(points) - 1):
        draw1.line([points[j], points[j+1]], fill=color, width=2)
    
    # Label
    draw1.text((500, 70 + i * 25), f"● {label}", font=font_small, fill=color)

img1.save('mermaid/05-pe-waveform.png', 'PNG')
print("Waveform diagram created!")

# ============ Figure 2: Positional Encoding Addition ============
width2, height2 = 620, 350
img2 = Image.new('RGB', (width2, height2), '#FFFFFF')
draw2 = ImageDraw.Draw(img2)

draw2.text((155, 2), "位置编码 + 词向量 = 最终输入", font=font_title, fill='#333')

# Layout parameters - optimized for 620px width (container max-width: 677px with 24px padding = 629px usable)
box_width = 130
box_height = 230
box_top = 40
spacing = 12

# Box 1: Embedding x
x1 = 10
draw2.rounded_rectangle([x1, box_top, x1 + box_width, box_top + box_height], radius=10, fill='#e3f2fd', outline='#1976d2', width=2)
draw2.text((x1 + 23, box_top + 8), "词向量 x", font=font_med, fill='#1565c0')
draw2.text((x1 + 10, box_top + 38), "[0.2, 0.5,", font=font_small, fill='#333')
draw2.text((x1 + 20, box_top + 58), " 0.8, 0.3", font=font_small, fill='#333')
draw2.text((x1 + 20, box_top + 78), " 0.6]", font=font_small, fill='#333')
draw2.text((x1 + 40, box_top + 110), "小明", font=font_med, fill='#333')
draw2.text((x1 + 40, box_top + 140), "喜欢", font=font_med, fill='#333')
draw2.text((x1 + 40, box_top + 170), "小红", font=font_med, fill='#333')

# Plus sign
plus_x = x1 + box_width + spacing
draw2.text((plus_x, box_top + 95), "+", font=ImageFont.truetype(font_path, 40), fill='#e91e63')

# Box 2: Positional Encoding p
x2 = plus_x + 35
draw2.rounded_rectangle([x2, box_top, x2 + box_width, box_top + box_height], radius=10, fill='#fce4ec', outline='#c2185b', width=2)
draw2.text((x2 + 13, box_top + 8), "位置编码 p", font=font_med, fill='#c2185b')
draw2.text((x2 + 8, box_top + 38), "[0, 1, 0,", font=font_small, fill='#333')
draw2.text((x2 + 13, box_top + 58), " 1, 0]", font=font_small, fill='#333')
draw2.text((x2 + 38, box_top + 90), "位置0", font=font_med, fill='#333')
draw2.text((x2 + 6, box_top + 120), "[0.84, 0.54", font=font_small, fill='#333')
draw2.text((x2 + 13, box_top + 140), " 0.01, 1,", font=font_small, fill='#333')
draw2.text((x2 + 23, box_top + 160), " 0]", font=font_small, fill='#333')
draw2.text((x2 + 38, box_top + 185), "位置1", font=font_med, fill='#333')

# Equals sign
equals_x = x2 + box_width + spacing
draw2.text((equals_x, box_top + 95), "=", font=ImageFont.truetype(font_path, 40), fill='#4caf50')

# Box 3: Final input
x3 = equals_x + 38
draw2.rounded_rectangle([x3, box_top, x3 + box_width, box_top + box_height], radius=10, fill='#e8f5e9', outline='#2e7d32', width=2)
draw2.text((x3 + 3, box_top + 8), "最终输入 x+p", font=font_med, fill='#2e7d32')
draw2.text((x3 + 8, box_top + 38), "[0.2, 1.5,", font=font_small, fill='#333')
draw2.text((x3 + 13, box_top + 58), " 0.8, 1.3", font=font_small, fill='#333')
draw2.text((x3 + 23, box_top + 78), " 0.6]", font=font_small, fill='#333')
draw2.text((x3 + 40, box_top + 110), "小明", font=font_med, fill='#333')
draw2.text((x3 + 40, box_top + 140), "喜欢", font=font_med, fill='#333')
draw2.text((x3 + 40, box_top + 170), "小红", font=font_med, fill='#333')

# Arrow and explanation at bottom
arrow_y = 300
arrow_start = x1 + 15
arrow_end = x3 + box_width - 15
draw2.line([(arrow_start, arrow_y), (arrow_end, arrow_y)], fill='#999', width=2)
draw2.polygon([(arrow_end, arrow_y), (arrow_end - 8, arrow_y - 6), (arrow_end - 8, arrow_y + 6)], fill='#999')
draw2.text((40, arrow_y - 22), "位置信息融入词向量 → 模型既能感知'词义'也能感知'位置'", font=font_small, fill='#666')

img2.save('mermaid/06-pe-addition.png', 'PNG')
print("Addition diagram created!")
