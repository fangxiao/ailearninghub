---
title: PM Skills /write-prd 深度实战：装前 vs 装后，PRD 质量差在哪
description: 用同一个功能点，对比"裸 Claude 写的 PRD"和"装了 PM Skills 后 /write-prd 写的 PRD"。看清楚结构化框架到底多值钱，以及怎么调出你们团队自己的 PRD 风格。
---

上一期总览了 [PM Skills 产品经理技能市场](pm-skills-产品经理技能市场-公众号版.html)，结尾说拆 /write-prd，用真实案例对比装前装后的 PRD 质量。这篇就干这事。

先说句大实话：PRD 这东西，花架子谁都会写，能拿去评审、不返工的没几个。我带过的需求里，一半以上 PRD 写完研发第一句是"你这降多少算成功"。问题不在文笔，在有没有框架兜底。裸聊容易漏非功能需求、成功指标、范围边界；/write-prd 把这些变必填项，出来的文档研发不用来回追问。下面用同一个功能点，两侧各写一遍，你自个儿看差距。

## /write-prd 是啥

它是 pm-skills 里 `pm-execution` 插件的一个命令，背后是 `create-prd` 这个 Skill——一套 8 节 PRD 模板：背景与问题、目标、用户与场景、需求（功能+非功能）、范围（做与不做）、成功指标、风险与依赖、开放问题。命令把你一句话想法按这 8 节展开，节点间还自动建议下一步，比如 `/red-team-prd` 红队压测、`/write-stories` 拆故事。

## 同一个需求，两侧对比

功能点：给后台系统做一个智能通知系统，降低告警疲劳。

### 装前：裸 Claude 写

> 用户：帮我写个 PRD，智能通知系统，减少告警疲劳。
>
> 产出（节选）：我们要做一个智能通知系统。核心功能：1) 汇总通知；2) 智能排序；3) 免打扰时段。界面放在设置页。预计两周做完。

这版拿去评审等于找骂。只有功能清单，没目标量化、没非功能需求（延迟、可靠性）、没说不做哪些、没成功指标、没风险。研发必然追着问"降多少算成功""和邮件通知啥关系""半夜炸了咋办"。

### 装后：/write-prd 写

> 用户：`/write-prd 智能通知系统，降低运维告警疲劳`
>
> 产出（节选）：
> 背景与问题：当前日均 1200 条告警，60% 低优先级重复，oncall 日均被打断 9 次。
> 目标：3 个月内有效打断降到日均 ≤3 次，且不漏高风险告警（召回 ≥99%）。
> 用户与场景：oncall 工程师（夜间）、SRE 负责人（配置规则）。
> 需求：功能——聚合、去重、优先级分级、免打扰窗口、渠道路由；非功能——聚合延迟 <30s、故障不丢告警、审计日志留 90 天。
> 范围：做规则引擎与聚合；不做多租户、不做移动端 Push（本期）。
> 成功指标：有效打断次数、漏报率、配置采纳率。
> 风险与依赖：依赖现有告警总线 schema 改造；误聚合致漏报。
> 开放问题：免打扰窗口谁有权改。

差距一眼能看出来。装后自带量化目标、非功能约束、范围边界、风险。评审不用补框架，直接聊判断。

## 差异摆这儿

| 维度 | 装前（裸聊） | 装后（/write-prd） |
| --- | --- | --- |
| 结构 | 自由发挥，易漏节 | 8 节模板，必填 |
| 目标 | 模糊"减少疲劳" | 量化"打断 ≤3 次/日" |
| 非功能需求 | 几乎没有 | 延迟 / 可靠性 / 审计 |
| 范围边界 | 不明确 | 做 / 不做写清 |
| 可评审性 | 低，需追问 | 高，直接判 |

## 怎么装

pm-skills 一份源能装到 Claude Code、Codex CLI、Cursor、OpenCode、Gemini CLI 等。

```bash
# Claude Code
claude plugin marketplace add phuryn/pm-skills
claude plugin install pm-execution@pm-skills

# Codex CLI（同套市场文件，原生装）
codex plugin marketplace add phuryn/pm-skills
codex plugin add pm-execution@pm-skills
```

其他助手（Gemini / OpenCode / Cursor）复制 `skills/` 到对应 `.gemini/skills/`、`.opencode/skills/`、`.cursor/skills/` 即可。命令（`/write-prd`）是 Claude 专属，Skill 通用。

## 调出你们团队自己的风格

/write-prd 不是死模板。两招：把团队历史优秀 PRD 贴给它，说"按这个语气和侧重点写"，它会对齐；跑完用 `/red-team-prd` 红队压测，挑最危险的假设，再用 `/write-stories` 把功能拆成用户故事。一套命令顺滑接力。

别指望它替你想需求。PM Skills 把 Teresa Torres、Marty Cagan 那套方法论固化进 Skill，它是结构化助手，判断还是你的。

## 一句心得

PRD 价值不在长，在该想的想到、该拒的拒了。/write-prd 把"该想什么"变模板，你只填判断。拿一个正写的需求试一遍，对比你手工版，差距自己会说话。

接着看：
- [PM Skills 产品经理技能市场总览](pm-skills-产品经理技能市场-公众号版.html)
- [手把手造你的第一个 Skill（skill-creator）](skill-creator-深度实战-公众号版.html)
- [wshobson/agents：202 个生产级 subagent](wshobson-agents-生产级subagent集合-公众号版.html)
- 下期预告：《wshobson/agents security-audit 实战：从威胁建模到漏洞修复》
