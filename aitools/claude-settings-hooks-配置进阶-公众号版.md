---
title: Claude Code 配置进阶：用 settings.json + Hooks 给自己装护栏
description: 装再多 Skill 不如先装护栏。讲清楚 settings.json 的权限三级（allow/deny/ask）和 Hooks 的 PreToolUse 拦截、PostToolUse 自动格式化、Stop 跑测试，配真实翻车故事和可直接抄的配置。
---

上一期讲了用 wshobson 做[安全审计](wshobson-security-audit-实战-公众号版.html)，那是"代码写完了再查"。但更省心的做法，是让危险动作**根本跑不起来**。这篇就聊 settings.json 和 Hooks——你给 Claude Code 装的两道护栏。

我吃过亏才重视这个。有回我没配 deny，让 Agent 自己跑命令，它图快用了 `git push --force`，把同事当天的提交覆盖了。那次之后我才学乖：信任要有，护栏也得有。

## settings.json 长在哪

Claude Code 的配置有四层，越靠前越狠：

- 系统级（IT 下发，组织策略）
- 项目级 `.claude/settings.json`（进版本库，团队共享）
- 项目个人级 `.claude/settings.local.json`（gitignore，自己折腾用）
- 用户级 `~/.claude/settings.json`（跨项目）

同名键项目级压过用户级。团队规范放项目级提交进去，个人习惯放 local。

## 第一道护栏：权限 allow / deny / ask

权限规则就三类，`deny` 最先判、其次 `ask`、最后 `allow`。一条 deny 在任何层级都盖不过去。

我个人的 `.claude/settings.json` 大概是这么写的：

```json
{
  "permissions": {
    "allow": [
      "Read(./src/**)",
      "Bash(npm run build)",
      "Bash(npm test)"
    ],
    "ask": [
      "Bash(git push *)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(git push --force *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  }
}
```

几个坑提醒你：
- 括号里的 glob **空格算数**。`Bash(ls *)` 匹配 `ls -la` 但不匹配 `lsof`；想要两者都中得写 `Bash(ls*)`。
- `deny` 挡得住读 `.env`，但别只靠它。`.claudeignore` 和 allow 列表能被索引、搜索、系统提示注入绕过去，deny 才是硬闸。
- 想看当前生效了哪些规则，会话里敲 `/permissions`，它会把每条规则的来源（哪个文件）列出来。

我刚用时犯过反方向的错：allow 写得太宽，等于没装护栏；又有一阵 deny 写太多，Agent 干啥都弹确认，烦到自己手动关。平衡点得自己试。

## 第二道护栏：Hooks 在事件上动手脚

权限只能"放行 / 拦截"，Hooks 能在**事件前后**跑你自己的脚本，灵活得多。常用事件：

- `PreToolUse`：工具执行前。能 allow / deny / ask，还能改它的入参（`updatedInput`）、塞额外上下文。
- `PostToolUse`：工具执行后。注意，它**拦不住**已经发生的动作，但可以补救，比如自动格式化。
- `Stop`：一轮对话结束时，用来跑测试、卡质量门禁。

### PreToolUse：危险命令直接掐

最实用的一个——让 Agent 碰 `rm -rf`、`git push --force` 这种之前先过一道你的脚本。配置长这样：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/guard_bash.py \"$TOOL_INPUT\"",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

`$TOOL_INPUT` 是 Claude Code 喂给脚本的 JSON（含 `tool_input.command`）。脚本读它、判危险、返回 deny：

```python
import sys, json, re
raw = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
cmd = json.loads(raw).get("tool_input", {}).get("command", "")
if re.search(r"rm -rf|git push --force|--no-verify|sudo", cmd):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "危险命令被拦截：" + cmd
        }
    }))
sys.exit(0)
```

返回 JSON 里 `permissionDecision` 取 `deny` 就拦下，理由会原样递给模型。也可以不返回 JSON、直接 `exit 2`，stderr 会被当作拦截原因——但 JSON 写法更清楚，我推荐这个。

### PostToolUse：改完自动格式化

Agent 写完代码，顺手让它跑一遍 formatter，省得之后自己整理：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/format.py \"$TOOL_INPUT\"",
            "timeout": 10000
          }
        ]
      }
    ]
  }
}
```

`format.py` 从 `tool_input.file_path` 拿到文件，调 prettier / ruff 重新格式化。它改不了"已经发生"这件事，但能立刻把格式掰正。

### Stop：收工前先跑测试

我给自己加的一条——每轮对话结束，自动 `npm test`，没过就 block 收工：

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "npm test",
            "timeout": 60000
          }
        ]
      }
    ]
  }
}
```

Stop 这类事件用顶层 `decision` 字段，`{"decision":"block","reason":"测试没过"}` 就能把收工卡住，逼 Agent 先把红的修掉。

## 组合起来才香

单看每一条都普通，串起来是另一回事：用 [claude-code-router](claude-code-router-公众号版.html) 把模型切到便宜的，用 [anthropics/skills](anthropics-skills-官方技能库-公众号版.html) 固化流程，再叠上这篇的护栏——Agent 既能干活，又越不了界。我现在的习惯是：新项目第一件事不是装 Skill，是先落一份 settings.json。

## 几句实话

Hooks 不是银弹，别神化。PreToolUse 的 deny 对部分工具历史上出过没拦住的情况，所以关键操作我仍然靠 `deny` 权限规则兜底——双保险。脚本本身也会写错，第一次一定用 `claude --debug` 看 hook 日志，确认它真跑了、判对了。glob 那点空格细节，坑过我一次。

护栏这东西，前期花半小时配，后面省的是半夜救火。

接着看：
- [wshobson 安全审计实战：从威胁建模到漏洞修复](wshobson-security-audit-实战-公众号版.html)
- [Claude Code 路由到任意模型——claude-code-router](claude-code-router-公众号版.html)
- [Anthropic 官方技能库总览](anthropics-skills-官方技能库-公众号版.html)
- [用看板管理 10+ AI 编程助手——Vibe Kanban](vibe-kanban-可视化看板管理AI编程-公众号版.html)
- 下期预告：《现成 MCP Server 巡礼： filesystem / github / 数据库，哪些值得装》
