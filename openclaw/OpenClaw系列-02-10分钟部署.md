# 10分钟部署你的第一只"龙虾"

阅读时间：10分钟
难度等级：⭐ 零基础
你将收获：完成OpenClaw安装，执行第一个任务，获得成就感

<br/>

## 准备工作

### 电脑要求（很低）

**最低配置：**

• 操作系统：Windows 10+ / macOS 10.14+ / Linux
• 内存：4GB+
• 硬盘：2GB可用空间
• 网络：需要联网（首次下载）

**推荐配置：**

• 内存：8GB+
• CPU：4核+

<br/>

### 账号准备

根据你的选择，准备：

• **微信账号**（小程序方式）
• **GitHub账号**（开源版）
• **邮箱**（注册用）

<br/>

***

<br/>

## 3种安装方式

### 🚀 方式一：微信小程序（最快，0门槛）

**适合人群：**完全新手，想最快体验

**优点：**

• ✅ 0门槛，不用安装
• ✅ 随时随地使用
• ✅ 免费体验

**缺点：**

• ❌ 功能相对简单
• ❌ 不能操作本地文件
• ❌ 需要联网

<br/>

#### 安装步骤（2分钟）

**Step 1：打开微信**

在手机或电脑上打开微信

**Step 2：搜索小程序**

在搜索框输入：**QClaw**

**Step 3：点击进入**

找到"QClaw智能助手"，点击进入

**Step 4：授权登录**

点击"微信授权登录"，确认授权

**Step 5：开始使用**

进入主界面，看到输入框，可以开始用了！

**✅ 安装完成！**

<br/>

***

<br/>

### 💻 方式二：桌面应用（推荐）

**适合人群：**日常使用，需要处理本地文件

**优点：**

• ✅ 功能完整
• ✅ 可操作本地文件
• ✅ 响应更快
• ✅ 界面友好

**缺点：**

• ❌ 需要下载安装
• ❌ 占用一定硬盘空间

<br/>

#### Windows安装（5分钟）

**Step 1：下载安装包**

访问官网：openclaw.ai/download

点击"Windows下载"，选择：

• 标准版（推荐）：500MB，功能完整
• 精简版：200MB，基础功能

**Step 2：运行安装程序**

找到下载的 OpenClaw-Setup.exe，双击运行

**Step 3：选择安装位置**

默认：C:\Program Files\OpenClaw
建议：D:\OpenClaw（如果C盘空间不足）

**Step 4：选择组件**

✅ OpenClaw核心（必须）
✅ Python运行时（必须）
✅ 常用工具包（推荐）
⬜ 开发工具（按需）

**Step 5：等待安装**

安装进度条，大约2-3分钟

**Step 6：首次配置**

安装完成后，自动打开配置向导：

1. 选择语言：中文

2. 选择模型：

**国际模型：**
• GPT-5（最新，最强，需要API Key）
• GPT-4o（推荐，性价比高）
• Claude 3.5（推理能力强）

**国内模型：**
• 智谱GLM-4（国产最强，推荐）
• 文心一言4.0（百度出品）
• 通义千问（阿里出品）
• DeepSeek（性价比高）

**本地模型：**
• Llama 3（免费，需配置）
• Qwen（免费，中文友好）

3. 输入API Key：
• 如果有OpenAI API Key，输入
• 如果有智谱/百度/阿里账号，输入
• 如果没有，选择"稍后配置"

4. 完成：点击"开始使用"

**✅ 安装完成！**

<br/>

#### macOS安装（5分钟）

**Step 1：下载DMG**

访问官网：openclaw.ai/download

点击"macOS下载"

**Step 2：打开DMG文件**

找到 OpenClaw.dmg，双击打开

**Step 3：拖拽安装**

将OpenClaw图标拖到"Applications"文件夹

**Step 4：首次打开**

打开"应用程序"文件夹，找到OpenClaw，双击打开

**⚠️ 注意：**

首次打开可能提示"无法验证开发者"，解决方法：

1. 右键点击OpenClaw
2. 选择"打开"
3. 点击"打开"确认

**Step 5：配置（同Windows）**

**✅ 安装完成！**

<br/>

***

<br/>

### ⌨️ 方式三：命令行（极客）

**适合人群：**开发者，喜欢折腾

**优点：**

• ✅ 完全自定义
• ✅ 可编程控制
• ✅ 最新版本

**缺点：**

• ❌ 有学习曲线
• ❌ 需要技术背景

<br/>

#### macOS/Linux安装（5分钟）

**Step 1：安装依赖**

# macOS
brew install python3 git

# Ubuntu/Debian
sudo apt install python3 python3-pip git

# CentOS/RHEL
sudo yum install python3 python3-pip git

**Step 2：安装OpenClaw**

# 方式A：Homebrew（推荐）
brew install openclaw

# 方式B：pip安装
pip3 install openclaw

