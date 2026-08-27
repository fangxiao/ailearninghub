# 实战08：数据分析 + AI 特性

阅读时间：35分钟
难度等级：⭐⭐⭐⭐ 进阶
你将收获：机器学习、LLM 集成、报告生成

<br/>

***

<br/>

## 智能化升级

**之前完成：**

```
✅ 实战01-07：完整平台
   - CLI 工具
   - Web API
   - MCP 集成
   - 前端界面
   - 用户系统
   - 团队协作
```

**当前能力：**

```
✅ 代码统计（基础）
   - 文件数量
   - 代码行数
   - 语言分布

❌ 缺少智能分析
   - 代码质量评分
   - 智能建议
   - 趋势预测
```

**AI 增强目标：**

```
✅ 机器学习模型
   - 代码质量评分
   - 异常检测
   - 趋势预测

✅ LLM 集成
   - 智能分析报告
   - 改进建议
   - 代码摘要

✅ 报告生成
   - PDF 导出
   - Excel 导出
   - HTML 报告
```

**本篇目标：**

```
添加 AI 分析能力

内容：
✅ 机器学习模型训练
✅ 代码质量评分
✅ LLM 智能建议
✅ 报告生成
✅ 数据导出
```

**学习要点：**

- ✅ 机器学习基础
- ✅ scikit-learn 使用
- ✅ LLM API 集成
- ✅ 报告生成工具
- ✅ 数据可视化

<br/>

***

<br/>

## 一、代码质量评分

### 1.1 特征工程

```python
# app/ml/feature_extraction.py
from typing import Dict, List
import numpy as np

class FeatureExtractor:
    """特征提取器"""
    
    def extract_features(self, stats: Dict) -> np.ndarray:
        """
        提取代码质量特征
        
        特征：
        1. 平均函数长度
        2. 注释比例
        3. 测试覆盖率
        4. 圈复杂度
        5. 代码重复率
        6. 文件大小分布
        """
        features = [
            stats.get('avg_function_length', 0),
            stats.get('comment_ratio', 0),
            stats.get('test_coverage', 0),
            stats.get('cyclomatic_complexity', 0),
            stats.get('duplication_rate', 0),
            stats.get('avg_file_size', 0),
            stats.get('file_size_std', 0),
            stats.get('total_files', 0),
            stats.get('code_files_ratio', 0),
        ]
        
        return np.array(features)
    
    def calculate_derived_stats(self, project_stats: Dict) -> Dict:
        """计算派生统计"""
        total_lines = project_stats.get('total_lines', 1)
        
        return {
            'comment_ratio': project_stats.get('comment_lines', 0) / total_lines,
            'code_files_ratio': project_stats.get('code_files', 0) / max(project_stats.get('total_files', 1), 1),
            'avg_file_size': total_lines / max(project_stats.get('total_files', 1), 1),
            # 其他派生统计...
        }
```

<br/>

### 1.2 训练模型

```python
# app/ml/quality_model.py
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

class QualityScorer:
    """代码质量评分器"""
    
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.feature_extractor = FeatureExtractor()
    
    def train(self, X, y):
        """
        训练模型
        
        Args:
            X: 特征矩阵
            y: 标签 (1-5 星评分)
        """
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        # 评估
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"模型准确率: {accuracy:.2f}")
        print(classification_report(y_test, y_pred))
        
        # 保存模型
        joblib.dump(self.model, 'models/quality_scorer.pkl')
    
    def predict(self, project_stats: Dict) -> int:
        """
        预测代码质量评分
        
        Returns:
            1-5 星评分
        """
        features = self.feature_extractor.extract_features(project_stats)
        features = features.reshape(1, -1)
        
        score = self.model.predict(features)[0]
        return int(score)
    
    def predict_proba(self, project_stats: Dict) -> Dict[int, float]:
        """
        预测各评分的概率
        
        Returns:
            {1: 0.1, 2: 0.2, 3: 0.3, 4: 0.25, 5: 0.15}
        """
        features = self.feature_extractor.extract_features(project_stats)
        features = features.reshape(1, -1)
        
        proba = self.model.predict_proba(features)[0]
        return {i+1: float(p) for i, p in enumerate(proba)}
```

<br/>

***

<br/>

## 二、LLM 智能建议

### 2.1 LLM 集成

