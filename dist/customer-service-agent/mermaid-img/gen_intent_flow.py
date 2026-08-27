#!/usr/bin/env python3
import base64
import subprocess
import os

base_dir = '/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/mermaid-img'

# 生成意图识别流程图
mermaid_code = '''
graph TB
    UserInput[用户输入] --> KeywordMatch[关键词快速匹配]
    
    KeywordMatch --> MatchSuccess{匹配成功?}
    
    MatchSuccess -->|Yes| ReturnIntent[返回意图]
    MatchSuccess -->|No| LLMRecognize[大模型识别]
    
    LLMRecognize --> ReturnIntent
    
    ReturnIntent --> BotProcess[Bot根据意图分流处理]
    
    subgraph Intents[意图类型]
        FAQ[faq_query<br/>FAQ查询]
        Order[order_query<br/>订单查询]
        Complaint[complaint<br/>投诉]
        Handoff[human_handoff<br/>转人工]
        Unknown[unknown<br/>未识别]
    end
    
    BotProcess --> FAQ
    BotProcess --> Order
    BotProcess --> Complaint
    BotProcess --> Handoff
    BotProcess --> Unknown
    
    FAQ --> FAQHandler[知识库检索]
    Order --> OrderHandler[订单查询接口]
    Complaint --> ComplaintHandler[立即转人工]
    Handoff --> HandoffHandler[转人工]
    Unknown --> LLMHandler[大模型处理]
    
    style UserInput fill:#fce4ec,stroke:#e91e63
    style KeywordMatch fill:#fff9c4,stroke:#fbc02d
    style LLMRecognize fill:#e3f2fd,stroke:#2196f3
    style BotProcess fill:#f3e5f5,stroke:#9c27b0
    style MatchSuccess fill:#e0e0e0,stroke:#9e9e9e
'''

# 保存mermaid文件
with open(f'{base_dir}/intent_flow.mmd', 'w', encoding='utf-8') as f:
    f.write(mermaid_code)

# 生成PNG
result = subprocess.run([
    '/opt/homebrew/bin/mmdc',
    '-i', f'{base_dir}/intent_flow.mmd',
    '-o', f'{base_dir}/intent_flow.png',
    '-b', 'white',
    '-w', '800',
    '-H', '600'
], capture_output=True, text=True)

print(f"mmdc output: {result.stdout}")
print(f"mmdc error: {result.stderr}")

# 检查是否成功
if os.path.exists(f'{base_dir}/intent_flow.png'):
    print("PNG生成成功")
    # 转换为base64
    with open(f'{base_dir}/intent_flow.png', 'rb') as f:
        img_data = f.read()
    base64_str = base64.b64encode(img_data).decode('utf-8')
    
    # 保存base64
    with open(f'{base_dir}/intent_flow.b64', 'w', encoding='utf-8') as f:
        f.write(f"data:image/png;base64,{base64_str}")
    
    print(f"Base64长度: {len(base64_str)} bytes")
else:
    print("PNG生成失败")