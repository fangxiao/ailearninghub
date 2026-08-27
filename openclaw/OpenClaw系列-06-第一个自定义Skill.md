# 从0到1：开发你的第一个自定义 Skill

阅读时间：20分钟
难度等级：⭐⭐⭐ 进阶入门
你将收获：开发第一个自定义 skill，打开新世界

<br/>

***

<br/>

## 为什么要开发自定义 Skill？

前 **5** 篇你学会了安装、使用、配置和 Skills 管理，但可能还有疑问：

• "内置功能不够用怎么办？"
• "Skills 市场找不到想要的 skill？"
• "能开发自己的功能吗？"
• "开发 skill 难吗？"

答案是：**开发自定义 Skill**

**开发 Skill 后你会发现：**

• ✅ 功能无限扩展
• ✅ 完全个性化定制
• ✅ 可以分享给他人
• ✅ Skill 还能赚钱（Skills 市场）

<br/>

***

<br/>

## 一、什么是 Skill？

### 1.1 概念解释

**Skill = 工具 + 流程**

就像给 **龙虾** 安装新能力：

• 🔍 **搜索 Skill**：搜索网络信息
• 📊 **分析 Skill**：数据分析可视化
• 📧 **邮件 Skill**：发送管理邮件
• 🌤️ **天气 Skill**：查询天气预报

### 1.2 Skill 类型

**官方 Skill：**

• **OpenClaw** 内置
• 经过测试，稳定可靠
• 免费使用

**社区 Skill：**

• 开发者分享
• 种类丰富
• 大部分免费

**自定义 Skill：**

• 自己开发
• 完全定制
• 可分享或出售

### 1.3 Skill 结构

一个 skill 包含 **3** 个部分：

> **配置文件（skill.yaml）：**
> 定义 skill 名称、描述、参数
>
> **代码文件（skill.py）：**
> 实现具体功能的代码
>
> **文档文件（README.md）：**
> 使用说明和示例

<br/>

***

<br/>

## 二、开发环境准备

### 2.1 安装Python

#### 检查是否已安装：

打开终端/命令行，输入：

```bash
python --version
```

如果显示版本号（如 Python **3.9.0**），说明已安装。

#### 未安装？

**Windows：**

1. 访问 python.org/downloads/
2. 下载 **Python 3.9+**
3. 安装时勾选"**Add Python to PATH**"

**macOS：**

```bash
brew install python3
```

**Linux：**

```bash
sudo apt install python3 python3-pip
```

### 2.2 安装开发工具

#### 推荐IDE：

**VS Code**（推荐新手）：

• 免费开源
• 插件丰富
• 易于使用

**PyCharm**（专业开发）：

• 功能强大
• 智能提示
• 社区版免费

**Sublime Text**（轻量级）：

• 启动快速
• 界面简洁
• 适合小项目

### 2.3 创建 Skill 目录

#### 标准目录结构：

```
my-weather-skill/（skill 文件夹）
├── skill.yaml（配置文件）
├── skill.py（代码文件）
└── README.md（文档文件）
```

#### 创建步骤：

**Step 1：打开 OpenClaw Skills 目录**

```
~/.openclaw/skills/（macOS/Linux）
C:\Users\用户名\.openclaw\skills\（Windows）
```

**Step 2：创建 skill 文件夹**

新建文件夹：my-weather-skill

**Step 3：创建 3 个文件**

• skill.yaml
• skill.py
• README.md

<br/>

***

<br/>

## 三、实战：开发"天气查询" Skill

### 3.1 需求分析

#### 功能需求：

• **输入**：城市名（如"北京"）
• **输出**：天气信息（温度、天气、湿度等）
• **API**：使用免费天气API

#### 技术选型：

• 语言：**Python 3**
• API：OpenWeatherMap（免费）
• 库：requests（HTTP请求）

### 3.2 编写配置文件（skill.yaml）

#### 文件内容：

```yaml
name: weather
version: 1.0.0
description: 查询城市天气信息
author: 生活助理

parameters:
  - name: city
    type: string
    description: 城市名称
    required: true
    example: "北京"

returns:
  type: string
  description: 天气信息文本
```

#### 配置说明：

