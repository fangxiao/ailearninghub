# 工具系统（Tool System）：扩展AI的能力边界

阅读时间：45分钟
难度等级：⭐⭐⭐⭐ 高级
前置知识：AI-28 Agent核心实现

<br/>

***

<br/>

## 上一篇回顾

**在AI-28《Agent核心实现》中，我们学习了：**

```
✅ Agent类的完整设计
✅ 消息循环机制
✅ 工具调用流程
✅ 流式响应处理
✅ 错误处理与重试
```

**本篇重点：**

```
本篇将深入工具系统，学习：
  └─ Tool接口的完整设计
  └─ 内置工具的实现细节
  └─ 工具注册与发现机制
  └─ 自定义工具开发
  └─ 安全与性能优化
```

**为什么工具系统重要：**

```
工具是Agent的"手脚"：
  ❓ 如何安全地执行文件操作？
  ❓ 如何防止危险命令执行？
  ❓ 如何实现工具的权限控制？
  ❓ 如何开发自定义工具？

掌握工具系统，你就能扩展AI的能力边界！
```

<br/>

***

<br/>

## 一、Tool 接口设计

### 1.1 Tool 接口定义

**基础接口：**

```typescript
/**
 * 工具接口 - 所有工具必须实现此接口
 */
interface Tool {
  // ===== 元数据 =====
  
  /**
   * 工具名称（唯一标识）
   * 规则：
   *   - 使用小写字母和下划线
   *   - 长度：3-30字符
   *   - 示例：read_file, write_file, execute_command
   */
  readonly name: string;
  
  /**
   * 工具描述（给Claude看的）
   * 要求：
   *   - 清晰说明工具功能
   *   - 说明使用场景
   *   - 说明注意事项
   *   - 长度：50-500字符
   */
  readonly description: string;
  
  /**
   * 输入参数定义（JSON Schema）
   * 用于：
   *   - 参数验证
   *   - 生成Claude的工具定义
   *   - 自动生成文档
   */
  readonly inputSchema: JSONSchema;
  
  // ===== 配置选项 =====
  
  /**
   * 是否需要权限批准
   * - true: 每次调用都需要用户批准
   * - false: 自动执行
   * @default true
   */
  readonly requiresApproval?: boolean;
  
  /**
   * 是否为危险操作
   * 危险操作会有额外的警告提示
   * @default false
   */
  readonly isDangerous?: boolean;
  
  /**
   * 超时时间（毫秒）
   * @default 30000
   */
  readonly timeout?: number;
  
  /**
   * 是否支持并发调用
   * @default true
   */
  readonly concurrent?: boolean;

  // ===== 核心方法 =====
  
  /**
   * 执行工具
   * @param input 工具输入参数
   * @param context 执行上下文
   * @returns 执行结果
   */
  execute(
    input: any,
    context: ToolContext
  ): Promise<ToolResult>;
  
  // ===== 生命周期钩子（可选）=====
  
  /**
   * 工具初始化
   * 在首次使用前调用
   */
  initialize?(): Promise<void>;
  
  /**
   * 工具清理
   * 在Agent关闭时调用
   */
  cleanup?(): Promise<void>;
  
  /**
   * 验证输入参数
   * 在execute前调用
   */
  validate?(input: any): Promise<boolean>;
}
```

**执行上下文：**

```typescript
/**
 * 工具执行上下文
 */
interface ToolContext {
  // 工作目录
  workingDirectory: string;
  
  // 环境变量
  environment: Record<string, string>;
  
  // 会话ID
  sessionId: string;
  
  // 请求批准函数
  requestApproval: (message: string) => Promise<boolean>;
  
  // 日志函数
  log: (level: 'info' | 'warn' | 'error', message: string) => void;
  
  // 配置选项
  options: {
    timeout: number;
    maxOutputSize: number;
    sandbox: boolean;
  };
}
```

**执行结果：**

```typescript
/**
 * 工具执行结果
 */
interface ToolResult {
  // 结果内容
  content: string;
  
  // 是否成功
  success: boolean;
  
  // 错误信息（如果失败）
  error?: {
    code: string;
    message: string;
    details?: any;
  };
  
  // 元数据
  metadata?: {
    duration: number;      // 执行时长（毫秒）
    bytesProcessed?: number;
    filesAffected?: number;
    [key: string]: any;
  };
}
```

