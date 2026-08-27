# 上下文管理（Context Management）：让AI记住关键信息

阅读时间：45分钟
难度等级：⭐⭐⭐⭐ 高级
前置知识：AI-29 工具系统

<br/>

***

<br/>

## 上一篇回顾

**在AI-29《工具系统》中，我们学习了：**

```
✅ Tool接口的完整设计
✅ 内置工具的实现（Read、Write、Edit、Exec）
✅ 工具注册与发现机制
✅ 自定义工具开发
✅ 安全与性能优化
```

**本篇重点：**

```
本篇将深入上下文管理，学习：
  └─ 为什么需要上下文管理
  └─ Token计数原理
  └─ 文件选择策略
  └─ 上下文压缩算法
  └─ 长对话处理技巧
```

**为什么上下文管理重要：**

```
Claude的上下文窗口有限（200K tokens）：
  ❓ 如何从1000+文件中选择最相关的？
  ❓ 如何在有限的token内提供足够信息？
  ❓ 如何处理超长对话历史？
  ❓ 如何优化token使用效率？

掌握上下文管理，是高效使用AI Coding工具的关键！
```

<br/>

***

<br/>

## 一、上下文管理概述

### 1.1 什么是上下文？

**上下文的组成：**

```
完整上下文 = 系统提示词 + 对话历史 + 项目文件 + 工具定义

1. 系统提示词（System Prompt）
   - 角色定义
   - 能力说明
   - 行为规则
   - 安全约束

2. 对话历史（Message History）
   - 用户消息
   - 助手回复
   - 工具调用
   - 工具结果

3. 项目文件（Project Files）
   - 源代码文件
   - 配置文件
   - 文档文件
   - 其他相关文件

4. 工具定义（Tool Definitions）
   - 工具名称
   - 工具描述
   - 参数Schema
```

**Token预算分配：**

```
总Token预算：200,000 tokens

分配示例：
┌─────────────────────────────┐
│ 系统提示词      1,000 tokens│
├─────────────────────────────┤
│ 对话历史     20,000 tokens  │
├─────────────────────────────┤
│ 项目文件    150,000 tokens  │
├─────────────────────────────┤
│ 工具定义       5,000 tokens │
├─────────────────────────────┤
│ 预留缓冲      24,000 tokens │
└─────────────────────────────┘
```

<br/>

### 1.2 为什么需要上下文管理？

**问题场景：**

```
场景1：大型项目
  - 项目有500个文件
  - 总代码量50MB
  - Claude只能接受部分文件
  ❓ 选择哪些文件？

场景2：长对话
  - 用户进行了100轮对话
  - 对话历史已经很长
  - Token接近上限
  ❓ 如何压缩历史？

场景3：多文件编辑
  - 需要修改10个文件
  - 每个文件1000行
  - 总Token超限
  ❓ 如何优化？
```

**解决方案：**

```
1. 智能文件选择
   ✅ 根据用户输入匹配相关文件
   ✅ 优先级排序
   ✅ Token预算控制

2. 对话历史压缩
   ✅ 保留关键信息
   ✅ 摘要化处理
   ✅ 滑动窗口

3. 文件内容优化
   ✅ 只包含相关部分
   ✅ 移除注释（可选）
   ✅ 代码压缩

4. 动态调整
   ✅ 实时监控Token
   ✅ 动态增减文件
   ✅ 自适应策略
```

<br/>

***

<br/>

## 二、Token计数原理

### 2.1 什么是Token？

**Token vs 字符：**

```
Token是Claude处理文本的基本单位：
  - 英文：约4字符 = 1 token
  - 中文：约1.5字符 = 1 token
  - 代码：约3字符 = 1 token

示例：
  "Hello World" → 2 tokens
  "你好世界" → 4 tokens
  "def hello():" → 3 tokens
```

**Token计算方法：**

