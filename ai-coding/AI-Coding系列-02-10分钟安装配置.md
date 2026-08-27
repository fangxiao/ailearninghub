# 10分钟安装配置，开始你的 AI 编程之旅

阅读时间：10分钟
难度等级：⭐ 零基础
你将收获：完成 Claude Code 安装配置，运行第一个示例

<br/>

***

<br/>

## 回顾：AI Coding 的核心概念

**上一篇我们讲到了：**

```
1. AI Coding 是什么？
   └─ 从"写代码"变成"描述需求"

2. AI Coding Agent 有哪些？
   ├─ 国际：Claude Code、Copilot、Cursor
   └─ 国内：通义灵码、CodeGeeX、MarsCode

3. 为什么本系列用 Claude Code？
   ├─ 模型灵活（最重要）
   ├─ 国内友好
   └─ 功能全面
```

<br/>

**但是，光知道概念还不够：**

```
问题1：有了工具，用哪个模型？
├─ Claude 官方模型？需要代理，价格高
├─ 国内模型？不知道选哪个
└─ 如何配置？一脸茫然

问题2：会不会很贵？
├─ 按 Token 计费？怕用超了
├─ 订阅套餐？不知道哪个合适
└─ 免费方案？够不够用？

问题3：怎么开始？
├─ 注册什么账号？
├─ 获取什么密钥？
└─ 怎么配置到工具里？
```

<br/>

**本篇回答这些问题，带你完成第一步实践：**

```
本篇内容：
1. 什么是 Coding Plan（订阅套餐）
2. Coding Plan 支持哪些工具
3. 为什么继续用 Claude Code 讲解
4. 选择适合你的 Coding Plan
5. 注册并获取 API Key
6. 安装配置 Claude Code
7. 运行第一个示例
```

<br/>

***

<br/>

## 一、什么是 Coding Plan？

**Coding Plan = AI 编程订阅套餐**

```
传统方式：
按 Token 计费，用多少付多少
⚠️ 价格不透明，容易超支
⚠️ 需要持续监控用量

Coding Plan（推荐）：
固定月费 + 额度/请求数
✅ 预算可控，不用担心超支
✅ 额度充足，正常使用无忧
✅ 功能完整，支持高级特性
```

<br/>

**为什么 2026 年推荐 Coding Plan？**

```
1. 成本可控
   - 固定月费，预算明确
   - 新客特惠（3.9-9.9元首月）
   
2. 额度充足
   - 轻度用户：1-9万次请求/月
   - 重度用户：无限次或超大额度
   
3. 国内友好
   - 无需代理
   - 支付方便（支付宝/微信）
   - 中文支持完善
   
4. 功能完整
   - 多模型切换
   - API 访问
   - 高级特性支持
```

<br/>

***

<br/>

## 二、Coding Plan 支持哪些 Coding 工具？

**主流 AI 编程工具对比（2026年3月）：**

| 工具 | 公司 | 定位 | 特点 | 模型支持 | 价格 |
|------|------|------|------|---------|------|
| **Claude Code** | Anthropic | CLI Agent | 模型灵活、深度理解 | 可配置多模型 | 免费软件 |
| **GitHub Copilot** | 微软 | IDE 补全 | 生态成熟、VS Code 集成 | 固定模型 | $10/月 |
| **Cursor** | 独立 | AI IDE | IDE 体验好、功能强 | 可配置多模型 | $20/月 |
| **通义灵码** | 阿里 | IDE 补全 | 开箱即用、阿里云集成 | 固定（通义） | 免费 |
| **CodeGeeX** | 智谱 | IDE 补全 | 完全免费、简单易用 | 固定（CodeGeeX） | 免费 |
| **MarsCode** | 字节 | IDE 补全 | 新产品、功能全 | 固定（豆包） | 免费 |

<br/>

**这些工具如何与 Coding Plan 配合？**

```
情况1：IDE 补全类（Copilot、通义灵码、CodeGeeX）
- 通常有自己的模型服务
- 不需要额外购买 Coding Plan
- 但功能相对单一（主要是补全）

情况2：CLI Agent 类（Claude Code、Cursor）
- 需要配置大模型 API
- 可以使用 Coding Plan 的 API Key
- 功能更强大（对话、理解、多文件编辑）

情况3：组合使用
- 快速补全：通义灵码/CodeGeeX（免费）
- 复杂任务：Claude Code + Coding Plan
```