<br/>

### 1.2 JSON Schema 设计

**什么是JSON Schema？**

```
JSON Schema用于定义输入参数的结构：
  ✅ 参数类型（string、number、boolean等）
  ✅ 必填字段
  ✅ 参数验证规则
  ✅ 参数说明
  ✅ 默认值

Claude会根据Schema生成正确的工具调用参数
```

**基础示例：**

```typescript
const readToolSchema: JSONSchema = {
  type: 'object',
  properties: {
    file_path: {
      type: 'string',
      description: '要读取的文件路径（相对或绝对路径）'
    },
    encoding: {
      type: 'string',
      enum: ['utf-8', 'gbk', 'ascii'],
      default: 'utf-8',
      description: '文件编码'
    },
    start_line: {
      type: 'integer',
      minimum: 1,
      description: '起始行号（可选，从第1行开始）'
    },
    end_line: {
      type: 'integer',
      minimum: 1,
      description: '结束行号（可选）'
    }
  },
  required: ['file_path']
};
```

**复杂示例：**

```typescript
const editToolSchema: JSONSchema = {
  type: 'object',
  properties: {
    file_path: {
      type: 'string',
      description: '要编辑的文件路径'
    },
    edits: {
      type: 'array',
      description: '编辑操作列表',
      items: {
        type: 'object',
        properties: {
          oldText: {
            type: 'string',
            description: '要替换的旧文本（必须完全匹配）'
          },
          newText: {
            type: 'string',
            description: '替换后的新文本'
          },
          startLine: {
            type: 'integer',
            description: '起始行号（用于定位）'
          }
        },
        required: ['oldText', 'newText']
      }
    },
    create_if_not_exists: {
      type: 'boolean',
      default: false,
      description: '文件不存在时是否创建'
    }
  },
  required: ['file_path', 'edits']
};
```

<br/>

***

<br/>

## 二、内置工具实现

### 2.1 ReadTool - 文件读取工具

**完整实现：**

```typescript
class ReadTool implements Tool {
  name = 'read';
  
  description = `读取文件内容。

使用场景：
- 查看代码文件
- 读取配置文件
- 检查日志文件

