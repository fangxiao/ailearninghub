# Agent工作流：让龙虾自动干活

阅读时间：18分钟
难度等级：⭐⭐⭐ 进阶篇
你将收获：掌握工作流编排，实现真正的自动化

<br/>

***

<br/>

## 为什么要学工作流？

上一篇你学会了开发自定义 Skill，但可能还有疑问：

• "能不能让多个任务自动执行？"
• "任务之间能传递数据吗？"
• "能设置条件判断吗？"
• "怎么实现复杂的自动化流程？"

答案是：**Agent工作流**

**学会工作流后你会发现：**

• ✅ 多个任务自动串联
• ✅ 任务间数据无缝传递
• ✅ 条件判断、循环处理
• ✅ 真正的自动化，解放双手

<br/>

***

<br/>

## 一、什么是工作流？

### 1.1 概念解释

**工作流 = 多个任务按规则自动执行**

就像工厂流水线：

• 任务A完成 → 自动触发任务B
• 任务B完成 → 自动触发任务C
• 一直到最后一个任务

<br/>

### 1.2 工作流 vs 单任务

**单任务模式：**

```
你：帮我把这个PDF转成Word
龙虾：✅ 转换完成

你：帮我翻译这个Word
龙虾：✅ 翻译完成

你：帮我发送邮件
龙虾：✅ 邮件已发送
```

**工作流模式：**

```
你：处理报告工作流
龙虾：自动执行...
  步骤1：PDF转Word ✅
  步骤2：翻译文档 ✅
  步骤3：发送邮件 ✅
全部完成！
```

<br/>

### 1.3 工作流核心概念

**任务节点（Node）：**

工作流中的每个步骤

<br/>

**连接线（Edge）：**

定义任务之间的执行顺序

<br/>

**变量（Variable）：**

在任务之间传递的数据

<br/>

**条件（Condition）：**

根据情况选择不同分支

<br/>

**循环（Loop）：**

重复执行某些任务

<br/>

***

<br/>

## 二、工作流设计原则

### 2.1 单一职责

**每个任务只做一件事**

✅ 好的设计：

• 任务1：下载文件
• 任务2：转换格式
• 任务3：发送邮件

❌ 不好的设计：

• 任务1：下载、转换、发送全做

<br/>

### 2.2 清晰的输入输出

**每个任务明确输入和输出**

```
任务：PDF转Word
输入：PDF文件路径
输出：Word文件路径
```

<br/>

### 2.3 错误处理

**考虑失败情况**

• 网络断了怎么办？
• 文件不存在怎么办？
• API调用失败怎么办？

<br/>

### 2.4 可观测性

**能看到执行过程**

• 每个步骤的状态
• 执行日志
• 错误信息

<br/>

***

<br/>

## 三、实战1：自动化日报

### 3.1 需求分析

**每天自动生成日报：**

1. 收集当天新闻
2. 筛选重要信息
3. 生成报告
4. 发送邮件

<br/>

### 3.2 工作流设计

```
[搜索新闻] → [筛选整理] → [生成报告] → [发送邮件]
```

<br/>

### 3.3 配置文件

**创建工作流文件：daily-report.yaml**

```yaml
name: daily-report
description: 自动生成日报
trigger:
  type: schedule
  time: "18:00"

steps:
  - name: search-news
    skill: web-search
    params:
      query: "今日AI新闻"
      limit: 10

  - name: filter-news
    skill: text-filter
    params:
      input: "${search-news.result}"
      criteria: "重要性 > 7"

  - name: generate-report
    skill: report-generator
    params:
      data: "${filter-news.result}"
      template: "daily-report"

  - name: send-email
    skill: email-sender
    params:
      to: "boss@company.com"
      subject: "AI日报 - ${date}"
      body: "${generate-report.result}"
```

<br/>

### 3.4 变量传递

**工作流中的数据流：**

```
步骤1输出 → 步骤2输入
步骤2输出 → 步骤3输入
步骤3输出 → 步骤4输入
```

**变量语法：**

```
${步骤名.结果字段}
```

<br/>

### 3.5 执行效果

**每天18:00自动执行：**

