# 核心循环：感知-思考-行动-反思

阅读时间：25分钟
难度等级：⭐⭐⭐⭐⭐ 原理篇
你将收获：深入理解Agent的"大脑"如何工作

<br/>

***

<br/>

## 从进阶到原理：为什么要学这个？

恭喜你完成进阶篇！你已经能：

• ✅ 开发自定义 Skill
• ✅ 设计工作流
• ✅ 组建多Agent团队
• ✅ 集成外部服务

**但你是否好奇：**

• "龙虾是怎么'思考'的？"
• "为什么有时候它很聪明，有时候又很笨？"
• "背后的原理是什么？"

原理篇，带你走进Agent的"大脑"。

<br/>

***

<br/>

## 一、什么是核心循环？

### 1.1 人类是如何工作的？

想象你在公司接到一个任务：

```
1. 感知：看到任务邮件，理解需求
2. 思考：分析怎么做，规划步骤
3. 行动：执行计划，完成任务
4. 反思：检查结果，总结经验
```

**Agent也是一样！**

<br/>

### 1.2 Agent核心循环

**四大环节：**

```
┌─────────────────────────────────────────┐
│            感知（Perception）            │
│        接收输入，理解用户意图            │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│            思考（Thinking）              │
│        分析问题，规划行动步骤            │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│            行动（Action）                │
│        执行工具，完成任务                │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│            反思（Reflection）            │
│        评估结果，优化策略                │
└─────────────────┬───────────────────────┘
                  │
                  └──────→ 继续循环
```

**这个循环不断重复，直到任务完成。**

<br/>

***

<br/>

## 二、感知：理解世界

### 2.1 感知什么？

**Agent能感知的信息：**

| 类型 | 示例 | 来源 |
|------|------|------|
| 文本输入 | "帮我整理文件" | 用户消息 |
| 文件输入 | PDF、Excel | 文件上传 |
| 环境信息 | 时间、位置 | 系统状态 |
| 上下文 | 历史对话 | 记忆系统 |
| 反馈 | 工具执行结果 | 上一步行动 |

<br/>

### 2.2 感知过程

**三步走：**

```
原始输入 → 信息提取 → 意图理解 → 结构化表示

示例：
"帮我把桌面上大于10MB的文件移到归档文件夹"
    ↓
信息提取：位置=桌面，条件=大于10MB，动作=移动，目标=归档文件夹
    ↓
意图理解：文件整理任务
    ↓
结构化表示：
{
  "task": "file_organize",
  "source": "desktop",
  "condition": {"size": ">10MB"},
  "target": "archive",
  "action": "move"
}
```

<br/>

### 2.3 信息提取技术

**关键信息识别：**

```python
def extract_entities(text: str) -> dict:
    """从文本中提取关键实体"""
    entities = {
        "时间": extract_time(text),      # "明天下午3点"
        "地点": extract_location(text),  # "上海浦东"
        "人物": extract_person(text),    # "张经理"
        "数量": extract_number(text),    # "10个文件"
        "动作": extract_action(text),    # "整理、发送"
    }
    return entities

# 示例
text = "明天下午3点把报告发给张经理"
result = extract_entities(text)
# {
#   "时间": "明天下午3点",
#   "人物": "张经理",
#   "动作": "发送",
#   "对象": "报告"
# }
```

<br/>

### 2.4 意图理解

**意图分类：**

```python
class IntentClassifier:
    """意图分类器"""
    
    def __init__(self):
        self.intents = {
            "file_organize": ["整理文件", "分类文件", "移动文件"],
            "web_search": ["搜索", "查找", "查询"],
            "send_message": ["发送", "通知", "提醒"],
            "data_analysis": ["分析", "统计", "计算"],
        }
    
    def classify(self, text: str) -> str:
        """判断用户意图"""
        for intent, keywords in self.intents.items():
            if any(kw in text for kw in keywords):
                return intent
        return "unknown"
```

<br/>

***

<br/>

## 三、思考：推理决策

### 3.1 思维链（Chain of Thought）

**核心思想：分步推理**

传统方式：

```
问题 → 直接答案
```

思维链：

```
问题 → 思考步骤1 → 思考步骤2 → ... → 答案
```

<br/>

**示例：**

用户问：

```
我有100个文件，每个文件平均处理需要30秒，处理完需要多久？
```

思维链推理：

```
思考1：理解问题
- 需要计算总时间
- 文件数 = 100
- 单文件时间 = 30秒

思考2：选择方法
- 总时间 = 文件数 × 单文件时间
- 可以串行或并行

思考3：计算结果
- 串行：100 × 30秒 = 3000秒 = 50分钟
- 如果10个并行：50分钟 ÷ 10 = 5分钟

结论：
串行处理需要50分钟，10个并行需要5分钟。
```