<br/>

***

<br/>

## 三、开始配置：选择 Coding Plan

**国内主流 AI 编程平台在 2026 年已形成成熟的 Coding Plan 套餐模式：**
- <span class="key">固定月费</span> + 额度/请求数
- 覆盖<span class="key">个人、团队、重度开发</span>等场景

<br/>

### 3.1 阿里云百炼（性价比之王）

```
Pro 版：200元/月（9万次请求/月，周上限4.5万次，5小时滑动窗口6000次）
新客特惠：首月39.9元，次月100元，第三月起200元

核心优势：
✅ 聚合 Qwen、GLM、Kimi、MiniMax 等多模型
✅ 兼容 OpenAI 协议，国内访问快
✅ 一个账号，多种模型切换

适合：
- 预算有限、需要多模型切换
- 日常开发的个人/小团队
```

<br/>

### 3.2 火山方舟（Claude Code 原生支持）

```
Lite 版：40元/月
Pro 版：200元/月
新客活动：首月约8.91元

核心优势：
✅ 原生支持 Anthropic 协议（Claude Code 无需代理）
✅ Auto 智能选模型
✅ 支持豆包编程模型 + DeepSeek

适合：
- Claude Code 重度用户
- 追求开箱即用的开发者
```

<br/>

### 3.3 智谱 GLM（功能最全）

```
Lite：49元/月（每5小时80 prompts，周约400）
Pro：149元/月
Max：469元/月

核心优势：
✅ GLM-5.1 模型，支持 MCP（AI 接管电脑）
✅ 20+ IDE 兼容
✅ 代码仓库检索

适合：
- 职业开发者
- 追求工具兼容性与全功能的团队
```

<br/>

### 3.4 其他平台对比

| 平台 | 入门价 | 首月特惠 | 核心亮点 | 适合人群 |
|------|--------|---------|---------|---------|
| MiniMax | 29元/月 | 9.9元 | 入门价低、M2.7 编程强 | 轻度个人、新手 |
| 百度千帆 | 40元/月 | 9.9元 | 新客低价、文心生态 | 学生、新手 |
| Kimi | 79元/月 | 无 | 代码能力顶尖、长文本 | 重度代码开发 |
| 科大讯飞 | 3.9元/月 | 3.9元 | Token 额度超大 | 批量/高频编程 |

<br/>

**快速推荐：**

```
新手/学生：MiniMax 或 百度千帆（首月9.9元试水）
Claude Code 用户：火山方舟（原生支持，8.91元首月）
多模型需求：阿里云百炼（39.9元首月）
专业开发：智谱 GLM（49元/月）或 Kimi（79元/月）
高频编程：科大讯飞星辰（Token 额度最大）
```

<br/>

***

<br/>

## 四、注册并获取 API Key

**注册流程大同小异，这里以阿里云百炼为例：**

```
1. 访问平台
   https://bailian.console.aliyun.com/

2. 登录/注册
   - 阿里云账号或支付宝扫码

3. 开通服务
   - 选择 Pro 版 ¥200/月
   - 新客首月39.9元

4. 获取 API Key
   - 进入"API-KEY管理"
   - 点击"创建新密钥"
   - 复制保存（只显示一次！）
```

<br/>

**其他平台快速入口：**

| 平台 | 地址 | 价格 | 特点 |
|------|------|------|------|
| 火山方舟 | volcengine.com/product/ark | 8.91元首月 | Claude Code 原生支持 |
| 智谱 AI | open.bigmodel.cn | 49元/月起 | 功能最全 |
| 百度千帆 | console.bce.baidu.com/qianfan | 9.9元首月 | 新客超低价 |
| MiniMax | minimaxi.com | 9.9元首月 | 入门价最低 |
| Kimi | platform.moonshot.cn | 79元/月 | 代码能力强 |
| 科大讯飞 | xingchen.xfyun.cn | 3.9元起 | Token 额度大 |

<br/>

**⚠️ API Key 安全提示：**

```
✅ 妥善保管，不要泄露
✅ 不要提交到 Git 仓库
✅ 可以随时重新生成
❌ 不要在代码中硬编码
```

<br/>

***

<br/>

## 五、安装 Claude Code

### 5.1 通过 npm 安装（推荐）

**前提条件：**

```bash
# 检查 Node.js 版本
node --version

# 需要 Node.js 18+
# 如果没有，先安装 Node.js
```

