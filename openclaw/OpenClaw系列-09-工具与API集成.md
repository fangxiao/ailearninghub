# 接入外部世界：工具与API集成

阅读时间：22分钟
难度等级：⭐⭐⭐⭐ 进阶篇
你将收获：学会集成外部工具，扩展能力边界

<br/>

***

<br/>

## 为什么要学工具集成？

前三篇你学会了Skill 开发、工作流、多Agent协作，但可能还有疑问：

• "怎么让龙虾搜索网络？"
• "怎么连接公司的数据库？"
• "怎么调用第三方API？"
• "能接入多少外部服务？"

答案是：**工具与API集成**

**学会工具集成后你会发现：**

• ✅ 能力无限扩展
• ✅ 连接真实世界
• ✅ 获取实时数据
• ✅ 操作外部系统

<br/>

***

<br/>

## 一、OpenClaw工具体系

### 1.1 工具分类

**内置工具：**

• 🔍 **搜索工具**：网络搜索
• 📁 **文件工具**：文件读写
• 💻 **代码工具**：代码执行
• 🖼️ **图片工具**：图片处理

<br/>

**自定义工具：**

• 你开发的工具
• 完全定制
• 满足特定需求

<br/>

**第三方工具：**

• 外部API封装
• 云服务集成
• 企业系统对接

<br/>

### 1.2 工具 vs Skill

| 维度 | 工具 | Skill |
|------|------|------|
| 定位 | 原子能力 | 组合能力 |
| 复杂度 | 单一功能 | 多步骤流程 |
| 调用方式 | Function Calling | 工作流编排 |
| 示例 | 搜索、发邮件 | 日报生成 |

**简单理解：**

> **工具** = 单个动作（如"搜索"）
> **Skill** = 多个工具的组合（如"搜索 + 整理 + 发送"）

<br/>

***

<br/>

## 二、Function Calling详解

### 2.1 什么是Function Calling？

**概念：LLM主动调用函数的能力**

传统方式：

```
用户 → LLM → 文本回复
```

Function Calling：

```
用户 → LLM → 决定调用工具 → 执行工具 → 返回结果 → LLM → 最终回复
```

<br/>

### 2.2 工作原理

**完整流程：**

```
┌─────────────────────────────────────────────────┐
│  1. 用户提问："北京今天天气怎么样？"             │
└─────────────────────┬───────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  2. LLM分析：需要调用天气工具                    │
│     工具名：get_weather                          │
│     参数：city="北京"                            │
└─────────────────────┬───────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  3. 系统执行工具：调用天气API                    │
│     返回：{temp: 25, weather: "晴"}             │
└─────────────────────┬───────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  4. LLM生成回复：                                │
│     "北京今天天气晴朗，气温25度，适合出门哦！"   │
└─────────────────────────────────────────────────┘
```

<br/>

### 2.3 工具定义

**标准格式：**

```python
@tool
def get_weather(city: str) -> dict:
    """
    查询城市天气
    
    Args:
        city: 城市名称，如"北京"、"上海"
    
    Returns:
        包含温度、天气等信息的字典
    """
    # 实现代码
    pass
```

**关键要素：**

• ✅ **函数名**：清晰描述功能
• ✅ **参数类型**：明确每个参数类型
• ✅ **文档字符串**：详细说明用途
• ✅ **返回值**：明确返回格式

<br/>

### 2.4 参数自动填充

**LLM会自动理解并填充参数：**

用户输入：

```
帮我查一下上海明天会下雨吗
```

LLM自动提取：

```json
{
  "tool": "get_weather",
  "params": {
    "city": "上海",
    "date": "明天"
  }
}
```

<br/>

***

<br/>

## 三、实战1：集成搜索API

### 3.1 需求分析

**目标：让龙虾能搜索网络**

• 输入：搜索关键词
• 输出：搜索结果摘要

<br/>

### 3.2 选择搜索API

**常用搜索API：**