• **name**：skill 名称（唯一标识）
• **version**：版本号
• **description**：skill 描述
• **parameters**：输入参数定义
• **returns**：返回值定义

### 3.3 编写代码文件（skill.py）

#### 代码结构：

> **第1步：导入库**
> import requests
> from openclaw import Skill
>
> **第2步：定义 Skill 类**
> class WeatherSkill(Skill):
>     name = "weather"
>     description = "查询天气"
>
> **第3步：实现执行方法**
> def execute(self, city):
>     # 获取天气数据
>     weather_data = self.get_weather(city)
>     # 格式化输出
>     return self.format_weather(weather_data)
>
> **第4步：实现辅助方法**
> def get_weather(self, city):
>     # 调用天气API
>     # 返回数据
>     pass

#### 完整代码（简化版）：

**注意**：这里展示代码结构，实际开发需要完整实现

主要包含：

• 导入依赖库
• 定义 Skill 类
• 实现execute方法（主逻辑）
• 实现辅助方法（API调用、数据处理）
• 错误处理

### 3.4 编写文档文件（README.md）

#### 文档内容：

```markdown
# 天气查询 Skill

## 功能
查询指定城市的天气信息

## 使用方法
输入：天气 北京
输出：北京今天晴，温度15-25°C

## 参数说明
- city: 城市名称（必填）

## 示例
查询上海天气：天气 上海
查询广州天气：天气 广州
```

#### 文档说明：

• **功能介绍**：简要说明 skill 用途
• **使用方法**：如何调用 skill
• **参数说明**：输入参数详解
• **示例**：实际使用示例

<br/>

***

<br/>

## 四、测试 Skill

### 4.1 本地测试

#### 测试步骤：

**Step 1：注册 Skill**

在 **OpenClaw** 中注册 skill：

设置 → Skills 管理 → 添加 skill → 选择 skill 文件夹

**Step 2：测试调用**

在对话中输入：

```
天气 北京
```

**Step 3：查看输出**

预期输出：

```
北京今天晴，温度15-25°C，湿度45%，空气质量良好
```

### 4.2 调试技巧

#### 常见问题：

**问题1：Skill 加载失败**

原因：配置文件格式错误
解决：检查 **YAML** 格式，注意缩进

**问题2：API调用失败**

原因：网络问题或API Key错误
解决：检查网络连接和API Key

**问题3：返回数据格式错误**

原因：数据处理逻辑有问题
解决：添加调试日志，检查数据结构

#### 调试方法：

• **打印日志**：在关键位置添加print语句
• **单元测试**：编写测试用例验证功能
• **逐步调试**：分段测试，定位问题

### 4.3 优化改进

#### 可以改进的地方：

• ✅ 添加更多天气信息（风向、紫外线等）
• ✅ 支持多天预报
• ✅ 添加天气图标
• ✅ 支持语音播报
• ✅ 添加错误重试机制

<br/>

***

<br/>

## 五、部署使用

### 5.1 本地部署

#### 部署步骤：

**Step 1：Skill 已自动加载**

注册成功后，**OpenClaw** 会自动加载 skill

**Step 2：直接使用**

在任意对话中调用 skill

**Step 3：查看日志**

如需查看运行日志：

```
~/.openclaw/logs/skills.log
```

### 5.2 分享 Skill

#### 分享方式：

**方式1：分享给朋友**

1. 打包 skill 文件夹为ZIP
2. 发送给朋友
3. 朋友解压到 Skills 目录
4. 注册后即可使用

**方式2：上传到社区**

1. 访问 **OpenClaw** Skills 市场
2. 点击"发布 Skill"
3. 上传 skill 文件
4. 填写 skill 信息
5. 审核通过后所有人可用

**方式3：开源到 GitHub**

1. 创建 **GitHub** 仓库
2. 上传 skill 代码
3. 编写详细文档
4. 分享仓库链接

### 5.3 Skills 市场

#### 赚钱机会：

**OpenClaw** Skills 市场支持：

• **免费 Skill**：完全免费，积累用户
• **付费 Skill**：设置价格，用户购买
• **订阅 Skill**：按月收费，持续收入

#### 成功案例：

