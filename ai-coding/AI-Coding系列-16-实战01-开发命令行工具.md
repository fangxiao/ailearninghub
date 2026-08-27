# 实战01：开发命令行工具

阅读时间：40分钟
难度等级：⭐⭐⭐ 进阶
你将收获：用 AI Coding 从零开发一个实用的 CLI 工具

<br/>

***

<br/>

## 从原理到实战：开启实践之旅

**前面学过的：**

```
✅ 原理篇（4篇）
   - 代码补全原理：AI 如何预测代码
   - 上下文管理：AI 如何记住代码
   - AI Coding 架构：系统如何工作
   - 安全与隐私：如何保护代码
```

**现在开始：将原理应用到实践**

**原理如何指导实战？**

| 原理篇知识 | 实战中的应用 |
|-----------|------------|
| **代码补全原理** | 写清晰的命名、类型提示 → AI 补全更准 |
| **上下文管理** | 分层架构、模块化 → AI 更容易理解项目 |
| **系统架构** | 选择合适工具（FastAPI vs Flask） |
| **安全与隐私** | 环境变量、脱敏处理 |

**实战篇设计思路：**

```
项目1：命令行工具（本篇）⭐⭐
├─ 学习：基础项目开发、文件操作
└─ 目标：掌握 AI 辅助开发流程

项目2：Web API ⭐⭐⭐
├─ 学习：RESTful、数据库、API 设计
└─ 目标：服务端开发

项目3：打包发布 ⭐⭐
├─ 学习：Poetry、PyPI、CI/CD
└─ 目标：项目发布

项目4-6：全栈应用 ⭐⭐⭐⭐
├─ 学习：前后端分离、部署
└─ 目标：完整应用开发

项目7：数据项目 ⭐⭐⭐⭐
├─ 学习：爬虫、数据分析
└─ 目标：数据技能
```

**准备好了吗？开始第一个实战项目！** 🚀

<br/>

***

<br/>

## 实战目标

**我们要开发：** `codestats` — 代码统计命令行工具

**功能：**

```
$ codestats /path/to/project

📊 代码统计报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
项目路径: /Users/admin/my_project
统计时间: 2026-04-05 10:40:00

📁 文件统计
  总文件数: 156
  代码文件: 89
  配置文件: 12
  其他文件: 55

📝 代码行数
  总行数: 12,345
  代码行: 8,234 (66.7%)
  注释行: 1,456 (11.8%)
  空白行: 2,655 (21.5%)

💻 语言分布
  Python: 6,234 行 (75.7%)
  JavaScript: 1,456 行 (17.7%)
  YAML: 544 行 (6.6%)

🏆 最大的文件
  1. models/user.py (456 行)
  2. services/order.py (378 行)
  3. utils/helpers.py (312 行)
```

**学习要点：**

- ✅ CLI 参数解析（argparse）
- ✅ 文件系统操作（os/pathlib）
- ✅ 数据统计和分析
- ✅ 格式化输出（rich/click）
- ✅ 完整的开发流程

<br/>

***

<br/>

## 一、项目规划

### 1.1 需求分析

**核心功能：**

```
输入：项目路径
处理：
  1. 扫描所有文件
  2. 识别文件类型（扩展名）
  3. 统计代码行数
  4. 区分代码/注释/空白
  5. 按语言分类
输出：格式化的统计报告
```

**扩展功能：**

```
- 排除特定目录（node_modules、.git）
- 只统计特定语言
- 输出 JSON 格式
- 导出报告文件
```

<br/>

### 1.2 技术选型

| 功能 | 技术选择 | 原因 |
|------|---------|------|
| **CLI 框架** | Click | 简单易用、功能强大 |
| **美化输出** | Rich | 美观、支持表格/进度条 |
| **文件操作** | pathlib | 现代、面向对象 |
| **配置管理** | dataclass | 类型安全、简洁 |

<br/>

### 1.3 项目结构

```
codestats/
├── codestats/
│   ├── __init__.py
│   ├── cli.py           # 命令行入口
│   ├── scanner.py       # 文件扫描
│   ├── analyzer.py      # 代码分析
│   ├── reporter.py      # 报告生成
│   └── config.py        # 配置定义
├── tests/
│   ├── test_scanner.py
│   ├── test_analyzer.py
│   └── test_reporter.py
├── pyproject.toml       # 项目配置
├── README.md
└── .gitignore
```

