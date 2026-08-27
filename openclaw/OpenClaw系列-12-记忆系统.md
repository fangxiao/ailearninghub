# 记忆系统：Agent如何"记住"

阅读时间：28分钟
难度等级：⭐⭐⭐⭐⭐ 原理篇
你将收获：理解Agent的记忆机制，掌握上下文管理

<br/>

***

<br/>

## 为什么Agent需要记忆？

上一篇你学会了核心循环：感知-思考-行动-反思。

**但有个问题：**

```
你：我叫张三
龙虾：好的，张三！

你：我叫什么？
龙虾：抱歉，我不知道...
```

**为什么？因为Agent没有"记住"！**

记忆系统，就是让Agent能记住：

• ✅ 用户是谁
• ✅ 之前聊过什么
• ✅ 学到了什么知识
• ✅ 积累了什么经验

<br/>

***

<br/>

## 一、记忆的类型

### 1.1 人类记忆 vs Agent记忆

**人类记忆：**

```
短期记忆：刚才说的话、当前的想法（几秒到几分钟）
长期记忆：童年回忆、学过的知识（永久）
肌肉记忆：骑车、打字（技能）
```

**Agent记忆类似：**

```
短期记忆：当前对话上下文
长期记忆：历史对话、知识库
程序性记忆：技能、工作流
```

<br/>

### 1.2 Agent记忆分类

| 类型 | 作用 | 存储 | 容量 | 持久性 |
|------|------|------|------|--------|
| 工作记忆 | 当前对话 | 内存 | 4K-8K tokens | 会话级 |
| 对话记忆 | 历史对话 | 数据库 | 无限 | 永久 |
| 知识记忆 | 知识库 | 向量库 | 无限 | 永久 |
| 技能记忆 | 技能定义 | 文件 | 无限 | 永久 |

<br/>

***

<br/>

## 二、工作记忆（短期记忆）

### 2.1 什么是工作记忆？

**定义：当前对话的上下文窗口**

```
┌────────────────────────────────────┐
│         工作记忆窗口               │
│  （容量限制：4K-128K tokens）      │
├────────────────────────────────────┤
│ [用户] 我叫张三                    │
│ [Agent] 好的，张三！               │
│ [用户] 今天天气怎么样？            │
│ [Agent] 北京今天晴天，25度...      │
│ [用户] 我叫什么？← 当前问题        │
└────────────────────────────────────┘
```

**特点：**

• ✅ 速度快（内存读写）
• ✅ 上下文连贯
• ❌ 容量有限
• ❌ 会话结束就消失

<br/>

### 2.2 Token限制问题

**什么是Token？**

> Token = 文本的最小单位
> 中文：1个汉字 ≈ 2个token
> 英文：1个单词 ≈ 1个token

**不同模型的Token限制：**

| 模型 | 上下文窗口 | 大约等于 |
|------|-----------|---------|
| GPT-3.5 | 4K tokens | 3000字中文 |
| GPT-4 | 8K tokens | 6000字中文 |
| GPT-4-Turbo | 128K tokens | 10万字中文 |
| Claude-3 | 200K tokens | 15万字中文 |
| GLM-4 | 128K tokens | 10万字中文 |

<br/>

### 2.3 上下文管理策略

**问题：对话太长，超过Token限制怎么办？**

**策略1：滑动窗口**

```python
class SlidingWindow:
    """滑动窗口：只保留最近的N条消息"""
    
    def __init__(self, max_messages: int = 20):
        self.max_messages = max_messages
        self.messages = []
    
    def add(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        # 超过限制，删除最早的
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
```

**优点：** 简单高效
**缺点：** 丢失早期信息

<br/>

**策略2：摘要压缩**

```python
class SummaryCompressor:
    """摘要压缩：把旧对话压缩成摘要"""
    
    def compress(self, messages: list) -> str:
        """将多条消息压缩成一段摘要"""
        prompt = f"""
        请将以下对话压缩成简洁的摘要：
        {messages}
        
        要求：
        1. 保留关键信息
        2. 不超过200字
        """
        return self.llm.generate(prompt)

# 使用示例
window = SummaryCompressor()
window.add("user", "我叫张三")
window.add("agent", "好的张三")
# ... 很多对话后 ...
summary = window.compress(old_messages)
# 摘要："用户名叫张三，讨论了天气和文件整理"
```

**优点：** 保留关键信息
**缺点：** 细节丢失

<br/>

**策略3：分层记忆**

