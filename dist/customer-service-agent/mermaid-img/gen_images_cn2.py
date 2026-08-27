#!/usr/bin/env python3
import base64
import os
import urllib.request
import time

def mmd_to_png(mmd_content, output_path):
    encoded = base64.b64encode(mmd_content.encode('utf-8')).decode().replace('\n', '')
    url = f"https://mermaid.ink/img/{encoded}"
    
    print(f"URL length: {len(url)}")
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
            with open(output_path, 'wb') as f:
                f.write(data)
        size = os.path.getsize(output_path)
        print(f"Generated: {output_path} ({size} bytes)")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

base_dir = '/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/mermaid-img'

# 图3: 数据流转过程（简化）
mmd3 = '''graph LR
    A[用户问题] --> B[意图识别]
    B --> C[知识库]
    B --> D[实体词典]
    C --> E[检索]
    D --> E
    E --> F[响应]
    style A fill:#e3f2fd
    style F fill:#e8f5e9'''
mmd_to_png(mmd3, f'{base_dir}/diagram3.png')
time.sleep(1)

# 图4: 快速验证流程（简化）
mmd4 = '''graph TB
    A[开始] --> B[安装依赖]
    B --> C[选择部署]
    C --> D[配置]
    D --> E[验证]
    E --> F[测试]
    F --> G[完成]
    style A fill:#e3f2fd
    style G fill:#e8f5e9'''
mmd_to_png(mmd4, f'{base_dir}/diagram4.png')

print("Done!")