# 方式C：源码安装
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pip3 install -r requirements.txt
python3 setup.py install

**Step 3：初始化**

# 初始化配置
openclaw init

会提示：
? 请选择默认模型
  - GPT-5（需要OpenAI API Key）
  - GPT-4o（推荐，性价比高）
  - GLM-4（智谱，国内推荐）
  - 文心4.0（百度）
  - 通义千问（阿里）
  - 本地模型（免费）
? 请输入API Key (可选)
? 请选择数据存储位置 [默认: ~/.openclaw]

**Step 4：启动服务**

# 启动后台服务
openclaw start

# 查看状态
openclaw status

输出：
✅ OpenClaw运行中
- 版本: 1.0.0
- 模型: GLM-4
- 端口: 8080

**Step 5：测试**

# 命令行交互
openclaw chat

# 或者直接执行任务
openclaw run "列出当前目录的所有PDF文件"

**✅ 安装完成！**

<br/>

#### Windows命令行安装

**Step 1：安装Python**

访问 python.org/downloads/，下载Python 3.9+

安装时勾选"Add Python to PATH"

**Step 2：安装OpenClaw**

# 使用pip
pip install openclaw

# 或使用scoop
scoop install openclaw

**Step 3：初始化**

openclaw init

**Step 4：启动**

openclaw start

**✅ 安装完成！**

<br/>

***

<br/>

## 第一个任务：整理桌面

### 任务描述

**场景：**桌面乱糟糟，有各种文件，想按类型整理

**目标：**让OpenClaw自动整理桌面文件

<br/>

### 方式一：图形界面操作

**Step 1：打开OpenClaw**

双击桌面图标，或从开始菜单打开

**Step 2：进入对话界面**

看到主界面，有一个输入框

**Step 3：输入任务**

在输入框输入：

帮我把桌面上的文件按类型整理到不同文件夹。
图片放Images文件夹，文档放Documents文件夹，
代码放Code文件夹，其他放Others文件夹

**Step 4：点击"执行"**

点击"发送"或按回车

**Step 5：观察执行过程**

OpenClaw会显示执行过程：

🤔 正在分析任务...
📋 发现桌面文件：15个

执行步骤：
1. 扫描桌面文件
2. 创建分类文件夹
3. 移动文件

正在执行...
✅ 创建文件夹: Images
✅ 创建文件夹: Documents
✅ 创建文件夹: Code
✅ 创建文件夹: Others
✅ 移动文件: screenshot.png → Images/
✅ 移动文件: report.docx → Documents/
...

**Step 6：查看结果**

大约10秒后，显示：

✅ 整理完成！

📊 统计：
• 图片文件：5个 → Images/
• 文档文件：6个 → Documents/
• 代码文件：2个 → Code/
• 其他文件：2个 → Others/

总计处理：15个文件
用时：10.3秒

**Step 7：检查桌面**

最小化OpenClaw，看看桌面...

**哇！桌面清爽了！** ✨

<br/>

***

<br/>

### 方式二：命令行操作

**Step 1：打开终端**

Windows: PowerShell
macOS: Terminal

**Step 2：输入命令**

openclaw run "整理桌面文件，按类型分类"

**Step 3：等待执行**

🤖 执行任务：整理桌面文件...

步骤1：扫描桌面
找到 15 个文件

步骤2：创建文件夹
✓ Images
✓ Documents
✓ Code
✓ Others

步骤3：移动文件
✓ screenshot.png → Images/
✓ report.docx → Documents/
...

✅ 完成！
处理文件：15个
用时：9.8秒

**✅ 任务完成！**

<br/>

***

<br/>

### 方式三：小程序操作

**Step 1：打开QClaw小程序**

微信 → 搜索"QClaw" → 进入

**Step 2：输入任务**

生成一个Python脚本，用于整理桌面文件

**Step 3：获得脚本**

OpenClaw会生成代码（此处省略，实际会显示完整代码）

**Step 4：复制保存**

复制代码，保存为 organize_desktop.py

**Step 5：运行脚本**

python organize_desktop.py

**✅ 桌面整理完成！**

<br/>

***

<br/>

## 常见问题解决

### 问题1：安装失败

**症状：**

• 安装进度卡住
• 提示"安装失败"
• 打不开应用

**解决方案：**

**Windows：**

1. 右键安装包 → 属性 → 解除锁定
2. 以管理员身份运行
3. 关闭杀毒软件后重试

**macOS：**

1. 系统偏好设置 → 安全性与隐私 → 允许OpenClaw
2. 右键点击 → 打开 → 打开

**Linux：**

# 检查依赖
python3 --version
pip3 --version

# 重新安装
pip3 uninstall openclaw
pip3 install openclaw

<br/>

***

<br/>

### 问题2：需要付费吗？

**A：不需要！**

**免费方案：**

• ✅ 开源版：GitHub下载，完全免费
• ✅ 小程序：基础功能免费
• ✅ 本地部署：无任何费用

