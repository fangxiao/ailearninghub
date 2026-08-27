import sys
import subprocess
import os

# Try to import PIL, if not found, install it
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Installing Pillow...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
    from PIL import Image, ImageDraw, ImageFont

# Create a new image
width, height = 800, 400
img = Image.new('RGB', (width, height), color='#1e1e1e') # Dark terminal background
draw = ImageDraw.Draw(img)

# Load a font (use a basic one available on macOS)
try:
    # macOS systems usually have SF Mono or Menlo
    font = ImageFont.truetype("/System/Library/Fonts/SFMono-Regular.otf", 18)
    font_bold = ImageFont.truetype("/System/Library/Fonts/SFMono-Bold.otf", 18)
except IOError:
    print("Special font not found, using default.")
    font = ImageFont.load_default()
    font_bold = font

# Draw terminal window title bar
draw.rectangle([0, 0, width, 30], fill='#333333')
draw.ellipse([10, 8, 22, 20], fill='#ff5f56') # Red close button
draw.ellipse([30, 8, 42, 20], fill='#ffbd2e') # Yellow minimize button
draw.ellipse([50, 8, 62, 20], fill='#27c93f') # Green maximize button
draw.text((width/2, 15), "~ terminal - zsh - 80x24", fill='#aaaaaa', anchor='mm', font=font)

# Draw terminal content
y_pos = 60

# User trying to run command
draw.text((30, y_pos), "$ python main.py", fill='#00ff00', font=font)
y_pos += 30

# Error message
draw.text((30, y_pos), "  File \"main.py\", line 12, in <module>", fill='#ffffff', font=font)
y_pos += 30
draw.text((30, y_pos), "    config = json.load(open('settings.json'))", fill='#ffffff', font=font)
y_pos += 30
draw.text((30, y_pos), "            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^", fill='#ff5f56', font=font)
y_pos += 30
draw.text((30, y_pos), "json.decoder.JSONDecodeError: Expecting ',' delimiter:", fill='#ff5f56', font=font_bold)
y_pos += 25
draw.text((30, y_pos), "line 9 column 14 (char 135)", fill='#ff5f56', font=font)
y_pos += 40

# Annotation bubble
draw.rounded_rectangle([30, y_pos, 600, y_pos + 50], radius=10, outline='#ffbd2e', width=2)
draw.text((50, y_pos + 25), ">>> 不小心多打了一个逗号，整个下午都在排查 JSON 错误...", fill='#ffbd2e', font=font, anchor='lm')

# Save the image
output_path = "/Users/admin/project/lovely/platform/doc/prototype/terminal_error.png"
img.save(output_path)
print(f"Image saved to {output_path}")