```typescript
class TokenCounter {
  private tokenizer: Tokenizer;

  constructor() {
    // 使用Claude的tokenizer
    this.tokenizer = new ClaudeTokenizer();
  }

  /**
   * 计算文本的Token数
   */
  count(text: string): number {
    return this.tokenizer.encode(text).length;
  }

  /**
   * 计算消息的Token数
   */
  countMessage(message: Message): number {
    let tokens = 0;

    // 角色标记
    tokens += 4;  // <|role|>

    // 内容
    if (typeof message.content === 'string') {
      tokens += this.count(message.content);
    } else {
      // 多部分内容
      for (const part of message.content) {
        if (part.type === 'text') {
          tokens += this.count(part.text);
        } else if (part.type === 'tool_use') {
          tokens += this.count(JSON.stringify(part.input));
          tokens += 10;  // 工具调用开销
        } else if (part.type === 'tool_result') {
          tokens += this.count(part.content);
          tokens += 5;  // 工具结果开销
        }
      }
    }

    return tokens;
  }

  /**
   * 计算整个上下文的Token数
   */
  countContext(context: Context): number {
    let total = 0;

    // 系统提示词
    total += this.count(context.systemPrompt);

    // 消息历史
    for (const message of context.messages) {
      total += this.countMessage(message);
    }

    // 项目文件
    for (const file of context.projectFiles) {
      total += this.count(file.content);
      total += 20;  // 文件元数据开销
    }

    // 工具定义
    for (const tool of context.toolDefinitions) {
      total += this.count(tool.description);
      total += this.count(JSON.stringify(tool.input_schema));
      total += 10;  // 工具定义开销
    }

    return total;
  }
}
```

<br/>

### 2.2 Token优化策略

**策略1：精确计算**

```typescript
class ContextManager {
  private tokenCounter: TokenCounter;
  private maxTokens: number = 200000;

  /**
   * 检查是否超限
   */
  isOverLimit(context: Context): boolean {
    const tokens = this.tokenCounter.countContext(context);
    return tokens > this.maxTokens;
  }

  /**
   * 获取剩余Token
   */
  getRemainingTokens(context: Context): number {
    const used = this.tokenCounter.countContext(context);
    return this.maxTokens - used;
  }

  /**
   * 确保不超限
   */
  async ensureWithinLimit(context: Context): Promise<Context> {
    while (this.isOverLimit(context)) {
      // 压缩上下文
      context = await this.compress(context);
    }
    return context;
  }
}
```

**策略2：分块计算**

```typescript
class ChunkedTokenCounter {
  /**
   * 分块计算大文件的Token
   */
  countLargeFile(filePath: string): number {
    const stats = fs.statSync(filePath);
    const fileSize = stats.size;
    
    // 小文件直接计算
    if (fileSize < 100 * 1024) {  // < 100KB
      const content = fs.readFileSync(filePath, 'utf-8');
      return this.tokenCounter.count(content);
    }
    
    // 大文件估算
    // 代码文件：约3字符 = 1 token
    // 文本文件：约4字符 = 1 token
    const avgCharsPerToken = 3;
    return Math.ceil(fileSize / avgCharsPerToken);
  }
}
```

<br/>

***

<br/>

## 三、文件选择策略

### 3.1 文件选择算法

**多阶段选择流程：**

```
第1阶段：快速过滤
  └─ 文件类型过滤（排除二进制、图片等）
  └─ 目录过滤（排除node_modules、.git等）
  └─ 大小过滤（排除超大文件）

第2阶段：相关性匹配
  └─ 文件名匹配
  └─ 路径匹配
  └─ 内容搜索（可选）

第3阶段：优先级排序
  └─ 匹配度评分
  └─ 文件类型权重
  └─ 修改时间权重

第4阶段：Token预算控制
  └─ 按优先级添加文件
  └─ 监控Token使用
  └─ 达到预算停止
```

**完整实现：**

