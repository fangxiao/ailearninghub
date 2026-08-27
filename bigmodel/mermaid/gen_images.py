#!/usr/bin/env python3
import subprocess
import base64
import os

def mmd_to_png(mmd_content, output_path):
    encoded = base64.b64encode(mmd_content.encode()).decode().replace('\n', '')
    url = f"https://mermaid.ink/img/{encoded}"
    subprocess.run(['curl', '-s', '-o', output_path, url], check=True)
    print(f"Generated: {output_path}")

os.chdir('/Users/admin/project/lovely/platform/doc/prototype/myagent/mermaid')

# 图1: RNN串行处理
mmd1 = '''graph LR
    A["Input: Hello"] --> B["Word 1"]
    B --> C["Word 2"]
    C --> D["Word 3"]
    D --> E["Word 4"]
    style A fill:#e1f5fe
    style E fill:#fff3e0'''
mmd_to_png(mmd1, '01-rnn-process.png')

# 图2: Self-Attention并行处理
mmd2 = '''graph TD
    subgraph Input
        W1["Word 1"]
        W2["Word 2"]
        W3["Word 3"]
    end
    W1 & W2 & W3 --> Q["Q/K/V Generation"]
    Q --> AS["Attention Scores"]
    AS --> O1["New Embed 1"]
    AS --> O2["New Embed 2"]
    AS --> O3["New Embed 3"]
    style Q fill:#e8f5e9
    style AS fill:#fff3e0'''
mmd_to_png(mmd2, '02-self-attention.png')

# 图3: GPT生成过程
mmd3 = '''flowchart LR
    A["Input: Hello"] --> B["Transformer"]
    B --> C["Word 1"]
    C --> D["Word 2"]
    D --> E["..."]
    E --> F["End"]
    B1["History"] --> B
    B2["Memory"] --> B
    style A fill:#e1f5fe
    style F fill:#ffecb3'''
mmd_to_png(mmd3, '03-gpt-generate.png')

print("All images generated!")
