#!/usr/bin/env python3
import base64

base_dir = '/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/mermaid-img'

# 使用已有的图片
with open(f'{base_dir}/diagram02_1.png', 'rb') as f:
    img1 = base64.b64encode(f.read()).decode()

# 读取HTML文件
with open('/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/客服Agent实战系列-03-公众号版.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 在第一个表格后、意图识别重要性之前添加图片
insert1 = '''</table>

<p style="text-align: center; color: #888; font-size: 12px; margin-top: 20px;">图：意图识别流程示意</p>
<img src="data:image/png;base64,{}" alt="意图识别流程" style="max-width:100%;height:auto;display:block;margin:20px auto;">

<p>意图识别的重要性：</p>

<blockquote class="highlight">'''

html = html.replace('</table>\n\n<p>意图识别的重要性：</p>\n\n<blockquote class="highlight">', insert1.format(img1))

# 保存
with open('/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/客服Agent实战系列-03-公众号版.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("第一张图片已添加")
print(f"文件大小: {len(html)} bytes")