---
name: wechat-official-account
description: Use this skill when creating, formatting, or converting articles for WeChat Official Accounts (微信公众号图文排版). Ensures 100% inline-styled CSS, flawless copy-pasting into WeChat editor, beautiful callout cards, section title badges, and mobile-optimized typography.
---

# 微信公众号专业排版与发布技能 (WeChat Official Account Skill)

## 核心设计铁律
1. **纯行内样式 (100% Pure Inline Styles)**：
   - 微信后台编辑器会强制剔除所有 `<style>` 标签与外部 CSS class；
   - 必须在每一个 HTML 标签上显式声明 `style="..."`（使用 `<section>`, `<p>`, `<span>`, `<strong>`, `<table>`）。
2. **移动端阅读美学**：
   - 字号：正文 15.5px ~ 16px，行高 2.0，字间距 0.5px，段间距 25px，首行缩进 2em；
   - 颜色：正文深灰 `#3f3f3f`，主色调翡翠绿 `#00897B` 或经典绿 `#07c160`，背景纯白 `#ffffff`。
3. **结构化卡片与组件规范**：
   - **章节标题**：带有彩色小方块序号（如 `<span style="background: #00897B; color: #fff; padding: 6px 14px; border-radius: 4px;">01</span>`）；
   - **高亮卡片 (Callouts)**：带有左侧高亮边条（如 `border-left: 4px solid #00897B; background: #f0fdfa;`）；
   - **代码块**：带有内嵌背景与等宽字体（`font-family: SF Mono, Consolas, Monaco, monospace;`）；
   - **文末引导卡片**：嵌入高清公众号二维码与回复关键词提示。

## 复制与发布流程
1. 将排版好的推文输出为 `[文章名]-公众号版.html`；
2. 浏览器打开该文件，直接按 `Cmd + A`（全选）➔ `Cmd + C`（复制）；
3. 打开微信公众号后台图文编辑器，按 `Cmd + V`（粘贴），格式 100% 保真还原。
