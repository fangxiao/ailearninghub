import base64
import sys

# Path to the generated image
image_path = "/Users/admin/project/lovely/platform/doc/prototype/terminal_error.png"
html_path = "/Users/admin/project/lovely/platform/doc/prototype/ccswitch搭配claude-code-01-公众号版.html"

# Read image and convert to base64
with open(image_path, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

# The new img tag
img_tag = f'''<section style="text-align: center; margin: 35px 0;">
    <img src="data:image/png;base64,{encoded_string}" alt="终端报错截图" style="max-width: 100%; border-radius: 8px;">
    <p style="font-size: 12px; color: #999; text-align: center; margin-top: 10px; font-style: italic;">“不小心多打了一个逗号，整个下午都在排查 JSON 错误”</p>
  </section>'''

# Read HTML file
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

# Replace the FIRST image placeholder
# Find the specific placeholder block for the first image
old_placeholder = '''  <!-- 图片占位 1：报错场景 -->
  <section style="text-align: center; margin: 35px 0; padding: 40px 20px; background: #fafafa; border: 2px dashed #ccc; border-radius: 8px;">
    <p style="margin: 0; font-size: 15px; color: #999;">[ 图片占位 ]</p>
    <p style="margin: 10px 0 0 0; font-size: 13px; color: #aaa;">请在此处插入：手动改配置后报错的截图 (如 JSON Parse Error 或 401 Unauthorized)</p>
  </section>
  <p style="font-size: 12px; color: #999; text-align: center; margin-top: 10px; font-style: italic;">“不小心多打了一个逗号，整个下午都在排查 JSON 错误”</p>'''

if old_placeholder in html_content:
    html_content = html_content.replace(old_placeholder, img_tag, 1)
    print("Successfully replaced the first image placeholder!")
else:
    print("Error: Could not find the exact placeholder. Searching for a fallback...")
    # Fallback: try to find just the unique text
    if "手动改配置后报错的截图" in html_content:
        # Replace the entire block by targeting a more unique string
        pass # We'll do a more careful replacement

# Write back to HTML file
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Updated {html_path}")
