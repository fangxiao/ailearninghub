# Agent 核心实现：消息循环与工具调用

阅读时间：45分钟
难度等级：⭐⭐⭐⭐ 高级
前置知识：AI-27 架构概览

<br/>

***

<br/>

## 上一篇回顾

**在AI-27《架构概览》中，我们了解了：**

```
✅ Claude Code 的整体架构
✅ 三大核心模块：Agent、Tools、Context
✅ 完整的工作流程
✅ 设计亮点与安全机制
```

**本篇重点：**

```
本篇将深入Agent模块，学习：
  └─ Agent 类的完整实现
  └─ 消息循环机制详解
  └─ 工具调用流程分析
  └─ 流式响应处理
  └─ 错误处理与重试
```

**为什么重要：**

```
Agent是整个系统的核心：
  ❓ 如何管理多轮对话？
  ❓ 如何决定何时调用工具？
  ❓ 如何处理工具返回的结果？
  ❓ 如何实现流式响应？

掌握Agent实现，你就掌握了AI Coding工具的核心逻辑！
```

<br/>

***

<br/>

## 一、Agent 类设计

### 1.1 Agent 的职责

**Agent是什么？**

```
Agent是系统的"指挥官"，负责：
  ┌─────────────────────────────┐
  │   接收用户输入               │
  └──────────┬──────────────────┘
             │
  ┌──────────▼──────────────────┐
  │   管理对话历史               │
  └──────────┬──────────────────┘
             │
  ┌──────────▼──────────────────┐
  │   调用Claude API             │
  └──────────┬──────────────────┘
             │
  ┌──────────▼──────────────────┐
  │   执行工具调用               │
  └──────────┬──────────────────┘
             │
  ┌──────────▼──────────────────┐
  │   返回结果给用户             │
  └─────────────────────────────┘
```

**核心能力：**

```typescript
interface AgentCapabilities {
  // 1. 对话管理
  manageConversation(): void;
  
  // 2. 工具编排
  orchestrateTools(): void;
  
  // 3. 上下文控制
  controlContext(): void;
  
  // 4. 错误恢复
  recoverFromErrors(): void;
}
```

<br/>

### 1.2 Agent 类结构

**基础结构：**

```typescript
class Agent {
  // ===== 成员变量 =====
  
  // API客户端
  private api: ClaudeAPI;
  
  // 消息历史
  private messages: Message[] = [];
  
  // 工具注册表
  private tools: Map<string, Tool> = new Map();
  
  // 上下文管理器
  private contextManager: ContextManager;
  
  // 配置选项
  private options: AgentOptions;
  
  // 状态管理
  private state: AgentState = {
    isProcessing: false,
    lastError: null,
    tokenUsage: { input: 0, output: 0 }
  };

  // ===== 核心方法 =====
  
  // 初始化
  constructor(options: AgentOptions) {
    this.api = new ClaudeAPI(options.apiKey);
    this.contextManager = new ContextManager(options.maxTokens);
    this.options = options;
    this.registerDefaultTools();
  }
  
  // 主入口：处理用户输入
  async chat(userInput: string): Promise<AgentResponse> {
    // 实现见下文
  }
  
  // 流式处理
  async *chatStream(userInput: string): AsyncGenerator<StreamChunk> {
    // 实现见下文
  }

  // ===== 工具管理 =====
  
  // 注册工具
  registerTool(tool: Tool): void {
    this.tools.set(tool.name, tool);
  }
  
  // 获取工具定义（给Claude看的）
  private getToolDefinitions(): ToolDefinition[] {
    return Array.from(this.tools.values()).map(tool => ({
      name: tool.name,
      description: tool.description,
      input_schema: tool.inputSchema
    }));
  }

  // ===== 消息管理 =====
  
  // 添加用户消息
  private addUserMessage(content: string): void {
    this.messages.push({ role: 'user', content });
  }
  
  // 添加助手消息
  private addAssistantMessage(content: Content[]): void {
    this.messages.push({ role: 'assistant', content });
  }
  
  // 添加工具结果
  private addToolResult(toolUseId: string, result: string): void {
    this.messages.push({
      role: 'user',
      content: [{
        type: 'tool_result',
        tool_use_id: toolUseId,
        content: result
      }]
    });
  }
}
```

