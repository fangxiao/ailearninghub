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
        "ui_framework": """
graph TD
    subgraph UI框架对比
        G1[Gradio]
        G2[Streamlit]
        G3[Chainlit]
    end
    
    G1 --> R1[简单易用]
    G1 --> R2[快速原型]
    G1 --> R3[适合演示]
    
    G2 --> R4[数据驱动]
    G2 --> R5[丰富组件]
    G2 --> R6[适合数据分析]
    
    G3 --> R7[专为LLM设计]
    G3 --> R8[聊天界面]
    G3 --> R9[文档展示]
    
    style G1 fill:#F87171
    style G2 fill:#60A5FA
    style G3 fill:#34D399
""",
        "chat_interface": """
graph TD
    A[用户输入] --> B[输入框组件]
    B --> C[发送按钮]
    C --> D[后端API]
    D --> E[加载状态]
    E --> F[流式输出]
    F --> G[消息气泡]
    G --> H[参考文档]
    H --> I[结束]
    
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
        "streaming_process": """
sequenceDiagram
    participant User as 用户
    participant UI as 界面
    participant API as 后端API
    participant LLM as 大模型
    
    User->>UI: 输入问题
    UI->>API: POST /api/chat
    API->>LLM: 生成回答（流式）
    LLM-->>API: token1
    API-->>UI: chunk(token1)
    UI->>User: 显示token1
    LLM-->>API: token2
    API-->>UI: chunk(token2)
    UI->>User: 显示token2
    ...
    LLM-->>API: done
    API-->>UI: done
    UI->>User: 显示完成
""",
        "app_structure": """
graph TD
    A[app.py] --> B[导入依赖]
    A --> C[初始化组件]
    A --> D[定义回调函数]
    A --> E[构建界面]
    A --> F[启动服务]
    
    B --> B1[gradio/streamlit]
    B --> B2[langchain]
    B --> B3[ollama]
    
    D --> D1[处理输入]
    D --> D2[调用RAG链]
    D --> D3[返回结果]
    
    E --> E1[聊天窗口]
    E --> E2[文件上传]
    E --> E3[参数设置]
    
    style A fill:#FFE0B2
    style B fill:#FFCC80
    style C fill:#FFB74D
    style D fill:#FFA726
    style E fill:#FB8C00
    style F fill:#F57C00
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