注意事项：
- 文件大小限制：10MB
- 支持文本文件，不支持二进制文件
- 支持相对路径和绝对路径`;

  inputSchema: JSONSchema = {
    type: 'object',
    properties: {
      file_path: {
        type: 'string',
        description: '文件路径'
      },
      encoding: {
        type: 'string',
        enum: ['utf-8', 'gbk', 'ascii'],
        default: 'utf-8',
        description: '文件编码'
      },
      start_line: {
        type: 'integer',
        minimum: 1,
        description: '起始行号'
      },
      end_line: {
        type: 'integer',
        minimum: 1,
        description: '结束行号'
      }
    },
    required: ['file_path']
  };

  requiresApproval = false;
  isDangerous = false;
  timeout = 5000;

  async execute(
    input: ReadInput,
    context: ToolContext
  ): Promise<ToolResult> {
    const startTime = Date.now();
    
    try {
      // 1. 解析路径
      const absolutePath = this.resolvePath(
        input.file_path,
        context.workingDirectory
      );
      
      // 2. 安全检查
      await this.validatePath(absolutePath, context);
      
      // 3. 检查文件大小
      const stats = await fs.stat(absolutePath);
      if (stats.size > 10 * 1024 * 1024) {
        return {
          success: false,
          content: '',
          error: {
            code: 'FILE_TOO_LARGE',
            message: '文件过大（>10MB），请使用更具体的路径或行号范围'
          }
        };
      }
      
      // 4. 读取文件
      let content = await fs.readFile(absolutePath, input.encoding || 'utf-8');
      
      // 5. 处理行号范围
      if (input.start_line || input.end_line) {
        content = this.extractLines(
          content,
          input.start_line,
          input.end_line
        );
      }
      
      // 6. 返回结果
      return {
        success: true,
        content,
        metadata: {
          duration: Date.now() - startTime,
          bytesProcessed: Buffer.byteLength(content, 'utf-8')
        }
      };
      
    } catch (error) {
      return {
        success: false,
        content: '',
        error: {
          code: this.getErrorCode(error),
          message: error.message
        }
      };
    }
  }

  private resolvePath(filePath: string, workDir: string): string {
    // 相对路径转换为绝对路径
    if (!path.isAbsolute(filePath)) {
      return path.join(workDir, filePath);
    }
    return filePath;
  }

  private async validatePath(
    absolutePath: string,
    context: ToolContext
  ): Promise<void> {
    // 1. 检查是否在工作目录内
    const normalized = path.normalize(absolutePath);
    if (!normalized.startsWith(context.workingDirectory)) {
      throw new Error('不允许访问工作目录外的文件');
    }
    
    // 2. 检查路径遍历攻击
    if (absolutePath.includes('..')) {
      throw new Error('路径中不允许包含 ".."');
    }
    
    // 3. 检查文件是否存在
    if (!await fs.pathExists(absolutePath)) {
      throw new Error(`文件不存在: ${absolutePath}`);
    }
    
    // 4. 检查是否为文件（不是目录）
    const stats = await fs.stat(absolutePath);
    if (!stats.isFile()) {
      throw new Error('路径必须指向文件，不是目录');
    }
  }

  private extractLines(
    content: string,
    startLine?: number,
    endLine?: number
  ): string {
    const lines = content.split('\n');
    const start = (startLine || 1) - 1;  // 转为0-based索引
    const end = endLine || lines.length;
    
    return lines.slice(start, end).join('\n');
  }

  private getErrorCode(error: any): string {
    if (error.code === 'ENOENT') return 'FILE_NOT_FOUND';
    if (error.code === 'EACCES') return 'PERMISSION_DENIED';
    if (error.code === 'EISDIR') return 'IS_DIRECTORY';
    return 'UNKNOWN_ERROR';
  }
}
```

<br/>

### 2.2 WriteTool - 文件写入工具

**完整实现：**

```typescript
class WriteTool implements Tool {
  name = 'write';
  
  description = `创建新文件或覆盖现有文件。

使用场景：
- 创建新文件
- 完全重写文件
- 生成配置文件

⚠️ 注意：
- 会完全覆盖现有文件
- 建议先使用read工具确认文件内容`;

  inputSchema: JSONSchema = {
    type: 'object',
    properties: {
      file_path: {
        type: 'string',
        description: '文件路径'
      },
      content: {
        type: 'string',
        description: '文件内容'
      },
      encoding: {
        type: 'string',
        enum: ['utf-8', 'gbk', 'ascii'],
        default: 'utf-8',
        description: '文件编码'
      },
      create_dirs: {
        type: 'boolean',
        default: true,
        description: '是否自动创建父目录'
      }
    },
    required: ['file_path', 'content']
  };

  requiresApproval = true;  // 写入需要批准
  isDangerous = true;       // 标记为危险操作
  timeout = 10000;

  async execute(
    input: WriteInput,
    context: ToolContext
  ): Promise<ToolResult> {
    const startTime = Date.now();
    
    try {
      // 1. 解析路径
      const absolutePath = this.resolvePath(
        input.file_path,
        context.workingDirectory
      );
      
      // 2. 安全检查
      await this.validatePath(absolutePath, context);
      
      // 3. 检查文件是否存在
      const exists = await fs.pathExists(absolutePath);
      if (exists) {
        // 文件已存在，确认覆盖
        const approved = await context.requestApproval(
          `文件 ${input.file_path} 已存在，是否覆盖？`
        );
        if (!approved) {
          return {
            success: false,
            content: '',
            error: {
              code: 'CANCELLED',
              message: '用户取消操作'
            }
          };
        }
      }
      
      // 4. 创建父目录
      if (input.create_dirs !== false) {
        await fs.ensureDir(path.dirname(absolutePath));
      }
      
      // 5. 写入文件
      await fs.writeFile(
        absolutePath,
        input.content,
        input.encoding || 'utf-8'
      );
      
      // 6. 返回结果
      return {
        success: true,
        content: `文件已写入: ${input.file_path}`,
        metadata: {
          duration: Date.now() - startTime,
          bytesProcessed: Buffer.byteLength(input.content, 'utf-8')
        }
      };
      
    } catch (error) {
      return {
        success: false,
        content: '',
        error: {
          code: this.getErrorCode(error),
          message: error.message
        }
      };
    }
  }

  private async validatePath(
    absolutePath: string,
    context: ToolContext
  ): Promise<void> {
    // 类似ReadTool的安全检查
    // ...
    
    // 额外检查：不允许写入敏感文件
    const sensitiveFiles = [
      '.env',
      '.git/config',
      'package.json',
      'tsconfig.json'
    ];
    
    const relativePath = path.relative(
      context.workingDirectory,
      absolutePath
    );
    
    if (sensitiveFiles.includes(relativePath)) {
      const approved = await context.requestApproval(
        `即将修改敏感文件 ${relativePath}，是否继续？`
      );
      if (!approved) {
        throw new Error('用户拒绝修改敏感文件');
      }
    }
  }

  private getErrorCode(error: any): string {
    if (error.code === 'EACCES') return 'PERMISSION_DENIED';
    if (error.code === 'ENOSPC') return 'NO_SPACE';
    return 'UNKNOWN_ERROR';
  }
}
```