**配置选项：**

```typescript
interface AgentOptions {
  // API配置
  apiKey: string;
  model: string;  // 'claude-3-opus' | 'claude-3-sonnet' | 'claude-3-haiku'
  
  // Token限制
  maxTokens: number;          // 最大输出token
  contextWindow: number;      // 上下文窗口大小
  
  // 行为控制
  autoApprove: boolean;       // 自动批准工具调用
  maxToolCalls: number;       // 最大工具调用次数
  timeout: number;            // 超时时间（毫秒）
  
  // 调试选项
  debug: boolean;
  logLevel: 'error' | 'warn' | 'info' | 'debug';
}

// 默认配置
const DEFAULT_OPTIONS: AgentOptions = {
  apiKey: process.env.ANTHROPIC_API_KEY,
  model: 'claude-3-opus',
  maxTokens: 4096,
  contextWindow: 200000,
  autoApprove: false,
  maxToolCalls: 10,
  timeout: 60000,
  debug: false,
  logLevel: 'info'
};
```

<br/>

***

<br/>

## 二、消息循环机制

### 2.1 消息循环是什么？

**为什么需要消息循环？**

```
简单对话：
  用户 → Claude → 回复 ✅（一次就完成）

工具调用对话：
  用户 → Claude → 工具调用 → 执行工具 → 
  工具结果 → Claude → 最终回复 ✅（需要多轮）

可能的情况：
  ❓ Claude可能一次调用多个工具
  ❓ 工具结果可能触发新的工具调用
  ❓ 需要循环直到Claude给出最终回复
```

**消息循环流程：**

```
┌─────────────┐
│ 用户输入     │
└──────┬──────┘
       │
       ▼
┌──────────────────────────────┐
│  Loop Start                   │
│  ┌────────────────────────┐  │
│  │ 1. 调用Claude API       │  │
│  └────────┬───────────────┘  │
│           │                   │
│  ┌────────▼───────────────┐  │
│  │ 2. Claude响应           │  │
│  │   - stop_reason?        │  │
│  └────────┬───────────────┘  │
│           │                   │
│      ┌────┴────┐              │
│      │         │              │
│   tool_use  end_turn          │
│      │         │              │
│      ▼         │              │
│  ┌─────────┐   │              │
│  │3.执行   │   │              │
│  │ 工具    │   │              │
│  └────┬────┘   │              │
│       │        │              │
│       ▼        │              │
│  ┌─────────┐   │              │
│  │4.返回   │   │              │
│  │ 结果    │   │              │
│  └────┬────┘   │              │
│       │        │              │
│       └────────┘              │
│           │                   │
│       继续循环                 │
└───────────┬───────────────────┘
            │
            ▼
       最终回复
```

<br/>

### 2.2 消息循环实现

**基础实现：**

```typescript
async chat(userInput: string): Promise<AgentResponse> {
  // 1. 添加用户消息
  if (userInput) {
    this.addUserMessage(userInput);
  }

  // 2. 消息循环
  let iteration = 0;
  const maxIterations = this.options.maxToolCalls + 1;

  while (iteration < maxIterations) {
    iteration++;
    
    try {
      // 2.1 调用Claude API
      const response = await this.callClaude();
      
      // 2.2 检查响应类型
      if (response.stop_reason === 'end_turn') {
        // Claude给出最终回复，退出循环
        return this.handleFinalResponse(response);
      }
      
      // 2.3 处理工具调用
      if (response.stop_reason === 'tool_use') {
        // 添加助手消息（包含工具调用）
        this.addAssistantMessage(response.content);
        
        // 执行所有工具调用
        const toolResults = await this.executeTools(response.content);
        
        // 添加工具结果到消息历史
        for (const result of toolResults) {
          this.addToolResult(result.tool_use_id, result.content);
        }
        
        // 继续循环，让Claude处理工具结果
        continue;
      }
      
      // 2.4 其他stop_reason（如max_tokens）
      return this.handleStopResponse(response);
      
    } catch (error) {
      // 错误处理
      return this.handleError(error);
    }
  }

  // 3. 超过最大迭代次数
  return this.handleError(new Error('超过最大工具调用次数'));
}
```

