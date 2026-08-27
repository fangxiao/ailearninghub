---
title: 用 wshobson/agents 做一次完整安全审计：从威胁建模到漏洞修复
description: AI 写代码快，但从不自己审自己。用 wshobson/agents 的安全能力，按"威胁建模→静态扫描→修复→复核"四步走完一次真实安全审计，并顺带介绍 HOL Guard 这道额外防线。
---

上一期总览了 [wshobson/agents：202 个生产级 subagent](wshobson-agents-生产级subagent集合-公众号版.html)，结尾说拆它的 security-audit 能力，做一次完整安全审计。这篇填坑。

我的立场先摆明：任何 AI 生成的代码，我默认当它有坑。Vibe Coding 让产量暴涨，但 AI 默认不审自己——它不会主动想"这段 SQL 会被注入""这个密钥会不会进仓库"。你产出越快，安全债滚得越狠。我审过自己 vibe 出来的一个小服务，二十行里两处能进生产环境的坑，后背发凉。所以审计不能等上线前，得变成可复跑的流程。wshobson/agents 把安全能力做成了可装插件，正好。

## wshobson/agents 的安全家底

这个市场一份源能装到 Claude Code、Codex、Cursor、OpenCode、Antigravity、Copilot 五家。和安全相关的两层：安全编排器（16 个编排器里含"安全"这一类，把架构、扫描、修复、复核串成多 Agent 协作）；还有 HOL Guard 外部集成，市场引入的 `hol-guard` 和 `plugin-scanner` 两个 Skill，专扫本地技能/插件的供应链与权限，装前要你批准。

下面四步走：威胁建模、静态扫描、修复、复核。任何一步的输出，我都不盲信，复核见真章。

## 第 0 步：装安全相关插件

```bash
claude plugin marketplace add wshobson/agents
claude plugin install application-security     # 安全编排器所在插件，名称以市场目录为准
# 额外防线（可选，需手动批准）
claude plugin install hol-guard
```

命令名随插件版本可能微调，装完用 `/plugin` 看实际列表。

## 第 1 步：威胁建模

别上来就扫代码，那是本末倒置。先让安全 Agent 画信任边界：哪些数据来自外部、哪些操作有副作用、哪些地方一旦被绕过就出事。

提示词示例：

```text
对 src/api/ 做一次威胁建模：列出外部输入点、信任边界、最该保护的资产
（如密钥、用户数据），以及每类资产"被攻破会怎样"。
```

它出一张清单，后面扫描照这张对账，边角不漏。

## 第 2 步：静态漏洞扫描

给一段真实有问题的代码，看它怎么抓。示例（故意留洞）：

```python
# src/api/user.py（有问题版本）
import os, sqlite3
def login(username, pwd):
    conn = sqlite3.connect("app.db")
    # 漏洞1：SQL 拼接
    cur = conn.execute(f"SELECT * FROM users WHERE name='{username}' AND pwd='{pwd}'")
    # 漏洞2：硬编码密钥
    token = os.getenv("TOKEN") or "sk_live_8f2c1a9b"   # 写死进代码
    return cur.fetchone()
```

安全 Agent 的静态审计会标出：SQL 注入，因为 `f-string` 拼了用户名和密码，建议参数化 `?` 占位；硬编码凭证，`sk_live_...` 进了源码，必须移进环境变量或密钥管理，且立刻轮换；顺带提醒密码明文比对、无速率限制、异常没记录。

它有个习惯我留着：每条发现先自己反驳一遍"这真算漏洞吗"，只报有证据支撑的风险。误报噪音小，但我仍然逐条复核——自动化也会看走眼。

## 第 3 步：修复

把上一步发现喂回去，让它出修复版：

```python
# 修复后
import os, sqlite3
def login(username, pwd):
    conn = sqlite3.connect("app.db")
    cur = conn.execute(
        "SELECT id, pwd_hash FROM users WHERE name=?", (username,)
    )
    row = cur.fetchone()
    return row and verify_pw(pwd, row[1])   # 参数化 + 哈希校验
```

密钥改只从环境变量读，仓库只留 `.env.example`。这步我一定逐条 review 它的改动——和 [新手第一步](ai-coding-agent-新手第一步-公众号版.html) 强调的一致，AI 出的代码你负最终责任，安全这块容不得甩手。

## 第 4 步：复核

修完绝不收工。让另一个视角（或同一 Agent 换一轮）重扫修复后的代码，确认原漏洞闭合、没引入新风险、密钥不再出现。wshobson 的多 Agent 编排器在这的价值，是写的人和复核的人可以是不同 Agent——天然对抗"自己审自己"的盲区。2026 年这股"跨模型对抗式 review"的风，我举双手赞成。

## 额外防线：HOL Guard

`hol-guard` / `plugin-scanner` 偏供应链安全：装第三方 Skill/插件前，扫一遍它会不会偷偷执行命令、外传数据、提权。Vibe Coding 时代你装了一堆社区技能，装前扫一道比事后救火划算。它默认走本地 CLI，不强制上云。

## 我的底线

AI 安全审计是放大器不是银弹。它擅长按已知模式抓明显漏洞、整理清单，但业务逻辑漏洞的判断还得靠人。把它当每次提交前的自动体检，高频、低成本、可复跑，真正的高风险设计你拍板。

安全债最怕等上线前才清。把 wshobson 的安全编排器接进提交流程，每次改动自动跑一遍四步法，爆雷变日清。

这一篇偏工程。下一篇换视角：用 Dify 把 Claude Code、Codex、Gemini 串成一条自动流水线，写代码、验代码、写文档全自动接力。

接着看：
- [wshobson/agents 生产级 subagent 总览](wshobson-agents-生产级subagent集合-公众号版.html)
- [Snyk 安全技能：漏洞修复](snyk-security-skills-漏洞修复-公众号版.html)
- [新手第一步：AI 编程 Agent 与 review 责任](ai-coding-agent-新手第一步-公众号版.html)
- 下期预告：《用 Dify 把 Claude / Codex / Gemini 编排成自动流水线》