```
⏰ 18:00 触发工作流：daily-report

步骤1/4：搜索新闻...
  ✅ 找到 10 条新闻

步骤2/4：筛选整理...
  ✅ 筛选出 5 条重要新闻

步骤3/4：生成报告...
  ✅ 日报已生成（1,234字）

步骤4/4：发送邮件...
  ✅ 邮件已发送至 boss@company.com

🎉 工作流执行完成！耗时 45 秒
```

<br/>

***

<br/>

## 四、实战2：批量文件处理

### 4.1 需求分析

**批量处理下载的图片：**

1. 遍历文件夹
2. 压缩图片
3. 重命名
4. 生成清单

<br/>

### 4.2 工作流设计

```
[遍历文件夹] → [循环处理每张图片] → [生成清单]
                    ↓
              [压缩图片] → [重命名]
```

<br/>

### 4.3 配置文件

```yaml
name: batch-image-process
description: 批量处理图片

steps:
  - name: list-files
    skill: file-lister
    params:
      path: "/Downloads/images"
      pattern: "*.jpg,*.png"

  - name: process-images
    loop: "${list-files.files}"
    steps:
      - name: compress
        skill: image-compress
        params:
          input: "${item.path}"
          quality: 80
      
      - name: rename
        skill: file-rename
        params:
          path: "${compress.output}"
          pattern: "IMG_${date}_${index}"

  - name: generate-list
    skill: file-list-generator
    params:
      files: "${process-images.results}"
      output: "/Downloads/images/清单.csv"
```

<br/>

### 4.4 循环处理

**工作流支持循环：**

```yaml
loop: "${list-files.files}"
```

**循环内可用变量：**

• `${item}` - 当前循环项
• `${index}` - 当前索引
• `${results}` - 所有结果

<br/>

***

<br/>

## 五、实战3：定时任务

### 5.1 定时触发

**支持多种触发方式：**

<br/>

**定时触发（Cron）：**

```yaml
trigger:
  type: schedule
  cron: "0 9 * * *"  # 每天9点
```

<br/>

**事件触发：**

```yaml
trigger:
  type: event
  event: file-created
  path: "/Downloads/*.pdf"
```

<br/>

**手动触发：**

```yaml
trigger:
  type: manual
```

<br/>

### 5.2 Cron表达式

**常用Cron表达式：**

```
0 9 * * *      # 每天9:00
0 18 * * 1-5   # 工作日18:00
0 0 1 * *      # 每月1号0:00
*/30 * * * *   # 每30分钟
0 9,12,18 * * *  # 每天9点、12点、18点
```

<br/>

### 5.3 失败重试

**配置重试策略：**

```yaml
retry:
  max_attempts: 3
  delay: 60  # 秒
  backoff: exponential  # 指数退避
```

<br/>

***

<br/>

## 六、条件分支

### 6.1 条件判断

**根据条件执行不同分支：**

```yaml
steps:
  - name: check-file-size
    skill: file-info
    params:
      path: "/Downloads/report.pdf"

  - name: branch
    condition: "${check-file-size.size > 10485760}"  # >10MB
    if_true:
      - name: compress
        skill: file-compress
    if_false:
      - name: send-directly
        skill: email-sender
```

<br/>

### 6.2 多条件判断

**支持多种条件：**

```yaml
condition:
  operator: and
  conditions:
    - "${file.size < 50000000}"
    - "${file.type == 'pdf'}"
```

<br/>

### 6.3 Switch分支

**多路分支：**

```yaml
switch: "${file.type}"
cases:
  pdf:
    - skill: pdf-processor
  image:
    - skill: image-processor
  video:
    - skill: video-processor
default:
  - skill: generic-processor
```

<br/>

***

<br/>

## 七、调试与优化

### 7.1 查看日志

**工作流执行日志：**

```bash
openclaw workflow logs daily-report
```

**日志内容：**

```
2026-03-20 18:00:00 [INFO] 工作流启动：daily-report
2026-03-20 18:00:05 [INFO] 步骤1完成：search-news
2026-03-20 18:00:10 [INFO] 步骤2完成：filter-news
2026-03-20 18:00:15 [INFO] 步骤3完成：generate-report
2026-03-20 18:00:20 [INFO] 步骤4完成：send-email
2026-03-20 18:00:20 [INFO] 工作流完成，耗时 20秒
```

