# 上下文管理：AI 如何记住你的代码

阅读时间：30分钟
难度等级：⭐⭐⭐⭐ 进阶
你将收获：理解 AI 的记忆机制，掌握上下文管理技巧

<br/>

***

<br/>

## 回顾：你已经掌握了什么？

**前面学过的：**

- ✅ 代码补全原理（AI 如何预测）
- ✅ 注意力机制（AI 如何关注重点）
- ✅ 上下文窗口（AI 能看到多远）

**但有一个问题：**

AI 的记忆有限，如何记住你的整个项目？

**这一篇将教你：** AI 如何管理上下文，以及如何让它"记住"更多

<br/>

***

<br/>

## 开篇：AI 的记忆困境

**场景：大型项目开发**

```python
# 文件1：models/user.py（第1-100行）
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

# 文件2：services/order.py（第200-300行）
class OrderService:
    def create_order(self, user_id, items):
        # AI 能看到 User 类吗？
```

**问题：**

- 文件1 在第1-100行
- 文件2 在第200-300行
- AI 的上下文窗口有限，可能看不到文件1

**如何解决？** 这就是上下文管理要解决的问题

<br/>

***

<br/>

## 一、上下文管理的挑战

### 1.1 上下文窗口限制

**每个模型的窗口大小：**

| 模型 | 上下文窗口 | 实际容量 |
|------|-----------|---------|
| GPT-3.5 | 4K tokens | ~3000字（1-2个文件） |
| GPT-4 | 8K-32K | ~6000-24000字（3-8个文件） |
| Claude 3 | 200K | ~150000字（50-100个文件） |
| GLM-4 | 128K | ~96000字（30-60个文件） |

**实际情况：**

一个中等项目：

```
my_project/
├── models/       (5个文件，2000行)
├── services/     (8个文件，3000行)
├── controllers/  (6个文件，2000行)
├── utils/        (10个文件，1500行)
└── tests/        (15个文件，3000行)

总计：44个文件，11500行代码
```

**问题：** 上下文窗口装不下所有代码

<br/>

### 1.2 相关性选择问题

**核心挑战：** 哪些代码是相关的？

**示例：**

```python
# 当前编辑：services/order.py
def create_order(user_id, items):
    user = User.query.get(user_id)  # 需要 User 类
    total = calculate_total(items)  # 需要 calculate_total 函数
    order = Order(user=user, items=items)  # 需要 Order 类
    db.session.add(order)  # 需要 db 对象
    return order
```

**需要的上下文：**

- models/user.py（User 类）
- utils/calculations.py（calculate_total 函数）
- models/order.py（Order 类）
- db.py（数据库实例）

**AI 如何找到这些文件？**

<br/>

***

<br/>

## 二、向量数据库：AI 的"图书馆"

### 2.1 什么是向量数据库？

**核心概念：**

将代码转换为向量（数字列表），然后通过向量相似度找到相关代码。

**示例：**

```python
# 代码片段
def calculate_discount(price, level):
    return price * 0.9

# 转换为向量（简化示例）
vector = [0.2, 0.8, 0.3, 0.9, 0.1, ...]
```

**相似度计算：**

```python
# 片段1
"计算折扣" → [0.8, 0.2, 0.9, ...]

# 片段2
"计算价格优惠" → [0.7, 0.3, 0.85, ...]

# 相似度：0.92（很相似）
```

<br/>

### 2.2 向量化的过程

**完整流程：**

第1步：代码分块

```python
# 原始文件：utils.py（500行）

# 分块后：
chunk_1 = "def calculate_discount(price, level):\n    ..."  # 1-50行
chunk_2 = "def calculate_total(items):\n    ..."  # 51-100行
chunk_3 = "class OrderProcessor:\n    ..."  # 101-200行
```

第2步：生成向量

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

# 每个代码块生成一个向量
vector_1 = model.encode(chunk_1)  # [0.2, 0.8, 0.3, ...]
vector_2 = model.encode(chunk_2)  # [0.1, 0.9, 0.4, ...]
vector_3 = model.encode(chunk_3)  # [0.3, 0.7, 0.2, ...]
```

第3步：存储到向量数据库

```python
import faiss

# 创建索引
index = faiss.IndexFlatL2(384)  # 384维向量

# 添加向量
index.add(np.array([vector_1, vector_2, vector_3]))
```

第4步：查询相关代码

```python
# 当前查询："创建订单需要什么？"
query = "create order user items"
query_vector = model.encode(query)

# 搜索最相似的代码块
distances, indices = index.search(np.array([query_vector]), k=5)