```python
class LayeredMemory:
    """分层记忆：重要信息永久保留，次要信息压缩"""
    
    def __init__(self):
        self.permanent = []  # 永久记忆（用户偏好等）
        self.recent = []     # 最近对话（完整保留）
        self.summary = ""    # 历史摘要（压缩）
    
    def add(self, message: dict):
        # 判断是否重要
        if self.is_important(message):
            self.permanent.append(message)
        else:
            self.recent.append(message)
        
        # 定期压缩
        if len(self.recent) > 50:
            self.summary = self.compress(self.recent[:-20])
            self.recent = self.recent[-20:]
    
    def is_important(self, message: dict) -> bool:
        """判断消息是否重要"""
        keywords = ["我叫", "我的", "记住", "偏好", "设置"]
        return any(kw in message["content"] for kw in keywords)
```

<br/>

***

<br/>

## 三、对话记忆（长期记忆）

### 3.1 什么是对话记忆？

**定义：持久化存储的历史对话**

```
会话1（2026-03-20）：
- 用户：我叫张三
- Agent：好的，张三！

会话2（2026-03-26）：
- 用户：我叫什么？
- Agent：你叫张三（从对话记忆中检索）
```

<br/>

### 3.2 对话存储

**存储结构：**

```python
class ConversationStore:
    """对话存储"""
    
    def save(self, session_id: str, messages: list):
        """保存对话"""
        record = {
            "session_id": session_id,
            "user_id": self.user_id,
            "messages": messages,
            "timestamp": datetime.now(),
            "summary": self.summarize(messages)
        }
        self.db.insert("conversations", record)
    
    def load(self, session_id: str) -> list:
        """加载对话"""
        return self.db.find("conversations", {"session_id": session_id})
    
    def search(self, query: str) -> list:
        """搜索历史对话"""
        # 根据摘要或关键词搜索
        return self.db.search("conversations", {"summary": {"$regex": query}})
```

<br/>

### 3.3 对话检索

**如何从海量对话中找到相关信息？**

**方法1：关键词搜索**

```python
def keyword_search(query: str, conversations: list) -> list:
    """关键词搜索"""
    keywords = extract_keywords(query)
    results = []
    
    for conv in conversations:
        if any(kw in conv["summary"] for kw in keywords):
            results.append(conv)
    
    return results
```

**方法2：语义搜索**

```python
def semantic_search(query: str, conversations: list) -> list:
    """语义搜索：理解含义，不只是匹配关键词"""
    
    # 1. 将query转为向量
    query_embedding = embed(query)
    
    # 2. 计算相似度
    results = []
    for conv in conversations:
        similarity = cosine_similarity(query_embedding, conv["embedding"])
        if similarity > 0.7:
            results.append((conv, similarity))
    
    # 3. 按相似度排序
    results.sort(key=lambda x: x[1], reverse=True)
    return [r[0] for r in results[:5]]
```

<br/>

***

<br/>

## 四、知识记忆（向量记忆）

### 4.1 什么是知识记忆？

**定义：存储和检索知识的向量数据库**

```
传统搜索：
关键词匹配 → 找到包含关键词的文档

向量搜索：
理解语义 → 找到含义相似的文档
```

<br/>

### 4.2 向量化原理

**什么是向量？**

```
文本 → Embedding模型 → 向量（数字数组）

示例：
"苹果" → [0.23, -0.15, 0.89, ...]（1536维）
"水果" → [0.21, -0.12, 0.85, ...]（相似！）
"汽车" → [-0.45, 0.78, -0.23, ...]（不相似）
```

**相似度计算：**

```python
import numpy as np

def cosine_similarity(vec1: list, vec2: list) -> float:
    """余弦相似度：衡量两个向量的相似程度"""
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    
    dot_product = np.dot(vec1, vec2)
    norm = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    
    return dot_product / norm

# 示例
similarity = cosine_similarity(
    embed("苹果"),
    embed("水果")
)
# 结果：0.85（很相似）
```

<br/>

### 4.3 向量数据库

**常用向量数据库：**

| 数据库 | 特点 | 适用场景 |
|--------|------|---------|
| Pinecone | 云服务，简单 | 快速原型 |
| Milvus | 开源，高性能 | 大规模生产 |
| Chroma | 轻量级 | 本地开发 |
| Qdrant | Rust实现，快 | 高性能需求 |
| FAISS | Meta开源 | 本地向量搜索 |

<br/>

**Chroma示例：**

