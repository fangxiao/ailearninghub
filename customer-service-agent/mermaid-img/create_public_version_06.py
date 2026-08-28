#!/usr/bin/env python3
import base64

base_dir = '/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/mermaid-img'

# 使用已有的图片
with open(f'{base_dir}/diagram02_1.png', 'rb') as f:
    img1 = base64.b64encode(f.read()).decode()

with open(f'{base_dir}/diagram1.png', 'rb') as f:
    img2 = base64.b64encode(f.read()).decode()

# 读取HTML文件
with open('/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/客服Agent实战系列-06.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 在第一个表格后添加情感分析流程图
insert1 = '''</table>

<p style="text-align: center; color: #888; font-size: 12px; margin-top: 20px;">图：情感分析流程</p>
<img src="data:image/png;base64,{}" alt="情感分析流程" style="max-width:100%;height:auto;display:block;margin:20px auto;">

<p>情感分析的重要性：</p>

<blockquote class="highlight">'''

html = html.replace('</table>\n\n<p>情感分析的重要性：</p>\n\n<blockquote class="highlight">', insert1.format(img1))

# 在实现方式表格后添加情感等级处理流程图
insert2 = '''</table>

<p style="text-align: center; color: #888; font-size: 12px; margin-top: 20px;">图：情感等级处理流程</p>
<img src="data:image/png;base64,{}" alt="情感等级处理流程" style="max-width:100%;height:auto;display:block;margin:20px auto;">

<p>客服场景我们选择<strong>关键词匹配 + 大模型识别</strong>的混合方案：</p>

<blockquote class="highlight">'''

html = html.replace('</table>\n\n<p>客服场景我们选择<strong>关键词匹配 + 大模型识别</strong>的混合方案：</p>\n\n<blockquote class="highlight">', insert2.format(img2))

# 保存公众号版本
with open('/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/客服Agent实战系列-06-公众号版.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("第六篇文章公众号版本已创建，包含2张流程图")
print(f"文件大小: {len(html)} bytes")