# 结果：返回最相关的5个代码块
```

<br/>

### 2.3 主流向量数据库

**对比表格：**

| 数据库 | 特点 | 适用场景 |
|--------|------|---------|
| **FAISS** | Facebook开源，快速 | 本地开发、中小项目 |
| **Pinecone** | 云服务，易用 | 生产环境、团队协作 |
| **Weaviate** | 开源，功能丰富 | 企业级应用 |
| **Chroma** | 轻量级，Python友好 | 快速原型、小项目 |
| **Milvus** | 高性能，分布式 | 大规模应用 |

<br/>

***

<br/>

## 三、RAG：检索增强生成

### 3.1 什么是 RAG？

**RAG（Retrieval-Augmented Generation）：**

结合检索和生成，让 AI 在回答前先查找相关信息。

**传统方式：**

```
用户问题 → AI 直接回答（可能不知道背景）
```

**RAG 方式：**

```
用户问题 → 检索相关代码 → AI 结合上下文回答
```

<br/>

### 3.2 RAG 工作流程

**完整流程图：**

```
第1步：用户输入
    ↓
第2步：向量化查询
    ↓
第3步：检索相关代码（向量数据库）
    ↓
第4步：组装上下文（查询 + 相关代码）
    ↓
第5步：AI 生成回答
    ↓
第6步：返回结果
```

<br/>

### 3.3 实战示例

**场景：查询如何使用某个函数**

第1步：用户输入

```
用户：如何在订单中使用优惠券？
```

第2步：向量化查询

```python
query = "订单使用优惠券"
query_vector = embedding_model.encode(query)
# 结果：[0.7, 0.3, 0.8, 0.5, ...]
```

第3步：检索相关代码

```python
# 从向量数据库检索
results = vector_db.search(query_vector, top_k=3)

# 返回结果：
# 1. services/coupon.py:apply_coupon()  (相似度: 0.89)
# 2. models/order.py:calculate_total()  (相似度: 0.82)
# 3. services/order.py:create_order()   (相似度: 0.78)
```

第4步：组装上下文

```python
context = f"""
用户问题：{query}

相关代码1：
{results[0].code}

相关代码2：
{results[1].code}

相关代码3：
{results[2].code}

请回答用户的问题：
"""
```

第5步：AI 生成回答

```python
response = llm.generate(context)

# AI 回答：
"""
在订单中使用优惠券，你需要：

1. 在 create_order 时传入 coupon_code：
   order = create_order(user_id, items, coupon_code='SAVE10')

2. 系统会调用 apply_coupon() 函数：
   discount = apply_coupon(coupon_code, total)

3. 最终价格会减去折扣：
   final_price = total - discount

示例代码：
order = OrderService().create_order(
    user_id=123,
    items=[{'price': 100, 'quantity': 2}],
    coupon_code='SAVE10'
)
"""
```

<br/>

***

<br/>

## 四、长期记忆：超越上下文窗口

### 4.1 为什么需要长期记忆？

**短期记忆限制：**

- 上下文窗口有限（200K tokens）
- 每次对话都从头开始
- 无法记住项目历史

**长期记忆需求：**

- 记住项目架构决策
- 记住代码风格偏好
- 记住之前解决过的问题

<br/>

### 4.2 实现长期记忆

**方案1：项目配置文件**

```yaml
# .ai/memory.yaml

project:
  name: "电商系统"
  framework: "Flask"
  database: "PostgreSQL"

conventions:
  naming: "snake_case"
  testing: "pytest"
  style: "Google Python Style Guide"

decisions:
  - date: "2026-03-15"
    decision: "使用 JWT 做认证"
    reason: "无状态，易扩展"

  - date: "2026-03-20"
    decision: "使用 Celery 处理异步任务"
    reason: "需要发送邮件、生成报表"
```

**AI 读取记忆：**

```python
# 每次 AI 启动时加载
memory = load_memory('.ai/memory.yaml')

# AI 知道：
# - 项目使用 Flask
# - 命名用 snake_case
# - 测试用 pytest
# - 之前的技术决策
```

<br/>

**方案2：向量数据库持久化**

```python
# 存储对话历史
def save_conversation(question, answer, code_context):
    # 向量化
    vector = embedding_model.encode(question)
    
    # 存储到向量数据库
    vector_db.add(
        vector=vector,
        metadata={
            'question': question,
            'answer': answer,
            'code': code_context,
            'timestamp': datetime.now()
        }
    )

# 查询历史对话
def find_similar_questions(query):
    query_vector = embedding_model.encode(query)
    results = vector_db.search(query_vector, top_k=5)
    return results
```

**使用示例：**

```python
# 用户之前问过类似问题
user_query = "如何处理支付超时？"

# 检索历史
history = find_similar_questions(user_query)