```typescript
class FileSelector {
  private tokenCounter: TokenCounter;
  private projectFiles: string[];

  /**
   * 选择相关文件
   */
  async selectRelevantFiles(
    query: string,
    maxTokens: number
  ): Promise<SelectedFile[]> {
    // 1. 快速过滤
    const candidates = await this.quickFilter(this.projectFiles);

    // 2. 相关性匹配
    const scored = await this.scoreByRelevance(query, candidates);

    // 3. 优先级排序
    const ranked = this.rankByPriority(scored);

    // 4. Token预算控制
    return this.selectWithinBudget(ranked, maxTokens);
  }

  /**
   * 快速过滤
   */
  private async quickFilter(files: string[]): Promise<string[]> {
    const excludePatterns = [
      /node_modules/,
      /\.git/,
      /dist/,
      /build/,
      /\.next/,
      /coverage/,
      /\.DS_Store/,
      /\.pyc$/,
      /\.exe$/,
      /\.bin$/,
      /\.jpg$/,
      /\.png$/,
      /\.pdf$/
    ];

    return files.filter(file => {
      // 排除特定模式
      for (const pattern of excludePatterns) {
        if (pattern.test(file)) {
          return false;
        }
      }

      // 排除大文件（>1MB）
      const stats = fs.statSync(file);
      if (stats.size > 1024 * 1024) {
        return false;
      }

      return true;
    });
  }

  /**
   * 相关性评分
   */
  private async scoreByRelevance(
    query: string,
    files: string[]
  ): Promise<ScoredFile[]> {
    const keywords = this.extractKeywords(query);
    const scored: ScoredFile[] = [];

    for (const file of files) {
      let score = 0;

      // 1. 文件名匹配（权重高）
      const fileName = path.basename(file).toLowerCase();
      for (const keyword of keywords) {
        if (fileName.includes(keyword.toLowerCase())) {
          score += 10;
        }
      }

      // 2. 路径匹配（权重中）
      for (const keyword of keywords) {
        if (file.toLowerCase().includes(keyword.toLowerCase())) {
          score += 5;
        }
      }

      // 3. 文件类型权重
      const ext = path.extname(file);
      if (['.ts', '.js', '.py', '.go'].includes(ext)) {
        score += 3;  // 源代码优先
      } else if (['.json', '.yaml', '.yml'].includes(ext)) {
        score += 2;  // 配置文件次之
      }

      // 4. 修改时间权重（最近修改的优先）
      const stats = fs.statSync(file);
      const daysSinceModified = 
        (Date.now() - stats.mtime.getTime()) / (1000 * 60 * 60 * 24);
      if (daysSinceModified < 1) {
        score += 5;  // 今天修改
      } else if (daysSinceModified < 7) {
        score += 3;  // 本周修改
      }

      scored.push({ file, score });
    }

    return scored;
  }

  /**
   * 提取关键词
   */
  private extractKeywords(query: string): string[] {
    // 移除常见停用词
    const stopWords = new Set([
      'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
      'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
      'would', 'could', 'should', 'may', 'might', 'must', 'shall',
      '的', '了', '在', '是', '我', '有', '和', '就', '不', '人'
    ]);

    // 分词
    const words = query.toLowerCase().split(/\s+/);
    
    return words.filter(word => 
      word.length > 2 && !stopWords.has(word)
    );
  }

  /**
   * 优先级排序
   */
  private rankByPriority(files: ScoredFile[]): ScoredFile[] {
    return files.sort((a, b) => b.score - a.score);
  }

  /**
   * Token预算控制
   */
  private async selectWithinBudget(
    files: ScoredFile[],
    maxTokens: number
  ): Promise<SelectedFile[]> {
    const selected: SelectedFile[] = [];
    let totalTokens = 0;

    for (const { file, score } of files) {
      // 读取文件内容
      const content = await fs.readFile(file, 'utf-8');
      const tokens = this.tokenCounter.count(content);

      // 检查是否超出预算
      if (totalTokens + tokens <= maxTokens) {
        selected.push({
          path: file,
          content,
          tokens,
          score
        });
        totalTokens += tokens;
      } else {
        // 预算用完，停止添加
        break;
      }
    }

    console.log(`已选择 ${selected.length} 个文件，共 ${totalTokens} tokens`);
    return selected;
  }
}
```

<br/>

### 3.2 智能搜索策略

**基于内容的搜索：**