<br/>

**安装命令：**

```bash
# 全局安装
npm install -g @anthropic-ai/claude-code

# 或使用 yarn
yarn global add @anthropic-ai/claude-code
```

<br/>

**验证安装：**

```bash
# 检查版本
claude --version

# 应该输出类似：
# claude-code v1.x.x
```

<br/>

### 5.2 其他安装方式

**macOS (Homebrew):**

```bash
brew tap anthropic-ai/claude-code
brew install claude-code
```

<br/>

**Windows (Scoop):**

```bash
scoop bucket add anthropic-ai https://github.com/anthropic-ai/scoop-bucket
scoop install claude-code
```

<br/>

**Linux:**

```bash
# 使用 npm
npm install -g @anthropic-ai/claude-code

# 或下载二进制
curl -fsSL https://claude.ai/install.sh | sh
```

<br/>

***

<br/>

## 六、配置模型

### 6.1 配置智谱 GLM（推荐）

**创建配置文件：**

```bash
# 创建配置目录
mkdir -p ~/.config/claude-code

# 创建配置文件
nano ~/.config/claude-code/config.json
```

<br/>

**配置内容：**

```json
{
  "model": "glm-4-plus",
  "api_key": "zhipu-api-key-你的密钥",
  "base_url": "https://open.bigmodel.cn/api/paas/v4",
  "max_tokens": 4096,
  "temperature": 0.7
}
```

<br/>

**或使用环境变量（更安全）：**

```bash
# 编辑 shell 配置文件
nano ~/.zshrc  # 或 ~/.bashrc

# 添加环境变量
export ZHIPU_API_KEY="zhipu-api-key-你的密钥"
export CLAUDE_MODEL="glm-4-plus"
export CLAUDE_BASE_URL="https://open.bigmodel.cn/api/paas/v4"

# 使配置生效
source ~/.zshrc
```

<br/>

### 6.2 配置通义千问

**配置文件：**

```json
{
  "model": "qwen-max",
  "api_key": "sk-你的密钥",
  "base_url": "https://dashscope.aliyuncs.com/api/v1",
  "max_tokens": 4096,
  "temperature": 0.7
}
```

<br/>

**环境变量：**

```bash
export DASHSCOPE_API_KEY="sk-你的密钥"
export CLAUDE_MODEL="qwen-max"
export CLAUDE_BASE_URL="https://dashscope.aliyuncs.com/api/v1"
```

<br/>

### 6.3 配置验证

**测试命令：**

```bash
# 运行 Claude Code
claude

# 应该看到欢迎界面
# ╭─────────────────────────────────────╮
# │ Welcome to Claude Code!            │
# │ Model: glm-4-plus                  │
# │ Ready to help you code! 🚀         │
# ╰─────────────────────────────────────╯
```

<br/>

***

<br/>

## 七、运行第一个示例

### 7.1 启动 Claude Code

**在终端中运行：**

```bash
# 进入项目目录
cd ~/projects

# 启动 Claude Code
claude
```

<br/>

### 7.2 第一个代码生成

**输入提示词：**

```
你：写一个 Python 函数，计算斐波那契数列的第 n 项
```

<br/>

**Claude Code 的回复：**

```python
def fibonacci(n: int) -> int:
    """
    计算斐波那契数列的第 n 项
    
    Args:
        n: 项数（从 0 开始）
    
    Returns:
        斐波那契数列的第 n 项
    
    Examples:
        >>> fibonacci(0)
        0
        >>> fibonacci(10)
        55
    """
    if n < 0:
        raise ValueError("n 必须是非负整数")
    if n <= 1:
        return n
    
    # 使用迭代方式，效率更高
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


# 测试
if __name__ == "__main__":
    print(f"第 10 项: {fibonacci(10)}")  # 输出: 55
    print(f"第 20 项: {fibonacci(20)}")  # 输出: 6765
```

<br/>

**解释代码：**

```
你：解释一下这段代码的原理

Claude：
这段代码使用迭代方式计算斐波那契数列：

1. 边界处理
   - n < 0：抛出异常
   - n <= 1：直接返回 n（0 或 1）

2. 迭代计算
   - 初始化 a=0, b=1
   - 循环计算下一个值
   - 时间复杂度 O(n)
   - 空间复杂度 O(1)

3. 优点
   - 比递归效率高
   - 不会栈溢出
   - 空间占用小
```