**完整的Claude API调用：**

```typescript
private async callClaude(): Promise<ClaudeResponse> {
  // 1. 构建系统提示词
  const systemPrompt = this.buildSystemPrompt();
  
  // 2. 准备工具定义
  const tools = this.getToolDefinitions();
  
  // 3. 计算token使用情况
  const currentTokens = this.countTokens();
  if (currentTokens > this.options.contextWindow) {
    // 上下文窗口超限，需要压缩
    await this.compressContext();
  }

  // 4. 调用API
  const response = await this.api.messages.create({
    model: this.options.model,
    max_tokens: this.options.maxTokens,
    system: systemPrompt,
    messages: this.messages,
    tools: tools.length > 0 ? tools : undefined
  });

  // 5. 更新token统计
  this.state.tokenUsage.input += response.usage.input_tokens;
  this.state.tokenUsage.output += response.usage.output_tokens;

  // 6. 记录日志
  if (this.options.debug) {
    console.log(`[Claude API] stop_reason: ${response.stop_reason}`);
    console.log(`[Claude API] tokens: ${response.usage.input_tokens} in, ${response.usage.output_tokens} out`);
  }

  return response;
}
```

<br/>

### 2.3 消息类型详解

**Claude API的消息类型：**

```typescript
// 用户消息
interface UserMessage {
  role: 'user';
  content: string | Content[];
}

// 助手消息
interface AssistantMessage {
  role: 'assistant';
  content: Content[];
}

// 内容类型
type Content = TextContent | ToolUseContent | ToolResultContent;

// 文本内容
interface TextContent {
  type: 'text';
  text: string;
}

// 工具调用
interface ToolUseContent {
  type: 'tool_use';
  id: string;          // 工具调用ID
  name: string;        // 工具名称
  input: any;          // 工具输入参数
}

// 工具结果
interface ToolResultContent {
  type: 'tool_result';
  tool_use_id: string; // 对应的tool_use ID
  content: string;     // 工具执行结果
  is_error?: boolean;  // 是否出错
}
```

**消息历史示例：**

```typescript
const messages: Message[] = [
  // 第1轮：用户提问
  {
    role: 'user',
    content: '读取src/index.ts文件'
  },
  
  // 第2轮：Claude调用工具
  {
    role: 'assistant',
    content: [
      {
        type: 'tool_use',
        id: 'toolu_01ABC',
        name: 'read',
        input: { file_path: 'src/index.ts' }
      }
    ]
  },
  
  // 第3轮：返回工具结果
  {
    role: 'user',
    content: [
      {
        type: 'tool_result',
        tool_use_id: 'toolu_01ABC',
        content: '文件内容...'
      }
    ]
  },
  
  // 第4轮：Claude的最终回复
  {
    role: 'assistant',
    content: [
      {
        type: 'text',
        text: '我已读取了文件，内容如下...'
      }
    ]
  }
];
```

<br/>

***

<br/>

## 三、工具调用流程

### 3.1 工具调用机制

**工具调用的完整流程：**

```
第1步：Claude分析用户需求
  用户："修复src/utils.ts中的bug"
  Claude分析：需要先读取文件

第2步：Claude决定调用工具
  {
    type: 'tool_use',
    id: 'toolu_01ABC',
    name: 'read',
    input: { file_path: 'src/utils.ts' }
  }

第3步：Agent接收并执行工具
  - 解析工具名称和参数
  - 查找对应的Tool实例
  - 调用tool.execute(input)

第4步：工具返回结果
  {
    type: 'tool_result',
    tool_use_id: 'toolu_01ABC',
    content: '文件内容...'
  }

第5步：Claude分析结果并决定下一步
  - 可能调用更多工具（如edit）
  - 或直接给出最终回复
```

**工具执行实现：**

