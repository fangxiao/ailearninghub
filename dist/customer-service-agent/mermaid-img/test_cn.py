#!/usr/bin/env python3
import subprocess
import base64
import os
import zlib
import urllib.parse

def mmd_to_png_pako(mmd_content, output_path):
    """使用 pako 压缩方式支持中文"""
    # 使用 pako 压缩
    import urllib.request
    
    # 先尝试用 base64 编码
    encoded = base64.b64encode(mmd_content.encode('utf-8')).decode().replace('\n', '')
    url = f"https://mermaid.ink/img/{encoded}"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
            with open(output_path, 'wb') as f:
                f.write(data)
        size = os.path.getsize(output_path)
        print(f"Generated: {output_path} ({size} bytes)")
        return size > 100
    except Exception as e:
        print(f"Error: {e}")
        return False

base_dir = '/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/mermaid-img'

# 测试中文
mmd_test = '''graph LR
    A[开始] --> B[结束]
    style A fill:#e3f2fd'''
mmd_to_png_pako(mmd_test, f'{base_dir}/test_cn.png')