<br/>

### 7.2 断点调试

**设置断点：**

```yaml
steps:
  - name: step1
    skill: xxx
    breakpoint: true  # 执行到这里暂停
```

**继续执行：**

```bash
openclaw workflow continue daily-report
```

<br/>

### 7.3 性能分析

**查看执行时间：**

```bash
openclaw workflow analyze daily-report
```

**优化建议：**

• 并行执行无依赖的任务
• 减少不必要的步骤
• 使用缓存

<br/>

***

<br/>

## 八、工作流管理

### 8.1 查看所有工作流

**命令行：**

```bash
openclaw workflow list
```

**图形界面：**

设置 → 工作流管理

<br/>

### 8.2 启用/禁用

**禁用工作流：**

```bash
openclaw workflow disable daily-report
```

**启用工作流：**

```bash
openclaw workflow enable daily-report
```

<br/>

### 8.3 手动触发

**立即执行：**

```bash
openclaw workflow run daily-report
```

**带参数执行：**

```bash
openclaw workflow run daily-report --param date=2026-03-20
```

<br/>

### 8.4 导入导出

**导出工作流：**

```bash
openclaw workflow export daily-report > daily-report.yaml
```

**导入工作流：**

```bash
openclaw workflow import daily-report.yaml
```

<br/>

***

<br/>

## 九、最佳实践

### 9.1 命名规范

**工作流命名：**

• 使用小写字母
• 用连字符分隔
• 描述性强

✅ 好的命名：`daily-report`, `batch-image-process`

❌ 不好的命名：`workflow1`, `test`

<br/>

### 9.2 模块化

**拆分复杂工作流：**

```
主工作流
├── 子工作流1：数据收集
├── 子工作流2：数据处理
└── 子工作流3：结果输出
```

<br/>

### 9.3 错误通知

**配置失败通知：**

```yaml
on_failure:
  - skill: notification
    params:
      type: email
      to: "admin@company.com"
      message: "工作流 ${workflow.name} 执行失败"
```

<br/>

### 9.4 版本管理

**使用Git管理工作流：**

```bash
git add workflows/
git commit -m "更新日报工作流"
```

<br/>

***

<br/>

## 十、小结

### 工作流核心能力

> **顺序执行：**
> 任务按顺序自动执行
>
> **条件分支：**
> 根据条件选择不同路径
>
> **循环处理：**
> 批量处理数据
>
> **定时触发：**
> 按时间自动执行

### 关键要点

• ✅ 单一职责，一个任务做一件事
• ✅ 清晰的输入输出
• ✅ 完善的错误处理
• ✅ 充分的日志记录
• ✅ 合理的重试策略

### 成就达成！

**你已经：**

• ✅ 理解工作流的概念
• ✅ 掌握工作流设计原则
• ✅ 完成日报自动化
• ✅ 学会批量处理
• ✅ 掌握定时任务

<br/>

***

<br/>

## 练习题

### 🎯 工作流挑战

完成以下工作流：

#### 挑战1：周报自动化

每周五自动收集本周数据，生成周报，发送邮件

#### 挑战2：文件监控

监控文件夹，有新文件时自动处理（压缩、重命名、归档）

#### 挑战3：多条件分支

根据文件类型、大小、来源选择不同处理方式

#### 挑战4：并行处理

同时处理多个任务，最后汇总结果

**完成的同学，评论区分享你的工作流！** 🎉

<br/>

***

<br/>

## 下期预告

**下一篇：**《多Agent协作：1+1>2的魔法》

**你将学到：**

• ✅ 为什么需要多Agent？
• ✅ 协作模式（流水线/主从/对等）
• ✅ 实战：打造内容生产团队
• ✅ 通信机制与冲突解决

**准备好让多个龙虾配合工作了吗？** 🚀

<br/>

***

**系列导航**

• 上一篇：从0到1：开发你的第一个自定义 Skill
• 下一篇：多Agent协作：1+1>2的魔法

<br/>

***

本文是《OpenClaw从入门到精通》系列第7篇
作者：生活助理 | 发布时间：2026-03-20
