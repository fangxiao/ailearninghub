#!/usr/bin/env python3
import re

def highlight_python(code):
    """为Python代码添加语法高亮"""
    keywords = ['import', 'from', 'class', 'def', 'return', 'if', 'else', 'elif', 'for', 'while', 'try', 'except', 'finally', 'with', 'as', 'in', 'not', 'and', 'or', 'is', 'None', 'True', 'False', 'raise', 'yield', 'lambda', 'pass', 'break', 'continue', 'global', 'nonlocal', 'assert', 'async', 'await', 'raise', 'print']
    
    # 先处理注释
    code = re.sub(r'(#.*$)', r'<span style="color: #a8a8a8; font-style: italic;">\1</span>', code, flags=re.MULTILINE)
    
    # 字符串
    code = re.sub(r'("(?:[^"\\]|\\.)*")', r'<span style="color: #e6db74">\1</span>', code)
    code = re.sub(r"('(?:[^'\\]|\\.)*')", r'<span style="color: #e6db74">\1</span>', code)
    
    # 数字
    code = re.sub(r'(\b\d+\b)', r'<span style="color: #ae81ff">\1</span>', code)
    
    # 关键字
    for kw in keywords:
        code = re.sub(rf'(\b{kw}\b)', r'<span style="color: #66d9ef">\1</span>', code)
    
    # 函数名
    code = re.sub(r'(def\s+)(\w+)', r'\1<span style="color: #a6e22e">\2</span>', code)
    
    # 类名
    code = re.sub(r'(class\s+)(\w+)', r'\1<span style="color: #a6e22e">\2</span>', code)
    
    # self
    code = re.sub(r'(\bself\b)', r'<span style="color: #f8f8f2">\1</span>', code)
    
    return code

def highlight_markdown(code):
    """为Markdown代码添加语法高亮"""
    # 标题
    code = re.sub(r'^(#{1,6}\s+.*)$', r'<span style="color: #66d9ef">\1</span>', code, flags=re.MULTILINE)
    
    # 列表项
    code = re.sub(r'^(\s*[-*]\s+)(.*)$', r'<span style="color: #f8f8f2">\1\2</span>', code, flags=re.MULTILINE)
    code = re.sub(r'^(\s*\d+\.\s+)(.*)$', r'<span style="color: #f8f8f2">\1\2</span>', code, flags=re.MULTILINE)
    
    # 强调
    code = re.sub(r'(\*\*[^*]+\*\*)', r'<span style="color: #e6db74">\1</span>', code)
    
    return code

# Python代码块1
python_code1 = '''import os
from pathlib import Path
import yaml

class CustomerServiceBot:
    def __init__(self, config_path: str = "config/customer_service.yaml"):
        self.config = self._load_config(config_path)
        self.system_prompt = self._load_prompt()
    
    def _load_config(self, config_path: str) -> dict:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _load_prompt(self) -> str:
        prompt_path = Path("config/prompts/system_prompt.md")
        if prompt_path.exists():
            return prompt_path.read_text(encoding="utf-8")
        return "你是一个客服助手。"
    
    def chat(self, user_input: str, history: list = None) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_input})
        return self._call_llm(messages)
    
    def _call_llm(self, messages: list) -> str:
        provider = self.config.get('llm', {}).get('provider', 'zhipu')
        model = self.config.get('llm', {}).get('model', 'glm-5.1-flash')
        if provider == 'zhipu':
            return self._call_zhipu(messages, model)
        elif provider == 'ollama':
            return self._call_ollama(messages, model)
        raise ValueError(f"Unsupported provider: {provider}")'''

# Python代码块2
python_code2 = '''# 测试客服Bot
from src.bot import CustomerServiceBot

bot = CustomerServiceBot()

# 测试1：FAQ问题
print(bot.chat("如何修改密码？"))
# 预期：从FAQ检索，给出标准答案

# 测试2：情绪激动
print(bot.chat("你们的服务太差了！我要投诉！"))
# 预期：表达歉意，主动转人工

# 测试3：无关问题
print(bot.chat("今天天气怎么样？"))
# 预期：礼貌拒绝，引导回客服话题'''

# Markdown代码块1
md_code1 = '''# 客服Bot System Prompt 模板

## 1. 角色定义
你是一个专业的客服助手，服务于XX公司的用户。

## 2. 能力说明
你可以：
- 回答产品相关问题
- 处理订单查询
- 解决常见问题（FAQ）
- 转接人工客服

## 3. 行为约束
- 使用礼貌、专业的语气
- 回答简洁明了，不超过200字
- 不确定的问题，主动承认并建议转人工
- 不回答与客服无关的问题

## 4. 知识来源
- FAQ知识库：回答常见问题
- 订单系统：查询订单状态
- 产品文档：回答产品细节

## 5. 异常处理
- 遇到投诉：安抚用户，立即转人工
- 遇到无法回答的问题：诚实说明，建议转人工
- 遇到无关问题：礼貌拒绝，引导回客服话题'''

# Markdown代码块2
md_code2 = '''# 智能客服助手

## 角色定义
你是"小助手"，XX公司的智能客服。

## 能力范围

### 你可以做的：
1. FAQ回答：回答产品使用、账户管理等常见问题
2. 订单查询：查询订单状态、物流信息
3. 问题诊断：帮助用户排查常见问题
4. 转人工：当无法解决时，转接人工客服

### 你不能做的：
1. 处理退款、取消订单（需要人工审核）
2. 修改用户账户信息
3. 回答与客服无关的问题

## 回答规范

### 语气风格：
- 礼貌、专业、耐心
- 使用"您"而非"你"

### 回答格式：
- 先给出核心答案
- 再补充必要细节
- 最后提供下一步建议

### 度控制：
- 单次回答不超过200字
- 复杂问题分步骤说明

## 转人工触发条件

以下情况必须转人工：
1. 用户明确要求转人工
2. 用户表达强烈不满或投诉
3. 问题涉及退款、账户修改等敏感操作
4. 连续3次无法回答用户问题'''

# 输出高亮后的代码
print("=== Python Code 1 ===")
print(highlight_python(python_code1))
print("\n=== Python Code 2 ===")
print(highlight_python(python_code2))
print("\n=== Markdown Code 1 ===")
print(highlight_markdown(md_code1))
print("\n=== Markdown Code 2 ===")
print(highlight_markdown(md_code2))