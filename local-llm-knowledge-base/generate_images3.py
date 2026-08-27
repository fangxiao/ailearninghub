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
        "rag_pipeline": """
graph TD
    A[原始文档] --> B[文档加载]
    B --> C[文本分割]
    C --> D[向量化]
    D --> E[存入向量数据库]
    E --> F[用户提问]
    F --> G[问题向量化]
    G --> H[向量检索]
    H --> I[相关文档]
    I --> J[LLM生成回答]
    J --> K[最终答案]
    
    style A fill:#E3F2FD
    style B fill:#BBDEFB
    style C fill:#90CAF9
    style D fill:#64B5F6
    style E fill:#42A5F5
    style F fill:#FFF3E0
    style G fill:#FFE0B2
    style H fill:#FFCC80
    style I fill:#FFB74D
    style J fill:#FFA726
    style K fill:#FB8C00
""",
        "knowledge_base_structure": """
graph TD
    subgraph 知识库架构
        A[文档层]
        B[向量层]
        C[检索层]
        D[应用层]
    end
    
    A --> A1[PDF/Word]
    A --> A2[Markdown]
    A --> A3[网页]
    
    B --> B1[Embedding模型]
    B --> B2[向量数据库]
    
    C --> C1[语义检索]
    C --> C2[关键词检索]
    
    D --> D1[问答系统]
    D --> D2[智能助手]
    D --> D3[文档分析]
    
    A --> B
    B --> C
    C --> D
    
    style A fill:#81C784
    style B fill:#66BB6A
    style C fill:#4CAF50
    style D fill:#43A047
""",
        "embedding_process": """
graph LR
    A[文本] --> B[Tokenization]
    B --> C[Embedding模型]
    C --> D[向量表示]
    D --> E[存储/检索]
    
    subgraph 向量空间
        F[语义相似的文本]
        G[语义不同的文本]
    end
    
    D --> F
    D --> G
    
    style F fill:#C8E6C9
    style G fill:#FFCDD2
""",
        "document_splitting": """
graph TD
    A[长篇文档] --> B[按字符数分割]
    A --> C[按段落分割]
    A --> D[按章节分割]
    
    B --> E[固定长度块]
    C --> F[自然段落块]
    D --> G[逻辑章节块]
    
    E --> H[可能截断语义]
    F --> I[保持语义完整]
    G --> J[保持逻辑完整]
    
    style B fill:#FFE0B2
    style C fill:#C8E6C9
    style D fill:#BBDEFB
    
    style I fill:#A5D6A7
    style J fill:#90CAF9
""",
        "vector_db_comparison": """
graph TD
    subgraph 向量数据库对比
        V1[Chroma]
        V2[FAISS]
        V3[Milvus]
        V4[Pinecone]
    end
    
    V1 --> R1[轻量级]
    V1 --> R2[无需部署]
    V1 --> R3[适合开发测试]
    
    V2 --> R4[Facebook出品]
    V2 --> R5[速度快]
    V2 --> R6[内存占用高]
    
    V3 --> R7[分布式]
    V3 --> R8[企业级]
    V3 --> R9[部署复杂]
    
    V4 --> R10[云端服务]
    V4 --> R11[托管式]
    V4 --> R12[需要付费]
    
    style V1 fill:#AED581
    style V2 fill:#FFF9C4
    style V3 fill:#FFCDD2
    style V4 fill:#E1BEE7
""",
        "full_workflow": """
sequenceDiagram
    participant User as 用户
    participant App as 应用程序
    participant VecDB as 向量数据库
    participant LLM as 本地大模型
    
    User->>App: 提问
    App->>LLM: 生成问题向量
    App->>VecDB: 检索相关文档
    VecDB-->>App: 返回相关文档片段
    App->>LLM: 结合文档生成回答
    LLM-->>App: 返回回答
    App-->>User: 显示答案
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
