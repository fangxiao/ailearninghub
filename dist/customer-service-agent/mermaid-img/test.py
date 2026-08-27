#!/usr/bin/env python3
import subprocess
import base64
import os

def mmd_to_png(mmd_content, output_path):
    encoded = base64.b64encode(mmd_content.encode()).decode().replace('\n', '')
    url = f"https://mermaid.ink/img/{encoded}"
    print(f"URL length: {len(url)}")
    result = subprocess.run(['curl', '-s', '-o', output_path, url], capture_output=True)
    size = os.path.getsize(output_path)
    print(f"Generated: {output_path} ({size} bytes)")
    return size > 100

base_dir = '/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/mermaid-img'

# 测试一个简单的图表
mmd_test = '''graph LR
    A[开始] --> B[结束]
    style A fill:#e3f2fd'''
mmd_to_png(mmd_test, f'{base_dir}/test.png')