```typescript
class ContentSearcher {
  /**
   * 在文件中搜索关键词
   */
  async searchInFiles(
    keywords: string[],
    files: string[]
  ): Promise<SearchResult[]> {
    const results: SearchResult[] = [];

    // 使用ripgrep进行快速搜索
    for (const keyword of keywords) {
      const matches = await this.ripgrep(keyword, files);
      results.push(...matches);
    }

    return results;
  }

  /**
   * 使用ripgrep搜索
   */
  private async ripgrep(
    pattern: string,
    files: string[]
  ): Promise<SearchResult[]> {
    return new Promise((resolve, reject) => {
      const rg = spawn('rg', [
        '-i',               // 忽略大小写
        '-n',               // 显示行号
        '--max-count=5',    // 每个文件最多5个匹配
        pattern,
        ...files
      ]);

      let output = '';
      rg.stdout.on('data', data => output += data);
      rg.on('close', code => {
        if (code === 0) {
          resolve(this.parseRipgrepOutput(output));
        } else {
          resolve([]);
        }
      });
    });
  }

  /**
   * 解析ripgrep输出
   */
  private parseRipgrepOutput(output: string): SearchResult[] {
    const results: SearchResult[] = [];
    const lines = output.split('\n');

    for (const line of lines) {
      const match = line.match(/^([^:]+):(\d+):(.+)$/);
      if (match) {
        results.push({
          file: match[1],
          line: parseInt(match[2]),
          content: match[3]
        });
      }
    }

    return results;
  }
}
```

<br/>

***

<br/>

## 四、上下文压缩算法

### 4.1 对话历史压缩

**滑动窗口策略：**

```typescript
class MessageCompressor {
  /**
   * 压缩对话历史
   */
  compress(
    messages: Message[],
    maxMessages: number = 20
  ): Message[] {
    // 1. 保留最近的N条消息
    if (messages.length <= maxMessages) {
      return messages;
    }

    // 2. 保留第一条和最后N-1条
    const first = messages[0];
    const recent = messages.slice(-(maxMessages - 1));

    // 3. 压缩中间消息为摘要
    const middle = messages.slice(1, -(maxMessages - 1));
    const summary = this.summarize(middle);

    return [
      first,
      { role: 'user', content: `[历史摘要]\n${summary}` },
      ...recent
    ];
  }

  /**
   * 生成摘要
   */
  private summarize(messages: Message[]): string {
    const summaries: string[] = [];

    for (let i = 0; i < messages.length; i += 2) {
      const userMsg = messages[i];
      const assistantMsg = messages[i + 1];

      if (userMsg && assistantMsg) {
        // 提取用户意图
        const intent = this.extractIntent(userMsg);
        
        // 提取助手行动
        const actions = this.extractActions(assistantMsg);

        summaries.push(`- ${intent}: ${actions.join(', ')}`);
      }
    }

    return summaries.join('\n');
  }

  /**
   * 提取意图
   */
  private extractIntent(message: Message): string {
    const content = typeof message.content === 'string'
      ? message.content
      : message.content.map(c => c.type === 'text' ? c.text : '').join('');

    // 提取前50个字符作为意图
    return content.substring(0, 50);
  }

  /**
   * 提取行动
   */
  private extractActions(message: Message): string[] {
    const actions: string[] = [];

    if (typeof message.content !== 'string') {
      for (const part of message.content) {
        if (part.type === 'tool_use') {
          actions.push(`调用${part.name}工具`);
        }
      }
    }

    return actions;
  }
}
```

<br/>

### 4.2 文件内容压缩

**部分内容包含：**