<br/>

### 2.3 EditTool - 文件编辑工具

**完整实现：**

```typescript
class EditTool implements Tool {
  name = 'edit';
  
  description = `编辑现有文件，替换指定文本。

使用场景：
- 修改代码片段
- 更新配置项
- 重构代码

优势：
- 精确替换，不影响其他内容
- 支持多次编辑
- 自动验证匹配`;

  inputSchema: JSONSchema = {
    type: 'object',
    properties: {
      file_path: {
        type: 'string',
        description: '文件路径'
      },
      edits: {
        type: 'array',
        description: '编辑操作列表',
        items: {
          type: 'object',
          properties: {
            oldText: {
              type: 'string',
              description: '要替换的旧文本（必须完全匹配）'
            },
            newText: {
              type: 'string',
              description: '替换后的新文本'
            }
          },
          required: ['oldText', 'newText']
        }
      },
      dry_run: {
        type: 'boolean',
        default: false,
        description: '试运行，只显示变更不实际修改'
      }
    },
    required: ['file_path', 'edits']
  };

  requiresApproval = true;
  isDangerous = false;
  timeout = 10000;

  async execute(
    input: EditInput,
    context: ToolContext
  ): Promise<ToolResult> {
    const startTime = Date.now();
    
    try {
      // 1. 读取文件
      const absolutePath = this.resolvePath(
        input.file_path,
        context.workingDirectory
      );
      
      await this.validatePath(absolutePath, context);
      let content = await fs.readFile(absolutePath, 'utf-8');
      
      // 2. 执行编辑
      const changes: EditChange[] = [];
      
      for (const edit of input.edits) {
        const result = this.applyEdit(content, edit);
        
        if (!result.found) {
          return {
            success: false,
            content: '',
            error: {
              code: 'TEXT_NOT_FOUND',
              message: `未找到匹配文本: ${edit.oldText.substring(0, 50)}...`
            }
          };
        }
        
        content = result.content;
        changes.push({
          oldText: edit.oldText,
          newText: edit.newText,
          lineNumber: result.lineNumber
        });
      }
      
      // 3. 试运行模式
      if (input.dry_run) {
        return {
          success: true,
          content: this.formatChanges(changes),
          metadata: {
            duration: Date.now() - startTime,
            filesAffected: 0
          }
        };
      }
      
      // 4. 写入文件
      await fs.writeFile(absolutePath, content, 'utf-8');
      
      // 5. 返回结果
      return {
        success: true,
        content: this.formatChanges(changes),
        metadata: {
          duration: Date.now() - startTime,
          filesAffected: 1
        }
      };
      
    } catch (error) {
      return {
        success: false,
        content: '',
        error: {
          code: this.getErrorCode(error),
          message: error.message
        }
      };
    }
  }

  private applyEdit(
    content: string,
    edit: { oldText: string; newText: string }
  ): { content: string; found: boolean; lineNumber: number } {
    // 1. 查找oldText
    const index = content.indexOf(edit.oldText);
    
    if (index === -1) {
      return { content, found: false, lineNumber: -1 };
    }
    
    // 2. 计算行号
    const lineNumber = content.substring(0, index).split('\n').length;
    
    // 3. 替换
    const newContent =
      content.substring(0, index) +
      edit.newText +
      content.substring(index + edit.oldText.length);
    
    return { content: newContent, found: true, lineNumber };
  }

  private formatChanges(changes: EditChange[]): string {
    return changes.map(change => 
      `- 第${change.lineNumber}行:\n` +
      `  - 删除: ${change.oldText.substring(0, 50)}...\n` +
      `  + 添加: ${change.newText.substring(0, 50)}...`
    ).join('\n');
  }

  private getErrorCode(error: any): string {
    if (error.code === 'ENOENT') return 'FILE_NOT_FOUND';
    if (error.code === 'EACCES') return 'PERMISSION_DENIED';
    return 'UNKNOWN_ERROR';
  }
}
```

