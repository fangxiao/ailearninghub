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

# 图1: 客服Agent核心架构
mmd1 = '''graph TB
    User[用户输入] --> Intent[意图识别]
    Intent --> |FAQ查询| KB[知识库检索]
    Intent --> |订单查询| Order[订单系统]
    Intent --> |转人工| Ticket[工单系统]
    KB --> LLM[大模型生成]
    Order --> LLM
    Ticket --> Human[人工客服]
    LLM --> Emotion[情感分析]
    Emotion --> Response[响应输出]
    style User fill:#e3f2fd
    style Response fill:#e8f5e9
    style LLM fill:#fff3e0'''
mmd_to_png(mmd1, f'{base_dir}/diagram1.png')
time.sleep(1)

# 图2: 云端 vs 本地部署（简化）
mmd2 = '''graph LR
    C1[智谱GLM] --> C1a[性价比高]
    C2[通义千问] --> C2a[极速响应]
    L1[Ollama] --> L1a[无需APIKey]
    L2[vLLM] --> L2a[高性能]
    style C1 fill:#e3f2fd
    style C2 fill:#e3f2fd
    style L1 fill:#fff3e0
    style L2 fill:#fff3e0'''
mmd_to_png(mmd2, f'{base_dir}/diagram2.png')
time.sleep(1)

# 图3: 数据流转过程
mmd3 = '''graph LR
    U[用户问题] --> I[意图识别]
    I --> |FAQ| F[知识库]
    I --> |实体| E[实体词典]
    F --> R[检索]
    E --> R
    R --> A[响应]
    style U fill:#e3f2fd
    style A fill:#e8f5e9'''
mmd_to_png(mmd3, f'{base_dir}/diagram3.png')
time.sleep(1)

# 图4: 快速验证流程
mmd4 = '''graph TB
    S[开始] --> A[安装依赖]
    A --> B[选择部署]
    B --> |云端| C[配置Key]
    B --> |本地| D[启动Ollama]
    C --> E[验证]
    D --> E
    E --> F[测试]
    F --> G[完成]
    style S fill:#e3f2fd
    style G fill:#e8f5e9'''
mmd_to_png(mmd4, f'{base_dir}/diagram4.png')

print("Done!")
