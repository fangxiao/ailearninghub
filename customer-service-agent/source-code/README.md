# 客服Agent实战项目

基于大模型构建的生产级智能客服系统，配套《客服Agent实战系列》14篇文章。

**GitHub 仓库**：[https://github.com/fangxiao/customer-service-agent](https://github.com/fangxiao/customer-service-agent)

## 项目结构

```
customer-service-agent/
├── config/                              # 配置文件
│   ├── base.yaml                        # 基础配置
│   ├── customer_service.yaml            # 客服专用配置
│   └── prompts/system_prompt.md          # System Prompt
├── data/                                # 数据文件
│   ├── faq.json                         # FAQ知识库
│   ├── intents.json                     # 意图定义
│   ├── sentiments.json                  # 情感词典
│   └── user_memory.json                 # 用户记忆存储
├── plugins/                             # 插件模块
│   ├── intent_recognition/              # 意图识别
│   ├── knowledge_base/                  # 关键词知识库
│   ├── sentiment_analysis/              # 情感分析
│   ├── order_query/                     # 订单查询（第7篇）
│   ├── vector_kb/                       # 向量知识库（第9篇）
│   ├── function_calling/                # Function Calling（第10篇）
│   └── multi_agent/                     # 多Agent路由（第11篇）
├── src/                                 # 核心模块
│   ├── bot.py                           # 主Bot类
│   ├── dialog_manager.py                # 对话管理（第5、8篇）
│   ├── user_memory.py                   # 用户记忆（第12篇）
│   └── evaluator.py                     # 效果评估（第13篇）
└── requirements.txt
```

## 快速开始

### 1. 进入项目目录

```bash
cd /Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/source-code
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行主Bot测试

```bash
python3 src/bot.py
```

这将执行 [bot.py](src/bot.py) 中的测试用例，依次演示：
- 问候 → 个性化回复
- 订单查询 → 调用订单插件
- 多轮对话 → 槽位填充
- 情绪激动 → 情感分析转人工
- FAQ → 向量检索
- 状态查询 → 评估指标

### 4. 启动 Web 界面（推荐）

#### 启动服务

```bash
# 确保在 source-code 目录下
cd /Users/admin/project/lovely/platform/doc/prototype/customer-service-agent/source-code

# 启动 Web 服务器
python3 web/app.py
```

看到以下输出表示启动成功：
```
==================================================
  客服Agent Web界面已启动
  访问: http://127.0.0.1:5000
  按 Ctrl+C 停止
==================================================
```

#### 访问界面

打开浏览器，访问：**http://127.0.0.1:5000**

#### Web 界面功能

| 功能 | 说明 |
|------|------|
| 💬 实时对话 | 在输入框输入问题，按回车或点击发送按钮 |
| ⚡ 快捷按钮 | 点击预设问题快速发送：订单查询/退款咨询/订购花束/投诉建议 |
| 📊 会话信息 | 右侧面板实时显示：用户ID、识别意图、对话轮数、响应时间、用户画像 |
| 🔄 重置对话 | 点击右上角"重置对话"或右侧"清空对话"按钮 |

#### API 接口说明

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/chat` | POST | 发送消息，返回 Bot 回复 |
| `/api/status` | GET | 获取当前会话状态 |
| `/api/reset` | POST | 重置对话历史 |
| `/api/health` | GET | 健康检查 |

#### 手动测试 API

```bash
# 发送消息
curl -X POST http://127.0.0.1:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "如何退款？", "user_id": "test_user"}'

# 查询状态
curl http://127.0.0.1:5000/api/status

# 重置对话
curl -X POST http://127.0.0.1:5000/api/reset
```

### 5. 单独测试某个模块

```bash
# 测试对话管理
python3 src/dialog_manager.py

# 测试用户记忆
python3 src/user_memory.py

# 测试效果评估
python3 src/evaluator.py

# 测试订单查询
python3 plugins/order_query/plugin.py

# 测试向量检索
python3 plugins/vector_kb/plugin.py

# 测试Function Calling
python3 plugins/function_calling/plugin.py
```

### 6. 查看配套文章

```bash
# 在文章目录启动HTTP服务器
cd /Users/admin/project/lovely/platform/doc/prototype/customer-service-agent
python3 -m http.server 8080

# 浏览器访问
# http://localhost:8080/客服Agent实战系列-14-公众号版.html
```

### 6. 接入真实大模型API（可选）

当前代码使用规则匹配模拟，无需API Key。如需接入真实大模型：

1. 编辑 `config/customer_service.yaml`，设置：
```yaml
llm:
  provider: zhipu    # 或 ollama
  model: glm-5.1-flash
```

2. 设置环境变量：
```bash
export ZHIPU_API_KEY="your-api-key"
```

3. 在 `src/bot.py` 的 `_call_llm` 方法中调用真实API。

## 功能模块

| 模块 | 文件 | 功能说明 |
|------|------|----------|
| 对话管理 | `src/dialog_manager.py` | 多轮对话、槽位填充、指代消解 |
| 意图识别 | `plugins/intent_recognition/` | 关键词+规则匹配识别用户意图 |
| 情感分析 | `plugins/sentiment_analysis/` | 5级情感识别，愤怒时转人工 |
| 订单查询 | `plugins/order_query/` | 数据库/API查询订单状态 |
| 知识库 | `plugins/knowledge_base/` | 关键词匹配FAQ |
| 向量检索 | `plugins/vector_kb/` | Embedding语义检索+关键词降级 |
| Function Calling | `plugins/function_calling/` | 大模型自主选择工具 |
| 多Agent | `plugins/multi_agent/` | 路由Agent协调多个子Agent |
| 用户记忆 | `src/user_memory.py` | 用户画像、分群、个性化推荐 |
| 效果评估 | `src/evaluator.py` | 意图准确率、解决率、满意度等指标 |

## 系列文章对照

| 篇号 | 文章主题 | 核心代码 |
|------|---------|---------|
| 01 | 客服Agent初体验 | `src/bot.py` 基础框架 |
| 02 | 配置与初始化 | `config/` |
| 03 | 意图识别 | `plugins/intent_recognition/` |
| 04 | 知识库 | `plugins/knowledge_base/` |
| 05 | 对话管理 | `src/dialog_manager.py` |
| 06 | 情感分析 | `plugins/sentiment_analysis/` |
| 07 | 订单查询插件 | `plugins/order_query/` |
| 08 | 多轮对话进阶 | `src/dialog_manager.py` 槽位/指代 |
| 09 | 知识库增强 | `plugins/vector_kb/` |
| 10 | Function Calling | `plugins/function_calling/` |
| 11 | 多Agent协作 | `plugins/multi_agent/` |
| 12 | 用户记忆 | `src/user_memory.py` |
| 13 | 效果评估 | `src/evaluator.py` |
| 14 | 架构总结 | 整体整合 `src/bot.py` |

## License

MIT
