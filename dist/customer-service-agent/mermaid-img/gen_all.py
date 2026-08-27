import subprocess, os, base64, re

OUT = '/Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/mermaid-img/generated'
os.makedirs(OUT, exist_ok=True)

def gen(name, mmd_text):
    path = os.path.join(OUT, name)
    with open('/tmp/cur.mmd', 'w') as f:
        f.write(mmd_text)
    subprocess.run(['curl', '-s', '-X', 'POST', '-H', 'Content-Type: text/plain',
                    '--data-binary', '@/tmp/cur.mmd', '-o', path,
                    'https://kroki.io/mermaid/png'])
    sz = os.path.getsize(path)
    print(f"{name}: {sz} bytes")
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

# === 第7篇：订单查询插件 ===
gen('a7-1-order-flow.png', r'''flowchart TD
    A[用户: 我的订单到哪了?] --> B{意图识别}
    B -->|订单查询| C[订单查询插件]
    C --> D{是否有订单号?}
    D -->|无| E[询问订单号/手机号]
    E --> F[用户提供信息]
    F --> G[数据库查询]
    D -->|有| G
    G --> H[返回订单信息]
    H --> I[大模型组织语言]
    I --> J[回复用户]
''')

gen('a7-2-order-plugin.png', r'''flowchart LR
    subgraph 输入
        U[用户查询]
    end
    subgraph 插件核心
        P[OrderQueryPlugin]
    end
    subgraph 数据源
        DB[(订单数据库)]
        API[订单API]
    end
    subgraph 输出
        R[订单详情]
    end
    U --> P
    P -->|SQL查询| DB
    P -->|HTTP调用| API
    DB --> R
    API --> R
''')

# === 第8篇：多轮对话进阶 ===
gen('a8-1-slot-filling.png', r'''flowchart TD
    A[用户: 我想订花] --> B{意图: 订花}
    B --> C{槽位检查}
    C -->|缺少花型| D[询问: 您要什么花?]
    D --> E[用户: 玫瑰]
    E --> C
    C -->|缺少数量| F[询问: 要多少朵?]
    F --> G[用户: 99朵]
    G --> C
    C -->|缺少配送地址| H[询问: 送到哪里?]
    H --> I[用户提供地址]
    I --> C
    C -->|信息齐全| J[提交订单]
''')

gen('a8-2-context-window.png', r'''flowchart LR
    subgraph 对话历史
        H1[消息1]
        H2[消息2]
        H3[消息3]
        H4[消息4]
    end
    subgraph 滑动窗口
        W1[最近N条]
        W2[关键信息]
    end
    H3 & H4 --> W1
    H1 & H2 -- 提取 --> W2
    W1 & W2 --> LLM[大模型]
''')

# === 第9篇：知识库增强 ===
gen('a9-1-vector-rag.png', r'''flowchart TD
    Q[用户问题] --> E[Embedding模型]
    E --> VQ[向量查询]
    VQ --> DB[(向量数据库)]
    DB --> TopK[Top-K相似文档]
    TopK --> LLM[大模型]
    Q --> LLM
    LLM --> A[生成答案]
    subgraph 离线入库
        Doc[文档数据] --> E2[Embedding]
        E2 --> DB
    end
''')

gen('a9-2-vs-keyword.png', r'''flowchart LR
    subgraph 关键词检索
        K1[精确匹配]
        K2[速度快]
        K3[同义词差]
    end
    subgraph 向量检索
        V1[语义匹配]
        V2[理解深]
        V3[计算重]
    end
    subgraph 混合方案
        M1[关键词快速分流]
        M2[向量深度检索]
    end
    K1 --> M1
    V1 --> M2
''')

# === 第10篇：Function Calling ===
gen('a10-1-function-calling.png', r'''flowchart TD
    U[用户: 查一下我的余额] --> LLM[大模型]
    LLM -->|决定调用函数| FC[Function Calling]
    FC -->|generate_function_call| C[调用get_balance]
    C --> R[返回余额数据]
    R --> LLM
    LLM -->|自然语言组织| A[您的余额是100元]
''')