<br/>

***

<br/>

## 二、用 AI 开始开发

### 2.1 初始化项目

**步骤1：创建项目目录**

```bash
mkdir codestats
cd codestats
```

**步骤2：用 AI 生成项目结构**

**提示词：**

```
我要创建一个 Python CLI 工具叫 codestats，用于统计代码行数。

请帮我：
1. 生成 pyproject.toml（使用 poetry）
2. 创建基本的项目结构
3. 包含 Click 和 Rich 依赖

项目信息：
- 名称：codestats
- 版本：0.1.0
- 描述：Code statistics CLI tool
- 作者：Your Name
```

**AI 生成：**

```toml
# pyproject.toml
[tool.poetry]
name = "codestats"
version = "0.1.0"
description = "Code statistics CLI tool"
authors = ["Your Name <your.email@example.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.9"
click = "^8.1.0"
rich = "^13.0.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-cov = "^4.1.0"

[tool.poetry.scripts]
codestats = "codestats.cli:main"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

```python
# codestats/__init__.py
"""Code statistics CLI tool"""

__version__ = "0.1.0"
```

```python
# codestats/cli.py
"""Command-line interface for codestats"""

import click
from rich.console import Console

console = Console()

@click.command()
@click.option('--path', '-p', default='.', help='项目路径')
@click.option('--exclude', '-e', multiple=True, help='排除的目录')
@click.option('--json', '-j', is_flag=True, help='输出 JSON 格式')
def main(path, exclude, json):
    """统计代码行数"""
    console.print(f"[green]统计项目:[/green] {path}")
    console.print(f"[green]排除目录:[/green] {exclude or '默认'}")
    console.print(f"[green]JSON 输出:[/green] {json}")

if __name__ == '__main__':
    main()
```

**安装依赖：**

```bash
poetry install
```

**测试运行：**

```bash
poetry run codestats --help
```

<br/>

### 2.2 开发文件扫描模块

**提示词：**

```
创建 codestats/scanner.py，实现文件扫描功能：

需求：
1. 扫描指定路径下的所有文件
2. 递归遍历子目录
3. 排除特定目录（如 .git、node_modules、__pycache__）
4. 按文件扩展名分类
5. 返回文件列表和统计信息

请提供完整的代码，包括类型提示和文档字符串。
```

**AI 生成：**

```python
# codestats/scanner.py
"""文件扫描模块"""

import os
from pathlib import Path
from typing import List, Dict, Set
from dataclasses import dataclass


@dataclass
class FileInfo:
    """文件信息"""
    path: Path
    extension: str
    size: int
    language: str


class FileScanner:
    """文件扫描器"""
    
    # 默认排除的目录
    DEFAULT_EXCLUDES = {
        '.git', '.svn', '.hg',
        'node_modules', '__pycache__', '.pytest_cache',
        'venv', 'env', '.venv',
        'build', 'dist', '*.egg-info',
    }
    
    # 扩展名到语言的映射
    EXTENSION_MAP = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.jsx': 'JavaScript',
        '.tsx': 'TypeScript',
        '.java': 'Java',
        '.go': 'Go',
        '.rs': 'Rust',
        '.rb': 'Ruby',
        '.php': 'PHP',
        '.c': 'C',
        '.cpp': 'C++',
        '.h': 'C',
        '.hpp': 'C++',
        '.cs': 'C#',
        '.swift': 'Swift',
        '.kt': 'Kotlin',
        '.scala': 'Scala',
        '.yaml': 'YAML',
        '.yml': 'YAML',
        '.json': 'JSON',
        '.xml': 'XML',
        '.html': 'HTML',
        '.css': 'CSS',
        '.scss': 'SCSS',
        '.sql': 'SQL',
        '.sh': 'Shell',
        '.md': 'Markdown',
    }
    
    def __init__(self, root_path: str, excludes: Set[str] = None):
        """
        初始化扫描器
        
        Args:
            root_path: 根路径
            excludes: 要排除的目录集合
        """
        self.root_path = Path(root_path).resolve()
        self.excludes = excludes or self.DEFAULT_EXCLUDES
    
    def scan(self) -> List[FileInfo]:
        """
        扫描所有文件
        
        Returns:
            文件信息列表
        """
        files = []
        
        for root, dirs, filenames in os.walk(self.root_path):
            # 排除特定目录
            dirs[:] = [d for d in dirs if not self._should_exclude(d)]
            
            for filename in filenames:
                file_path = Path(root) / filename
                
                # 跳过隐藏文件
                if filename.startswith('.'):
                    continue
                
                file_info = self._get_file_info(file_path)
                files.append(file_info)
        
        return files
    
    def _should_exclude(self, dirname: str) -> bool:
        """判断是否应该排除目录"""
        return dirname in self.excludes
    
    def _get_file_info(self, file_path: Path) -> FileInfo:
        """获取文件信息"""
        extension = file_path.suffix.lower()
        language = self.EXTENSION_MAP.get(extension, 'Unknown')
        size = file_path.stat().st_size
        
        return FileInfo(
            path=file_path,
            extension=extension,
            size=size,
            language=language,
        )
    
    def get_statistics(self, files: List[FileInfo]) -> Dict[str, int]:
        """
        获取统计信息
        
        Args:
            files: 文件列表
        
        Returns:
            统计字典
        """
        stats = {
            'total_files': len(files),
            'by_language': {},
            'by_extension': {},
        }
        
        for file_info in files:
            # 按语言统计
            lang = file_info.language
            stats['by_language'][lang] = stats['by_language'].get(lang, 0) + 1
            
            # 按扩展名统计
            ext = file_info.extension
            stats['by_extension'][ext] = stats['by_extension'].get(ext, 0) + 1
        
        return stats