<br/>

### 3.2 ReAct模式

**ReAct = Reasoning + Acting**

交替进行思考和行动：

```
用户：帮我查找OpenClaw的最新版本

Agent思考：需要搜索网络获取信息
Agent行动：调用web_search工具，搜索"OpenClaw latest version"
工具返回：OpenClaw 2.5.0 released on 2026-03-01

Agent思考：获取到了版本信息，需要整理回答
Agent行动：生成最终回复

Agent回复：OpenClaw最新版本是2.5.0，于2026年3月1日发布。
```

<br/>

**完整流程图：**

```
┌──────────┐
│ 用户提问  │
└────┬─────┘
     ↓
┌─────────────────────────────────────┐
│ 思考1：需要什么信息？               │
│ 结论：需要搜索OpenClaw版本信息      │
└────┬────────────────────────────────┘
     ↓
┌─────────────────────────────────────┐
│ 行动1：调用搜索工具                 │
│ 工具：web_search("OpenClaw version")│
│ 结果：找到版本2.5.0                 │
└────┬────────────────────────────────┘
     ↓
┌─────────────────────────────────────┐
│ 思考2：信息够了吗？                 │
│ 结论：够了，可以回答了              │
└────┬────────────────────────────────┘
     ↓
┌─────────────────────────────────────┐
│ 行动2：生成最终回复                 │
│ 回复：最新版本是2.5.0...            │
└────┬────────────────────────────────┘
     ↓
┌──────────┐
│ 完成任务  │
└──────────┘
```

<br/>

### 3.3 规划（Planning）

**任务分解：**

复杂任务需要分解成子任务：

```
任务："帮我准备明天的会议"

分解：
1. 查看日历，确认会议时间
2. 搜索会议相关资料
3. 整理会议议程
4. 准备演示文档
5. 发送会议邀请
```

<br/>

**规划算法：**

```python
class TaskPlanner:
    """任务规划器"""
    
    def decompose(self, task: str) -> list:
        """将复杂任务分解为子任务"""
        prompt = f"""
        将以下任务分解为具体的子任务：
        任务：{task}
        
        要求：
        1. 每个子任务清晰明确
        2. 子任务之间有依赖关系
        3. 按执行顺序排列
        
        输出格式：
        1. [子任务1]
        2. [子任务2]
        ...
        """
        return self.llm.generate(prompt)
    
    def prioritize(self, subtasks: list) -> list:
        """按优先级排序"""
        # 考虑依赖关系、紧急程度、重要性
        pass
```

<br/>

***

<br/>

## 四、行动：执行任务

### 4.1 工具选择

**如何选择合适的工具？**

```
决策因素：
1. 任务类型（搜索、文件、数据库...）
2. 工具能力（能做什么、不能做什么）
3. 工具效率（速度、准确性）
4. 工具成本（API费用、资源消耗）
```

<br/>

**工具选择器：**

```python
class ToolSelector:
    """工具选择器"""
    
    def __init__(self):
        self.tools = {
            "web_search": {
                "capabilities": ["搜索", "查询", "查找"],
                "cost": "low",
                "speed": "fast"
            },
            "database": {
                "capabilities": ["数据查询", "统计"],
                "cost": "low",
                "speed": "fast"
            },
            "llm_generate": {
                "capabilities": ["生成", "写作", "总结"],
                "cost": "high",
                "speed": "medium"
            }
        }
    
    def select(self, task_type: str) -> str:
        """选择最合适的工具"""
        for tool_name, tool_info in self.tools.items():
            if task_type in tool_info["capabilities"]:
                return tool_name
        return None
```

<br/>

### 4.2 参数填充

**LLM自动填充参数：**

```python
def fill_parameters(tool_schema: dict, user_input: str) -> dict:
    """根据用户输入填充工具参数"""
    
    # 工具定义
    # {
    #   "name": "web_search",
    #   "parameters": {
    #     "query": {"type": "string", "description": "搜索关键词"},
    #     "count": {"type": "int", "default": 5}
    #   }
    # }
    
    # LLM提取参数
    prompt = f"""
    用户输入：{user_input}
    工具参数：{tool_schema}
    
    请从用户输入中提取工具需要的参数值。
    """
    
    return llm.generate(prompt)
    
# 示例
user_input = "搜索最近关于AI的新闻，要10条"
params = fill_parameters(tool_schema, user_input)
# {"query": "AI 新闻", "count": 10}
```

<br/>

### 4.3 执行监控

**监控工具执行：**