| API | 特点 | 价格 |
|-----|------|------|
| Brave Search | 免费额度大 | 免费/月3000次 |
| Serper | 速度快 | $50/月5000次 |
| Google Custom | 结果精准 | $5/1000次 |
| Bing Search | 微软生态 | 免费/月1000次 |

**推荐：Brave Search（免费够用）**

<br/>

### 3.3 实现代码

**创建搜索工具：search_tool.py**

```python
import requests
from openclaw import tool

@tool
def web_search(query: str, count: int = 5) -> str:
    """
    搜索网络信息
    
    Args:
        query: 搜索关键词
        count: 返回结果数量，默认5条
    
    Returns:
        搜索结果摘要
    """
    # API配置
    api_key = "YOUR_BRAVE_API_KEY"
    url = "https://api.search.brave.com/res/v1/web/search"
    
    # 请求参数
    headers = {"X-Subscription-Token": api_key}
    params = {"q": query, "count": count}
    
    try:
        # 发送请求
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        # 解析结果
        data = response.json()
        results = []
        
        for item in data.get("web", {}).get("results", [])[:count]:
            results.append(f"""
标题：{item.get("title")}
链接：{item.get("url")}
摘要：{item.get("description")}
---""")
        
        return "\n".join(results)
    
    except Exception as e:
        return f"搜索失败：{str(e)}"
```

<br/>

### 3.4 注册使用

**注册工具：**

```bash
openclaw tool register search_tool.py
```

**测试调用：**

```
你：搜索一下 OpenClaw 最新动态
龙虾：让我搜索一下...
找到以下信息：
标题：OpenClaw 发布2.0版本
链接：https://...
摘要：新增多Agent协作功能...
```

<br/>

***

<br/>

## 四、实战2：集成数据库

### 4.1 需求分析

**目标：让龙虾能查询数据库**

• 支持MySQL、PostgreSQL、MongoDB
• 安全的SQL执行
• 结果格式化

<br/>

### 4.2 数据库工具

**创建数据库工具：database_tool.py**

```python
import pymysql
from openclaw import tool
from typing import Optional

@tool
def query_mysql(
    host: str,
    database: str,
    sql: str,
    user: Optional[str] = None,
    password: Optional[str] = None
) -> str:
    """
    查询MySQL数据库
    
    Args:
        host: 数据库地址
        database: 数据库名
        sql: SQL查询语句（仅支持SELECT）
        user: 用户名（可从环境变量读取）
        password: 密码（可从环境变量读取）
    
    Returns:
        查询结果的表格格式
    """
    # 安全检查：只允许SELECT
    if not sql.strip().upper().startswith("SELECT"):
        return "错误：只允许执行SELECT查询"
    
    try:
        # 连接数据库
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        with connection.cursor() as cursor:
            cursor.execute(sql)
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
        
        connection.close()
        
        # 格式化输出
        result = "| " + " | ".join(columns) + " |\n"
        result += "|" + "|".join(["---"] * len(columns)) + "|\n"
        
        for row in rows[:20]:  # 最多返回20条
            result += "| " + " | ".join(str(cell) for cell in row) + " |\n"
        
        return result
    
    except Exception as e:
        return f"查询失败：{str(e)}"
```

<br/>

### 4.3 安全考虑

**数据库工具的安全措施：**

• ✅ **只读操作**：限制只能SELECT
• ✅ **敏感信息**：从环境变量读取
• ✅ **结果限制**：最多返回20条
• ✅ **超时控制**：设置查询超时
• ✅ **日志记录**：记录所有查询

<br/>

***

<br/>

## 五、实战3：集成云服务

### 5.1 需求分析

**目标：让龙虾能操作云存储**

• 上传文件到OSS
• 下载文件从OSS
• 列出文件列表

<br/>

### 5.2 阿里云OSS工具

**创建OSS工具：oss_tool.py**