```

<br/>

### 2.3 开发代码分析模块

**提示词：**

```
创建 codestats/analyzer.py，实现代码分析功能：

需求：
1. 读取文件内容
2. 统计总行数
3. 区分代码行、注释行、空白行
4. 支持 Python、JavaScript、YAML 等语言
5. 处理编码错误

请提供完整的代码，支持多种语言的注释识别。
```

**AI 生成：**

```python
# codestats/analyzer.py
"""代码分析模块"""

import re
from pathlib import Path
from typing import Dict, Tuple
from dataclasses import dataclass


@dataclass
class LineStats:
    """行数统计"""
    total: int
    code: int
    comments: int
    blanks: int


class CodeAnalyzer:
    """代码分析器"""
    
    # 不同语言的注释模式
    COMMENT_PATTERNS = {
        'Python': {
            'single': r'#.*$',
            'multi_start': r'"""|\'\'\'',
            'multi_end': r'"""|\'\'\'',
        },
        'JavaScript': {
            'single': r'//.*$',
            'multi_start': r'/\*',
            'multi_end': r'\*/',
        },
        'TypeScript': {
            'single': r'//.*$',
            'multi_start': r'/\*',
            'multi_end': r'\*/',
        },
        'Java': {
            'single': r'//.*$',
            'multi_start': r'/\*',
            'multi_end': r'\*/',
        },
        'Go': {
            'single': r'//.*$',
            'multi_start': r'/\*',
            'multi_end': r'\*/',
        },
        'C': {
            'single': r'//.*$',
            'multi_start': r'/\*',
            'multi_end': r'\*/',
        },
        'C++': {
            'single': r'//.*$',
            'multi_start': r'/\*',
            'multi_end': r'\*/',
        },
        'YAML': {
            'single': r'#.*$',
            'multi_start': None,
            'multi_end': None,
        },
        'Shell': {
            'single': r'#.*$',
            'multi_start': None,
            'multi_end': None,
        },
        'Ruby': {
            'single': r'#.*$',
            'multi_start': r'=begin',
            'multi_end': r'=end',
        },
    }
    
    def analyze_file(self, file_path: Path, language: str) -> LineStats:
        """
        分析单个文件
        
        Args:
            file_path: 文件路径
            language: 编程语言
        
        Returns:
            行数统计
        """
        try:
            # 尝试多种编码
            content = self._read_file(file_path)
        except Exception:
            # 无法读取，返回空统计
            return LineStats(total=0, code=0, comments=0, blanks=0)
        
        lines = content.split('\n')
        total = len(lines)
        
        # 获取注释模式
        patterns = self.COMMENT_PATTERNS.get(language, {})
        
        # 统计各类行数
        code_lines = 0
        comment_lines = 0
        blank_lines = 0
        in_multiline_comment = False
        
        for line in lines:
            stripped = line.strip()
            
            # 空白行
            if not stripped:
                blank_lines += 1
                continue
            
            # 多行注释处理
            if patterns.get('multi_start'):
                if re.search(patterns['multi_start'], stripped):
                    in_multiline_comment = True
                
                if in_multiline_comment:
                    comment_lines += 1
                    if re.search(patterns['multi_end'], stripped):
                        in_multiline_comment = False
                    continue
            
            # 单行注释
            if patterns.get('single') and re.match(patterns['single'], stripped):
                comment_lines += 1
                continue
            
            # 代码行
            code_lines += 1
        
        return LineStats(
            total=total,
            code=code_lines,
            comments=comment_lines,
            blanks=blank_lines,
        )
    
    def _read_file(self, file_path: Path) -> str:
        """
        读取文件（尝试多种编码）
        
        Args:
            file_path: 文件路径
        
        Returns:
            文件内容
        """
        encodings = ['utf-8', 'gbk', 'latin1']
        
        for encoding in encodings:
            try:
                return file_path.read_text(encoding=encoding)
            except (UnicodeDecodeError, UnicodeError):
                continue
        
        raise ValueError(f"无法读取文件: {file_path}")
    
    def analyze_directory(
        self,
        file_stats: Dict[str, LineStats]
    ) -> Dict[str, LineStats]:
        """
        汇总目录统计
        
        Args:
            file_stats: 每个文件的统计
        
        Returns:
            汇总统计
        """
        total_stats = LineStats(total=0, code=0, comments=0, blanks=0)
        
        for stats in file_stats.values():
            total_stats.total += stats.total
            total_stats.code += stats.code
            total_stats.comments += stats.comments
            total_stats.blanks += stats.blanks
        
        return {'total': total_stats}
