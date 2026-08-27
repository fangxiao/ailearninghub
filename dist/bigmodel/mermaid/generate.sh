#!/bin/bash

MMD_FILE="/Users/admin/project/lovely/platform/doc/prototype/myagent/mermaid"
OUT_FILE="/Users/admin/project/lovely/platform/doc/prototype/myagent/mermaid"

# 图1: RNN串行处理
MMD1='graph LR
    A["输入: 你好"] --> B["字1: 你"]
    B --> C["字2: 好"]
    C --> D["字3: 啊"]
    D --> E["字4: ？"]
    style A fill:#e1f5fe
    style E fill:#fff3e0'

# 图2: Self-Attention
MMD2='graph TD
    subgraph 输入["输入层"]
        W1["字1: 小明"]
        W2["字2: 喜欢"]
        W3["字3: 小红"]
    end
    W1 & W2 & W3 --> Q["Query/Key/Value生成"]
    Q --> AS["注意力分数矩阵"]
    AS --> O1["小明的新表示"]
    AS --> O2["喜欢的新表示"]
    AS --> O3["小红的新表示"]
    style Q fill:#e8f5e9
    style AS fill:#fff3e0'

# 图3: GPT生成过程
MMD3='flowchart LR
    A["输入: 你好"] --> B["Transformer"]
    B --> C["字1: 啊"]
    C --> D["字2: ？"]
    D --> E["...生成中"]
    E --> F["结束符"]
    B1["历史上下文"] --> B
    B2["记忆信息"] --> B
    style A fill:#e1f5fe
    style F fill:#ffecb3'

encode_and_fetch() {
    local mmd="$1"
    local output="$2"
    local encoded=$(echo "$mmd" | base64 | tr -d '\n')
    curl -s -o "$output" "https://mermaid.ink/img/$encoded"
    echo "Generated: $output"
}

encode_and_fetch "$MMD1" "$OUT_FILE/01-rnn-process.png"
encode_and_fetch "$MMD2" "$OUT_FILE/02-self-attention.png"
encode_and_fetch "$MMD3" "$OUT_FILE/03-gpt-generate.png"