```python
import oss2
from openclaw import tool
import os

# 初始化OSS客户端
auth = oss2.Auth(
    os.getenv("OSS_ACCESS_KEY"),
    os.getenv("OSS_SECRET_KEY")
)
bucket = oss2.Bucket(auth, "oss-cn-shanghai.aliyuncs.com", "my-bucket")

@tool
def upload_to_oss(file_path: str, object_name: str) -> str:
    """
    上传文件到阿里云OSS
    
    Args:
        file_path: 本地文件路径
        object_name: OSS对象名称
    
    Returns:
        上传结果和文件URL
    """
    try:
        bucket.put_object_from_file(object_name, file_path)
        url = f"https://my-bucket.oss-cn-shanghai.aliyuncs.com/{object_name}"
        return f"上传成功！文件URL：{url}"
    except Exception as e:
        return f"上传失败：{str(e)}"

@tool
def download_from_oss(object_name: str, local_path: str) -> str:
    """
    从阿里云OSS下载文件
    
    Args:
        object_name: OSS对象名称
        local_path: 本地保存路径
    
    Returns:
        下载结果
    """
    try:
        bucket.get_object_to_file(object_name, local_path)
        return f"下载成功！保存到：{local_path}"
    except Exception as e:
        return f"下载失败：{str(e)}"

@tool
def list_oss_files(prefix: str = "") -> str:
    """
    列出OSS文件列表
    
    Args:
        prefix: 文件前缀筛选
    
    Returns:
        文件列表
    """
    try:
        files = []
        for obj in oss2.ObjectIterator(bucket, prefix=prefix):
            files.append(f"- {obj.key} ({obj.size} bytes)")
        return "\n".join(files[:50])  # 最多50条
    except Exception as e:
        return f"查询失败：{str(e)}"
```

<br/>

### 5.3 腾讯云COS工具

**类似实现，使用cos-python-sdk：**

```python
from qcloud_cos import CosConfig, CosS3Client

# 初始化客户端
config = CosConfig(
    Region="ap-shanghai",
    SecretId=os.getenv("COS_SECRET_ID"),
    SecretKey=os.getenv("COS_SECRET_KEY")
)
client = CosS3Client(config)

@tool
def upload_to_cos(file_path: str, key: str) -> str:
    """上传文件到腾讯云COS"""
    # 实现代码...
    pass
```

<br/>

***

<br/>

## 六、工具安全

### 6.1 权限控制

**工具级别的权限控制：**

```yaml
tools:
  web_search:
    permission: public  # 所有人可用
  
  query_database:
    permission: admin   # 仅管理员可用
  
  send_email:
    permission: user    # 登录用户可用
```

<br/>

### 6.2 敏感信息保护

**最佳实践：**

• ✅ **环境变量**：敏感信息存环境变量
• ✅ **加密存储**：密钥加密后存储
• ✅ **不记录日志**：敏感信息不入日志
• ✅ **定期轮换**：定期更换密钥

<br/>

### 6.3 审计日志

**记录所有工具调用：**

```yaml
audit:
  enabled: true
  log_file: /var/log/openclaw/tool_audit.log
  fields:
    - timestamp
    - user
    - tool_name
    - params  # 敏感参数脱敏
    - result_summary
    - duration
```

<br/>

***

<br/>

## 七、最佳实践

### 7.1 工具设计原则

**单一职责：**

```python
# ✅ 好的设计
@tool
def send_email(to: str, subject: str, body: str):
    """发送邮件"""
    pass

# ❌ 不好的设计
@tool
def send_email_and_sms_and_wechat(...):
    """发送邮件、短信、微信"""
    pass
```

<br/>

**清晰的参数：**

```python
# ✅ 好的设计
@tool
def search_product(
    keyword: str,
    category: str = None,
    min_price: float = None,
    max_price: float = None,
    sort_by: str = "relevance"
):
    """搜索商品"""
    pass

# ❌ 不好的设计
@tool
def search_product(params: dict):
    """搜索商品"""
    pass
```