> **数据分析师小王：**
> 开发了"数据可视化" skill
> 定价 **¥99** /月
> **3个月** 获得 **200+** 付费用户
> 月收入 **¥2万+**

<br/>

***

<br/>

## 六、Skill 开发规范

### 6.1 命名规范

#### Skill 命名：

• 使用小写字母
• 用连字符分隔单词
• 简洁有意义

**✅ 好的命名：**

weather-query, pdf-converter, email-sender

**❌ 不好的命名：**

WeatherQuery, pdf_converter_v2, my-skill

### 6.2 错误处理

#### 必须处理的错误：

• ✅ 网络请求失败
• ✅ 参数缺失或错误
• ✅ API返回异常
• ✅ 数据格式不正确

#### 错误处理示例：

• 使用try-except捕获异常
• 返回友好的错误提示
• 记录错误日志

### 6.3 日志记录

#### 日志级别：

• **DEBUG**：调试信息
• **INFO**：正常运行信息
• **WARNING**：警告信息
• **ERROR**：错误信息

#### 日志最佳实践：

• 记录关键操作
• 记录错误详情
• 不要记录敏感信息
• 定期清理旧日志

<br/>

***

<br/>

## 七、进阶方向

### 7.1 更复杂的 Skill

#### 可以尝试开发：

• **邮件 Skill**：自动发送邮件
• **数据库 Skill**：查询数据库
• **爬虫 Skill**：抓取网页数据
• **文件处理 Skill**：批量处理文件
• **数据分析 Skill**：可视化分析

### 7.2 Skill 组合

#### 多个 skill 协同工作：

例如"新闻简报"工作流：

> **步骤1**：搜索 Skill → 获取新闻
> **步骤2**：分析 Skill → 提取要点
> **步骤3**：写作 Skill → 生成简报
> **步骤4**：邮件 Skill → 发送邮件

### 7.3 学习资源

#### 官方文档：

docs.openclaw.ai（完整开发文档）

#### 社区论坛：

community.openclaw.ai（开发者交流）

#### 视频教程：

B站搜索"**OpenClaw** Skill 开发"

#### 示例代码：

github.com/openclaw/skills（官方 skill 仓库）

<br/>

***

<br/>

## 八、小结

### 开发流程回顾

> **1. 需求分析** → 明确功能需求
> **2. 环境准备** → 安装工具，创建目录
> **3. 编写配置** → skill.yaml定义参数
> **4. 编写代码** → skill.py实现功能
> **5. 编写文档** → README.md说明用法
> **6. 测试调试** → 本地测试，修复问题
> **7. 部署分享** → 本地使用或分享

### 关键要点

• ✅ Skill = 配置 + 代码 + 文档
• ✅ 先简单后复杂
• ✅ 充分测试再发布
• ✅ 良好的错误处理
• ✅ 详细的文档说明

### 成就达成！

**你已经：**

• ✅ 理解 Skill 的概念和结构
• ✅ 搭建开发环境
• ✅ 完成第一个 skill 开发
• ✅ 掌握测试和部署方法
• ✅ 了解 Skills 市场机会

<br/>

***

<br/>

## 练习题

### 🎯 开发挑战

完成以下 skill 开发：

#### 挑战1：汇率查询 Skill

输入货币对（如USD/CNY），返回汇率信息

#### 挑战2：翻译 Skill

输入文本和目标语言，返回翻译结果

#### 挑战3：计算器 Skill

输入数学表达式，返回计算结果

#### 挑战4：二维码生成 Skill

输入文本，生成二维码图片

**完成的同学，评论区分享你的 skill！** 🎉

<br/>

***

<br/>

## 下期预告

**下一篇：**《Agent工作流：让龙虾自动干活》

**你将学到：**

• ✅ 什么是工作流？
• ✅ 工作流设计原则
• ✅ 实战：自动化日报
• ✅ 批量文件处理

**准备好让龙虾自动干活了吗？** 🚀

<br/>

***

**系列导航**

• 上一篇：认识 Skills 系统：默认 Skills 与管理
• 下一篇：Agent工作流：让龙虾自动干活

<br/>

***

本文是《OpenClaw从入门到精通》系列第6篇
作者：生活助理 | 发布时间：2026-03-20