```

<br/>

***

<br/>

## 三、整合与测试

### 3.1 更新 CLI

**提示词：**

```
更新 codestats/cli.py，整合 scanner 和 analyzer：

需求：
1. 扫描项目文件
2. 分析代码行数
3. 按语言汇总统计
4. 使用 Rich 美化输出
5. 支持 JSON 格式输出

请提供完整的代码。
```

**AI 生成：**

```python
# codestats/cli.py
"""Command-line interface for codestats"""

import click
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.panel import Panel

from .scanner import FileScanner, FileInfo
from .analyzer import CodeAnalyzer, LineStats

console = Console()


@click.command()
@click.argument('path', type=click.Path(exists=True), default='.')
@click.option('--exclude', '-e', multiple=True, help='排除的目录')
@click.option('--json', '-j', 'output_json', is_flag=True, help='输出 JSON 格式')
@click.option('--top', '-t', default=5, help='显示最大的 N 个文件')
def main(path: str, exclude: tuple, output_json: bool, top: int):
    """
    统计代码行数
    
    PATH: 项目路径（默认当前目录）
    """
    # 扫描文件
    scanner = FileScanner(path, set(exclude))
    
    with Progress() as progress:
        task = progress.add_task("[cyan]扫描文件...", total=None)
        files = scanner.scan()
        progress.update(task, completed=True)
    
    if not files:
        console.print("[yellow]未找到任何文件[/yellow]")
        return
    
    # 分析代码
    analyzer = CodeAnalyzer()
    file_stats = {}
    language_stats = {}
    
    with Progress() as progress:
        task = progress.add_task("[cyan]分析代码...", total=len(files))
        
        for file_info in files:
            # 只分析已知语言
            if file_info.language != 'Unknown':
                stats = analyzer.analyze_file(
                    file_info.path,
                    file_info.language
                )
                file_stats[str(file_info.path)] = stats
                
                # 按语言汇总
                lang = file_info.language
                if lang not in language_stats:
                    language_stats[lang] = LineStats(
                        total=0, code=0, comments=0, blanks=0
                    )
                language_stats[lang].total += stats.total
                language_stats[lang].code += stats.code
                language_stats[lang].comments += stats.comments
                language_stats[lang].blanks += stats.blanks
            
            progress.update(task, advance=1)
    
    # 输出结果
    if output_json:
        output_json_result(files, file_stats, language_stats)
    else:
        output_rich_result(path, files, file_stats, language_stats, top)