<br/>

### 7.2 错误处理

**完善的错误处理：**

```python
@tool
def api_call(url: str) -> str:
    """调用API"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.Timeout:
        return "错误：请求超时，请稍后重试"
    except requests.HTTPError as e:
        return f"错误：HTTP错误 {e.response.status_code}"
    except requests.RequestException as e:
        return f"错误：网络请求失败 - {str(e)}"
    except Exception as e:
        return f"错误：未知错误 - {str(e)}"
```

<br/>

### 7.3 性能优化

**缓存策略：**

```python
from functools import lru_cache

@tool
@lru_cache(maxsize=100)
def get_exchange_rate(currency: str) -> float:
    """获取汇率（带缓存）"""
    # 缓存100个结果，避免重复请求
    pass
```

<br/>

**异步执行：**

```python
import asyncio
import aiohttp

@tool
async def batch_api_call(urls: list) -> list:
    """批量异步调用API"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)
```

<br/>

***

<br/>

## 八、常用工具推荐

### 8.1 信息获取类

| 工具 | 用途 | API |
|------|------|-----|
| 网络搜索 | 搜索信息 | Brave/Google |
| 天气查询 | 查天气 | OpenWeather |
| 新闻获取 | 获取新闻 | NewsAPI |
| 汇率查询 | 查汇率 | ExchangeRate |

<br/>

### 8.2 文件处理类

| 工具 | 用途 | 服务 |
|------|------|------|
| 云存储 | 文件上传下载 | OSS/COS |
| OCR识别 | 图片转文字 | 百度OCR |
| 文件转换 | 格式转换 | CloudConvert |
| 图片处理 | 压缩裁剪 | TinyPNG |

<br/>

### 8.3 通信类

| 工具 | 用途 | API |
|------|------|-----|
| 邮件发送 | 发邮件 | SMTP |
| 短信发送 | 发短信 | 阿里短信 |
| 微信推送 | 公众号推送 | 微信API |
| 钉钉通知 | 机器人通知 | 钉钉API |

<br/>

***

<br/>

## 九、小结

### 工具集成核心能力

> **Function Calling：**
> LLM主动调用工具的能力
>
> **API集成：**
> 连接外部服务的桥梁
>
> **安全控制：**
> 权限、加密、审计
>
> **性能优化：**
> 缓存、异步、批处理

### 关键要点

• ✅ 单一职责，功能明确
• ✅ 参数类型清晰
• ✅ 完善的错误处理
• ✅ 敏感信息保护
• ✅ 合理的性能优化

### 成就达成！

**你已经：**

• ✅ 理解Function Calling原理
• ✅ 集成了搜索API
• ✅ 集成了数据库
• ✅ 集成了云服务
• ✅ 掌握安全最佳实践

<br/>

***

<br/>

## 练习题

### 🎯 工具开发挑战

完成以下工具开发：

#### 挑战1：翻译工具

集成翻译API（百度/有道/DeepL）

#### 挑战2：地图工具

集成地图API，查询路线和地点

#### 挑战3：支付工具

集成支付宝/微信支付API

#### 挑战4：AI绘图工具

集成Midjourney/DALL-E API

**完成的同学，评论区分享你的工具代码！** 🎉

<br/>

***

<br/>

## 下期预告

**下一篇：**《进阶篇总结：你已经进阶了！》

**你将学到：**

• ✅ 进阶篇内容回顾
• ✅ 能力自测清单
• ✅ 接下来的学习路径
• ✅ 原理篇预告

**准备好进入原理篇了吗？** 🚀

<br/>

***

**系列导航**

• 上一篇：多Agent协作：1+1>2的魔法
• 下一篇：进阶篇总结：你已经进阶了！

<br/>

***

本文是《OpenClaw从入门到精通》系列第9篇
作者：生活助理 | 发布时间：2026-03-23