```typescript
class FileContentCompressor {
  /**
   * 压缩文件内容
   */
  compress(
    content: string,
    options: CompressOptions = {}
  ): string {
    const {
      maxLines = 500,
      removeComments = false,
      removeEmptyLines = false,
      includeImports = true,
      includeExports = true
    } = options;

    let lines = content.split('\n');

    // 1. 移除注释（可选）
    if (removeComments) {
      lines = this.removeComments(lines);
    }

    // 2. 移除空行（可选）
    if (removeEmptyLines) {
      lines = lines.filter(line => line.trim().length > 0);
    }

    // 3. 如果行数超限，智能截取
    if (lines.length > maxLines) {
      lines = this.smartTruncate(lines, maxLines, {
        includeImports,
        includeExports
      });
    }

    return lines.join('\n');
  }

  /**
   * 移除注释
   */
  private removeComments(lines: string[]): string[] {
    return lines.filter(line => {
      const trimmed = line.trim();
      // JavaScript/TypeScript注释
      if (trimmed.startsWith('//')) return false;
      if (trimmed.startsWith('/*')) return false;
      if (trimmed.startsWith('*')) return false;
      // Python注释
      if (trimmed.startsWith('#')) return false;
      return true;
    });
  }

  /**
   * 智能截取
   */
  private smartTruncate(
    lines: string[],
    maxLines: number,
    options: { includeImports: boolean; includeExports: boolean }
  ): string[] {
    const {
      imports = [],
      exports = [],
      mainCode = []
    } = this.categorizeLines(lines);

    const result: string[] = [];
    let lineCount = 0;

    // 1. 包含imports
    if (options.includeImports) {
      result.push(...imports);
      lineCount += imports.length;
    }

    // 2. 包含部分main code
    const remainingLines = maxLines - lineCount;
    if (remainingLines > 0) {
      result.push(...mainCode.slice(0, remainingLines));
    }

    // 3. 如果还有空间，包含exports
    if (options.includeExports && lineCount + remainingLines < maxLines) {
      const moreSpace = maxLines - lineCount - remainingLines;
      if (moreSpace > 0) {
        result.push('// ...', ...exports.slice(0, moreSpace));
      }
    }

    return result;
  }

  /**
   * 分类代码行
   */
  private categorizeLines(lines: string[]): {
    imports: string[];
    exports: string[];
    mainCode: string[];
  } {
    const imports: string[] = [];
    const exports: string[] = [];
    const mainCode: string[] = [];

    for (const line of lines) {
      if (line.includes('import ') || line.includes('require(')) {
        imports.push(line);
      } else if (line.includes('export ')) {
        exports.push(line);
      } else {
        mainCode.push(line);
      }
    }

    return { imports, exports, mainCode };
  }
}
```

<br/>

***

<br/>

## 五、长对话处理技巧

### 5.1 对话分段策略

**按任务分段：**

```typescript
class ConversationSegmenter {
  /**
   * 将长对话分段
   */
  segment(messages: Message[]): ConversationSegment[] {
    const segments: ConversationSegment[] = [];
    let currentSegment: Message[] = [];
    let currentTask = '';

    for (const message of messages) {
      // 检测新任务开始
      if (this.isNewTask(message, currentTask)) {
        // 保存当前段
        if (currentSegment.length > 0) {
          segments.push({
            task: currentTask,
            messages: currentSegment
          });
        }
        
        // 开始新段
        currentTask = this.extractTask(message);
        currentSegment = [message];
      } else {
        currentSegment.push(message);
      }
    }

    // 保存最后一段
    if (currentSegment.length > 0) {
      segments.push({
        task: currentTask,
        messages: currentSegment
      });
    }

    return segments;
  }

  /**
   * 检测是否是新任务
   */
  private isNewTask(message: Message, currentTask: string): boolean {
    if (message.role !== 'user') return false;

    const content = typeof message.content === 'string'
      ? message.content
      : '';

    // 简单规则：检测明确的任务切换关键词
    const taskSwitchPatterns = [
      /帮我/,
      /现在/,
      /接下来/,
      /换个/,
      /new task/i,
      /switch to/i
    ];

    return taskSwitchPatterns.some(pattern => pattern.test(content));
  }

  /**
   * 提取任务描述
   */
  private extractTask(message: Message): string {
    const content = typeof message.content === 'string'
      ? message.content
      : '';

    // 提取前50字符作为任务描述
    return content.substring(0, 50);
  }
}
```

<br/>

### 5.2 关键信息保留

**提取并保留关键信息：**

