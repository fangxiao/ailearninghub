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
        "installation_flow": """
graph TD
    A[安装Ollama] --> B[拉取大模型]
    B --> C[命令行测试]
    C --> D[成功运行]
    
    subgraph 不同平台
        A1[macOS]
        A2[Linux]
        A3[Windows]
    end
    
    A --> A1
    A --> A2
    A --> A3
""",
        "model_comparison": """
graph TD
    subgraph 模型选择
        M1[Llama3-8B]
        M2[Qwen-7B]
        M3[DeepSeek-7B]
    end
    
    M1 --> R1[通用能力强]
    M1 --> R2[英文出色]
    
    M2 --> R3[中文优秀]
    M2 --> R4[开源免费]
    
    M3 --> R5[代码能力强]
    M3 --> R6[数学推理]
    
    style M1 fill:#90EE90
    style M2 fill:#87CEEB
    style M3 fill:#FFB6C1
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