<br/>

### 2.4 ExecTool - 命令执行工具

**完整实现（带沙箱）：**

```typescript
class ExecTool implements Tool {
  name = 'exec';
  
  description = `执行shell命令。

使用场景：
- 运行测试
- 构建项目
- Git操作
- 包管理

⚠️ 安全限制：
- 只允许白名单命令
- 超时限制：30秒
- 输出限制：10MB`;

  inputSchema: JSONSchema = {
    type: 'object',
    properties: {
      command: {
        type: 'string',
        description: '要执行的命令'
      },
      args: {
        type: 'array',
        items: { type: 'string' },
        description: '命令参数'
      },
      cwd: {
        type: 'string',
        description: '工作目录（可选）'
      },
      timeout: {
        type: 'integer',
        minimum: 1000,
        maximum: 60000,
        default: 30000,
        description: '超时时间（毫秒）'
      }
    },
    required: ['command']
  };

  requiresApproval = true;
  isDangerous = true;
  timeout = 60000;

  // 命令白名单
  private static readonly ALLOWED_COMMANDS = new Set([
    'npm', 'yarn', 'pnpm',
    'node', 'python', 'python3',
    'git',
    'pytest', 'jest', 'vitest',
    'tsc', 'eslint', 'prettier',
    'ls', 'cat', 'grep', 'find'
  ]);

  // 危险模式黑名单
  private static readonly DANGEROUS_PATTERNS = [
    /rm\s+-rf/,           // 删除命令
    />\s*\//,             // 重定向到根目录
    /\|\s*sh/,            // 管道到shell
    /\$\(/,               // 命令替换
    /`.*`/,               // 反引号执行
    /curl.*\|.*sh/,       // 下载并执行
    /wget.*\|.*sh/        // 下载并执行
  ];

  async execute(
    input: ExecInput,
    context: ToolContext
  ): Promise<ToolResult> {
    const startTime = Date.now();
    
    try {
      // 1. 命令白名单检查
      if (!ExecTool.ALLOWED_COMMANDS.has(input.command)) {
        return {
          success: false,
          content: '',
          error: {
            code: 'COMMAND_NOT_ALLOWED',
            message: `命令 "${input.command}" 不在白名单中`
          }
        };
      }
      
      // 2. 参数安全检查
      if (input.args) {
        for (const arg of input.args) {
          if (this.isDangerous(arg)) {
            return {
              success: false,
              content: '',
              error: {
                code: 'DANGEROUS_ARGUMENT',
                message: `危险的参数: ${arg}`
              }
            };
          }
        }
      }
      
      // 3. 构建命令
      const fullCommand = input.args
        ? `${input.command} ${input.args.join(' ')}`
        : input.command;
      
      // 4. 执行命令（带超时和输出限制）
      const result = await this.executeCommand(
        fullCommand,
        {
          cwd: input.cwd || context.workingDirectory,
          timeout: input.timeout || 30000,
          maxBuffer: 10 * 1024 * 1024,  // 10MB
          env: {
            ...process.env,
            ...context.environment
          }
        }
      );
      
      // 5. 返回结果
      return {
        success: result.exitCode === 0,
        content: result.stdout || result.stderr,
        metadata: {
          duration: Date.now() - startTime,
          exitCode: result.exitCode
        }
      };
      
    } catch (error) {
      return {
        success: false,
        content: '',
        error: {
          code: this.getErrorCode(error),
          message: error.message
        }
      };
    }
  }

  private isDangerous(arg: string): boolean {
    return ExecTool.DANGEROUS_PATTERNS.some(
      pattern => pattern.test(arg)
    );
  }

  private async executeCommand(
    command: string,
    options: ExecOptions
  ): Promise<ExecResult> {
    return new Promise((resolve, reject) => {
      const timeoutId = setTimeout(() => {
        reject(new Error('命令执行超时'));
      }, options.timeout);

      exec(command, options, (error, stdout, stderr) => {
        clearTimeout(timeoutId);
        
        if (error) {
          resolve({
            exitCode: error.code || 1,
            stdout,
            stderr
          });
        } else {
          resolve({
            exitCode: 0,
            stdout,
            stderr
          });
        }
      });
    });
  }

  private getErrorCode(error: any): string {
    if (error.message.includes('timeout')) return 'TIMEOUT';
    if (error.message.includes('maxBuffer')) return 'OUTPUT_TOO_LARGE';
    return 'EXECUTION_ERROR';
  }
}
```

