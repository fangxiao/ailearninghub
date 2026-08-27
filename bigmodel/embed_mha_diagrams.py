#!/usr/bin/env python3
"""Embed MHA diagrams into article 04 HTML."""

import base64

def img_to_base64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

# Read images
fig1_b64 = img_to_base64('mermaid/07-single-vs-multi-head.png')
fig2_b64 = img_to_base64('mermaid/08-vector-split-concat.png')
fig3_b64 = img_to_base64('mermaid/09-mha-flow.png')

# Read HTML
with open('大模型原理系列-04.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Insert figure 1 after section 1 (after "多头注意力：给模型多双眼睛")
insert_pos1 = html.find('<!-- 对话块 -->')
if insert_pos1 != -1:
    fig1_block = '''
<!-- 图1: 单头 vs 多头 -->
<section style="text-align:center;margin:30px 0;">
<img src="data:image/png;base64,''' + fig1_b64 + '''" alt="单头注意力 vs 多头注意力" style="max-width:100%;border-radius:8px;">
<p style="font-size:12px;color:#888;text-align:center;margin-top:8px;font-style:italic;">图1：单头注意力只能从单一视角理解，多头注意力从多个视角综合分析</p>
</section>

'''
    html = html[:insert_pos1] + fig1_block + html[insert_pos1:]

# Insert figure 2 after section 3 (after "多头注意力的计算过程")
insert_pos2 = html.find('<!-- feynman块 -->')
if insert_pos2 != -1:
    fig2_block = '''
<!-- 图2: 向量拆分与拼接 -->
<section style="text-align:center;margin:30px 0;">
<img src="data:image/png;base64,''' + fig2_b64 + '''" alt="向量拆分与拼接" style="max-width:100%;border-radius:8px;">
<p style="font-size:12px;color:#888;text-align:center;margin-top:8px;font-style:italic;">图2：512维向量拆分为8个64维子向量，分别计算后拼接</p>
</section>

'''
    html = html[:insert_pos2] + fig2_block + html[insert_pos2:]

# Insert figure 3 after section 7 (after "多头注意力的变体")
insert_pos3 = html.find('<!-- 彩蛋 -->')
if insert_pos3 != -1:
    fig3_block = '''
<!-- 图3: 多头注意力流程 -->
<section style="text-align:center;margin:30px 0;">
<img src="data:image/png;base64,''' + fig3_b64 + '''" alt="多头注意力流程" style="max-width:100%;border-radius:8px;">
<p style="font-size:12px;color:#888;text-align:center;margin-top:8px;font-style:italic;">图3：多头注意力完整计算流程——每个头独立计算Q、K、V，然后拼接输出</p>
</section>

'''
    html = html[:insert_pos3] + fig3_block + html[insert_pos3:]

# Write back
with open('大模型原理系列-04.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Images embedded successfully!')
print('Updated: 大模型原理系列-04.html')