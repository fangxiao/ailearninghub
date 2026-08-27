#!/usr/bin/env python3
"""Embed PE diagrams into HTML."""

import base64

def img_to_base64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

html_path = '大模型原理系列-03.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Embed waveform
wave_b64 = img_to_base64('mermaid/05-pe-waveform.png')
html = html.replace('PLACEHOLDER_PE_WAVE', wave_b64)

# Embed addition diagram
add_b64 = img_to_base64('mermaid/06-pe-addition.png')
html = html.replace('PLACEHOLDER_PE_ADD', add_b64)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Both diagrams embedded successfully!")