```typescript
private async executeTools(content: Content[]): Promise<ToolResultContent[]> {
  // 1. 筛选出工具调用
  const toolCalls = content.filter(c => c.type === 'tool_use') as ToolUseContent[];
  
  // 2. 执行所有工具调用（并发）
  const results = await Promise.all(
    toolCalls.map(call => this.executeSingleTool(call))
  );
  
  return results;
}

private async executeSingleTool(call: ToolUseContent): Promise<ToolResultContent> {
  const { id, name, input } = call;
  
  try {
    // 1. 查找工具
    const tool = this.tools.get(name);
    if (!tool) {
      throw new Error(`工具未找到: ${name}`);
    }
    
    // 2. 权限检查（如果未启用自动批准）
    if (!this.options.autoApprove) {
      const approved = await this.requestApproval(name, input);
      if (!approved) {
        throw new Error('用户拒绝执行工具');
      }
    }
    
    // 3. 执行工具
    const startTime = Date.now();
    const result = await tool.execute(input);
    const duration = Date.now() - startTime;
    
    // 4. 记录日志
    if (this.options.debug) {
      console.log(`[Tool] ${name} executed in ${duration}ms`);
      console.log(`[Tool] Input:`, input);
      console.log(`[Tool] Output:`, result.substring(0, 100) + '...');
    }
    
    // 5. 返回成功结果
    return {
      type: 'tool_result',
      tool_use_id: id,
      content: result
    };
    
  } catch (error) {
    // 6. 返回错误结果
    return {
      type: 'tool_result',
      tool_use_id: id,
      content: `错误: ${error.message}`,
      is_error: true
    };
  }
}
```

<br/>

### 3.2 权限请求机制

**为什么需要权限请求？**

```
安全考虑：
  ❌ 防止AI执行危险操作（如删除文件）
  ❌ 让用户知情和控制
  ❌ 审计和追踪

实现方式：
  ✅ 每次工具调用前请求批准
  ✅ 显示工具名称和参数
  ✅ 用户可以选择批准或拒绝
  ✅ 支持自动批准模式
```

**权限请求实现：**

```typescript
private async requestApproval(toolName: string, input: any): Promise<boolean> {
  // 1. 构建请求消息
  const message = this.formatApprovalRequest(toolName, input);
  
  // 2. 显示给用户
  console.log('\n' + message);
  console.log('批准执行？ (y/n/a)');
  
  // 3. 等待用户输入
  const answer = await this.waitForInput();
  
  // 4. 处理用户响应
  switch (answer.toLowerCase()) {
    case 'y':
      return true;
    case 'n':
      return false;
    case 'a':
      // 自动批准后续所有工具调用
      this.options.autoApprove = true;
      return true;
    default:
      return false;
  }
}

private formatApprovalRequest(toolName: string, input: any): string {
  const lines = [
    '┌─────────────────────────────────┐',
    '│  工具调用请求                    │',
    '├─────────────────────────────────┤',
  ];
  
  // 工具名称
  lines.push(`│  工具: ${toolName.padEnd(24)}│`);
  
  // 参数（格式化显示）
  const inputStr = JSON.stringify(input, null, 2);
  const inputLines = inputStr.split('\n').slice(0, 5); // 最多显示5行
  for (const line of inputLines) {
    lines.push(`│  ${line.padEnd(32)}│`);
  }
  
  if (inputLines.length < inputStr.split('\n').length) {
    lines.push(`│  ... (更多参数省略)${' '.repeat(13)}│`);
  }
  
  lines.push('└─────────────────────────────────┘');
  
  return lines.join('\n');
}
```

<br/>

***

<br/>

## 四、流式响应处理

### 4.1 为什么需要流式响应？

**传统方式的问题：**

```
非流式：
  用户发送 → 等待... → 完整回复
  
问题：
  ❌ 等待时间长（可能10-30秒）
  ❌ 用户体验差
  ❌ 无法提前看到进度
```

**流式响应的优势：**

```
流式：
  用户发送 → 立即开始返回 → 逐字显示
  
优势：
  ✅ 即时反馈
  ✅ 用户体验好
  ✅ 可以提前中断
  ✅ 显示进度
```

<br/>

### 4.2 流式响应实现

**AsyncGenerator实现：**

