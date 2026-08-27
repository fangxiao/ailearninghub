# ECC 文章代码块公众号兼容性修复方案

## 问题分析

用户反馈：Agent 用法部分的代码块在公众号上展示有问题。

**根因**：
- 当前代码块使用 `<p>` + `white-space: pre-wrap` 包裹多行内容
- 微信公众号渲染器对 `white-space: pre-wrap` 支持不稳定
- 多行代码会被合并成一行或错位显示

**影响范围**：
- Agent 用法部分（3 个代码块）
- Skill 用法部分（2 个代码块）
- 安装命令、实战演示中的代码块

## 修复方案

### 方案：逐行渲染（每行用 `<p>` 单独包裹）

将代码块从：
```html
<section>
  <p style="white-space: pre-wrap;">/plan  # 注释
/tdd    # 注释</p>
</section>
```

改为：
```html
<section>
  <p style="margin: 0; ...">/plan <span style="color: #999;"># 规划 Agent 拆解任务</span></p>
  <p style="margin: 0; ...">/tdd <span style="color: #999;"># TDD Agent 强制测试驱动</span></p>
</section>
```

### 具体修改点

#### 文件：`ecc-everything-claude-code-公众号版.html`

1. **Agent 用法 - 方式一代码块**（约 L217-L223）
   - 每行命令拆成独立 `<p>`，注释用 `<span>` 灰色显示

2. **Agent 用法 - 方式二代码块**（约 L230-L234）
   - 每行对话拆成独立 `<p>`，箭头用 `→` 符号，调用目标用 `<span>` 绿色显示

3. **Agent 用法 - 方式三代码块**（约 L241-L243）
   - 同方式一处理

4. **Skill 用法 - 触发方式代码块**（约 L300 附近）
   - 同方式二处理

5. **安装命令代码块**（约 L170 附近）
   - 逐行拆分

6. **实战演示中的代码块**
   - 检查并修复

## 样式规范

- 代码行：`font-family: 'SF Mono', Menlo, Monaco, Consolas, monospace; font-size: 13px; line-height: 1.8; color: #333; margin: 0;`
- 注释/说明：`color: #999; font-size: 12px;`
- 对话内容：不用等宽字体，用普通字体即可

## 风险

- 公众号对 `<section>` 标签内多个 `<p>` 的嵌套支持需要验证
- 建议保持 section 包裹 + 多个 `<p>` 的结构，这是公众号兼容的写法
