---
title: 手把手造你的第一个 Claude Skill：从想法到可用 Skill 全流程
description: 基于 Anthropic 官方 skill-creator，带你把一个"总在重复的工作流"固化成一个可复用、可触发、可迭代的 Skill。含真实示例、SKILL.md 模板、触发描述怎么写才不漏触发。
---

上一期介绍了 [Anthropic 官方技能库](anthropics-skills-官方技能库-公众号版.html)，结尾说要写一篇 skill-creator 实战。咱们今天就来，别紧张，跟着走一遍你就会了。

先聊清楚 Skill 是干嘛的。你肯定有那种活儿，每次都手动做——整理会议纪要、按团队规范审代码、把需求拆成用户故事。这些流程，其实值得固化成一个文件，让 Claude 在该用的时候自己跳出来用。第一次造 Skill 的人容易懵，一上来就琢磨"文件长啥样"，其实该先想的是"它啥时候该冒出来"。咱们拿一个真实例子走全程：造一个 `pr-summary` Skill，你给它 `git diff`，它吐一份结构化 PR 说明。

## 第 0 步：把环境弄好

skill-creator 不用单独装，它跟着 `anthropics/skills` 走，Claude Code 里直接就能调：

```bash
claude plugin marketplace add anthropics/skills
claude plugin install skill-creator@anthropics/skills
```

装好之后，你对话里说一句"帮我把 xxx 做成一个 skill"，Claude 就会自动进下面这套流程。下面几步，就是它会在背后陪你走的。

## 第 1 步：先想清楚要它干啥

别急着写文件。咱们先把四件事理顺，最好让 Claude 帮你问：这个 Skill 让 Claude 做什么（读 diff 出 PR 说明）、什么时候该触发（用户提"写 PR 说明""总结改动"）、输出什么格式（固定模板）、要不要写测试用例验证（有确定输出的活值得写）。

skill-creator 挺贴心的一点：它会先从当前对话里挖。要是你刚才手搓过一次，它直接把步骤、格式、你改过的地方提取出来，能少问你好几个问题。

## 第 2 步：让它把细节问透

接着它会追问边界情况、输入文件长啥样、成功标准、要不要调 `git`。这步你别嫌烦，答得越细，出来的 Skill 越准。我见过有人省了这步，结果 Skill 一跑就卡在"diff 从哪读"，又得返工。

## 第 3 步：写 SKILL.md

一个 Skill 的物理结构特别简单：

```
pr-summary/
├── SKILL.md          # 必需：frontmatter(name, description) + 正文指令
└── references/       # 可选：需要时再读进上下文的长文档
```

SKILL.md 长这样，你照着套：

```markdown
---
name: pr-summary
description: 把 git diff 整理成结构化 PR 说明（变更点/风险/测试建议）。
  当用户提到"写 PR 说明""总结改动""PR summary"，或贴了 diff 想生成提交说明时，
  务必使用本 skill，即使他没明说"PR"。
---

# PR Summary

## 输入
读取当前分支相对 main 的 diff：`git diff main...HEAD`

## 输出模板（严格照此）
# 变更概要
- 做了什么（一句话）
## 关键改动
- 逐文件：改了什么、为什么
## 风险点
- 可能影响的功能 / 兼容性
## 测试建议
- 该补的测试
```

有个坑咱们得重点说：description 要写得"有点 pushy"。Claude 有欠触发的小毛病，该用的时候不用。所以触发场景你得写全、写具体，甚至"用户没明说 PR 也要用"。官方原话大意是：别写"如何做仪表盘"，要写"用户一提到仪表盘、数据可视化、内部指标就务必用"。

## 第 4 步：渐进式披露

Skill 用三级加载来省上下文：元数据常驻（约 100 词）、SKILL.md 正文触发时才进（理想 <500 行）、references 按需读（无限大）。

做法是正文保持精简，长清单长文档丢进 `references/`，正文写清"何时去读"。快到 500 行就加层目录拆文件。别全堆正文里，那每次都吃上下文。

## 第 5 步：写测试、跑对比

有确定输出的 Skill（文件转换、提取、固定模板）值得写测试。skill-creator 让你列 2–3 个真实 prompt，存进 `evals/evals.json`，然后同时跑两遍：带 Skill 一遍、不带一遍（baseline）。它用子 Agent 并行跑，省时间。

跑完开一个 review 页面，左边看每个用例输出，右边看量化指标（通过率、耗时、token）。你勾哪里不满意，它据此改，再跑下一轮，直到你点头。

主观类 Skill（写作风格、设计）就别硬写断言了，靠人看就行。

## 第 6 步：迭代改进

三条心法，来自 skill-creator 自己：从反馈里泛化，别为几个例子过拟合；保持指令精简，看跑出来的过程，模型在瞎忙就砍掉对应段落；解释 why 而不是堆 MUST。今天模型有心智理论，你讲清为什么，比下 ALWAYS/NEVER 命令更靠谱。

## 第 7 步：把触发描述调准

Skill 写完后，skill-creator 能自动调 description 的命中率：生成 20 条"该触发/不该触发"的查询，60% 训练、40% 留测试，跑几轮挑测试集得分最高的描述。这一步直接决定"用户一说相关的话，Skill 跳不跳得出来"。

## 第 8 步：打包

```bash
python -m scripts.package_skill pr-summary/   # 产出 pr-summary.skill
```

把 `.skill` 发给同事，或放进团队技能市场，别人一键装。

## 咱们小结一下

造 Skill 的门槛不在写代码，在于你有没有把"平时怎么做的"说清楚。先从一个每周重复三次的小流程开始，比如 `pr-summary`，跑通一轮，你就有了可复用资产，后面越攒越快。

造好的 Skill 想进团队工作流，下一步可以看 [PM Skills 的 /write-prd](pm-skills-产品经理技能市场-公众号版.html)，别人是怎么把一整套方法论固化成命令的。

接着看：
- [Anthropic 官方技能库总览](anthropics-skills-官方技能库-公众号版.html)
- [PM Skills：把产品方法论固化成命令](pm-skills-产品经理技能市场-公众号版.html)
- [wshobson/agents：202 个生产级 subagent](wshobson-agents-生产级subagent集合-公众号版.html)
- 下期预告：《PM Skills /write-prd 深度实战：装前 vs 装后 PRD 对比》