```typescript
async *chatStream(userInput: string): AsyncGenerator<StreamChunk> {
  // 1. 添加用户消息
  if (userInput) {
    this.addUserMessage(userInput);
  }

  // 2. 消息循环
  let iteration = 0;
  const maxIterations = this.options.maxToolCalls + 1;

  while (iteration < maxIterations) {
    iteration++;
    
    // 2.1 流式调用Claude API
    const stream = await this.callClaudeStream();
    
    // 2.2 处理流式响应
    let currentContent: Content[] = [];
    let currentTextBlock: TextContent | null = null;
    let currentToolUse: ToolUseContent | null = null;
    
    for await (const chunk of stream) {
      // 处理不同类型的chunk
      switch (chunk.type) {
        case 'content_block_start':
          // 新的内容块开始
          if (chunk.content_block.type === 'text') {
            currentTextBlock = { type: 'text', text: '' };
          } else if (chunk.content_block.type === 'tool_use') {
            currentToolUse = {
              type: 'tool_use',
              id: chunk.content_block.id,
              name: '',
              input: {}
            };
          }
          break;
          
        case 'content_block_delta':
          // 内容块增量
          if (chunk.delta.type === 'text_delta' && currentTextBlock) {
            // 文本增量
            currentTextBlock.text += chunk.delta.text;
            
            // 立即yield给用户
            yield {
              type: 'text',
              text: chunk.delta.text
            };
          } else if (chunk.delta.type === 'input_json_delta' && currentToolUse) {
            // 工具输入增量
            // 累积JSON字符串
            if (!currentToolUse.inputJson) {
              currentToolUse.inputJson = '';
            }
            currentToolUse.inputJson += chunk.delta.partial_json;
          }
          break;
          
        case 'content_block_stop':
          // 内容块结束
          if (currentTextBlock) {
            currentContent.push(currentTextBlock);
            currentTextBlock = null;
          } else if (currentToolUse) {
            // 解析完整的工具输入JSON
            try {
              currentToolUse.input = JSON.parse(currentToolUse.inputJson || '{}');
              delete currentToolUse.inputJson;
              currentContent.push(currentToolUse);
            } catch (error) {
              console.error('工具输入JSON解析失败:', error);
            }
            currentToolUse = null;
          }
          break;
          
        case 'message_stop':
          // 消息结束
          this.addAssistantMessage(currentContent);
          
          // 检查是否需要继续循环
          if (this.hasToolUse(currentContent)) {
            // 执行工具
            const toolResults = await this.executeTools(currentContent);
            
            // 添加工具结果
            for (const result of toolResults) {
              this.addToolResult(result.tool_use_id, result.content);
              
              // Yield工具执行结果
              yield {
                type: 'tool_result',
                tool_name: this.getToolName(currentContent, result.tool_use_id),
                result: result.content
              };
            }
            
            // 继续循环
            currentContent = [];
            continue;
          }
          
          // 最终回复，退出循环
          return;
      }
    }
  }
}
```

**StreamChunk类型：**

```typescript
interface StreamChunk {
  type: 'text' | 'tool_result' | 'error';
  
  // 文本内容
  text?: string;
  
  // 工具结果
  tool_name?: string;
  result?: string;
  
  // 错误
  error?: string;
}
```

**使用示例：**

```typescript
const agent = new Agent(options);

// 流式处理
for await (const chunk of agent.chatStream('帮我读取package.json')) {
  switch (chunk.type) {
    case 'text':
      // 实时显示文本
      process.stdout.write(chunk.text);
      break;
      
    case 'tool_result':
      // 显示工具执行结果
      console.log(`\n[工具 ${chunk.tool_name} 执行完成]`);
      break;
      
    case 'error':
      // 显示错误
      console.error(`\n错误: ${chunk.error}`);
      break;
  }
}
```

<br/>

***

<br/>

## 五、错误处理与重试

### 5.1 错误类型

**可能的错误：**