# AI 发现：
# - 2026-03-10 用户问过："支付接口超时怎么办？"
# - 当时的解决方案：重试3次，失败后记录日志

# AI 参考历史回答
```

<br/>

### 4.3 记忆管理策略

**记忆分层：**

```
第1层：即时记忆（上下文窗口）
    ↓ 当前对话、正在编辑的文件

第2层：短期记忆（会话级）
    ↓ 本次会话的对话历史

第3层：长期记忆（项目级）
    ↓ 向量数据库、配置文件

第4层：元记忆（知识库）
    ↓ 最佳实践、常见问题
```

**记忆更新：**

```python
# 定期更新向量数据库
def update_codebase_index():
    # 扫描代码变化
    changed_files = git.diff('--name-only')
    
    # 重新索引变化的文件
    for file in changed_files:
        chunks = split_code(file)
        vectors = embed(chunks)
        vector_db.update(file, vectors)
    
    print("代码库索引已更新")
```

<br/>

***

<br/>

## 五、实战：构建项目的上下文系统

### 5.1 项目结构

```
my_project/
├── .ai/
│   ├── config.yaml        # AI 配置
│   ├── memory.yaml        # 项目记忆
│   └── codebase.index     # 代码库索引
├── src/
│   ├── models/
│   ├── services/
│   └── utils/
└── tests/
```

<br/>

### 5.2 配置示例

**AI 配置文件：**

```yaml
# .ai/config.yaml

model:
  name: "gpt-4"
  temperature: 0.7
  max_tokens: 2000

context:
  max_files: 20
  max_tokens_per_file: 5000
  include_tests: false

indexing:
  vector_db: "faiss"
  chunk_size: 500
  overlap: 50
  update_on_save: true

memory:
  persist_conversations: true
  max_history: 100
  similarity_threshold: 0.75
```

<br/>

### 5.3 使用流程

**初始化项目：**

```bash
# 第1步：初始化 AI 配置
ai-coding init

# 第2步：索引代码库
ai-coding index

# 第3步：开始使用
ai-coding chat
```

**日常使用：**

```bash
# 更新索引
ai-coding update

# 查看记忆
ai-coding memory list

# 清除记忆
ai-coding memory clear
```

<br/>

***

<br/>

## 六、最佳实践

### 6.1 代码组织技巧

**好的组织：**

```python
# 每个文件职责单一
# models/user.py - 只定义 User 模型
# services/user_service.py - 只处理用户业务逻辑

# AI 更容易找到相关代码
```

**不好的组织：**

```python
# utils.py - 包含所有工具函数（1000行）
# AI 很难定位具体功能
```

<br/>

### 6.2 注释和文档

**添加清晰的注释：**

```python
def calculate_discount(price: float, level: str) -> float:
    """
    根据用户等级计算折扣价格
    
    Args:
        price: 原价（必须大于0）
        level: 用户等级（gold/silver/bronze）
    
    Returns:
        折扣后的价格
    
    Example:
        >>> calculate_discount(100, 'gold')
        90.0
    """
    discounts = {'gold': 0.9, 'silver': 0.95, 'bronze': 1.0}
    return price * discounts.get(level, 1.0)
```

**为什么有效：**

- 注释会被向量化
- 搜索"折扣"时能找到这个函数
- AI 理解函数用途

<br/>

### 6.3 定期更新索引

**建议频率：**

```bash
# 每次提交代码后
git commit -m "xxx"
ai-coding update

# 或者设置钩子
# .git/hooks/post-commit
#!/bin/bash
ai-coding update --quiet
```

<br/>

***

<br/>

## 七、总结

### 核心要点

**1. 上下文管理挑战**

- 窗口限制（装不下所有代码）
- 相关性选择（找到需要的代码）

**2. 向量数据库**

- 将代码向量化
- 通过相似度搜索
- 找到相关代码

**3. RAG 技术**

```
查询 → 检索 → 组装上下文 → AI 回答
```

**4. 长期记忆**

- 项目配置
- 对话历史
- 知识库

**5. 实战技巧**

- 良好的代码组织
- 清晰的注释
- 定期更新索引

<br/>

### 效率提升

```
无上下文管理 → AI 只能看到当前文件
    ↓
有向量数据库 → AI 能搜索整个项目
    ↓
有长期记忆 → AI 记住项目历史
    ↓
效率提升：2-5倍
```

<br/>

***

<br/>

**系列导航**

• 上一篇：代码补全原理：AI 如何"读懂"代码
• 下一篇：AI Coding 架构：技术实现揭秘

<br/>

***

本文是《AI Coding 从入门到精通》系列第13篇  
作者：生活助理 | 发布时间：2026-04-04

**掌握上下文管理，让 AI 成为真正的项目助手！** 🚀
