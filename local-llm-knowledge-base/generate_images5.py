import base64
import requests
import os

def generate_mermaid_image(mermaid_code, output_file):
    url = "https://kroki.io/mermaid/png"
    headers = {"Content-Type": "text/plain"}
    
    response = requests.post(url, data=mermaid_code.encode('utf-8'), headers=headers)
    
    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"Image saved to {output_file}")
        
        base64_str = base64.b64encode(response.content).decode('utf-8')
        return base64_str
    else:
        print(f"Failed to generate image: {response.status_code}")
        return None

def generate_images():
    mermaid_diagrams = {
        "deployment_options": """
graph TD
    subgraph 部署方案
        D1[本地直接运行]
        D2[Docker部署]
        D3[云服务器部署]
        D4[Kubernetes部署]
    end
    
    D1 --> R1[开发测试]
    D1 --> R2[简单快速]
    
    D2 --> R3[环境隔离]
    D2 --> R4[便于迁移]
    
    D3 --> R5[远程访问]
    D3 --> R6[24/7运行]
    
    D4 --> R7[高可用]
    D4 --> R8[弹性伸缩]
    
    style D1 fill:#C8E6C9
    style D2 fill:#BBDEFB
    style D3 fill:#FFE0B2
    style D4 fill:#E1BEE7
""",
        "optimization_flow": """
graph TD
    A[性能瓶颈] --> B[分析问题]
    B --> C{瓶颈类型}
    
    C -->|模型推理| D1[量化模型]
    C -->|模型推理| D2[切换小模型]
    C -->|模型推理| D3[使用GPU加速]
    
    C -->|向量检索| E1[优化chunk_size]
    C -->|向量检索| E2[使用更优Embedding]
    C -->|向量检索| E3[切换向量数据库]
    
    C -->|整体架构| F1[增加缓存]
    C -->|整体架构| F2[异步处理]
    C -->|整体架构| F3[分布式部署]
    
    D1 --> G[验证效果]
    D2 --> G
    D3 --> G
    E1 --> G
    E2 --> G
    E3 --> G
    F1 --> G
    F2 --> G
    F3 --> G
    
    G --> H[达到目标]
    G -->|未达标| B
    
    style A fill:#FFCDD2
    style B fill:#FFAB91
    style G fill:#C8E6C9
    style H fill:#81C784
""",
        "model_quantization": """
graph TD
    A[原始模型] --> B[FP16精度]
    B --> C[INT8量化]
    C --> D[INT4量化]
    D --> E[GPTQ/AWQ]
    
    B --> R1[精度高]
    B --> R2[速度慢]
    B --> R3[内存占用大]
    
    C --> R4[精度略降]
    C --> R5[速度提升]
    C --> R6[内存减半]
    
    D --> R7[精度下降]
    D --> R8[速度更快]
    D --> R9[内存更小]
    
    E --> R10[无损量化]
    E --> R11[接近原始精度]
    E --> R12[大幅提速]
    
    style B fill:#BBDEFB
    style C fill:#90CAF9
    style D fill:#64B5F6
    style E fill:#42A5F5
""",
        "cache_strategy": """
graph TD
    A[用户请求] --> B{检查缓存}
    
    B -->|命中| C[直接返回]
    B -->|未命中| D[调用RAG链]
    
    D --> E[生成回答]
    E --> F[存入缓存]
    F --> G[返回结果]
    
    subgraph 缓存类型
        H1[问题缓存]
        H2[文档缓存]
        H3[Embedding缓存]
    end
    
    H1 --> B
    H2 --> D
    H3 --> D
    
    style B fill:#FFE0B2
    style C fill:#81C784
    style D fill:#90CAF9
""",
        "production_stack": """
graph TD
    subgraph 生产环境架构
        LB[负载均衡]
        API[FastAPI服务]
        Worker[Worker进程]
        Cache[Redis缓存]
        DB[向量数据库]
        LLM[Ollama服务]
    end
    
    LB --> API
    API --> Worker
    Worker --> Cache
    Worker --> DB
    Worker --> LLM
    
    style LB fill:#F48FB1
    style API fill:#CE93D8
    style Worker fill:#BA68C8
    style Cache fill:#AB47BC
    style DB fill:#8E24AA
    style LLM fill:#6A1B9A
""",
        "monitoring": """
graph TD
    A[监控指标] --> B[CPU使用率]
    A --> C[内存使用率]
    A --> D[GPU使用率]
    A --> E[响应时间]
    A --> F[吞吐量]
    A --> G[错误率]
    
    B --> H[告警阈值]
    C --> H
    D --> H
    E --> H
    F --> H
    G --> H
    
    H --> I[告警通知]
    
    style A fill:#E1BEE7
    style B fill:#CE93D8
    style C fill:#BA68C8
    style D fill:#AB47BC
    style E fill:#8E24AA
    style F fill:#6A1B9A
    style G fill:#4A148C
    style I fill:#FFAB91
"""
    }
    
    base64_images = {}
    for name, code in mermaid_diagrams.items():
        output_file = f"mermaid-img/{name}.png"
        os.makedirs("mermaid-img", exist_ok=True)
        b64 = generate_mermaid_image(code, output_file)
        if b64:
            base64_images[name] = b64
    
    return base64_images

if __name__ == "__main__":
    images = generate_images()
    for name, b64 in images.items():
        print(f"\n{name}:")
        print(f"data:image/png;base64,{b64[:100]}...")