def output_rich_result(
    path: str,
    files: list,
    file_stats: dict,
    language_stats: dict,
    top: int
):
    """使用 Rich 输出美化结果"""
    
    # 标题
    console.print(Panel.fit(
        "[bold cyan]📊 代码统计报告[/bold cyan]",
        border_style="cyan"
    ))
    
    console.print(f"[bold]项目路径:[/bold] {Path(path).resolve()}")
    console.print()
    
    # 文件统计
    console.print("[bold]📁 文件统计[/bold]")
    console.print(f"  总文件数: {len(files)}")
    console.print(f"  代码文件: {len(file_stats)}")
    console.print()
    
    # 代码行数
    total_lines = sum(s.total for s in language_stats.values())
    total_code = sum(s.code for s in language_stats.values())
    total_comments = sum(s.comments for s in language_stats.values())
    total_blanks = sum(s.blanks for s in language_stats.values())
    
    console.print("[bold]📝 代码行数[/bold]")
    console.print(f"  总行数: {total_lines:,}")
    console.print(f"  代码行: {total_code:,} ({total_code/total_lines*100:.1f}%)")
    console.print(f"  注释行: {total_comments:,} ({total_comments/total_lines*100:.1f}%)")
    console.print(f"  空白行: {total_blanks:,} ({total_blanks/total_lines*100:.1f}%)")
    console.print()
    
    # 语言分布表格
    console.print("[bold]💻 语言分布[/bold]")
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("语言", style="green")
    table.add_column("代码行", justify="right")
    table.add_column("占比", justify="right")
    
    # 按代码行数排序
    sorted_langs = sorted(
        language_stats.items(),
        key=lambda x: x[1].code,
        reverse=True
    )
    
    for lang, stats in sorted_langs:
        if stats.code > 0:
            percentage = stats.code / total_code * 100
            table.add_row(
                lang,
                f"{stats.code:,}",
                f"{percentage:.1f}%"
            )
    
    console.print(table)
    console.print()
    
    # 最大的文件
    console.print(f"[bold]🏆 最大的 {top} 个文件[/bold]")
    sorted_files = sorted(
        file_stats.items(),
        key=lambda x: x[1].total,
        reverse=True
    )[:top]
    
    for i, (file_path, stats) in enumerate(sorted_files, 1):
        relative_path = Path(file_path).relative_to(Path(path).resolve())
        console.print(f"  {i}. {relative_path} ({stats.total} 行)")


def output_json_result(files, file_stats, language_stats):
    """输出 JSON 格式结果"""
    result = {
        'summary': {
            'total_files': len(files),
            'code_files': len(file_stats),
        },
        'lines': {
            'total': sum(s.total for s in language_stats.values()),
            'code': sum(s.code for s in language_stats.values()),
            'comments': sum(s.comments for s in language_stats.values()),
            'blanks': sum(s.blanks for s in language_stats.values()),
        },
        'by_language': {
            lang: {
                'total': stats.total,
                'code': stats.code,
                'comments': stats.comments,
                'blanks': stats.blanks,
            }
            for lang, stats in language_stats.items()
        },
    }
    
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
```

<br/>

### 3.2 测试工具

**测试命令：**

```bash
# 统计当前项目
poetry run codestats

# 统计指定项目
poetry run codestats /path/to/project

# 排除特定目录
poetry run codestats --exclude tests --exclude docs

# 输出 JSON
poetry run codestats --json

# 显示最大的 10 个文件
poetry run codestats --top 10
```

**测试输出：**

```
╭──────────────────────╮
│ 📊 代码统计报告      │
╰──────────────────────╯

项目路径: /Users/admin/codestats

📁 文件统计
  总文件数: 12
  代码文件: 8

📝 代码行数
  总行数: 456
  代码行: 312 (68.4%)
  注释行: 78 (17.1%)
  空白行: 66 (14.5%)

💻 语言分布
┏━━━━━━━━━━┳━━━━━━━━┳━━━━━━┓
┃ 语言     ┃ 代码行 ┃ 占比 ┃
┡━━━━━━━━━━╇━━━━━━━━╇━━━━━━┩
│ Python   │    312 │ 100% │
└──────────┴────────┴──────┘

🏆 最大的 5 个文件
  1. codestats/cli.py (142 行)
  2. codestats/analyzer.py (128 行)
  3. codestats/scanner.py (86 行)
```

<br/>

***

<br/>

## 四、添加单元测试

### 4.1 测试代码

**提示词：**

```
为 codestats 创建单元测试：

需求：
1. 测试 scanner.py 的文件扫描功能
2. 测试 analyzer.py 的代码分析功能
3. 使用 pytest 框架
4. 使用临时目录测试