<br/>

***

<br/>

## 三、工具注册与发现

### 3.1 ToolRegistry 实现

**工具注册表：**

```typescript
class ToolRegistry {
  private tools: Map<string, Tool> = new Map();
  private categories: Map<string, Set<string>> = new Map();

  /**
   * 注册工具
   */
  register(tool: Tool, category?: string): void {
    // 1. 验证工具
    this.validateTool(tool);
    
    // 2. 检查重名
    if (this.tools.has(tool.name)) {
      throw new Error(`工具 "${tool.name}" 已存在`);
    }
    
    // 3. 注册工具
    this.tools.set(tool.name, tool);
    
    // 4. 添加到分类
    if (category) {
      if (!this.categories.has(category)) {
        this.categories.set(category, new Set());
      }
      this.categories.get(category)!.add(tool.name);
    }
    
    console.log(`✅ 工具已注册: ${tool.name}`);
  }

  /**
   * 批量注册工具
   */
  registerAll(tools: Tool[]): void {
    for (const tool of tools) {
      this.register(tool);
    }
  }

  /**
   * 获取工具
   */
  get(name: string): Tool | undefined {
    return this.tools.get(name);
  }

  /**
   * 获取所有工具
   */
  getAll(): Tool[] {
    return Array.from(this.tools.values());
  }

  /**
   * 按分类获取工具
   */
  getByCategory(category: string): Tool[] {
    const toolNames = this.categories.get(category);
    if (!toolNames) return [];
    
    return Array.from(toolNames)
      .map(name => this.tools.get(name))
      .filter((tool): tool is Tool => tool !== undefined);
  }

  /**
   * 获取工具定义（给Claude的）
   */
  getToolDefinitions(): ToolDefinition[] {
    return this.getAll().map(tool => ({
      name: tool.name,
      description: tool.description,
      input_schema: tool.inputSchema
    }));
  }

  /**
   * 验证工具
   */
  private validateTool(tool: Tool): void {
    // 1. 检查必需字段
    if (!tool.name) {
      throw new Error('工具必须有name字段');
    }
    if (!tool.description) {
      throw new Error('工具必须有description字段');
    }
    if (!tool.inputSchema) {
      throw new Error('工具必须有inputSchema字段');
    }
    if (typeof tool.execute !== 'function') {
      throw new Error('工具必须有execute方法');
    }
    
    // 2. 检查name格式
    if (!/^[a-z_]{3,30}$/.test(tool.name)) {
      throw new Error('工具名称必须是3-30个小写字母或下划线');
    }
    
    // 3. 检查description长度
    if (tool.description.length < 50 || tool.description.length > 500) {
      throw new Error('工具描述必须是50-500字符');
    }
  }

  /**
   * 清除所有工具
   */
  clear(): void {
    this.tools.clear();
    this.categories.clear();
  }
}
```

**使用示例：**

