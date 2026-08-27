#!/usr/bin/env python3
import base64

base_dir = '/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/mermaid-img'

# 读取图片的base64
with open(f'{base_dir}/diagram02_1.png', 'rb') as f:
    img1 = base64.b64encode(f.read()).decode()

with open(f'{base_dir}/diagram1.png', 'rb') as f:
    img2 = base64.b64encode(f.read()).decode()

# 读取HTML文件
with open('/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/客服Agent实战系列-02-公众号版.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 在第一个表格后添加图片
insert1 = '''</table>

<p style="text-align: center; color: #888; font-size: 12px; margin-top: 20px;">图：System Prompt 在对话中的位置</p>
<img src="data:image/png;base64,{}" alt="System Prompt流程图" style="max-width:100%;height:auto;display:block;margin:20px auto;">

<h3><span class="icon">2</span>'''

html = html.replace('</table>\n\n<h3><span class="icon">2</span>', insert1.format(img1))

# 在Prompt加载部分添加图片
insert2 = '''<p>在代码中加载 System Prompt：</p>

<p style="text-align: center; color: #888; font-size: 12px; margin-top: 20px;">图：Bot初始化流程</p>
<img src="data:image/png;base64,{}" alt="Bot初始化流程" style="max-width:100%;height:auto;display:block;margin:20px auto;">

<p><strong>src/bot.py：</strong></p>'''

html = html.replace('<p>在代码中加载 System Prompt：</p>\n\n<p><strong>src/bot.py：</strong></p>', insert2.format(img2))

# 保存
with open('/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/客服Agent实战系列-02-公众号版.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("图片已添加到文章中")
print(f"文件大小: {len(html)} bytes")