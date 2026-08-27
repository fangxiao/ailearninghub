#!/usr/bin/env python3
import re

def highlight_python(code):
    """为Python代码添加语法高亮"""
    # 关键字
    keywords = ['import', 'from', 'class', 'def', 'return', 'if', 'else', 'elif', 'for', 'while', 'try', 'except', 'finally', 'with', 'as', 'in', 'not', 'and', 'or', 'is', 'None', 'True', 'False', 'raise', 'yield', 'lambda', 'pass', 'break', 'continue', 'global', 'nonlocal', 'assert', 'async', 'await']
    
    # 注释
    code = re.sub(r'(#.*$)', r'<span style="color: #a8a8a8; font-style: italic;">\1</span>', code, flags=re.MULTILINE)
    
    # 字符串（单引号和双引号）
    code = re.sub(r'("(?:[^"\\]|\\.)*")', r'<span style="color: #e6db74">\1</span>', code)
    code = re.sub(r"('(?:[^'\\]|\\.)*')", r'<span style="color: #e6db74">\1</span>', code)
    
    # 数字
    code = re.sub(r'(\b\d+\b)', r'<span style="color: #ae81ff">\1</span>', code)
    
    # 关键字
    for kw in keywords:
        code = re.sub(rf'(\b{kw}\b)', r'<span style="color: #66d9ef">\1</span>', code)
    
    # 函数名（def后面的）
    code = re.sub(r'(def\s+)(\w+)', r'\1<span style="color: #a6e22e">\2</span>', code)
    
    # 类名（class后面的）
    code = re.sub(r'(class\s+)(\w+)', r'\1<span style="color: #a6e22e">\2</span>', code)
    
    return code

def highlight_markdown(code):
    """为Markdown代码添加语法高亮"""
    # 标题
    code = re.sub(r'^(#{1,6}\s+.*)$', r'<span style="color: #66d9ef">\1</span>', code, flags=re.MULTILINE)
    
    # 列表项
    code = re.sub(r'^(\s*[-*]\s+.*)$', r'<span style="color: #f8f8f2">\1</span>', code, flags=re.MULTILINE)
    code = re.sub(r'^(\s*\d+\.\s+.*)$', r'<span style="color: #f8f8f2">\1</span>', code, flags=re.MULTILINE)
    
    # 强调
    code = re.sub(r'(\*\*[^*]+\*\*)', r'<span style="color: #e6db74">\1</span>', code)
    
    return code

def process_code_block(code, language):
    """处理代码块"""
    if language.lower() == 'python':
        return highlight_python(code)
    elif language.lower() == 'markdown' or language.lower() == 'md':
        return highlight_markdown(code)
    else:
        return code

if __name__ == "__main__":
    # 测试
    test_code = '''import os
from pathlib import Path

class CustomerServiceBot:
    def __init__(self, config_path: str = "config/customer_service.yaml"):
        self.config = self._load_config(config_path)
        # 加载配置
        return self.config'''
    
    print(highlight_python(test_code))