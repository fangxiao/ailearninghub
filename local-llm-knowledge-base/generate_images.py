import base64
import requests

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
        "rag_flow": """
graph TD
    A[用户提问] --> B[检索相关文档]
    B --> C[生成回答]
    C --> D[返回答案]
    
    subgraph 知识库
        E[文档1]
        F[文档2]
        G[文档3]
    end
    
    B --> E
    B --> F
    B --> G
    C --> B
""",
        "local_vs_cloud": """
graph TD
    subgraph 本地部署
        A1[数据存储] --> A2[本地服务器]
        A3[大模型] --> A4[本地运行]
        A5[安全] --> A6[完全自主]
    end
    
    subgraph 云端服务
        B1[数据上传] --> B2[第三方服务器]
        B3[大模型] --> B4[云端运行]
        B5[安全] --> B6[依赖服务商]
    end
    
    style A1 fill:#90EE90
    style A3 fill:#90EE90
    style A5 fill:#90EE90
    style B1 fill:#FFB6C1
    style B3 fill:#FFB6C1
    style B5 fill:#FFB6C1
"""
    }
    
    base64_images = {}
    for name, code in mermaid_diagrams.items():
        output_file = f"mermaid-img/{name}.png"
        import os
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