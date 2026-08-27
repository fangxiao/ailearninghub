---
title: 不花钱也能用 AI 编程：OpenCode + Zen 免费模型，新手一步步跑通
description: 写给想试试 AI 编程但不想先花钱的新手。用 OpenCode + 官方 Zen 网关当例子，一步步装好、连上、选到免费且 zero-retention 的模型，跑通第一个任务。这类限时免费模型会轮换，看到这篇时未必还是 Ox Alpha Free，但选法完全一样。
---

最近圈子里在传一个"神秘免费大模型"：它藏在 OpenCode 的 Zen 里，免费用，而且明确写着不拿你的数据去训练。它就是 **Ox Alpha Free**。

> ⚠️ 时效性提醒：Ox Alpha Free 是 OpenCode 在 2026 年 8 月下旬搞的**限时免费**活动（官方 8/20 宣布"免费一周"，窗口大致到 8/27 前后，随时可能结束或改为收费）。如果你看到这篇时它已经从 `/models` 里消失，别慌。Zen 里总有别的 Free 模型顶上，下面这套选法照用不误。本文拿它当例子，讲清楚"限时免费模型到底怎么用"。

为什么现在聊这个？DeepSeek 8 月刚把 API 价格整体上调（新价 8/17 生效，部分档位涨幅不小），智谱、月之暗面等国产厂商年内也多次跟涨。曾经"白菜价"的国产模型正在集体变贵，所以这种明摆着免费、还承诺不训练你数据的入口，对想试水 AI 编程的新手就更值钱了。

这篇不聊参数、不聊排名，只做一件事：带纯新手把 OpenCode 装好、把 Zen 连上、把 Ox Alpha Free 选出来，然后真的跑通一个小任务。你不需要先办任何付费账号，也不用懂太多命令行。

> 截图位：下文标了「截图」的地方，把你的对话/界面截图按对应文件名放进 `screenshots/` 目录即可（例如 `screenshots/step3-models.png`）。没截图也不影响阅读，只是少了画面感。

## 先搞清楚：OpenCode 和 Zen 是什么

OpenCode 是个开源的 AI 编程助手，跑在终端里。它本身免费（MIT 协议），但自己不带大模型，信奉的是"自带密钥"：你连哪个模型提供商，它就用什么模型。

Zen 是 OpenCode 官方做的一个模型网关，相当于一个"精选超市"：官方把一堆对编程助手好用的模型测过、调过，摆进去。其中有一批标着 **Free** 的模型，价格全是 0。Ox Alpha Free 就是其中之一，而且它额外标注了 **zero-retention（零留存）**，也就是不会用你的对话去训练模型。对新手来说，这点比"免费"还重要：练手可以，别把公司代码和密钥贴进去。

记住这三层关系：你 → 用自然语言下指令 → OpenCode（助手）→ 通过 Zen（网关）→ 调用 Ox Alpha Free（模型）→ 改你的代码。

## 上手前，准备四样

一台电脑（macOS / Linux / Windows 的 WSL 都行），会最基础的终端操作（`cd` 进一个文件夹就够了）。再准备一个不重要的练手项目文件夹。最后需要一个 OpenCode Zen 账号。注册细节第二步会说，这里先给结论：只选带 **Free** 标签的模型，花费就是 0 美元，Ox Alpha Free 本身不收钱。

## 第一步：安装 OpenCode

三种装法，挑顺手的。Mac 新手推荐前两种。

用 Homebrew：

```bash
brew install anomalyco/tap/opencode
```

用 npm（装过 Node.js 就行）：

```bash
npm install -g opencode-ai
```

嫌麻烦也可以直接跑官方安装脚本：

```bash
curl -fsSL https://opencode.ai/install | bash
```

装完验证一下：

```bash
opencode --version
```

能打印出版本号，就说明装好了。

## 第二步：连上 Zen，拿到免费模型

最简单的方式，在终端里直接登录 Zen：

```bash
opencode auth login --provider zen
```

这条命令走的是 Zen 的免费档，通常不需要你手动建 API key。如果它弹出浏览器让你去 Zen 官网登录，照着走就行。

注意：Zen 开户时一般会要求**先存一笔 $20 余额**（相当于自动扣费的押金，不是立刻花掉）。只要你一直在 `/models` 里挑带 **Free** 标签的模型，token 费用就是 0，这笔余额基本碰不到。不过开户流程摆在那里，提前有个数，别以为"免费"就完全不用填支付信息。

> 另一种走法（截图位 `screenshots/step2-zen.png`，推送前记得补这张图；没图也不影响读）：进 OpenCode 之后在输入框打 `/connect`，选 `OpenCode Zen`，再把从 opencode.ai/auth 创建的 API key 粘进去。两种等价，选你顺手的。

## 第三步：进项目，启动 OpenCode

OpenCode 必须在一个项目文件夹里启动，它才会"看见"你的代码。别在桌面根目录直接跑。

```bash
cd my-project
opencode
```

第一次进项目，建议跑一下初始化，让它生成 `AGENTS.md`（记录项目约定的文件，以后每次对话自动读）：

```bash
/init
```

启动后你会看到一个终端界面：上面是聊天记录，底部是输入栏。

## 第四步：选中 Ox Alpha Free

