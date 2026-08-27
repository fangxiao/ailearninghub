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
        return base64.b64encode(response.content).decode('utf-8')
    else:
        print(f"Failed to generate image: {response.status_code}")
        return None

def generate_images():
    mermaid_diagrams = {
        "rag_principle": """
graph TD
    A[用户提问] --> B[问题向量化]
    B --> C[向量检索]
    C --> D[相关文档片段]
    D --> E[构建Prompt]
    E --> F[LLM生成回答]
    F --> G[返回结果]
    
    subgraph 知识库
        K1[文档1]
        K2[文档2]
        K3[文档3]
        K4[向量数据库]
    end
    
    K1 --> K4
    K2 --> K4
    K3 --> K4
    C --> K4
    
    style A fill:#FFF3E0
    style B fill:#FFE0B2
    style C fill:#FFCC80
    style D fill:#FFB74D
    style E fill:#FFA726
    style F fill:#FB8C00
    style G fill:#F57C00
    style K4 fill:#42A5F5
""",
        "rag_vs_llm": """
graph TD
    subgraph 纯LLM回答
        A1[用户提问] --> B1[LLM直接生成]
        B1 --> C1[返回回答]
    end
    
    subgraph RAG回答
        A2[用户提问] --> B2[检索相关文档]
        B2 --> C2[文档+问题构建Prompt]
        C2 --> D2[LLM生成回答]
        D2 --> E2[返回带引用的回答]
    end
    
    B1 --> P1[知识来自模型训练数据]
    P1 --> Q1[可能过时]
    Q1 --> R1[可能不准确]
    
    D2 --> P2[知识来自用户知识库]
    P2 --> Q2[数据最新]
    Q2 --> R2[来源可追溯]
    
    style A1 fill:#FFCDD2
    style B1 fill:#EF9A9A
    style C1 fill:#E57373
    
    style A2 fill:#C8E6C9
    style B2 fill:#81C784
    style C2 fill:#66BB6A
    style D2 fill:#4CAF50
    style E2 fill:#43A047
""",
        "prompt_engineering": """
graph TD
    A[原始Prompt] --> B[添加角色设定]
    B --> C[添加上下文信息]
    C --> D[添加格式要求]
    D --> E[添加引用要求]
    E --> F[最终Prompt]
    
    B --> B1[你是一个专业助手]
    C --> C1[基于以下文档回答]
    D --> D1[使用Markdown格式]
    E --> E1[引用文档来源]
    
    F --> G[LLM]
    G --> H[高质量回答]
    
    style A fill:#E3F2FD
    style B fill:#BBDEFB
    style C fill:#90CAF9
    style D fill:#64B5F6
    style E fill:#42A5F5
    style F fill:#1E88E5
""",
        "qa_interface": """
graph TD
    A[用户输入] --> B[查询预处理]
    B --> C[调用检索器]
    C --> D[获取相关文档]
    D --> E[构建Prompt]
    E --> F[调用LLM]
    F --> G[解析回答]
    G --> H[添加引用标注]
    H --> I[返回结果]
    
    subgraph 错误处理
        B --> B1[格式验证]
        B1 --> B2[空输入检查]
        C --> C1[检索超时]
        F --> F1[LLM调用失败]
    end
    
    style A fill:#E0F2F1
    style B fill:#B2EBF2
    style C fill:#80DEEA
    style D fill:#4DD0E1
    style E fill:#26C6DA
    style F fill:#00BCD4
    style G fill:#00ACC1
    style H fill:#0097A7
    style I fill:#00838F
""",
        "source_citation": """
graph TD
    A[检索结果] --> B[提取文档元数据]
    B --> C[获取文档名称]
    B --> D[获取页码信息]
    B --> E[获取段落位置]
    
    C --> F[构建引用标记]
    D --> F
    E --> F
    
    F --> G[在回答中标注]
    G --> H[格式化为超链接]
    H --> I[用户可点击查看来源]
    
    style A fill:#FFF3E0
    style B fill:#FFE0B2
    style C fill:#FFCC80
    style D fill:#FFB74D
    style E fill:#FFA726
    style F fill:#FB8C00
    style G fill:#F57C00
    style H fill:#EF6C00
    style I fill:#E65100
""",
        "web_architecture": """
graph TD
    subgraph 前端
        F1[HTML页面]
        F2[CSS样式]
        F3[JavaScript交互]
    end
    
    subgraph 后端
        B1[Flask路由]
        B2[API接口]
        B3[业务逻辑]
    end
    
    subgraph 数据层
        D1[向量数据库]
        D2[Ollama服务]
        D3[文件存储]
    end
    
    F1 --> B1
    B1 --> B2
    B2 --> B3
    B3 --> D1
    B3 --> D2
    B3 --> D3
    
    style F1 fill:#CE93D8
    style F2 fill:#BA68C8
    style F3 fill:#AB47BC
    
    style B1 fill:#64B5F6
    style B2 fill:#42A5F5
    style B3 fill:#1E88E5
    
    style D1 fill:#81C784
    style D2 fill:#66BB6A
    style D3 fill:#4CAF50
""",
        "api_design": """
graph TD
    subgraph API接口
        A1[GET /api/health]
        A2[POST /api/chat]
        A3[POST /api/documents]
        A4[GET /api/documents]
        A5[DELETE /api/documents/<id>]
    end
    
    A1 --> R1[健康检查]
    A2 --> R2[问答接口]
    A3 --> R3[上传文档]
    A4 --> R4[获取文档列表]
    A5 --> R5[删除文档]
    
    R2 --> P1[查询参数]
    R2 --> P2[返回结果]
    
    P1 --> Q1[query: 用户问题]
    P1 --> Q2[top_k: 返回数量]
    
    P2 --> Q3[answer: 回答内容]
    P2 --> Q4[sources: 引用来源]
    
    style A1 fill:#C8E6C9
    style A2 fill:#BBDEFB
    style A3 fill:#E3F2FD
    style A4 fill:#FFF3E0
    style A5 fill:#FFEBEE
""",
        "optimization_strategy": """
graph TD
    A[性能瓶颈] --> B[分析阶段]
    B --> C[定位瓶颈类型]
    
    C -->|检索慢| D1[优化Embedding]
    C -->|检索慢| D2[调整chunk_size]
    C -->|检索慢| D3[使用索引]
    
    C -->|生成慢| E1[使用更小模型]
    C -->|生成慢| E2[模型量化]
    C -->|生成慢| E3[减少上下文]
    
    C -->|整体慢| F1[添加缓存]
    C -->|整体慢| F2[异步处理]
    C -->|整体慢| F3[批量处理]
    
    D1 --> G[验证效果]
    D2 --> G
    D3 --> G
    E1 --> G
    E2 --> G
    E3 --> G
    F1 --> G
    F2 --> G
    F3 --> G
    
    G --> H[达标]
    G -->|未达标| B
    
    style A fill:#EF9A9A
    style B fill:#FFAB91
    style G fill:#A5D6A7
    style H fill:#66BB6A
""",
        "embedding_comparison": """
graph TD
    subgraph Embedding模型对比
        M1[all-MiniLM-L6-v2]
        M2[bge-base-zh]
        M3[text2vec-large-chinese]
        M4[gte-base]
    end
    
    M1 --> R1[轻量快速]
    M1 --> R2[英文好]
    M1 --> R3[中文一般]
    
    M2 --> R4[中文优化]
    M2 --> R5[效果好]
    M2 --> R6[速度适中]
    
    M3 --> R7[中文最好]
    M3 --> R8[效果最优]
    M3 --> R9[速度较慢]
    
    M4 --> R10[多语言]
    M4 --> R11[通用好]
    M4 --> R12[平衡选择]
    
    style M1 fill:#BBDEFB
    style M2 fill:#81C784
    style M3 fill:#FFE0B2
    style M4 fill:#CE93D8
""",
        "multimodal": """
graph TD
    subgraph 多模态输入
        I1[PDF文档]
        I2[图片]
        I3[扫描件]
        I4[网页截图]
    end
    
    I1 --> A1[文本提取]
    I1 --> A2[表格提取]
    I1 --> A3[图表描述]
    
    I2 --> B1[图像理解]
    I2 --> B2[OCR识别]
    I2 --> B3[描述生成]
    
    A1 --> C[文本向量化]
    A2 --> C
    A3 --> D[图像向量化]
    B1 --> D
    B2 --> C
    B3 --> D
    
    C --> E[向量数据库]
    D --> E
    
    E --> F[混合检索]
    F --> G[LLM生成回答]
    
    style I1 fill:#E3F2FD
    style I2 fill:#C8E6C9
    style I3 fill:#FFF3E0
    style I4 fill:#F3E5F5
""",
        "multimodal_workflow": """
graph TD
    A[上传多模态文件] --> B[文件类型检测]
    
    B -->|PDF| C1[提取文本和图像]
    B -->|图片| C2[直接处理图像]
    B -->|扫描件| C3[OCR识别]
    
    C1 --> D1[文本分割]
    C1 --> D2[图表理解]
    
    C2 --> D3[图像描述]
    
    C3 --> D4[文本提取]
    
    D1 --> E[文本Embedding]
    D2 --> F[图像Embedding]
    D3 --> F
    D4 --> E
    
    E --> G[向量数据库]
    F --> G
    
    G --> H[混合检索]
    H --> I[LLM生成回答]
    
    style A fill:#E0F2F1
    style B fill:#80DEEA
    style G fill:#42A5F5
    style I fill:#FB8C00
""",
        "production_deployment": """
graph TD
    subgraph 生产环境
        LB[Nginx负载均衡]
        API[Flask应用]
        Worker[Celery异步任务]
        Cache[Redis缓存]
        VecDB[ChromaDB集群]
        LLM[Ollama集群]
        DB[PostgreSQL]
        Monitor[Prometheus+Grafana]
        Log[ELK日志系统]
    end
    
    LB --> API
    API --> Worker
    API --> Cache
    API --> VecDB
    API --> LLM
    API --> DB
    
    Worker --> Cache
    Worker --> VecDB
    Worker --> LLM
    
    Monitor --> API
    Monitor --> Worker
    Monitor --> LLM
    
    Log --> API
    Log --> Worker
    
    style LB fill:#F48FB1
    style API fill:#CE93D8
    style Worker fill:#BA68C8
    style Cache fill:#AB47BC
    style VecDB fill:#8E24AA
    style LLM fill:#6A1B9A
    style DB fill:#4A148C
    style Monitor fill:#311B92
    style Log fill:#1A237E
""",
        "docker_deployment": """
graph TD
    subgraph Docker Compose
        C1[web服务]
        C2[ollama服务]
        C3[redis服务]
        C4[postgres服务]
    end
    
    C1 --> R1[Flask应用]
    C1 --> R2[端口8080]
    
    C2 --> R3[Ollama模型]
    C2 --> R4[端口11434]
    
    C3 --> R5[缓存]
    C3 --> R6[端口6379]
    
    C4 --> R7[元数据存储]
    C4 --> R8[端口5432]
    
    C1 --> C2
    C1 --> C3
    C1 --> C4
    
    style C1 fill:#FFB74D
    style C2 fill:#81C784
    style C3 fill:#64B5F6
    style C4 fill:#CE93D8
""",
        "security": """
graph TD
    subgraph 安全防护
        S1[输入验证]
        S2[权限控制]
        S3[数据加密]
        S4[访问日志]
    end
    
    S1 --> R1[XSS过滤]
    S1 --> R2[SQL注入防护]
    S1 --> R3[输入长度限制]
    
    S2 --> R4[用户认证]
    S2 --> R5[角色授权]
    S2 --> R6[文档权限]
    
    S3 --> R7[传输加密]
    S3 --> R8[存储加密]
    S3 --> R9[敏感数据脱敏]
    
    S4 --> R10[操作日志]
    S4 --> R11[审计追踪]
    S4 --> R12[异常检测]
    
    style S1 fill:#EF9A9A
    style S2 fill:#FFAB91
    style S3 fill:#FFCC80
    style S4 fill:#A5D6A7
""",
        "monitoring": """
graph TD
    subgraph 监控体系
        M1[性能指标]
        M2[业务指标]
        M3[日志管理]
        M4[告警系统]
    end
    
    M1 --> R1[CPU/内存]
    M1 --> R2[响应时间]
    M1 --> R3[吞吐量]
    
    M2 --> R4[问答成功率]
    M2 --> R5[用户满意度]
    M2 --> R6[文档覆盖率]
    
    M3 --> R7[错误日志]
    M3 --> R8[访问日志]
    M3 --> R9[性能日志]
    
    M4 --> R10[阈值告警]
    M4 --> R11[异常检测]
    M4 --> R12[通知渠道]
    
    style M1 fill:#CE93D8
    style M2 fill:#64B5F6
    style M3 fill:#81C784
    style M4 fill:#FFB74D
""",
        "series_overview": """
graph TD
    subgraph 第一阶段：环境准备
        S1[01-入门]
        S2[02-环境搭建]
        S3[03-工具链整合]
    end
    
    subgraph 第二阶段：知识库构建
        S4[04-文档处理]
        S5[05-向量数据库]
        S6[06-Embedding]
    end
    
    subgraph 第三阶段：RAG核心
        S7[07-RAG原理]
        S8[08-问答接口]
        S9[09-Web界面]
    end
    
    subgraph 第四阶段：优化部署
        S10[10-性能优化]
        S11[11-多模态]
        S12[12-生产部署]
    end
    
    S1 --> A
    S2 --> A
    S3 --> A
    A --> B
    S4 --> B
    S5 --> B
    S6 --> B
    B --> C
    S7 --> C
    S8 --> C
    S9 --> C
    C --> D
    S10 --> D
    S11 --> D
    S12 --> D
    
    A[入门完成]
    B[进阶完成]
    C[高级完成]
    D[部署完成]
    
    style S1 fill:#81C784
    style S2 fill:#81C784
    style S3 fill:#81C784
    style S4 fill:#66BB6A
    style S5 fill:#66BB6A
    style S6 fill:#66BB6A
    style S7 fill:#4CAF50
    style S8 fill:#4CAF50
    style S9 fill:#4CAF50
    style S10 fill:#2E7D32
    style S11 fill:#2E7D32
    style S12 fill:#2E7D32
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
        print(f"data:image/png;base64,{b64[:80]}...")
