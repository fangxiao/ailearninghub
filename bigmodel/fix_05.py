#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复HTML中重复的base64前缀
"""

with open('大模型原理系列-05.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

if 'data:image/png;base64,data:image/png;base64,' in html_content:
    html_content = html_content.replace('data:image/png;base64,data:image/png;base64,', 'data:image/png;base64,')
    print("05: 已修复重复前缀")

with open('大模型原理系列-05.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("完成")