<br/>

### 7.3 保存代码

**创建文件：**

```bash
# 在 Claude Code 中
你：把这个函数保存到 fib.py 文件

Claude：
已创建 fib.py 文件，代码如下：
[显示代码]

你可以运行测试：
python fib.py
```

<br/>

**验证运行：**

```bash
# 在另一个终端
python fib.py

# 输出：
# 第 10 项: 55
# 第 20 项: 6765
```

<br/>

***

<br/>

## 常见问题

### Q1：配置文件在哪？

```
位置：
~/.config/claude-code/config.json

或使用环境变量：
~/.zshrc 或 ~/.bashrc
```

<br/>

### Q2：如何切换模型？

```bash
# 临时切换
export CLAUDE_MODEL="glm-4"

# 永久切换
# 编辑配置文件，修改 model 字段
```

<br/>

### Q3：Coding Plan 和 Token 计费的区别？

```
Coding Plan（推荐）：
✅ 固定费用（¥99/月）
✅ 无限次请求
✅ 不用担心用超
✅ 预算可控

Token 计费：
⚠️ 按使用量计费
⚠️ 可能产生高额费用
⚠️ 需要监控用量
✅ 适合轻度使用
```

<br/>

### Q4：API Key 泄露了怎么办？

```
1. 立即在平台上重新生成
2. 删除旧的 Key
3. 更新配置文件
4. 检查账单是否有异常
```

<br/>

### Q5：能否同时配置多个模型？

```
可以！使用不同的环境变量：

# GLM-5
export GLM_API_KEY="xxx"

# 通义千问
export QWEN_API_KEY="xxx"

# 在配置中动态选择
```

<br/>

***

<br/>

## 八、最佳实践

### 8.1 安全建议

```
✅ 使用环境变量存储 API Key
✅ 不要把 API Key 提交到 Git
✅ 定期更换 API Key
✅ 使用 .gitignore 排除配置文件
❌ 不要在代码中硬编码 API Key
```

<br/>

### 8.2 性能优化

```
1. 选择合适的模型
   - 简单任务：glm-4-flash（快）
   - 复杂任务：glm-4-plus（强）

2. 调整参数
   - max_tokens：控制输出长度
   - temperature：控制创造性（0.7 适中）

3. 使用缓存
   - 相同问题不重复请求
   - 节省请求次数
```

<br/>

### 8.3 成本控制

```
Coding Plan 用户：
✅ 不用担心成本
✅ 随意使用
✅ 固定预算

Token 计费用户：
⚠️ 监控使用量
⚠️ 设置预算提醒
⚠️ 优化提示词减少 token
```

<br/>

***

<br/>

## 总结

### 安装流程回顾

```
1. 选择 Coding Plan
   └─ 新手：百度千帆/MiniMax（9.9元首月）
   └─ Claude Code 用户：火山方舟（8.91元首月）
   └─ 专业开发：智谱 GLM/Kimi（49-79元/月）

2. 注册并获取 API Key
   └─ 根据选择的平台完成注册 → 开通套餐 → 获取 Key

3. 安装 Claude Code
   └─ npm install -g @anthropic-ai/claude-code

4. 配置模型
   └─ 编辑 config.json 或设置环境变量

5. 运行第一个示例
   └─ claude → 输入提示词 → 查看结果
```

<br/>

### 推荐配置（按人群）

**新手/学生：**
```
平台：百度千帆 Lite 或 MiniMax Starter
价格：9.9元首月
特点：低成本试水，门槛极低
```

**Claude Code 用户：**
```
平台：火山方舟 Lite
价格：8.91元首月 → 40元/月
特点：原生支持，无需代理，开箱即用
```

**日常开发者：**
```
平台：阿里云百炼 Pro
价格：39.9元首月 → 200元/月
特点：多模型聚合，性价比最高
```

**专业开发者：**
```
平台：智谱 GLM Lite 或 Kimi Moderato
价格：49-79元/月
特点：功能全、能力强，支持高级特性
```

<br/>

***

<br/>

**系列导航**

• 上一篇：AI Coding 是什么？从手动编程到 AI 辅助
• 下一篇：基础操作：5个必会命令

<br/>

***

<br/>

本文是《AI Coding 从入门到精通》系列第2篇  
作者：生活助理 | 发布时间：2026-03-31

**配置完成！开始你的 AI 编程之旅！** 🚀