```python
class ActionExecutor:
    """行动执行器"""
    
    def execute(self, tool_name: str, params: dict) -> dict:
        """执行工具并监控"""
        result = {
            "tool": tool_name,
            "params": params,
            "start_time": time.time(),
            "status": "running"
        }
        
        try:
            # 执行工具
            output = self.tools[tool_name].execute(**params)
            result["output"] = output
            result["status"] = "success"
            
        except TimeoutError:
            result["status"] = "timeout"
            result["error"] = "执行超时"
            
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
            
        finally:
            result["end_time"] = time.time()
            result["duration"] = result["end_time"] - result["start_time"]
        
        return result
```

<br/>

***

<br/>

## 五、反思：自我优化

### 5.1 结果评估

**如何判断任务是否成功？**

```python
class ResultEvaluator:
    """结果评估器"""
    
    def evaluate(self, task: str, result: str) -> dict:
        """评估执行结果"""
        evaluation = {
            "success": False,
            "score": 0,
            "issues": []
        }
        
        # 检查1：结果是否为空
        if not result or result == "":
            evaluation["issues"].append("结果为空")
            return evaluation
        
        # 检查2：是否包含错误信息
        if "错误" in result or "失败" in result:
            evaluation["issues"].append("执行过程中出现错误")
            return evaluation
        
        # 检查3：是否满足任务要求
        prompt = f"""
        任务：{task}
        结果：{result}
        
        请判断结果是否满足任务要求。
        输出：满足/不满足，以及理由。
        """
        judgement = self.llm.generate(prompt)
        
        if "满足" in judgement:
            evaluation["success"] = True
            evaluation["score"] = 0.9
        else:
            evaluation["issues"].append(judgement)
        
        return evaluation
```

<br/>

### 5.2 策略调整

**失败后如何调整？**

```
策略1：重试
- 简单错误，直接重试
- 最多重试3次

策略2：换工具
- 工具不合适，换一个
- 选择替代工具

策略3：分解任务
- 任务太复杂，分解成子任务
- 逐个完成

策略4：求助用户
- 无法自动解决
- 询问用户如何处理
```

<br/>

**策略选择器：**

```python
class StrategySelector:
    """策略选择器"""
    
    def select_strategy(self, error_type: str, retry_count: int) -> str:
        """选择应对策略"""
        
        if retry_count < 3 and error_type in ["timeout", "network"]:
            return "retry"
        
        elif error_type == "tool_not_found":
            return "switch_tool"
        
        elif error_type == "task_too_complex":
            return "decompose"
        
        else:
            return "ask_user"
```

<br/>

### 5.3 经验积累

**从错误中学习：**

```python
class ExperienceLearner:
    """经验学习器"""
    
    def __init__(self):
        self.experiences = []  # 经验库
    
    def record(self, task: str, action: str, result: str, success: bool):
        """记录经验"""
        experience = {
            "task": task,
            "action": action,
            "result": result,
            "success": success,
            "timestamp": datetime.now()
        }
        self.experiences.append(experience)
    
    def get_similar_experiences(self, task: str) -> list:
        """获取相似任务的经验"""
        # 使用向量搜索找相似经验
        return [exp for exp in self.experiences 
                if self.similarity(task, exp["task"]) > 0.8]
```

<br/>

***

<br/>

## 六、完整循环示例

### 6.1 场景：整理会议纪要

**用户输入：**

```
帮我把这个会议录音整理成会议纪要
[上传音频文件 meeting.mp3]
```

<br/>

**完整循环过程：**

```
═══════════════════════════════════════════
【第1轮循环】
═══════════════════════════════════════════

1️⃣ 感知：
- 输入类型：音频文件
- 任务目标：转换为会议纪要
- 关键信息：meeting.mp3

2️⃣ 思考：
- 需要先转录音频为文字
- 然后提取关键信息
- 最后格式化为纪要

3️⃣ 行动：
- 调用语音转文字工具
- 工具：speech_to_text("meeting.mp3")
- 结果：转录文本（5000字）

4️⃣ 反思：
- 转录成功 ✅
- 但文字太长，需要进一步处理
- 继续 next step

═══════════════════════════════════════════
【第2轮循环】
═══════════════════════════════════════════

1️⃣ 感知：
- 当前状态：已转录文本
- 待处理：5000字文本

2️⃣ 思考：
- 需要提取关键信息
- 参会人员、讨论内容、决议事项

3️⃣ 行动：
- 调用LLM提取关键信息
- 工具：extract_key_points(transcript)
- 结果：提取了5个关键点

4️⃣ 反思：
- 提取成功 ✅
- 需要格式化成标准纪要

═══════════════════════════════════════════
【第3轮循环】
═══════════════════════════════════════════

1️⃣ 感知：
- 当前状态：已提取关键点
- 待处理：格式化

2️⃣ 思考：
- 使用标准会议纪要模板
- 包含：时间、参会人、议题、决议

3️⃣ 行动：
- 调用格式化工具
- 工具：format_minutes(key_points)
- 结果：生成Markdown格式纪要

4️⃣ 反思：
- 格式化成功 ✅
- 任务完成！

═══════════════════════════════════════════
【最终输出】
═══════════════════════════════════════════

会议纪要已生成：
# 产品评审会议纪要
时间：2026-03-26 14:00
参会人：张总、李经理、王工
...
```