```typescript
enum AgentErrorType {
  // API错误
  API_KEY_INVALID = 'api_key_invalid',
  RATE_LIMIT = 'rate_limit',
  NETWORK_ERROR = 'network_error',
  CONTEXT_LENGTH_EXCEEDED = 'context_length_exceeded',
  
  // 工具错误
  TOOL_NOT_FOUND = 'tool_not_found',
  TOOL_EXECUTION_FAILED = 'tool_execution_failed',
  PERMISSION_DENIED = 'permission_denied',
  
  // Agent错误
  MAX_ITERATIONS_EXCEEDED = 'max_iterations_exceeded',
  TIMEOUT = 'timeout',
  INVALID_STATE = 'invalid_state'
}

class AgentError extends Error {
  constructor(
    public type: AgentErrorType,
    message: string,
    public retryable: boolean = false
  ) {
    super(message);
  }
}
```

<br/>

### 5.2 重试策略

**指数退避重试：**

```typescript
private async withRetry<T>(
  fn: () => Promise<T>,
  options: RetryOptions = {}
): Promise<T> {
  const {
    maxRetries = 3,
    baseDelay = 1000,
    maxDelay = 30000,
    shouldRetry = this.defaultShouldRetry
  } = options;
  
  let lastError: Error;
  
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      
      // 检查是否应该重试
      if (!shouldRetry(error)) {
        throw error;
      }
      
      // 指数退避
      const delay = Math.min(baseDelay * Math.pow(2, i), maxDelay);
      
      console.warn(`尝试 ${i + 1}/${maxRetries} 失败: ${error.message}`);
      console.warn(`等待 ${delay}ms 后重试...`);
      
      await this.sleep(delay);
    }
  }
  
  throw lastError;
}

private defaultShouldRetry(error: any): boolean {
  // 网络错误
  if (error.code === 'ECONNREFUSED' || error.code === 'ETIMEDOUT') {
    return true;
  }
  
  // 限流错误
  if (error.status === 429) {
    return true;
  }
  
  // 服务器错误
  if (error.status >= 500 && error.status < 600) {
    return true;
  }
  
  // 其他错误不重试
  return false;
}
```

**完整的错误处理：**

```typescript
private async handleApiError(error: any): Promise<AgentResponse> {
  // 1. 识别错误类型
  const errorType = this.classifyError(error);
  
  // 2. 根据错误类型采取不同策略
  switch (errorType) {
    case AgentErrorType.RATE_LIMIT:
      // 限流：等待后重试
      const retryAfter = error.headers?.['retry-after'] || 60;
      console.warn(`API限流，${retryAfter}秒后重试`);
      await this.sleep(retryAfter * 1000);
      return this.retryLastMessage();
      
    case AgentErrorType.CONTEXT_LENGTH_EXCEEDED:
      // 上下文超限：压缩历史
      console.warn('上下文超限，压缩消息历史');
      await this.compressContext();
      return this.retryLastMessage();
      
    case AgentErrorType.NETWORK_ERROR:
      // 网络错误：重试
      return this.retryWithBackoff();
      
    case AgentErrorType.API_KEY_INVALID:
      // API密钥无效：无法恢复
      throw new AgentError(
        AgentErrorType.API_KEY_INVALID,
        'API密钥无效，请检查配置',
        false
      );
      
    default:
      // 未知错误
      throw new AgentError(
        AgentErrorType.INVALID_STATE,
        `未知错误: ${error.message}`,
        false
      );
  }
}
```

<br/>

***

<br/>

## 六、状态管理

### 6.1 Agent状态

**状态定义：**

```typescript
interface AgentState {
  // 处理状态
  isProcessing: boolean;
  isPaused: boolean;
  
  // 错误状态
  lastError: AgentError | null;
  errorCount: number;
  
  // Token使用
  tokenUsage: {
    input: number;
    output: number;
    total: number;
  };
  
  // 工具调用统计
  toolCalls: {
    [toolName: string]: number;  // 调用次数
  };
  
  // 会话信息
  sessionId: string;
  startTime: number;
  messageCount: number;
}
```

**状态更新：**

```typescript
private updateState(updates: Partial<AgentState>): void {
  this.state = { ...this.state, ...updates };
  
  // 触发状态变化事件
  this.emit('stateChange', this.state);
}

// 在关键位置更新状态
async chat(userInput: string): Promise<AgentResponse> {
  this.updateState({ isProcessing: true });
  
  try {
    const response = await this.chatInternal(userInput);
    
    this.updateState({
      isProcessing: false,
      messageCount: this.messages.length
    });
    
    return response;
  } catch (error) {
    this.updateState({
      isProcessing: false,
      lastError: error,
      errorCount: this.state.errorCount + 1
    });
    
    throw error;
  }
}
```

