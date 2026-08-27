# 本地大模型知识库系统

一个完全本地化的AI知识库问答系统，数据不出域，隐私有保障。

## 技术栈

- **大模型**：Ollama（支持 Llama3、Qwen、DeepSeek 等）
- **向量数据库**：ChromaDB（轻量级、无需额外部署）
- **Embedding**：Sentence-Transformers（all-MiniLM-L6-v2）
- **框架**：LangChain（编排大模型与向量检索）
- **Web界面**：Flask + HTML/CSS

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 安装 Ollama

根据你的操作系统安装 Ollama：

- **macOS**：`brew install ollama`
- **Linux**：`curl -fsSL https://ollama.com/install.sh | sh`
- **Windows**：下载 https://ollama.com/download

### 3. 下载大模型

```bash
ollama pull llama3:8b
```

### 4. 启动命令行模式

```bash
cd source-code
python src/main.py
```

### 5. 启动 Web 界面

```bash
cd source-code
python web/app.py
```

然后访问 http://localhost:5000

## 项目结构

```
source-code/
├── config/
│   └── config.py          # 配置管理
├── data/
│   ├── chroma_db/         # 向量数据库存储
│   └── docs/              # 知识库文档目录
├── src/
│   ├── __init__.py
│   ├── main.py            # 主入口（命令行模式）
│   ├── config.py          # 配置类
│   ├── utils.py           # 工具函数
│   ├── embedding.py       # Embedding模型封装
│   ├── document_processor.py  # 文档加载与分割
│   ├── vector_db.py       # 向量数据库封装
│   └── rag.py             # RAG核心逻辑
├── web/
│   ├── app.py             # Flask Web应用
│   └── templates/
│       └── index.html     # 前端界面
├── requirements.txt       # 依赖清单
└── .env.example           # 环境变量示例
```

## 使用方法

### 添加文档

将你的文档放入 `data/docs/` 目录，支持以下格式：
- `.txt`：纯文本文件
- `.md`：Markdown 文件
- `.pdf`：PDF 文件
- `.docx`：Word 文件

### 构建知识库

启动 Web 界面后，点击"重建知识库"按钮，系统会自动加载并处理文档。

### 提问

在 Web 界面输入问题，系统会基于知识库内容进行回答，并标注参考来源。

## 配置说明

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

配置项说明：

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| OLLAMA_MODEL | llama3:8b | 使用的大模型名称 |
| EMBEDDING_MODEL | all-MiniLM-L6-v2 | 使用的Embedding模型 |
| CHROMA_DB_PATH | ./data/chroma_db | 向量数据库存储路径 |
| DOCS_PATH | ./data/docs | 文档目录路径 |
| MAX_DOC_LENGTH | 500 | 文档片段最大长度 |
| TOP_K_RESULTS | 3 | 检索返回的最大结果数 |
| SIMILARITY_THRESHOLD | 0.7 | 相似度阈值 |
| FLASK_HOST | 0.0.0.0 | Web服务绑定地址 |
| FLASK_PORT | 5000 | Web服务端口 |

## 常见问题

### Q: 模型下载太慢怎么办？

A: 可以设置 Ollama 镜像源：
```bash
export OLLAMA_HOST=https://ollama.cn
```

### Q: 内存不足怎么办？

A: 使用更小的模型，如 `qwen:0.5b` 或 `phi3:3.8b`

### Q: 如何更换模型？

A: 修改 `.env` 文件中的 `OLLAMA_MODEL` 配置，然后重启服务。

## License

MIT