**收费情况：**

• 💰 大厂产品的高级功能可能收费
• 💰 云端API调用可能收费（很便宜）
• 💰 企业版有收费版本

**新手建议：**

> 先用免费版体验
> 需要时再考虑付费版

<br/>

***

<br/>

### 问题3：安全吗？

**A：相对安全**

**开源版：**

• ✅ 代码公开，可审计
• ✅ 本地运行，数据不上传
• ✅ 完全控制权限

**大厂产品：**

• ✅ 有安全合规
• ✅ 数据加密传输
• ⚠️ 数据会上传云端

**安全建议：**

1. 敏感数据用本地部署
2. 不要在对话中输入密码
3. 定期清理历史记录
4. 使用官方渠道下载

<br/>

***

<br/>

### 问题4：API Key是什么？一定要有吗？

**A：不一定！**

**API Key是什么：**

• 调用GPT-5、GLM-4等模型的密钥
• 类似"身份证"

**什么情况需要：**

• 使用GPT-5、Claude等国际模型
• 使用GLM-4、文心4.0等国内模型
• 需要更强大的能力

**什么情况不需要：**

• 使用本地模型（完全免费）
• 使用小程序（基础功能免费）
• 使用国内模型的免费额度（GLM、文心都有）
• 大厂产品的免费版

**如何获取：**

**国际模型：**

• OpenAI：platform.openai.com
• Anthropic（Claude）：console.anthropic.com
• 价格：GPT-5约$0.05/1K tokens

**国内模型：**

• 智谱AI：open.bigmodel.cn（推荐，性价比高）
• 百度智能云：console.bce.baidu.com
• 阿里云：dashscope.aliyun.com
• 价格：GLM-4约¥0.1/1K tokens（便宜！）

**新手建议：**

> 先用免费模型体验
> 或使用国内模型的免费额度
> 熟悉后再购买API Key

<br/>

***

<br/>

### 问题5：占多少内存/硬盘？

**内存占用：**

• 空闲：200-500MB
• 执行任务：500MB-2GB
• 推荐：4GB+内存

**硬盘占用：**

• 应用：500MB-1GB
• 数据：根据使用情况
• 推荐：5GB+可用空间

**性能优化：**

在配置文件 ~/.openclaw/config.yaml 中设置：

performance:
  max_memory: 2GB
  cache_size: 500MB

<br/>

***

<br/>

## 下一步建议

### 完成安装后

**1. 完成新手任务**

尝试以下任务，巩固学习：

• ✅ 整理下载文件夹
• ✅ 批量重命名文件
• ✅ 生成文件清单

**2. 学习常用功能**

看下一篇：《10个实用任务》

**3. 加入社区**

• 官方Discord：discord.gg/clawd
• 微信群：扫码加入
• GitHub：github.com/openclaw

<br/>

***

<br/>

## 小结

### 安装方式对比

方式 | 时间 | 难度 | 功能 | 推荐度
---|---|---|---|---
微信小程序 | 2分钟 | ⭐ | 基础 | ⭐⭐⭐
桌面应用 | 5分钟 | ⭐⭐ | 完整 | ⭐⭐⭐⭐⭐
命令行 | 5分钟 | ⭐⭐⭐ | 完整 | ⭐⭐⭐⭐

### 核心步骤回顾

**图形界面：**

1. 下载安装包
2. 双击安装
3. 首次配置
4. 开始使用

**命令行：**

brew install openclaw
openclaw init
openclaw start

**小程序：**

1. 微信搜索QClaw
2. 授权登录
3. 开始使用

### 成就达成！

**你已经：**

• ✅ 成功安装OpenClaw
• ✅ 完成第一个任务
• ✅ 看到实际效果
• ✅ 建立初步信心

<br/>

***

<br/>

## 练习题

**任务：**

选择一个你常用的文件夹（比如下载文件夹），让OpenClaw帮你整理一下。

**要求：**

1. 按文件类型分类
2. 删除重复文件
3. 生成整理报告

**提示：**

帮我整理Downloads文件夹：
1. 按类型分类文件
2. 删除重复文件
3. 生成整理报告

**完成的同学，评论区分享你的成果！** 📸

<br/>

***

<br/>

## 下期预告

**下一篇：**《新手必学的10个实用任务》

**你将学到：**

• ✅ 文件整理类任务（3个）
• ✅ 文档处理类任务（3个）
• ✅ 信息整理类任务（3个）
• ✅ 自动化类任务（1个）

**准备好解锁更多Skill吗？** 🚀

<br/>

***

<br/>

**系列导航**

• 上一篇：OpenClaw是什么？5分钟看懂AI Agent
• 下一篇：新手必学的10个实用任务

<br/>

***

<br/>

本文是《OpenClaw从入门到精通》系列第2篇
作者：生活助理 | 发布时间：2026-03-20