<br/>

***

<br/>

## 七、循环优化

### 7.1 减少循环次数

**问题：循环太多，效率低**

**优化方法：**

```python
# 优化前：每次只做一件事
循环1：分析任务
循环2：选择工具
循环3：执行工具
循环4：检查结果

# 优化后：合并步骤
一次循环：
- 分析 + 选择 + 执行 + 检查
```

<br/>

### 7.2 提前终止

**问题：任务已完成，还在循环**

**优化方法：**

```python
def should_continue(result: dict) -> bool:
    """判断是否需要继续循环"""
    
    # 成功标志
    if result.get("success"):
        return False
    
    # 达到最大循环次数
    if result.get("loop_count", 0) >= 10:
        return False
    
    # 用户明确终止
    if result.get("user_cancelled"):
        return False
    
    return True
```

<br/>

### 7.3 并行执行

**问题：多个独立任务串行执行太慢**

**优化方法：**

```python
async def parallel_execute(tasks: list) -> list:
    """并行执行多个独立任务"""
    
    # 识别独立任务
    independent_tasks = find_independent(tasks)
    
    # 并行执行
    results = await asyncio.gather(*[
        execute_task(task) for task in independent_tasks
    ])
    
    return results
```

<br/>

***

<br/>

## 八、与进阶篇的联系

### 8.1 核心循环 vs Skill

**Skill是什么？**

> Skill = 预定义的"行动"模板

```yaml
# 天气查询Skill
name: weather_query
steps:
  - action: call_tool
    tool: web_search
    params: "{city}天气"
  
  - action: extract_info
    fields: [温度, 天气, 湿度]
  
  - action: format_response
    template: "{city}今天{weather}，温度{temp}度"
```

**本质：把常用的"行动"固化成Skill**

<br/>

### 8.2 核心循环 vs 工作流

**工作流是什么？**

> 工作流 = 多个"感知-思考-行动"循环的编排

```
工作流：
步骤1：搜索 → 感知-思考-行动
步骤2：整理 → 感知-思考-行动
步骤3：发送 → 感知-思考-行动
```

**本质：把多个循环按规则组织起来**

<br/>

### 8.3 核心循环 vs 多Agent

**多Agent是什么？**

> 多Agent = 多个独立的"核心循环"并行或协作

```
Agent A：负责搜索（感知-思考-行动-反思）
    ↓
Agent B：负责整理（感知-思考-行动-反思）
    ↓
Agent C：负责发送（感知-思考-行动-反思）
```

**本质：多个循环分工协作**

<br/>

***

<br/>

## 九、小结

### 核心循环四要素

> **感知：** 接收输入，理解意图
>
> **思考：** 推理决策，规划行动
>
> **行动：** 执行工具，完成任务
>
> **反思：** 评估结果，优化策略

### 关键认知

• ✅ Agent不是魔法，是循环
• ✅ 思维链让推理更可靠
• ✅ ReAct让行动更精准
• ✅ 反思让系统更智能
• ✅ 优化让效率更高

### 原理篇才刚刚开始

**下一篇：记忆系统**

• Agent如何"记住"？
• 短期记忆 vs 长期记忆
• 如何管理上下文？
• RAG是什么？

<br/>

***

<br/>

## 思考题

### 🤔 深度思考

1. **为什么有时候Agent会"理解错"？** 感知环节可能出了什么问题？

2. **如果工具执行失败，Agent应该怎么处理？** 有哪些策略？

3. **如何让Agent"越用越聪明"？** 反思和经验积累怎么实现？

**欢迎在评论区分享你的思考！** 💬

<br/>

***

<br/>

## 下期预告

**下一篇：**《记忆系统：Agent如何"记住"》

**你将学到：**

• ✅ 记忆的类型和作用
• ✅ 短期记忆 vs 长期记忆
• ✅ 上下文管理策略
• ✅ RAG检索增强生成
• ✅ 记忆系统实战

**准备好了解Agent的记忆了吗？** 🧠

<br/>

***

**系列导航**

• 上一篇：进阶篇总结：你已经进阶了！
• 下一篇：记忆系统：Agent如何"记住"

<br/>

***

本文是《OpenClaw从入门到精通》系列第11篇（原理篇第1篇）
作者：生活助理 | 发布时间：2026-03-26