请提供完整的测试代码。
```

**AI 生成：**

```python
# tests/test_scanner.py
"""测试文件扫描器"""

import pytest
from pathlib import Path
from codestats.scanner import FileScanner


@pytest.fixture
def temp_project(tmp_path):
    """创建临时项目"""
    # 创建文件结构
    (tmp_path / "main.py").write_text("print('hello')")
    (tmp_path / "utils.py").write_text("# utils\npass")
    
    # 创建子目录
    subdir = tmp_path / "services"
    subdir.mkdir()
    (subdir / "user.py").write_text("class User:\n    pass")
    
    # 创建要排除的目录
    venv = tmp_path / "venv"
    venv.mkdir()
    (venv / "lib.py").write_text("# should be excluded")
    
    return tmp_path


def test_scan_basic(temp_project):
    """测试基本扫描"""
    scanner = FileScanner(str(temp_project))
    files = scanner.scan()
    
    # 应该找到 3 个文件（排除 venv）
    assert len(files) == 3
    
    # 检查文件类型
    extensions = {f.extension for f in files}
    assert extensions == {'.py'}


def test_scan_excludes(temp_project):
    """测试排除目录"""
    scanner = FileScanner(str(temp_project))
    files = scanner.scan()
    
    # venv 目录应该被排除
    for f in files:
        assert 'venv' not in str(f.path)


def test_get_statistics(temp_project):
    """测试统计功能"""
    scanner = FileScanner(str(temp_project))
    files = scanner.scan()
    stats = scanner.get_statistics(files)
    
    assert stats['total_files'] == 3
    assert stats['by_language']['Python'] == 3
```

```python
# tests/test_analyzer.py
"""测试代码分析器"""

import pytest
from pathlib import Path
from codestats.analyzer import CodeAnalyzer


@pytest.fixture
def python_file(tmp_path):
    """创建 Python 测试文件"""
    content = '''
"""模块文档"""

def hello():
    """函数文档"""
    # 注释
    print("hello")
    pass

# 另一个注释
'''
    file_path = tmp_path / "test.py"
    file_path.write_text(content)
    return file_path


def test_analyze_python_file(python_file):
    """测试 Python 文件分析"""
    analyzer = CodeAnalyzer()
    stats = analyzer.analyze_file(python_file, 'Python')
    
    # 检查统计
    assert stats.total == 10  # 总行数
    assert stats.code >= 3    # 至少 3 行代码
    assert stats.comments >= 2  # 至少 2 行注释
    assert stats.blanks >= 2    # 至少 2 行空白


def test_analyze_empty_file(tmp_path):
    """测试空文件"""
    file_path = tmp_path / "empty.py"
    file_path.write_text("")
    
    analyzer = CodeAnalyzer()
    stats = analyzer.analyze_file(file_path, 'Python')
    
    assert stats.total == 1  # 空文件有 1 行
    assert stats.code == 0
```

**运行测试：**

```bash
poetry run pytest tests/ -v
```

<br/>

***

<br/>

## 五、总结与改进

### 5.1 学到了什么

**技术要点：**

```
✅ CLI 开发：Click 框架的使用
✅ 文件操作：pathlib、os.walk
✅ 代码分析：正则表达式、字符串处理
✅ 美化输出：Rich 库的使用
✅ 单元测试：pytest、临时目录
✅ 项目管理：poetry、pyproject.toml
```

**AI Coding 技巧：**

```
1. 明确需求 → AI 生成代码骨架
2. 逐步完善 → AI 填充细节
3. 提出问题 → AI 修复 bug
4. 请求测试 → AI 生成测试用例
```

<br/>

### 5.2 可能的改进

**功能增强：**

```
📋 添加更多语言支持（Go、Rust、Java）
📋 生成趋势图（代码增长曲线）
📋 对比不同版本
📋 生成 HTML 报告
📋 添加 CI 集成
```

**性能优化：**

```
📋 多线程扫描
📋 增量更新
📋 缓存结果
```

<br/>

***

<br/>

**系列导航**

• 上一篇：安全与隐私：代码安全吗？
• 下一篇：实战02：开发 Web API

<br/>

***

本文是《AI Coding 从入门到精通》系列第16篇  
作者：生活助理 | 发布时间：2026-04-05

**动手实践，从工具开发开始！** 🔧