```python
import chromadb

# 初始化客户端
client = chromadb.Client()

# 创建集合
collection = client.create_collection("knowledge")

# 添加文档
collection.add(
    documents=["OpenClaw是AI Agent平台", "Agent能自动执行任务"],
    metadatas=[{"source": "doc1"}, {"source": "doc2"}],
    ids=["doc1", "doc2"]
)

# 查询
results = collection.query(
    query_texts=["什么是OpenClaw"],
    n_results=2
)

print(results["documents"])
# ["OpenClaw是AI Agent平台", "Agent能自动执行任务"]
```

<br/>

***

<br/>

## 五、RAG：检索增强生成

### 5.1 什么是RAG？

**RAG = Retrieval-Augmented Generation**

> 先检索相关知识，再生成回答

```
传统LLM：
问题 → LLM → 回答（可能编造）

RAG：
问题 → 检索知识 → 知识+问题 → LLM → 回答（有依据）
```

<br/>

### 5.2 RAG工作流程

```
┌─────────────────────────────────────────┐
│  1. 用户提问：OpenClaw支持哪些模型？     │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  2. 向量化问题                           │
│     embed("OpenClaw支持哪些模型")        │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  3. 向量检索                             │
│     在知识库中找相似文档                  │
│     找到：OpenClaw支持GPT/Claude/GLM...  │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  4. 构造提示词                           │
│     上下文：检索到的知识                  │
│     问题：用户原始问题                    │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  5. LLM生成回答                          │
│     基于检索到的知识生成                  │
│     "OpenClaw支持GPT-5、Claude、GLM..."  │
└─────────────────────────────────────────┘
```

<br/>

### 5.3 RAG实现

```python
class RAGSystem:
    """RAG检索增强生成系统"""
    
    def __init__(self, vector_db, llm):
        self.db = vector_db
        self.llm = llm
    
    def query(self, question: str, top_k: int = 3) -> str:
        """查询并生成回答"""
        
        # 1. 检索相关知识
        context = self.retrieve(question, top_k)
        
        # 2. 构造提示词
        prompt = f"""
        请根据以下知识回答问题。
        
        【知识】
        {context}
        
        【问题】
        {question}
        
        【要求】
        - 只基于知识回答，不要编造
        - 如果知识中没有答案，请诚实说明
        """
        
        # 3. 生成回答
        answer = self.llm.generate(prompt)
        return answer
    
    def retrieve(self, query: str, top_k: int) -> str:
        """检索相关文档"""
        results = self.db.query(
            query_texts=[query],
            n_results=top_k
        )
        return "\n\n".join(results["documents"][0])

# 使用示例
rag = RAGSystem(chroma_collection, llm)
answer = rag.query("OpenClaw如何配置模型？")
```

<br/>

### 5.4 RAG优化技巧

**技巧1：分块策略**

```python
def chunk_documents(docs: list, chunk_size: int = 500) -> list:
    """将长文档分块"""
    chunks = []
    for doc in docs:
        # 按段落分割
        paragraphs = doc.split("\n\n")
        
        # 合并小块，拆分大块
        current_chunk = ""
        for para in paragraphs:
            if len(current_chunk) + len(para) < chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = para + "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk)
    
    return chunks
```

<br/>

**技巧2：重排序**

```python
def rerank(query: str, candidates: list, top_k: int = 5) -> list:
    """重排序：用更强的模型对结果重新排序"""
    
    # 1. 向量检索得到候选（快速但粗糙）
    initial_results = vector_search(query, candidates, top_k=20)
    
    # 2. 用Cross-Encoder重排序（慢但精准）
    reranker = CrossEncoder("model-name")
    scores = reranker.predict([(query, doc) for doc in initial_results])
    
    # 3. 按分数排序，返回top_k
    ranked = sorted(zip(initial_results, scores), key=lambda x: x[1], reverse=True)
    return [doc for doc, score in ranked[:top_k]]
```

<br/>

**技巧3：混合检索**

```python
def hybrid_search(query: str, alpha: float = 0.5) -> list:
    """混合检索：关键词 + 向量"""
    
    # 关键词检索
    keyword_results = keyword_search(query)
    keyword_scores = {r["id"]: r["score"] for r in keyword_results}
    
    # 向量检索
    vector_results = vector_search(query)
    vector_scores = {r["id"]: r["score"] for r in vector_results}
    
    # 融合分数
    all_ids = set(keyword_scores.keys()) | set(vector_scores.keys())
    final_scores = {}
    
    for doc_id in all_ids:
        kw_score = keyword_scores.get(doc_id, 0)
        vec_score = vector_scores.get(doc_id, 0)
        final_scores[doc_id] = alpha * kw_score + (1 - alpha) * vec_score
    
    # 排序返回
    ranked = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
    return ranked[:10]
```

<br/>

***

<br/>

