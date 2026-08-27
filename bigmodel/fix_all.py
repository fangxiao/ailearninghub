#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复HTML中重复的base64前缀
"""

files = [
    '大模型原理系列-04.html',
    '大模型原理系列-05.html',
    '大模型原理系列-06.html',
    '大模型原理系列-07.html',
    '大模型原理系列-08.html',
]

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            html_content = file.read()

        if 'data:image/png;base64,data:image/png;base64,' in html_content:
            html_content = html_content.replace('data:image/png;base64,data:image/png;base64,', 'data:image/png;base64,')
            print(f"{f}: 已修复重复前缀")

            with open(f, 'w', encoding='utf-8') as file:
                file.write(html_content)
        else:
            print(f"{f}: 无问题")
    except FileNotFoundError:
        print(f"{f}: 文件不存在")

print("完成")