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
        "use_cases": """
graph TD
    subgraph 应用场景
        U1[企业知识库]
        U2[个人知识管理]
        U3[教育辅助]
        U4[文档分析]
        U5[客服助手]
        U6[代码助手]
    end
    
    U1 --> R1[内部文档问答]
    U1 --> R2[员工培训]
    
    U2 --> R3[读书笔记]
    U2 --> R4[知识整理]
    
    U3 --> R5[智能辅导]
    U3 --> R6[作业批改]
    
    U4 --> R7[合同分析]
    U4 --> R8[报告生成]
    
    U5 --> R9[常见问题]
    U5 --> R10[自动回复]
    
    U6 --> R11[代码解释]
    U6 --> R12[Bug修复]
    
    style U1 fill:#EF9A9A
    style U2 fill:#CE93D8
    style U3 fill:#90CAF9
    style U4 fill:#81C784
    style U5 fill:#FFE082
    style U6 fill:#FFAB91
""",
        "best_practices": """
graph TD
    A[最佳实践] --> B[文档质量]
    A --> C[模型选择]
    A --> D[检索优化]
    A --> E[安全防护]
    A --> F[用户体验]
    
    B --> B1[格式标准化]
    B --> B2[内容精炼]
    B --> B3[定期更新]
    
    C --> C1[根据场景选择]
    C --> C2[中文选Qwen]
    C --> C3[英文选Llama]
    
    D --> D1[合理chunk_size]
    D --> D2[多种检索策略]
    D --> D3[结果重排序]
    
    E --> E1[输入过滤]
    E --> E2[敏感信息检测]
    E --> E3[权限控制]
    
    F --> F1[清晰的提示]
    F --> F2[友好的界面]
    F --> F3[快速的响应]
    
    style B fill:#C8E6C9
    style C fill:#BBDEFB
    style D fill:#E3F2FD
    style E fill:#FFEBEE
    style F fill:#FFF3E0
""",
        "enterprise_deployment": """
graph TD
    subgraph 企业级部署
        LB[负载均衡]
        API[API网关]
        Auth[认证中心]
        Cache[Redis集群]
        VecDB[Milvus集群]
        LLM[模型集群]
        Monitor[监控系统]
        Log[日志系统]
    end
    
    LB --> API
    API --> Auth
    API --> Cache
    API --> VecDB
    API --> LLM
    Monitor --> LB
    Monitor --> API
    Monitor --> LLM
    Log --> API
    Log --> LLM
    
    style LB fill:#F48FB1
    style API fill:#CE93D8
    style Auth fill:#BA68C8
    style Cache fill:#AB47BC
    style VecDB fill:#8E24AA
    style LLM fill:#6A1B9A
    style Monitor fill:#4A148C
    style Log fill:#311B92
""",
        "knowledge_curation": """
graph TD
    A[知识管理流程] --> B[收集]
    B --> C[整理]
    C --> D[标注]
    D --> E[审核]
    E --> F[入库]
    F --> G[更新]
    
    B --> B1[文档导入]
    B --> B2[网页抓取]
    B --> B3[手动输入]
    
    C --> C1[格式转换]
    C --> C2[内容提取]
    C --> C3[去重]
    
    D --> D1[关键词标注]
    D --> D2[分类标签]
    D --> D3[质量评分]
    
    E --> E1[人工审核]
    E --> E2[自动检查]
    E --> E3[反馈修正]
    
    G --> G1[定期更新]
    G --> G2[版本管理]
    G --> G3[知识淘汰]
    
    style A fill:#E1BEE7
    style B fill:#CE93D8
    style C fill:#BA68C8
    style D fill:#AB47BC
    style E fill:#8E24AA
    style F fill:#6A1B9A
    style G fill:#4A148C
""",
        "future_trends": """
graph TD
    A[未来趋势] --> B[多模态RAG]
    A --> C[Agent化]
    A --> D[边缘部署]
    A --> E[联邦学习]
    A --> F[持续学习]
    
    B --> B1[图文检索]
    B --> B2[视频理解]
    B --> B3[语音问答]
    
    C --> C1[自动规划]
    C --> C2[工具调用]
    C --> C3[多Agent协作]
    
    D --> D1[手机端]
    D --> D2[IoT设备]
    D --> D3[离线运行]
    
    E --> E1[数据隐私]
    E --> E2[协同训练]
    E --> E3[模型共享]
    
    F --> F1[增量学习]
    F --> F2[自适应优化]
    F --> F3[知识进化]
    
    style B fill:#C8E6C9
    style C fill:#BBDEFB
    style D fill:#FFE0B2
    style E fill:#E1BEE7
    style F fill:#FFCDD2
""",
        "series_summary": """
graph TD
    S1[第01篇] --> T1[为什么需要本地知识库]
    S2[第02篇] --> T2[搭建Ollama环境]
    S3[第03篇] --> T3[构建本地知识库]
    S4[第04篇] --> T4[打造智能问答界面]
    S5[第05篇] --> T5[部署与性能优化]
    S6[第06篇] --> T6[应用场景与最佳实践]
    
    T1 --> U[完整系统]
    T2 --> U
    T3 --> U
    T4 --> U
    T5 --> U
    T6 --> U
    
    style S1 fill:#81C784
    style S2 fill:#66BB6A
    style S3 fill:#4CAF50
    style S4 fill:#43A047
    style S5 fill:#388E3C
    style S6 fill:#2E7D32
    style U fill:#FFE0B2
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