```python
# app/ai/llm_client.py
from openai import OpenAI
from typing import Dict, List
import os

class LLMClient:
    """LLM 客户端"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        )
        self.model = os.getenv("LLM_MODEL", "gpt-4")
    
    async def analyze_project(self, stats: Dict) -> Dict:
        """
        分析项目并生成建议
        
        Args:
            stats: 项目统计数据
        
        Returns:
            {
                "summary": "项目概要",
                "strengths": ["优点1", "优点2"],
                "improvements": ["改进建议1", "建议2"],
                "score": 4
            }
        """
        prompt = f"""
你是一个代码质量分析师。请分析以下项目的统计数据，并提供专业建议。

项目统计：
- 总文件数: {stats['total_files']}
- 代码文件: {stats['code_files']}
- 总代码行数: {stats['total_lines']}
- 代码行: {stats['code_lines']} ({stats['code_lines']/stats['total_lines']*100:.1f}%)
- 注释行: {stats['comment_lines']} ({stats['comment_lines']/stats['total_lines']*100:.1f}%)
- 语言分布: {stats['language_stats']}

请以 JSON 格式返回：
{{
  "summary": "1-2句话的项目概要",
  "strengths": ["优点1", "优点2", "优点3"],
  "improvements": ["改进建议1", "建议2", "建议3"],
  "score": 1-5的评分
}}
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是专业的代码质量分析师"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        import json
        return json.loads(response.choices[0].message.content)
    
    async def generate_report(self, project: Dict) -> str:
        """生成 Markdown 报告"""
        analysis = await self.analyze_project(project['stats'])
        
        report = f"""
# {project['name']} - 代码质量报告

## 项目概要

{analysis['summary']}

## 统计数据

| 指标 | 数值 |
|------|------|
| 总文件数 | {project['stats']['total_files']} |
| 代码行数 | {project['stats']['code_lines']:,} |
| 注释比例 | {project['stats']['comment_lines']/project['stats']['total_lines']*100:.1f}% |

## 优点

{chr(10).join(f'- {s}' for s in analysis['strengths'])}

## 改进建议

{chr(10).join(f'{i+1}. {s}' for i, s in enumerate(analysis['improvements']))}

## 评分

{'⭐' * analysis['score']} ({analysis['score']}/5)

---
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return report
```

<br/>

***

<br/>

## 三、报告生成

### 3.1 PDF 报告

```python
# app/reports/pdf_generator.py
from reportlab import pdfgen
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, Image
import matplotlib.pyplot as plt

class PDFReportGenerator:
    """PDF 报告生成器"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
    
    def generate(self, project: Dict, output_path: str):
        """生成 PDF 报告"""
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # 标题
        title = Paragraph(
            f"<h1>{project['name']} - 代码质量报告</h1>",
            self.styles['Heading1']
        )
        story.append(title)
        story.append(Spacer(1, 12))
        
        # 基本信息
        info_table = Table([
            ['总文件数', str(project['stats']['total_files'])],
            ['代码行数', f"{project['stats']['code_lines']:,}"],
            ['注释比例', f"{project['stats']['comment_lines']/project['stats']['total_lines']*100:.1f}%"],
        ])
        story.append(info_table)
        story.append(Spacer(1, 12))
        
        # 语言分布图
        pie_chart = self._create_language_pie(project['stats']['language_stats'])
        story.append(Image(pie_chart, width=400, height=300))
        
        # 趋势图
        trend_chart = self._create_trend_chart(project['history'])
        story.append(Image(trend_chart, width=500, height=250))
        
        # 生成 PDF
        doc.build(story)
    
    def _create_language_pie(self, language_stats: Dict) -> str:
        """创建语言分布饼图"""
        plt.figure(figsize=(6, 4.5))
        
        labels = list(language_stats.keys())
        sizes = [s['code'] for s in language_stats.values()]
        
        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.title('语言分布')
        
        chart_path = '/tmp/language_pie.png'
        plt.savefig(chart_path, dpi=100, bbox_inches='tight')
        plt.close()
        
        return chart_path
    
    def _create_trend_chart(self, history: List) -> str:
        """创建趋势折线图"""
        plt.figure(figsize=(7, 3.5))
        
        dates = [h['analyzed_at'][:10] for h in history]
        values = [h['code_lines'] for h in history]
        
        plt.plot(dates, values, marker='o')
        plt.title('代码行数趋势')
        plt.xlabel('日期')
        plt.ylabel('代码行数')
        plt.xticks(rotation=45)
        
        chart_path = '/tmp/trend.png'
        plt.savefig(chart_path, dpi=100, bbox_inches='tight')
        plt.close()
        
        return chart_path
```

<br/>

### 3.2 Excel 导出