```typescript
class KeyInfoExtractor {
  /**
   * 提取关键信息
   */
  extract(messages: Message[]): KeyInfo {
    const keyInfo: KeyInfo = {
      decisions: [],
      filesCreated: [],
      filesModified: [],
      toolsUsed: new Set(),
      errors: []
    };

    for (const message of messages) {
      // 1. 提取决策
      if (this.containsDecision(message)) {
        keyInfo.decisions.push(this.extractDecision(message));
      }

      // 2. 提取文件操作
      if (typeof message.content !== 'string') {
        for (const part of message.content) {
          if (part.type === 'tool_use') {
            keyInfo.toolsUsed.add(part.name);
            
            if (part.name === 'write') {
              keyInfo.filesCreated.push(part.input.file_path);
            } else if (part.name === 'edit') {
              keyInfo.filesModified.push(part.input.file_path);
            }
          } else if (part.type === 'tool_result' && part.is_error) {
            keyInfo.errors.push(part.content);
          }
        }
      }
    }

    return keyInfo;
  }

  /**
   * 检测是否包含决策
   */
  private containsDecision(message: Message): boolean {
    const content = typeof message.content === 'string'
      ? message.content
      : '';

    const decisionPatterns = [
      /决定/,
      /选择/,
      /采用/,
      /使用/,
      /decided/i,
      /chose/i,
      /will use/i
    ];

    return decisionPatterns.some(pattern => pattern.test(content));
  }

  /**
   * 提取决策内容
   */
  private extractDecision(message: Message): string {
    const content = typeof message.content === 'string'
      ? message.content
      : '';

    // 提取包含决策关键词的句子
    const sentences = content.split(/[。.]/);
    for (const sentence of sentences) {
      if (this.containsDecision({ role: 'assistant', content: sentence })) {
        return sentence.trim();
      }
    }

    return '';
  }
}
```

<br/>

***

<br/>

## 六、实际应用案例

### 6.1 大型项目上下文管理

**案例：1000+文件的项目**

```typescript
async function handleLargeProject(
  projectPath: string,
  userQuery: string
): Promise<Context> {
  const contextManager = new ContextManager();
  
  // 1. 扫描项目文件
  const allFiles = await scanProject(projectPath);
  console.log(`发现 ${allFiles.length} 个文件`);

  // 2. 快速过滤
  const relevantFiles = await quickFilter(allFiles);
  console.log(`过滤后 ${relevantFiles.length} 个文件`);

  // 3. 选择最相关的文件
  const selector = new FileSelector();
  const selectedFiles = await selector.selectRelevantFiles(
    userQuery,
    relevantFiles,
    150000  // 150K tokens预算
  );
  console.log(`选择 ${selectedFiles.length} 个文件`);

  // 4. 构建上下文
  const context = await contextManager.buildContext({
    systemPrompt: getSystemPrompt(),
    files: selectedFiles,
    maxTokens: 200000
  });

  // 5. 验证Token限制
  const tokens = contextManager.countTokens(context);
  console.log(`总Token数: ${tokens}`);

  return context;
}
```

<br/>

### 6.2 长对话压缩案例

**案例：100轮对话压缩**

```typescript
async function handleLongConversation(
  messages: Message[]
): Promise<Message[]> {
  const compressor = new MessageCompressor();
  
  console.log(`原始消息数: ${messages.length}`);

  // 1. 分段
  const segmenter = new ConversationSegmenter();
  const segments = segmenter.segment(messages);
  console.log(`分为 ${segments.length} 个任务段`);

  // 2. 提取关键信息
  const extractor = new KeyInfoExtractor();
  const keyInfo = extractor.extract(messages);
  console.log(`提取到 ${keyInfo.decisions.length} 个决策`);

  // 3. 压缩每段
  const compressedSegments = segments.map(segment => ({
    task: segment.task,
    summary: compressor.summarize(segment.messages)
  }));

  // 4. 构建压缩后的历史
  const compressedHistory: Message[] = [
    {
      role: 'user',
      content: `[历史摘要]\n\n${compressedSegments.map(s => 
        `任务: ${s.task}\n${s.summary}`
      ).join('\n\n')}`
    },
    {
      role: 'user',
      content: `[关键信息]\n\n决策:\n${keyInfo.decisions.map(d => `- ${d}`).join('\n')}\n\n创建的文件:\n${keyInfo.filesCreated.map(f => `- ${f}`).join('\n')}\n\n修改的文件:\n${keyInfo.filesModified.map(f => `- ${f}`).join('\n')}`
    },
    // 保留最近10条消息
    ...messages.slice(-10)
  ];

  console.log(`压缩后消息数: ${compressedHistory.length}`);

  return compressedHistory;
}
```

