# 客服Agent实战项目

基于 myAgent 框架构建的智能客服系统。

## 项目结构

```
customer-service-agent/
├── config/              # 配置文件
│   ├── base.yaml       # 基础配置（继承myAgent）
│   ├── customer_service.yaml  # 客服专用配置
│   └── prompts/        # 提示词模板
├── data/               # 数据文件
│   ├── faq.json        # FAQ知识库
│   ├── intents.json    # 意图定义
│   └── entities.json   # 实体词典
├── plugins/            # 客服专用插件
│   ├── intent_recognition/  # 意图识别
│   ├── knowledge_base/      # 知识库检索
│   ├── emotion_analysis/    # 情感分析
│   └── ticket_system/       # 工单系统
├── src/                # 核心代码
├── tests/              # 测试文件
├── web/                # Web接口
└── examples/           # 示例代码
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
export OPENAI_API_KEY="your-api-key"
# 或使用国内模型
export DASHSCOPE_API_KEY="your-dashscope-key"
```

### 3. 运行基础示例

```bash
python examples/basic_chat.py
```

### 4. 启动Web服务

```bash
python web/app.py
```

## 系列文章

本代码库配套《客服Agent实战系列》文章：

| 序号 | 标题 | 对应代码 |
|------|------|----------|
| 01 | 项目初始化 | `config/`, `requirements.txt` |
| 02 | Bot定义 | `src/bot.py` |
| 03 | 意图识别 | `plugins/intent_recognition/` |
| 04 | 知识库 | `plugins/knowledge_base/` |
| 05 | 对话管理 | `src/dialogue.py` |
| 06 | 回答生成 | `src/response.py` |
| 07 | 情感分析 | `plugins/emotion_analysis/` |
| 08 | 工单系统 | `plugins/ticket_system/` |
| 09 | Web接口 | `web/app.py` |
| 10 | 前端界面 | `web/templates/` |
| 11 | 测试调试 | `tests/` |
| 12 | 部署上线 | `Dockerfile` |
| 13 | 效果评估 | `scripts/evaluate.py` |
| 14 | 完整演示 | `examples/full_demo.py` |

## 前置知识

本系列基于 [myAgent开发系列](../myagent/) 构建，建议先学习：

- myAgent 04：项目初始化
- myAgent 06：Prompt工程
- myAgent 09-10：插件架构
- myAgent 12：LLM集成

## License

MIT