## 六、程序性记忆（技能记忆）

### 6.1 什么是程序性记忆？

**定义：存储技能和流程定义**

```
陈述性记忆：知道"是什么"
- OpenClaw是什么
- 天气API怎么用

程序性记忆：知道"怎么做"
- 如何查询天气
- 如何生成日报
```

<br/>

### 6.2 技能存储

**技能定义格式：**

```yaml
# skill.yaml
name: weather_query
description: 查询城市天气
version: 1.0.0

# 参数定义
parameters:
  city:
    type: string
    description: 城市名称
    required: true

# 工作流定义
workflow:
  - step: search
    action: web_search
    input: "${city}天气"
  
  - step: extract
    action: extract_info
    fields:
      - 温度
      - 天气状况
      - 湿度
  
  - step: format
    action: format_response
    template: |
      ${city}今天天气：
      - 温度：${temp}
      - 天气：${weather}
      - 湿度：${humidity}%
```

<br/>

### 6.3 技能检索

```python
class SkillRetriever:
    """技能检索器"""
    
    def find_skill(self, task_description: str) -> str:
        """根据任务描述找到合适的技能"""
        
        # 向量化任务描述
        task_embedding = embed(task_description)
        
        # 在技能库中搜索
        skills = self.db.query(
            query_embeddings=[task_embedding],
            n_results=3
        )
        
        # 返回最匹配的技能
        return skills["metadatas"][0][0]["skill_name"]

# 示例
retriever = SkillRetriever()
skill = retriever.find_skill("我想查北京的天气")
# 返回：weather_query
```

<br/>

***

<br/>

## 七、完整记忆系统

### 7.1 架构设计

```
┌─────────────────────────────────────────────┐
│              记忆系统架构                    │
├─────────────────────────────────────────────┤
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │  工作记忆（内存）                    │   │
│  │  - 当前对话上下文                    │   │
│  │  - 临时变量                         │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │  对话记忆（数据库）                  │   │
│  │  - 历史会话                         │   │
│  │  - 用户偏好                         │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │  知识记忆（向量库）                  │   │
│  │  - 文档知识                         │   │
│  │  - FAQ知识                          │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │  技能记忆（文件系统）                │   │
│  │  - Skill定义                        │   │
│  │  - 工作流定义                       │   │
│  └─────────────────────────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
```

<br/>

### 7.2 统一接口

```python
class MemorySystem:
    """统一记忆系统"""
    
    def __init__(self):
        self.working = WorkingMemory()      # 工作记忆
        self.conversation = ConversationDB() # 对话记忆
        self.knowledge = VectorDB()          # 知识记忆
        self.skills = SkillStore()           # 技能记忆
    
    def remember(self, info: dict, memory_type: str):
        """记住信息"""
        if memory_type == "working":
            self.working.add(info)
        elif memory_type == "conversation":
            self.conversation.save(info)
        elif memory_type == "knowledge":
            self.knowledge.add(info)
        elif memory_type == "skill":
            self.skills.save(info)
    
    def recall(self, query: str, memory_types: list) -> dict:
        """回忆信息"""
        results = {}
        
        if "working" in memory_types:
            results["working"] = self.working.get_recent()
        
        if "conversation" in memory_types:
            results["conversation"] = self.conversation.search(query)
        
        if "knowledge" in memory_types:
            results["knowledge"] = self.knowledge.query(query)
        
        if "skill" in memory_types:
            results["skill"] = self.skills.find(query)
        
        return results
```

<br/>

### 7.3 记忆管理

```python
class MemoryManager:
    """记忆管理器"""
    
    def cleanup(self):
        """清理过期记忆"""
        # 1. 清理工作记忆
        self.working.clear_old()
        
        # 2. 归档旧对话
        old_conversations = self.conversation.get_older_than(days=30)
        for conv in old_conversations:
            self.archive(conv)
        
        # 3. 优化向量索引
        self.knowledge.optimize_index()
    
    def compress(self):
        """压缩记忆"""
        # 1. 压缩对话摘要
        conversations = self.conversation.get_all()
        summary = self.summarize(conversations)
        self.save_summary(summary)
        
        # 2. 删除原始对话（保留摘要）
        self.conversation.clear()
```

<br/>

***

<br/>

## 八、实战：为Agent添加记忆

### 8.1 场景：记住用户偏好

**需求：Agent记住用户的偏好设置**