```typescript
// 创建注册表
const registry = new ToolRegistry();

// 注册内置工具
registry.register(new ReadTool(), 'file');
registry.register(new WriteTool(), 'file');
registry.register(new EditTool(), 'file');
registry.register(new ExecTool(), 'system');

// 注册自定义工具
registry.register(new MyCustomTool(), 'custom');

// 获取所有文件操作工具
const fileTools = registry.getByCategory('file');

// 获取工具定义（传给Claude）
const definitions = registry.getToolDefinitions();
```

<br/>

***

<br/>

## 四、自定义工具开发

### 4.1 开发步骤

**步骤1：定义工具类**

```typescript
class MyCustomTool implements Tool {
  name = 'my_custom_tool';
  description = '这是我的自定义工具';
  inputSchema = {
    type: 'object',
    properties: {
      param1: { type: 'string' }
    },
    required: ['param1']
  };
  
  async execute(input: any, context: ToolContext): Promise<ToolResult> {
    // 实现你的逻辑
    return {
      success: true,
      content: '执行成功'
    };
  }
}
```

**步骤2：注册到Agent**

```typescript
const agent = new Agent(options);
agent.registerTool(new MyCustomTool());
```

**步骤3：测试**

```typescript
// 测试工具
const tool = new MyCustomTool();
const result = await tool.execute(
  { param1: 'test' },
  mockContext
);

console.log(result);
```

<br/>

### 4.2 最佳实践

**1. 清晰的描述**

```typescript
// ❌ 不好
description = '处理文件';

// ✅ 好
description = `处理文本文件的编码转换。

支持格式：
- UTF-8 → GBK
- GBK → UTF-8

使用场景：
- 处理中文文档
- 解决乱码问题`;
```

**2. 完善的输入验证**

```typescript
async execute(input: any, context: ToolContext): Promise<ToolResult> {
  // 1. 参数验证
  if (!input.file_path) {
    return {
      success: false,
      content: '',
      error: {
        code: 'INVALID_INPUT',
        message: 'file_path是必需参数'
      }
    };
  }
  
  // 2. 类型检查
  if (typeof input.file_path !== 'string') {
    return {
      success: false,
      content: '',
      error: {
        code: 'INVALID_TYPE',
        message: 'file_path必须是字符串'
      }
    };
  }
  
  // 3. 执行逻辑
  // ...
}
```

**3. 详细的错误信息**

```typescript
// ❌ 不好
throw new Error('执行失败');

// ✅ 好
throw new Error(
  `文件处理失败: ${input.file_path}\n` +
  `原因: 文件被占用\n` +
  `建议: 关闭文件后重试`
);
```

**4. 性能考虑**

```typescript
async execute(input: any, context: ToolContext): Promise<ToolResult> {
  const startTime = Date.now();
  
  try {
    // 执行操作
    const result = await this.doWork(input);
    
    return {
      success: true,
      content: result,
      metadata: {
        duration: Date.now() - startTime
      }
    };
  } catch (error) {
    // 错误处理
    return {
      success: false,
      content: '',
      error: {
        code: 'EXECUTION_ERROR',
        message: error.message
      },
      metadata: {
        duration: Date.now() - startTime
      }
    };
  }
}
```

<br/>

***

<br/>

## 五、安全与性能优化

### 5.1 安全最佳实践

**1. 路径验证**

```typescript
private validatePath(path: string, workDir: string): void {
  // 1. 规范化路径
  const normalized = pathLib.normalize(path);
  
  // 2. 检查路径遍历
  if (normalized.includes('..')) {
    throw new Error('不允许路径遍历');
  }
  
  // 3. 检查是否在工作目录内
  if (!normalized.startsWith(workDir)) {
    throw new Error('不允许访问工作目录外的文件');
  }
}
```

**2. 输入清理**

```typescript
private sanitizeInput(input: string): string {
  // 1. 移除危险字符
  input = input.replace(/[<>:"|?*]/g, '');
  
  // 2. 限制长度
  if (input.length > 1000) {
    input = input.substring(0, 1000);
  }
  
  return input;
}
```

**3. 权限控制**