gen('a10-2-tools.png', r'''flowchart TD
    subgraph 可用工具
        T1[get_weather]
        T2[get_order_status]
        T3[transfer_money]
        T4[search_product]
    end
    subgraph LLM决策
        L[分析用户意图]
    end
    subgraph 执行
        E[调用工具]
    end
    subgraph 返回
        R[结果→自然语言]
    end
    L --> E
    E --> R
    T1 & T2 & T3 & T4 -.-> L
''')

# === 第11篇：多Agent协作 ===
gen('a11-1-router.png', r'''flowchart TD
    U[用户请求] --> R[路由Agent]
    R -->|闲聊| A1[闲聊Agent]
    R -->|订单| A2[订单Agent]
    R -->|投诉| A3[投诉Agent]
    R -->|咨询| A4[咨询Agent]
    A1 & A2 & A3 & A4 --> RESP[统一回复]
''')

gen('a11-2-handoff.png', r'''flowchart LR
    subgraph 前台
        F1[一线Agent]
        F2[二线Agent]
    end
    subgraph 后台
        B1[专家Agent]
        B2[数据库Agent]
    end
    U[用户] --> F1
    F1 -->|复杂问题| F2
    F2 -->|专业咨询| B1
    F2 -->|数据查询| B2
    B1 & B2 --> F2
    F2 --> F1
    F1 --> U
''')

# === 第12篇：记忆与个性化 ===
gen('a12-1-memory.png', r'''flowchart TD
    subgraph 短期记忆
        S[当前会话]
    end
    subgraph 长期记忆
        L[用户画像]
        H[历史偏好]
    end
    subgraph 个性化响应
        R[推荐内容]
    end
    U[用户] --> S
    S -->|提取信息| L
    S -->|提取偏好| H
    L & H --> R
    S & L & H --> P[个性化Prompt]
    P --> B[Bot回复]
''')

gen('a12-2-profile.png', r'''flowchart TD
    subgraph 用户画像
        P1[基本信息]
        P2[兴趣偏好]
        P3[历史行为]
        P4[情感特征]
    end
    subgraph 应用
        A1[个性化问候]
        A2[智能推荐]
        A3[语气调整]
        A4[服务升级]
    end
    P1 & P2 & P3 & P4 --> A1 & A2 & A3 & A4
''')

# === 第13篇：效果评估 ===
gen('a13-1-metrics.png', r'''flowchart TD
    subgraph 核心指标
        M1[意图识别准确率]
        M2[问题解决率]
        M3[平均响应时长]
        M4[转人工率]
        M5[用户满意度]
    end
    subgraph 数据源
        L1[对话日志]
        L2[用户反馈]
        L3[工单数据]
    end
    L1 & L2 & L3 --> M1 & M2 & M3 & M4 & M5
''')

gen('a13-2-optimize-loop.png', r'''flowchart TD
    A[数据采集] --> B[效果分析]
    B --> C[问题定位]
    C --> D[策略优化]
    D --> E[AB测试]
    E --> F[全量上线]
    F --> A
''')

# === 第14篇：架构总结 ===
gen('a14-1-architecture.png', r'''flowchart TB
    subgraph 接入层
        W[Web/APP]
        API[API网关]
    end
    subgraph Agent层
        R[路由调度]
        A1[对话Agent]
        A2[订单Agent]
        A3[情感Agent]
    end
    subgraph 能力层
        P1[插件系统]
        P2[工具调用]
        P3[记忆系统]
    end
    subgraph 数据层
        DB1[(MySQL)]
        DB2[(向量库)]
        DB3[(Redis)]
    end
    W --> API --> R
    R --> A1 & A2 & A3
    A1 & A2 & A3 --> P1 & P2 & P3
    P1 & P2 & P3 --> DB1 & DB2 & DB3
''')

gen('a14-2-roadmap.png', r'''flowchart LR
    S1[基础能力<br/>意图/知识库] --> S2[感知能力<br/>情感/对话]
    S2 --> S3[执行能力<br/>工具/多Agent]
    S3 --> S4[智能能力<br/>记忆/学习]
    S4 --> S5[生产部署<br/>监控/优化]
''')

print("\nAll diagrams generated!")