<br/>

***

<br/>

## 七、最佳实践

### 7.1 上下文管理清单

```
✅ 开始任务前
  □ 了解项目规模
  □ 估算Token需求
  □ 准备文件选择策略

✅ 选择文件时
  □ 使用智能匹配
  □ 考虑文件类型权重
  □ 优先最近修改的文件
  □ 控制Token预算

✅ 处理长对话时
  □ 定期压缩历史
  □ 保留关键决策
  □ 维护任务摘要
  □ 监控Token使用

✅ 优化性能时
  □ 使用增量更新
  □ 缓存常用文件
  □ 并行处理文件
  □ 定期清理缓存
```

<br/>

### 7.2 性能优化建议

```typescript
// 1. 使用缓存
class CachedContextManager extends ContextManager {
  private cache = new Map<string, CachedContext>();

  async getContext(projectPath: string): Promise<Context> {
    const cacheKey = this.getCacheKey(projectPath);
    
    // 检查缓存
    const cached = this.cache.get(cacheKey);
    if (cached && !this.isStale(cached)) {
      return cached.context;
    }

    // 构建新上下文
    const context = await this.buildContext(projectPath);
    
    // 更新缓存
    this.cache.set(cacheKey, {
      context,
      timestamp: Date.now()
    });

    return context;
  }
}

// 2. 增量更新
class IncrementalUpdater {
  async updateContext(
    context: Context,
    changes: FileChange[]
  ): Promise<Context> {
    for (const change of changes) {
      const index = context.projectFiles.findIndex(
        f => f.path === change.path
      );

      if (index >= 0) {
        // 更新现有文件
        context.projectFiles[index].content = change.content;
      } else if (change.type === 'add') {
        // 添加新文件
        context.projectFiles.push({
          path: change.path,
          content: change.content,
          tokens: this.countTokens(change.content)
        });
      }
    }

    return context;
  }
}

// 3. 并行处理
async function processFilesInParallel(
  files: string[]
): Promise<ProcessedFile[]> {
  const batchSize = 10;
  const results: ProcessedFile[] = [];

  for (let i = 0; i < files.length; i += batchSize) {
    const batch = files.slice(i, i + batchSize);
    const processed = await Promise.all(
      batch.map(file => processFile(file))
    );
    results.push(...processed);
  }

  return results;
}
```

<br/>

***

<br/>

## 八、总结

### 8.1 核心要点

**上下文管理的三大支柱：**

```
1. Token管理
   ✅ 精确计数
   ✅ 预算控制
   ✅ 实时监控

2. 文件选择
   ✅ 智能匹配
   ✅ 优先级排序
   ✓ 动态调整

3. 压缩优化
   ✅ 对话摘要
   ✅ 文件裁剪
   ✅ 关键信息保留
```

**关键设计模式：**

```
✅ 策略模式（多种压缩策略）
✅ 责任链模式（多阶段选择）
✅ 观察者模式（Token监控）
✅ 缓存模式（性能优化）
```

<br/>

### 8.2 下一篇预告

**在AI-31《安全与性能》中，我们将学习：**

```
🔄 安全机制设计
   - 多层防护体系
   - 权限控制
   - 审计日志

🔄 性能优化策略
   - 缓存机制
   - 并发控制
   - 资源管理

🔄 测试策略
   - 单元测试
   - 集成测试
   - 性能测试
```

<br/>

***

<br/>

**系列导航**

• 上一篇：AI-29 工具系统（Tool System）
• 下一篇：AI-31 安全与性能（Security & Performance）

<br/>

***

本文是《Claude Code 源代码解读与分析》系列第4篇
作者：生活助理 | 发布时间：2026-04-07

**掌握上下文管理，让AI记住关键信息！** 🧠✨