```typescript
async execute(input: any, context: ToolContext): Promise<ToolResult> {
  // 1. 检查权限
  if (this.requiresApproval) {
    const approved = await context.requestApproval(
      this.formatApprovalMessage(input)
    );
    
    if (!approved) {
      return {
        success: false,
        content: '',
        error: {
          code: 'CANCELLED',
          message: '用户取消操作'
        }
      };
    }
  }
  
  // 2. 执行操作
  // ...
}
```

<br/>

### 5.2 性能优化

**1. 并发控制**

```typescript
class ToolExecutor {
  private queue: Queue<() => Promise<any>>;
  private concurrency: number = 5;

  async executeConcurrently(
    toolCalls: ToolCall[]
  ): Promise<ToolResult[]> {
    const tasks = toolCalls.map(call => 
      this.queue.add(() => this.executeTool(call))
    );
    
    return Promise.all(tasks);
  }
}
```

**2. 结果缓存**

```typescript
class CachedTool implements Tool {
  private cache = new Map<string, ToolResult>();

  async execute(input: any, context: ToolContext): Promise<ToolResult> {
    // 1. 生成缓存key
    const cacheKey = this.getCacheKey(input);
    
    // 2. 检查缓存
    const cached = this.cache.get(cacheKey);
    if (cached) {
      return cached;
    }
    
    // 3. 执行
    const result = await this.executeInternal(input, context);
    
    // 4. 缓存结果
    this.cache.set(cacheKey, result);
    
    return result;
  }

  private getCacheKey(input: any): string {
    return JSON.stringify(input);
  }
}
```

**3. 输出限制**

```typescript
private truncateOutput(output: string, maxLength: number = 10000): string {
  if (output.length <= maxLength) {
    return output;
  }
  
  return output.substring(0, maxLength) + 
    `\n... (输出已截断，总长度: ${output.length})`;
}
```

<br/>

***

<br/>

## 六、总结

### 6.1 核心要点

**Tool系统的设计原则：**

```
1. 接口统一
   ✅ 所有工具实现相同接口
   ✅ 统一的输入输出格式
   ✅ 统一的错误处理

2. 安全第一
   ✅ 多层验证
   ✅ 权限控制
   ✅ 沙箱隔离

3. 可扩展性
   ✅ 简单的注册机制
   ✅ 清晰的开发指南
   ✅ 丰富的示例
```

**关键设计模式：**

```
✅ 策略模式（不同工具实现）
✅ 工厂模式（工具创建）
✅ 模板方法模式（execute流程）
✅ 装饰器模式（缓存、日志）
```

<br/>

### 6.2 实战练习

**练习1：开发一个API调用工具**

```typescript
class ApiCallTool implements Tool {
  name = 'api_call';
  description = '调用REST API';
  inputSchema = {
    type: 'object',
    properties: {
      method: { type: 'string', enum: ['GET', 'POST', 'PUT', 'DELETE'] },
      url: { type: 'string' },
      headers: { type: 'object' },
      body: { type: 'string' }
    },
    required: ['method', 'url']
  };
  
  async execute(input: any, context: ToolContext): Promise<ToolResult> {
    // 实现API调用逻辑
    // ...
  }
}
```

**练习2：开发一个数据库查询工具**

```typescript
class DatabaseQueryTool implements Tool {
  name = 'db_query';
  description = '执行数据库查询';
  
  async execute(input: any, context: ToolContext): Promise<ToolResult> {
    // 实现数据库查询逻辑
    // 注意：要防止SQL注入！
  }
}
```

<br/>

### 6.3 下一篇预告

**在AI-30《上下文管理》中，我们将学习：**

```
🔄 上下文管理器的实现
   - Token计数原理
   - 文件选择策略
   - 上下文压缩算法

🔄 上下文优化技巧
   - 长对话处理
   - 大型项目支持
   - Token预算控制

🔄 实际应用场景
   - 代码库理解
   - 重构大项目
   - 多文件编辑
```

<br/>

***

<br/>

**系列导航**

• 上一篇：AI-28 Agent核心实现
• 下一篇：AI-30 上下文管理（Context Management）

<br/>

***

本文是《Claude Code 源代码解读与分析》系列第3篇
作者：生活助理 | 发布时间：2026-04-07

**掌握工具系统，扩展AI的能力边界！** 🔧✨