在输入框里打 `/models`，会列出 Zen 推荐的模型清单。找到标注 **Ox Alpha Free** 的那一项（Zen 里的 id 形如 `opencode/x-preview-f-free`；具体以你当下 `/models` 列表里显示为准，这类免费模型会轮换），选中它。

> 截图位 `screenshots/step3-models.png`（推送前补图；没图也能读）：把 `/models` 列表里能看到 Free 模型、尤其 Ox Alpha Free 的那一屏放这里。

想一劳永逸，也可以把模型写进配置（`~/.config/opencode/opencode.json` 或项目根目录的 `opencode.json`）：

```json
{
  "model": "opencode/x-preview-f-free"
}
```

> 这个 id 会随活动轮换。哪天 Ox Alpha Free 不在了，把这里换成 `/models` 里下一个 Free 模型的 id 就行，用法不变。

Zen 里的免费模型不止 Ox Alpha Free 一个。写这篇时（2026 年 8 月下旬）Free 列表里还常能看到 Hy3 Free、Nemotron 3 Ultra / 3.5 Lightning Free、Muse Spark 1.2 Contributor Free，偶尔也冒出来 Big Pickle 这类 stealth 模型。它们的隐私条款并不一样：Ox Alpha Free 明确 zero-retention，而 Big Pickle 在免费期可能会拿你的数据去改进模型。所以挑模型别光看"免费"俩字，顺手扫一眼它带不带头 retention 说明。今天拿 Ox Alpha Free 当例子，哪天它轮换下去了，换一个 Free 的照样用。

## 第五步：跑通第一个任务

OpenCode 有两个常用模式，按 **Tab** 切换：

- **Plan（规划）**：只读，不改文件。你讲需求，它出方案，你先看对不对。
- **Build（执行）**：有完整权限，真的改文件、跑命令。

新手建议先 Plan 再 Build。比如你想让它在项目里建个文件，先在 Plan 模式说："在当前文件夹新建 hello.py，打印一句你好"。看它给的计划没问题，按 Tab 切到 Build，说"按这个计划做"。它改完你用 `/undo` 能一键回退，不怕改坏。

> 截图位 `screenshots/step4-chat.png`（推送前补图；没图也能读）：放一段你第一次用免费模型对话的截图（比如它建好文件、你确认输出的那一屏）。

做到这步，你就用上了免费、且不训练你数据的 AI 编程助手。后面只是把"小任务"换成"大任务"。

## 新手常踩的坑

以为 Zen 完全不用登录和账单：注册环节可能要填账单信息，但那是为了付费模型准备的；你只用 Free 标签的模型，账单就是 0。

把公司代码或密钥贴进免费模型：Ox Alpha Free 明确 zero-retention，但 Zen 里其他免费模型不一定。练手项目随便试，正经工作代码别往免费模型里贴。

盯着一个 Free 模型不放：它们是轮换的，别假设 Ox Alpha Free 永远在。养成"打开 `/models` 看当下哪个 Free"的习惯。

不在项目目录里启动 OpenCode：它启动时在哪个文件夹，就只看得见那个文件夹。先 `cd` 进去再 `opencode`。

盲目信任输出不 review：免费模型也是模型，出的代码可能有 bug。改完看一眼，不对就 `/undo`。

## 客观说：它适合谁、不适合谁

OpenCode 软件本身免费，但模型走的是 Zen 这个第三方网关，服务器在美国。Ox Alpha Free 是官方点名的 zero-retention、不拿你数据训练的模型。但它其实是个**匿名 stealth 模型**，provider 到底是谁官方还没公开。所以我的建议是：把它当"练手、写小工具"的免费入口完全没问题，但**公司代码、密钥、客户数据别往里贴**。匿名预览模型的"不留存"只是官方一面之词，你既没法审计、也没处投诉。真要处理敏感场景，走本地模型（见下）。

免费模型的水平，通常比顶级付费模型慢一点、偶尔笨一点，但限时免费期本就是官方在"展示"这些模型，用来练手、写小工具完全够。

如果你想要彻底离线、数据不出本机，OpenCode 也能接 Ollama 跑本地模型（如 qwen2.5-coder:7b）。那是另一条路，以后可以单独写一篇。

## 写在最后

Ox Alpha Free 这类"限时免费 + 不训练数据"的模型，是新手入门 AI 编程最低成本的入口：装好 OpenCode、连上 Zen、选它、跑一个小任务，全程不用先掏钱。

钱不是门槛。门槛是你愿不愿意建个练手文件夹、跑通那第一行输出。迈过去之后，要不要升级付费模型，是你自己的事。

> 想试就试：装 OpenCode → `opencode auth login --provider zen` → 进项目 `opencode` → `/models` 里选标 Free 的模型（现在是 Ox Alpha Free）→ 让它写一行代码。哪天这个模型没了，挑列表里下一个 Free 的，步骤一模一样。

跑通之后，可以接着看：

- [新手第一步：5 分钟搞懂 AI 编程 Agent 并跑通第一个任务](ai-coding-agent-新手第一步-公众号版.html)（先搞清 Agent 到底是什么）
- [用看板管理 10+ AI 编程助手——Vibe Kanban 实战](vibe-kanban-可视化看板管理AI编程-公众号版.html)（多个 Agent 一起干活怎么管）
- 下期预告：用 Ollama 在本地跑开源编程模型，数据完全不出本机
