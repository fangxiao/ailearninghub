import base64
import zlib
import urllib.request
import json
import time

def generate_mermaid_image_kroki(mmd_code, output_file):
    """使用 Kroki API 生成图片"""
    url = "https://kroki.io/mermaid/png"
    
    data = json.dumps({"diagramSource": mmd_code}).encode('utf-8')
    
    try:
        req = urllib.request.Request(url, data=data, headers={
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        })
        with urllib.request.urlopen(req, timeout=30) as response:
            img_data = response.read()
            with open(output_file, 'wb') as f:
                f.write(img_data)
        print(f"Generated: {output_file} ({len(img_data)} bytes)")
        return True
    except Exception as e:
        print(f"Error generating {output_file}: {e}")
        return False

mmd1 = """graph TB
    User[用户输入] --> Intent[意图识别<br/>intent_recognition]
    Intent --> |FAQ查询| KB[知识库检索<br/>knowledge_base]
    Intent --> |订单查询| Order[订单系统]
    Intent --> |转人工| Ticket[工单系统<br/>ticket_system]
    KB --> LLM[大模型生成<br/>GLM-5.1/Qwen3]
    Order --> LLM
    Ticket --> Human[人工客服]
    LLM --> Emotion[情感分析<br/>emotion_analysis]
    Emotion --> Response[响应输出]
    style User fill:#e3f2fd
    style Response fill:#e8f5e9
    style LLM fill:#fff3e0"""

mmd2 = """graph LR
    subgraph 云端部署
        C1[智谱 GLM-5.1] --> C1a[性价比高<br/>中文强]
        C2[通义千问3] --> C2a[极速响应<br/>企业级]
        C3[DeepSeek V3] --> C3a[代码能力强]
    end
    subgraph 本地部署
        L1[Ollama + Qwen3] --> L1a[无需API Key<br/>数据不出本地]
        L2[vLLM + GLM5] --> L2a[高性能推理<br/>生产环境]
    end
    style C1 fill:#e3f2fd
    style C2 fill:#e3f2fd
    style C3 fill:#e3f2fd
    style L1 fill:#fff3e0
    style L2 fill:#fff3e0"""

mmd3 = """graph LR
    U[用户问题] --> I[意图识别<br/>intents.json]
    I --> |匹配FAQ| F[FAQ知识库<br/>faq.json]
    I --> |提取实体| E[实体词典<br/>entities.json]
    F --> R[检索相关答案]
    E --> R
    R --> A[生成响应]
    style U fill:#e3f2fd
    style A fill:#e8f5e9
    style F fill:#fff3e0
    style E fill:#fff3e0"""

mmd4 = """graph TB
    S[开始] --> A[安装依赖<br/>pip install -r requirements.txt]
    A --> B{选择部署方式}
    B --> |云端| C[配置API Key]
    B --> |本地| D[启动Ollama<br/>ollama serve]
    C --> E[验证配置]
    D --> E
    E --> F[测试大模型]
    F --> G[完成]
    style S fill:#e3f2fd
    style G fill:#e8f5e9"""

base_dir = "/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/mermaid-img"

print("Generating diagrams with Kroki...")
generate_mermaid_image_kroki(mmd1, f"{base_dir}/diagram1.png")
time.sleep(0.5)
generate_mermaid_image_kroki(mmd2, f"{base_dir}/diagram2.png")
time.sleep(0.5)
generate_mermaid_image_kroki(mmd3, f"{base_dir}/diagram3.png")
time.sleep(0.5)
generate_mermaid_image_kroki(mmd4, f"{base_dir}/diagram4.png")
print("Done!")