<br/>

### 6.2 事件系统

**事件类型：**

```typescript
enum AgentEvent {
  // 生命周期事件
  START = 'start',
  END = 'end',
  ERROR = 'error',
  
  // 消息事件
  USER_MESSAGE = 'user_message',
  ASSISTANT_MESSAGE = 'assistant_message',
  TOOL_CALL = 'tool_call',
  TOOL_RESULT = 'tool_result',
  
  // 状态事件
  STATE_CHANGE = 'state_change',
  TOKEN_UPDATE = 'token_update'
}

interface EventPayload {
  type: AgentEvent;
  timestamp: number;
  data: any;
}
```

**事件发射器：**

```typescript
class Agent extends EventEmitter {
  // ... 其他代码
  
  private emit(event: AgentEvent, data?: any): void {
    super.emit(event, {
      type: event,
      timestamp: Date.now(),
      data
    });
  }
}

// 使用示例
const agent = new Agent(options);

agent.on(AgentEvent.TOOL_CALL, (payload) => {
  console.log(`工具调用: ${payload.data.name}`);
});

agent.on(AgentEvent.TOKEN_UPDATE, (payload) => {
  console.log(`Token使用: ${payload.data.total}`);
});

agent.on(AgentEvent.ERROR, (payload) => {
  console.error(`错误: ${payload.data.message}`);
});
```

<br/>

***

<br/>

## 七、总结

### 7.1 核心要点

**Agent实现的三大支柱：**

```
1. 消息循环
   ✅ 管理多轮对话
   ✅ 处理工具调用链
   ✅ 支持递归处理

2. 工具编排
   ✅ 工具查找和执行
   ✅ 权限控制
   ✅ 错误处理

3. 流式响应
   ✅ 即时反馈
   ✅ 提升用户体验
   ✅ 支持中断
```

**关键设计模式：**

```
✅ 状态机模式（消息循环）
✅ 策略模式（错误处理）
✅ 观察者模式（事件系统）
✅ 迭代器模式（流式响应）
```

<br/>

### 7.2 实战练习

**练习1：添加自定义工具**

```typescript
// 创建一个发送通知的工具
class NotifyTool implements Tool {
  name = 'notify';
  description = '发送桌面通知';
  inputSchema = {
    type: 'object',
    properties: {
      title: { type: 'string' },
      message: { type: 'string' }
    },
    required: ['title', 'message']
  };

  async execute(input: { title: string; message: string }): Promise<string> {
    // 实现通知逻辑
    return `通知已发送: ${input.title}`;
  }
}

// 注册到Agent
agent.registerTool(new NotifyTool());
```

**练习2：自定义错误处理**

```typescript
// 添加自定义错误处理
agent.on(AgentEvent.ERROR, async (payload) => {
  const error = payload.data;
  
  // 记录到日志系统
  await logToSystem(error);
  
  // 发送告警
  if (error.retryable === false) {
    await sendAlert(error);
  }
});
```

<br/>

### 7.3 下一篇预告

**在AI-29《工具系统》中，我们将学习：**

```
🔄 Tool接口的完整设计
   - 输入验证
   - 输出格式化
   - 错误处理

🔄 内置工具的实现细节
   - ReadTool：文件读取
   - WriteTool：文件写入
   - EditTool：文件编辑
   - ExecTool：命令执行

🔄 如何开发自定义工具
   - 最佳实践
   - 安全考虑
   - 性能优化
```

<br/>

***

<br/>

**系列导航**

• 上一篇：AI-27 Claude Code 架构概览
• 下一篇：AI-29 工具系统（Tool System）

<br/>

***

本文是《Claude Code 源代码解读与分析》系列第2篇
作者：生活助理 | 发布时间：2026-04-07

**深入Agent核心，掌握AI编程工具的灵魂！** 🧠✨