```python
# app/reports/excel_generator.py
import openpyxl
from openpyxl.styles import Font, PatternFill
from openpyxl.chart import PieChart, LineChart

class ExcelReportGenerator:
    """Excel 报告生成器"""
    
    def generate(self, project: Dict, output_path: str):
        """生成 Excel 报告"""
        wb = openpyxl.Workbook()
        
        # 概览页
        ws = wb.active
        ws.title = "概览"
        
        ws['A1'] = f"{project['name']} - 代码质量报告"
        ws['A1'].font = Font(size=16, bold=True)
        
        ws['A3'] = "总文件数"
        ws['B3'] = project['stats']['total_files']
        
        ws['A4'] = "代码行数"
        ws['B4'] = project['stats']['code_lines']
        
        # 语言分布页
        ws_lang = wb.create_sheet("语言分布")
        
        row = 1
        for lang, stats in project['stats']['language_stats'].items():
            ws_lang[f'A{row}'] = lang
            ws_lang[f'B{row}'] = stats['code']
            row += 1
        
        # 保存
        wb.save(output_path)
```

<br/>

***

<br/>

## 四、API 集成

### 4.1 分析 API

```python
# app/api/analysis.py
from fastapi import APIRouter, Depends
from ..ml.quality_model import QualityScorer
from ..ai.llm_client import LLMClient
from ..reports.pdf_generator import PDFReportGenerator
from ..reports.excel_generator import ExcelReportGenerator

router = APIRouter(prefix="/analysis", tags=["Analysis"])

quality_scorer = QualityScorer()
llm_client = LLMClient()

@router.post("/{project_id}/score")
async def get_quality_score(project_id: int):
    """获取代码质量评分"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    score = quality_scorer.predict(project.stats)
    proba = quality_scorer.predict_proba(project.stats)
    
    return {
        "project_id": project_id,
        "score": score,
        "probability": proba
    }

@router.post("/{project_id}/suggestions")
async def get_ai_suggestions(project_id: int):
    """获取 AI 建议"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    analysis = await llm_client.analyze_project(project.stats)
    
    return analysis

@router.post("/{project_id}/report/pdf")
async def generate_pdf_report(project_id: int):
    """生成 PDF 报告"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    generator = PDFReportGenerator()
    output_path = f"/tmp/project_{project_id}_report.pdf"
    
    generator.generate(project, output_path)
    
    return FileResponse(
        output_path,
        media_type="application/pdf",
        filename=f"{project.name}_report.pdf"
    )

@router.post("/{project_id}/report/excel")
async def generate_excel_report(project_id: int):
    """生成 Excel 报告"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    generator = ExcelReportGenerator()
    output_path = f"/tmp/project_{project_id}_report.xlsx"
    
    generator.generate(project, output_path)
    
    return FileResponse(
        output_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=f"{project.name}_report.xlsx"
    )
```

<br/>

***

<br/>

## 五、总结

### 5.1 完成的功能

**机器学习：**

```
✅ 特征提取
✅ 模型训练
✅ 质量评分
✅ 概率预测
```

**LLM 集成：**

```
✅ 项目分析
✅ 智能建议
✅ 报告生成
✅ 代码摘要
```

**报告导出：**

```
✅ PDF 报告
✅ Excel 报告
✅ Markdown 报告
✅ 图表嵌入
```

<br/>

### 5.2 技术栈总结

```
机器学习：scikit-learn, numpy
LLM：OpenAI API, LangChain
图表：matplotlib, seaborn
PDF：ReportLab
Excel：openpyxl
```

<br/>

### 5.3 系列总结

**从实战01到实战08：**

```
✅ 实战01：CLI 工具
✅ 实战02：Web API
✅ 实战03：MCP 集成
✅ 实战04：打包发布
✅ 实战05：架构设计
✅ 实战06：后端 + Skills
✅ 实战07：前端界面
✅ 实战08：AI 特性
```

**项目规模：**

```
代码量：~15,000 行
技术栈：15+ 个技术
功能：30+ 个功能点
时间：8 篇教程
```

**核心收获：**

```
✅ 从 CLI 到平台
✅ 从单机到协作
✅ 从基础到智能
✅ 从开发到生产
```

<br/>

***

<br/>

**系列导航**

• 上一篇：实战07：前端界面
• 下一篇：专题篇：多语言开发

<br/>

***

本文是《AI Coding 从入门到精通》系列第23篇  
作者：生活助理 | 发布时间：2026-04-06

**用 AI 赋能，让数据说话！** 🤖
