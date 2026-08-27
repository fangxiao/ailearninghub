#!/usr/bin/env python3
import subprocess
import base64
import os

def mmd_to_png(mmd_content, output_path):
    encoded = base64.b64encode(mmd_content.encode()).decode().replace('\n', '')
    url = f"https://mermaid.ink/img/{encoded}"
    result = subprocess.run(['curl', '-s', '-o', output_path, url], capture_output=True)
    size = os.path.getsize(output_path)
    print(f"Generated: {output_path} ({size} bytes)")
    return size > 100

base_dir = '/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/mermaid-img'

# 图1: 客服Agent核心架构
mmd1 = '''graph TB
    User[User Input] --> Intent[Intent Recognition]
    Intent --> |FAQ| KB[Knowledge Base]
    Intent --> |Order| Order[Order System]
    Intent --> |Human| Ticket[Ticket System]
    KB --> LLM[LLM Generation]
    Order --> LLM
    Ticket --> Human[Human Agent]
    LLM --> Emotion[Emotion Analysis]
    Emotion --> Response[Response Output]
    style User fill:#e3f2fd
    style Response fill:#e8f5e9
    style LLM fill:#fff3e0'''
mmd_to_png(mmd1, f'{base_dir}/diagram1.png')

# 图2: 云端 vs 本地部署
mmd2 = '''graph LR
    C1[GLM-5.1] --> C1a[Cost Effective]
    C2[Qwen3] --> C2a[Fast Response]
    C3[DeepSeek] --> C3a[Code Strong]
    L1[Ollama] --> L1a[No API Key]
    L2[vLLM] --> L2a[High Performance]
    style C1 fill:#e3f2fd
    style C2 fill:#e3f2fd
    style C3 fill:#e3f2fd
    style L1 fill:#fff3e0
    style L2 fill:#fff3e0'''
mmd_to_png(mmd2, f'{base_dir}/diagram2.png')

# 图3: 数据流转过程
mmd3 = '''graph LR
    U[User Query] --> I[Intent]
    I --> |FAQ| F[FAQ Base]
    I --> |Entity| E[Entity Dict]
    F --> R[Search]
    E --> R
    R --> A[Response]
    style U fill:#e3f2fd
    style A fill:#e8f5e9
    style F fill:#fff3e0
    style E fill:#fff3e0'''
mmd_to_png(mmd3, f'{base_dir}/diagram3.png')

# 图4: 快速验证流程
mmd4 = '''graph TB
    S[Start] --> A[Install Deps]
    A --> B[Choose Deploy]
    B --> |Cloud| C[Config API Key]
    B --> |Local| D[Start Ollama]
    C --> E[Verify Config]
    D --> E
    E --> F[Test LLM]
    F --> G[Done]
    style S fill:#e3f2fd
    style G fill:#e8f5e9'''
mmd_to_png(mmd4, f'{base_dir}/diagram4.png')

print("All images generated!")
