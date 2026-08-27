---
title: 用 Dify 把 Claude / Codex / Gemini 编排成自动流水线：写代码→验代码→写文档
description: 单一 Agent 再强也只干一类活。用 Dify 的可视化工作流，把 Anthropic、OpenAI、Google 三家模型接进同一条画布，实现"Claude 写代码、Codex 验代码、Gemini 写文档"全自动接力。含一步步搭建步骤。
---

[vibe-kanban](vibe-kanban-可视化看板管理AI编程-公众号版.html) 结尾预告过，聊一个把 AI 编程助手编排成流水线的工具。之前我们横评过四个助手（[横评](ai-coding-横评-公众号版.html)），结论是按任务切模型最香，但手动切累得要死。这篇用 Dify 把"切模型"变成一条自动流水线——我玩了一下午，真上头。

先说为啥不相死用一个：同一个需求，不同环节要的不同。写代码要质量稳（Claude），挑错要对抗式审查（Codex/GPT），写文档要快且顺（Gemini）。让一个模型又写又审又写文档，等于又当裁判又当运动员，它自己都迷。跨模型接力能互相纠错，这股"对抗式 review"的风 2026 年越吹越实。

难点在接力：怎么把 A 的输出喂给 B，再把 B 的结果喂给 C。Dify 的爽点就在这——把链路画成一张画布，三家模型同在画布上，变量自动传递。我第一次串起来最爽的，是不用在三个终端间复制粘贴了。

## Dify 是啥

Dify 是开源的 LLM 应用平台，云端注册或 docker 自托管都行。它的 Workflow 是一块节点画布，每个节点干一件事，节点间用变量连线。你能把 Anthropic、OpenAI、Google 三家同时配成 Model Provider，于是在同一个流程里，节点 1 用 Claude、节点 2 用 GPT、节点 3 用 Gemini，互不打架。

## 第 0 步：开通与接模型

去 `cloud.dify.ai` 注册，或 `docker compose` 自托管。接模型：左侧 Settings → Model Provider，分别加 Anthropic（填 Claude API Key）、OpenAI（Codex 同源）、Google（Gemini API Key）。三家都加上后，任何 LLM 节点下拉里就能切厂商，跟换灯泡一样。

## 第 1 步：新建 Workflow

Studio → Create App → Workflow，命名 `code-pipeline`。画布默认有 Start 节点，先给它一个输入变量 `query`（文本），放功能需求描述。

## 第 2 步：节点 1，Claude 写代码

拖一个 LLM 节点，连到 Start。Model 选 Anthropic 的 `claude-...`，Prompt：

```text
你是一名资深工程师。根据需求写实现代码。
需求：{{#start.query#}}
只输出代码 + 简短说明，不要做审查。
```

它的输出变量叫 `text`，下一步接着用。

## 第 3 步：节点 2，Codex 验代码

再拖一个 LLM 节点，连到节点 1。Model 选 OpenAI 的 `gpt-...`（Codex 同源），Prompt：

```text
你是严苛的代码审查员。审查下面代码，列出：1) 正确性 bug；
2) 安全隐患；3) 边界情况遗漏。每条给严重级别。
代码：{{#llm1.text#}}
```

输出 `text` 即审查意见。关键在这：节点 2 吃的是节点 1 的 `{{#llm1.text#}}`，不是 Start。这就是接力，Claude 的产出自动喂给 Codex，丝滑。

## 第 4 步：节点 3，Gemini 写文档

再拖一个 LLM 节点，连到节点 2。Model 选 Google 的 `gemini-...`，Prompt：

```text
根据代码和审查意见，写一份面向开发的 README 片段：
功能说明、使用方式、已知限制。
代码：{{#llm1.text#}}
审查意见：{{#llm2.text#}}
```

## 第 5 步：收口与运行

拖一个 End 节点，把三个输出（`llm1.text` / `llm2.text` / `llm3.text`）作为最终返回。点右上角 Run，填一条需求，看三个模型依次点亮：Claude 出代码，Codex 吐审查，Gemini 出文档，全程不用手动复制。

跑顺了 Publish 成 WebApp 或暴露 API，接进 CI 或提交流程，提需求即出代码加审查加文档，爽。

## 进阶：让流水线会打回

光接力不够刺激。加个 IF/ELSE 节点，读节点 2 输出，严重 bug 数大于 0 就走打回重写分支，把审查意见喂回节点 1 重新生成，直到通过。再加 Iteration 节点能批量处理多个需求。这样流水线从串行升级成带质量门禁的循环，更好玩。

## 泼点冷水

三家 API Key 都在 Dify 里，自托管更可控；多模型接力 token 消耗是单模型几倍，先小任务试水。Dify 是编排层不是执行层，它不碰你仓库、不跑测试，要真改文件真跑测试，把输出接回 [Claude Code](ai-coding-agent-新手第一步-公众号版.html) 或 CI，别指望它替你提交。Codex 挑的问题，合并前你还得过一眼。

编排的本质就一句：对的模型干对的活，且自动接力。Dify 把这件事从人肉复制粘贴变成画一张图。先把这条三节点流水线搭出来跑通，你肯定想给自己加第四条第五条链路。

到这里，第一类"已预告的续集"全部补齐：横评、skill-creator、/write-prd、security-audit、Dify 流水线。AI 编程的玩法，从单个助手走到了多助手编排。下一步值得聊的，是 [用看板把 10+ 助手管起来](vibe-kanban-可视化看板管理AI编程-公众号版.html) 之后的团队协作范式。

接着看：
- [Vibe Kanban：用看板管理 10+ AI 编程助手](vibe-kanban-可视化看板管理AI编程-公众号版.html)
- [2026 主流 AI 编程助手横评](ai-coding-横评-公众号版.html)
- [Claude Code 路由到任意模型](claude-code-router-公众号版.html)
- [wshobson 安全审计实战](wshobson-security-audit-实战-公众号版.html)
