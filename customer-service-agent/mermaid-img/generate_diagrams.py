import subprocess
import base64
import os
import time

def generate_mermaid_image(mermaid_code, output_file):
    with open('temp.mmd', 'w', encoding='utf-8') as f:
        f.write(mermaid_code)
    
    result = subprocess.run([
        '/opt/homebrew/bin/mmdc',
        '-i', 'temp.mmd',
        '-o', output_file,
        '-b', 'white',
        '-w', '600',
        '-H', '400'
    ], capture_output=True, text=True)
    
    print(f"mmdc output: {result.stdout}")
    print(f"mmdc error: {result.stderr}")
    
    time.sleep(1)
    
    if not os.path.exists(output_file):
        print(f"Error: {output_file} not created")
        os.remove('temp.mmd')
        return None
    
    with open(output_file, 'rb') as f:
        img_data = f.read()
    
    base64_str = base64.b64encode(img_data).decode('utf-8')
    
    os.remove('temp.mmd')
    os.remove(output_file)
    
    return base64_str

diagrams = {
    'system_prompt_flow': '''
graph TB
    S[System Prompt<br/>角色设定] --> C[对话上下文]
    U[用户输入] --> C
    C --> LLM[大模型]
    LLM --> R[响应输出]
    
    style S fill:#fff3e0,stroke:#ff9800
    style LLM fill:#e3f2fd,stroke:#2196f3
    style R fill:#e8f5e9,stroke:#4caf50
    style U fill:#fce4ec,stroke:#e91e63
    style C fill:#f5f5f5,stroke:#9e9e9e
''',
    
    'bot_init_flow': '''
graph TB
    Start[创建Bot实例] --> LoadConfig[加载配置文件<br/>customer_service.yaml]
    LoadConfig --> LoadPrompt[加载System Prompt<br/>system_prompt.md]
    LoadPrompt --> InitComplete[初始化完成]
    
    LoadConfig --> ConfigData[配置数据<br/>LLM provider, model等]
    LoadPrompt --> PromptData[Prompt内容<br/>角色定义、能力等]
    
    ConfigData --> Store[存储到self.config]
    PromptData --> Store2[存储到self.system_prompt]
    
    Store --> InitComplete
    Store2 --> InitComplete
    
    style Start fill:#e1f5fe,stroke:#0288d1
    style InitComplete fill:#c8e6c9,stroke:#388e3c
    style LoadConfig fill:#fff9c4,stroke:#fbc02d
    style LoadPrompt fill:#fff9c4,stroke:#fbc02d
''',
    
    'chat_flow': '''
graph TB
    UserInput[用户输入] --> BuildMsg[构建消息列表]
    
    subgraph Messages[消息结构]
        M1[System Message<br/>角色设定]
        M2[History<br/>历史对话]
        M3[User Message<br/>当前问题]
    end
    
    BuildMsg --> M1
    BuildMsg --> M2
    BuildMsg --> M3
    
    M1 --> CallLLM[调用大模型API]
    M2 --> CallLLM
    M3 --> CallLLM
    
    CallLLM --> Response[获取响应]
    Response --> Return[返回给用户]
    
    style UserInput fill:#fce4ec,stroke:#e91e63
    style CallLLM fill:#e3f2fd,stroke:#2196f3
    style Response fill:#e8f5e9,stroke:#4caf50
    style Return fill:#c8e6c9,stroke:#388e3c
'''
}

base64_images = {}
for name, code in diagrams.items():
    print(f"\nGenerating {name}...")
    result = generate_mermaid_image(code, f'{name}.png')
    if result:
        base64_images[name] = result
        print(f"Done: {len(result)} bytes")
    else:
        print(f"Failed to generate {name}")

with open('images_base64.txt', 'w', encoding='utf-8') as f:
    for name, b64 in base64_images.items():
        f.write(f"\n=== {name} ===\n")
        f.write(f"data:image/png;base64,{b64}\n")

print("\nAll images generated and saved to images_base64.txt")