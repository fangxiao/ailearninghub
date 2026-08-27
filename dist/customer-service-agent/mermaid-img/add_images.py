#!/usr/bin/env python3
import base64
import re

base_dir = '/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/mermaid-img'

# 读取图片的base64
png_files = {
    'system_prompt_flow': f'{base_dir}/diagram02_1.png',
}

img_tags = {}
for name, png_file in png_files.items():
    with open(png_file, 'rb') as f:
        data = base64.b64encode(f.read()).decode()
    img_tags[name] = f'<img src="data:image/png;base64,{data}" alt="System Prompt流程图" style="max-width:100%;height:auto;display:block;margin:20px auto;">'
    print(f"Generated base64 for {name}: {len(data)} bytes")

# 读取HTML文件
html_file = '/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/客服Agent实战系列-02-公众号版.html'
with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

# 在表格后面添加图片
pattern = r'</table>\s*<h3><span class="icon">2</span>'
replacement = f'''</table>

<p style="text-align: center; color: #888; font-size: 12px; margin-top: 20px;">图：System Prompt 在对话中的位置</p>
{img_tags['system_prompt_flow']}

<h3><span class="icon">2</span>'''

html = html.replace(pattern, replacement)

# 在Prompt加载部分添加图片
pattern2 = r'<p>在代码中加载 System Prompt：</p>\s*<p><strong>src/bot.py：</strong></p>'
replacement2 = f'''<p>在代码中加载 System Prompt：</p>

<p style="text-align: center; color: #888; font-size: 12px; margin-top: 20px;">图：Bot初始化流程</p>
<img src="data:image/png;base64,{base64.b64encode(open(f"{base_dir}/diagram1.png", "rb").read()).decode()}" alt="Bot初始化流程" style="max-width:100%;height:auto;display:block;margin:20px auto;">

<p><strong>src/bot.py：</strong></p>'''

html = html.replace(pattern2, replacement2)

# 保存
output_file = '/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/客服Agent实战系列-02-公众号版.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nGenerated: {output_file}")
print(f"Size: {len(html)} bytes")