```python
class UserPreferenceMemory:
    """用户偏好记忆"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.db = SQLiteDB("preferences.db")
    
    def set_preference(self, key: str, value: any):
        """设置偏好"""
        self.db.upsert(
            table="preferences",
            data={
                "user_id": self.user_id,
                "key": key,
                "value": json.dumps(value),
                "updated_at": datetime.now()
            },
            keys=["user_id", "key"]
        )
    
    def get_preference(self, key: str, default=None):
        """获取偏好"""
        result = self.db.find_one(
            table="preferences",
            where={"user_id": self.user_id, "key": key}
        )
        if result:
            return json.loads(result["value"])
        return default

# 使用示例
pref = UserPreferenceMemory("user_123")

# 用户说："以后都用中文回复"
pref.set_preference("language", "中文")

# 下次对话时
language = pref.get_preference("language", "英文")
# Agent用中文回复
```

<br/>

### 8.2 场景：知识问答

**需求：基于文档回答问题**

```python
class KnowledgeQA:
    """知识问答系统"""
    
    def __init__(self):
        self.vector_db = ChromaDB()
        self.llm = LLM()
    
    def add_knowledge(self, documents: list):
        """添加知识"""
        # 分块
        chunks = self.chunk(documents)
        
        # 向量化存储
        self.vector_db.add(
            documents=[c["content"] for c in chunks],
            metadatas=[c["metadata"] for c in chunks],
            ids=[c["id"] for c in chunks]
        )
    
    def answer(self, question: str) -> str:
        """回答问题"""
        # RAG检索增强
        context = self.vector_db.query(
            query_texts=[question],
            n_results=3
        )
        
        # 生成回答
        prompt = f"""
        基于以下知识回答问题：
        
        知识：
        {context["documents"]}
        
        问题：{question}
        """
        
        return self.llm.generate(prompt)

# 使用示例
qa = KnowledgeQA()

# 添加公司文档
qa.add_knowledge([
    "公司成立于2020年，专注于AI Agent开发...",
    "OpenClaw是我们的核心产品，提供..."
])

# 问答
answer = qa.answer("公司是做什么的？")
# "公司专注于AI Agent开发，核心产品是OpenClaw..."
```

<br/>

***

<br/>

## 九、记忆 vs 核心循环

### 9.1 记忆在核心循环中的作用

```
感知环节：
- 从记忆中加载上下文
- 检索相关知识
- 回忆用户偏好

思考环节：
- 基于历史经验推理
- 参考相似案例
- 规划行动步骤

行动环节：
- 调用技能（程序性记忆）
- 执行工作流

反思环节：
- 记录执行结果
- 更新经验库
- 优化策略
```

<br/>

### 9.2 记忆让Agent更智能

| 没有记忆 | 有记忆 |
|---------|--------|
| 每次对话从零开始 | 记住历史，连贯对话 |
| 不知道用户是谁 | 知道用户偏好 |
| 无法利用知识 | RAG增强，回答准确 |
| 重复犯同样错误 | 从经验中学习 |

<br/>

***

<br/>

## 十、小结

### 记忆系统四层架构

> **工作记忆：** 当前对话，快速但有限
>
> **对话记忆：** 历史会话，持久化存储
>
> **知识记忆：** 向量数据库，语义检索
>
> **技能记忆：** 流程定义，程序性知识

### 关键技术

• ✅ Token管理与上下文压缩
• ✅ 向量化与语义搜索
• ✅ RAG检索增强生成
• ✅ 分层记忆管理
• ✅ 记忆清理与优化

### 下一篇预告

**第13篇：OpenClaw架构解析**

• 整体架构设计
• 核心组件分析
• 设计哲学与原则
• 与其他框架对比

<br/>

***

<br/>

## 思考题

### 🤔 深度思考

1. **如果用户说"忘记我刚才说的"，怎么实现？** 需要删除哪些记忆？

2. **RAG和微调（Fine-tuning）有什么区别？** 各自适合什么场景？

3. **如何平衡记忆容量和检索速度？** 有什么优化策略？

**欢迎在评论区分享你的思考！** 💬

<br/>

***

<br/>

## 下期预告

**下一篇：**《OpenClaw架构解析：设计哲学》

**你将学到：**

• ✅ OpenClaw整体架构
• ✅ 核心组件深度解析
• ✅ 设计哲学与原则
• ✅ 与LangChain/AutoGPT对比
• ✅ 扩展机制

**准备好深入架构了吗？** 🏗️

<br/>

***

**系列导航**

• 上一篇：核心循环：感知-思考-行动-反思
• 下一篇：OpenClaw架构解析：设计哲学

<br/>

***

本文是《OpenClaw从入门到精通》系列第12篇（原理篇第2篇）
作者：生活助理 | 发布时间：2026-03-26
