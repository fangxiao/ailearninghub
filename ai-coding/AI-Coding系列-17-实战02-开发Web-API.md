# 实战02：开发 Web API

阅读时间：45分钟
难度等级：⭐⭐⭐ 进阶
你将收获：把 CLI 工具扩展成 Web API，学习 RESTful 设计

<br/>

***

<br/>

## 从 CLI 到 API：项目进化

**上篇回顾：**

```
✅ 实战01：codestats CLI 工具
   - 扫描本地项目
   - 统计代码行数
   - 美化输出
   - JSON 导出
```

**使用场景的局限：**

```bash
# 每次都要手动运行
$ codestats /path/to/project

# 无法多项目管理
$ codestats /project1
$ codestats /project2

# 无法查看历史趋势
# 只能看到当前快照

# 无法团队共享
# 每个人都要安装工具
```

**进化方向：Web API**

```
CLI 工具（单机）
  └─ 手动运行
  └─ 本地数据
  └─ 单人使用

      ↓ 升级

Web API（服务化）
  └─ 持续运行
  └─ 数据库存储
  └─ 多人访问
  └─ 支持前端界面
```

**本篇目标：**

```
把 codestats CLI 改造成 Web API

API 功能：
✅ 管理多个项目
✅ 获取项目统计
✅ 项目对比分析
✅ 历史记录查询
✅ 数据持久化
```

**学习要点：**

- ✅ RESTful API 设计原则
- ✅ FastAPI 框架使用
- ✅ 数据库模型设计
- ✅ 请求验证和错误处理
- ✅ API 文档自动生成

<br/>

***

<br/>

## 一、项目规划

### 1.1 功能设计

**项目名称：** `codestats-api`

**API 端点：**

```
项目管理
POST   /api/projects              # 添加项目
GET    /api/projects              # 获取项目列表
GET    /api/projects/{id}         # 获取单个项目
DELETE /api/projects/{id}         # 删除项目

统计分析
POST   /api/projects/{id}/analyze # 分析项目
GET    /api/projects/{id}/stats   # 获取统计结果

增强功能
GET    /api/projects/compare      # 项目对比
GET    /api/projects/{id}/history # 历史记录
GET    /api/stats/trends          # 趋势分析
```

**技术栈：**

```
框架：FastAPI（现代、快速、自动文档）
数据库：SQLite + SQLAlchemy
验证：Pydantic
部署：Uvicorn
```

<br/>

### 1.2 项目结构

```
codestats-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 应用
│   ├── config.py            # 配置
│   ├── database.py          # 数据库连接
│   ├── models/
│   │   ├── __init__.py
│   │   └── project.py       # 项目模型
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── project.py       # Pydantic 模型
│   ├── api/
│   │   ├── __init__.py
│   │   └── projects.py      # API 路由
│   └── services/
│       ├── __init__.py
│       ├── scanner.py       # 复用 CLI 的扫描逻辑
│       └── analyzer.py      # 复用 CLI 的分析逻辑
├── tests/
├── requirements.txt
└── README.md
```

<br/>

***

<br/>

## 二、项目初始化

### 2.1 创建项目

```bash
# 创建项目目录
mkdir codestats-api
cd codestats-api

# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖（下一步生成）
```

<br/>

### 2.2 生成项目文件

**使用 AI 生成所有配置文件：**

```
我要创建一个 FastAPI 项目 codestats-api，用于代码统计分析。

请生成：
1. requirements.txt
2. app/__init__.py
3. app/config.py
4. app/database.py

要求：
- FastAPI 最新版
- SQLAlchemy + Pydantic
- SQLite 数据库
- 完整的配置管理
```

**完整代码：**

```python
# requirements.txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
pydantic==2.5.0
pydantic-settings==2.1.0

# app/__init__.py
__version__ = "0.1.0"

# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "CodeStats API"
    app_version: str = "0.1.0"
    database_url: str = "sqlite:///./codestats.db"
    api_prefix: str = "/api"
    
    class Config:
        env_file = ".env"

settings = Settings()

# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

```bash
# 安装依赖
pip install -r requirements.txt
```

<br/>

***

<br/>

## 三、数据模型

### 3.1 数据库模型

**创建 `app/models/project.py`：**

```python
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from ..database import Base

class Project(Base):
    """项目模型"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    path = Column(String(500), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    
    # 统计数据
    total_files = Column(Integer, default=0)
    code_files = Column(Integer, default=0)
    total_lines = Column(Integer, default=0)
    code_lines = Column(Integer, default=0)
    comment_lines = Column(Integer, default=0)
    blank_lines = Column(Integer, default=0)
    language_stats = Column(JSON, default=dict)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_analyzed_at = Column(DateTime, nullable=True)
    
    # 关联历史记录
    history = relationship("AnalysisHistory", back_populates="project", cascade="all, delete-orphan")

class AnalysisHistory(Base):
    """分析历史记录"""
    __tablename__ = "analysis_history"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, nullable=False, index=True)
    
    # 统计快照
    total_files = Column(Integer, default=0)
    code_files = Column(Integer, default=0)
    total_lines = Column(Integer, default=0)
    code_lines = Column(Integer, default=0)
    comment_lines = Column(Integer, default=0)
    blank_lines = Column(Integer, default=0)
    language_stats = Column(JSON, default=dict)
    
    analyzed_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # 关联项目
    project = relationship("Project", back_populates="history")
```

<br/>

### 3.2 Pydantic 模型

**创建 `app/schemas/project.py`：**

```python
from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

# 项目基础模型
class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    path: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: int
    total_files: int = 0
    code_files: int = 0
    total_lines: int = 0
    code_lines: int = 0
    comment_lines: int = 0
    blank_lines: int = 0
    language_stats: Dict[str, int] = {}
    created_at: datetime
    updated_at: datetime
    last_analyzed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# 历史记录模型
class HistoryResponse(BaseModel):
    id: int
    project_id: int
    total_files: int
    code_files: int
    total_lines: int
    code_lines: int
    comment_lines: int
    blank_lines: int
    language_stats: Dict[str, int]
    analyzed_at: datetime
    
    class Config:
        from_attributes = True

# 对比模型
class CompareItem(BaseModel):
    project_name: str
    total_files: int
    total_lines: int
    code_lines: int

class CompareResponse(BaseModel):
    projects: List[CompareItem]
    comparison: Dict[str, Dict[str, float]]

# 通用响应
class MessageResponse(BaseModel):
    message: str
    detail: Optional[str] = None
```

<br/>

***

<br/>

## 四、业务逻辑

### 4.1 复用 CLI 核心代码

```bash
# 复制 CLI 的核心模块
cp ../codestats/codestats/scanner.py app/services/
cp ../codestats/codestats/analyzer.py app/services/

# 调整导入路径（移除相对导入）
# scanner.py: from pathlib import Path
# analyzer.py: import re, from pathlib import Path
```

<br/>

### 4.2 创建分析服务

**创建 `app/services/stats_service.py`：**

```python
from pathlib import Path
from typing import Dict, Any
from sqlalchemy.orm import Session
from .scanner import FileScanner
from .analyzer import CodeAnalyzer
from ..models.project import Project, AnalysisHistory

class StatsService:
    """统计分析服务"""
    
    def __init__(self, db: Session):
        self.db = db
        self.scanner = FileScanner
        self.analyzer = CodeAnalyzer()
    
    def analyze_project(self, project: Project) -> Dict[str, Any]:
        """分析项目"""
        project_path = Path(project.path)
        
        if not project_path.exists():
            raise ValueError(f"项目路径不存在: {project_path}")
        
        # 扫描文件
        scanner = self.scanner(str(project_path))
        files = scanner.scan()
        
        if not files:
            return self._empty_result()
        
        # 分析代码
        file_stats = {}
        language_stats = {}
        
        for file_info in files:
            if file_info.language != 'Unknown':
                stats = self.analyzer.analyze_file(
                    file_info.path,
                    file_info.language
                )
                file_stats[str(file_info.path)] = stats
                
                # 按语言汇总
                lang = file_info.language
                if lang not in language_stats:
                    language_stats[lang] = {
                        'files': 0, 'total': 0,
                        'code': 0, 'comments': 0, 'blanks': 0
                    }
                
                language_stats[lang]['files'] += 1
                language_stats[lang]['total'] += stats.total
                language_stats[lang]['code'] += stats.code
                language_stats[lang]['comments'] += stats.comments
                language_stats[lang]['blanks'] += stats.blanks
        
        # 汇总统计
        result = {
            'total_files': len(files),
            'code_files': len(file_stats),
            'total_lines': sum(s['total'] for s in language_stats.values()),
            'code_lines': sum(s['code'] for s in language_stats.values()),
            'comment_lines': sum(s['comments'] for s in language_stats.values()),
            'blank_lines': sum(s['blanks'] for s in language_stats.values()),
            'language_stats': language_stats,
        }
        
        # 更新项目
        for key, value in result.items():
            setattr(project, key, value)
        
        from datetime import datetime
        project.last_analyzed_at = datetime.utcnow()
        
        # 保存历史记录
        history = AnalysisHistory(project_id=project.id, **result)
        self.db.add(history)
        self.db.commit()
        
        return result
    
    def _empty_result(self):
        return {
            'total_files': 0, 'code_files': 0,
            'total_lines': 0, 'code_lines': 0,
            'comment_lines': 0, 'blank_lines': 0,
            'language_stats': {}
        }
    
    def get_history(self, project_id: int, limit: int = 10):
        """获取分析历史"""
        return self.db.query(AnalysisHistory).filter(
            AnalysisHistory.project_id == project_id
        ).order_by(
            AnalysisHistory.analyzed_at.desc()
        ).limit(limit).all()
    
    def compare_projects(self, project_ids: list):
        """对比多个项目"""
        projects = self.db.query(Project).filter(
            Project.id.in_(project_ids)
        ).all()
        
        if not projects:
            return None
        
        comparison = {
            'by_total_lines': {},
            'by_code_lines': {},
            'by_files': {}
        }
        
        total_lines_sum = sum(p.total_lines for p in projects)
        code_lines_sum = sum(p.code_lines for p in projects)
        files_sum = sum(p.total_files for p in projects)
        
        for project in projects:
            name = project.name
            comparison['by_total_lines'][name] = (
                project.total_lines / total_lines_sum * 100 
                if total_lines_sum > 0 else 0
            )
            comparison['by_code_lines'][name] = (
                project.code_lines / code_lines_sum * 100 
                if code_lines_sum > 0 else 0
            )
            comparison['by_files'][name] = (
                project.total_files / files_sum * 100 
                if files_sum > 0 else 0
            )
        
        return {'projects': projects, 'comparison': comparison}
```

<br/>

***

<br/>

## 五、API 路由

### 5.1 项目管理 API

**创建 `app/api/projects.py`：**

```python
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.project import Project
from ..schemas.project import (
    ProjectCreate, ProjectUpdate, ProjectResponse,
    HistoryResponse, CompareResponse, MessageResponse
)
from ..services.stats_service import StatsService

router = APIRouter(prefix="/projects", tags=["Projects"])

# ========== CRUD 操作 ==========

@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(project_data: ProjectCreate, db: Session = Depends(get_db)):
    """创建项目"""
    existing = db.query(Project).filter(Project.path == project_data.path).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"项目路径已存在: {project_data.path}")
    
    project = Project(**project_data.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.get("/", response_model=List[ProjectResponse])
def list_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """获取项目列表"""
    query = db.query(Project)
    
    if search:
        query = query.filter(
            (Project.name.ilike(f"%{search}%")) |
            (Project.path.ilike(f"%{search}%"))
        )
    
    return query.offset(skip).limit(limit).all()

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """获取单个项目"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    return project

@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db)
):
    """更新项目"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    update_data = project_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    return project

@router.delete("/{project_id}", response_model=MessageResponse)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """删除项目"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    db.delete(project)
    db.commit()
    return {"message": "项目已删除", "detail": f"项目 {project.name} 已删除"}

# ========== 分析相关 ==========

@router.post("/{project_id}/analyze", response_model=ProjectResponse)
def analyze_project(project_id: int, db: Session = Depends(get_db)):
    """分析项目"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    service = StatsService(db)
    try:
        service.analyze_project(project)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")
    
    db.refresh(project)
    return project

@router.get("/{project_id}/history", response_model=List[HistoryResponse])
def get_project_history(
    project_id: int,
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """获取项目历史记录"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    service = StatsService(db)
    return service.get_history(project_id, limit)

# ========== 对比功能 ==========

@router.get("/compare", response_model=CompareResponse)
def compare_projects(
    project_ids: str = Query(..., description="项目ID列表，用逗号分隔"),
    db: Session = Depends(get_db)
):
    """对比多个项目"""
    try:
        ids = [int(id.strip()) for id in project_ids.split(",")]
    except ValueError:
        raise HTTPException(status_code=400, detail="无效的项目 ID 列表")
    
    if len(ids) < 2:
        raise HTTPException(status_code=400, detail="至少需要 2 个项目进行对比")
    
    service = StatsService(db)
    result = service.compare_projects(ids)
    
    if not result:
        raise HTTPException(status_code=404, detail="未找到任何项目")
    
    return CompareResponse(
        projects=[
            CompareItem(
                project_name=p.name,
                total_files=p.total_files,
                total_lines=p.total_lines,
                code_lines=p.code_lines
            )
            for p in result['projects']
        ],
        comparison=result['comparison']
    )
```

<br/>

***

<br/>

## 六、主应用

### 6.1 创建 FastAPI 应用

**创建 `app/main.py`：**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import engine, Base
from .api import projects

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建应用
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
## CodeStats API

代码统计分析 API 服务

### 功能特性

- ✅ 管理多个项目
- ✅ 代码统计分析
- ✅ 历史记录查询
- ✅ 项目对比分析

### 快速开始

1. 创建项目：POST /api/projects
2. 分析项目：POST /api/projects/{id}/analyze
3. 查看统计：GET /api/projects/{id}
4. 对比项目：GET /api/projects/compare?project_ids=1,2,3
    """,
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(projects.router, prefix=settings.api_prefix)

# 健康检查
@app.get("/")
def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

# 启动事件
@app.on_event("startup")
async def startup_event():
    print(f"🚀 {settings.app_name} v{settings.app_version} 启动")
    print(f"📚 API 文档: http://localhost:8000/docs")
```

<br/>

***

<br/>

## 七、测试 API

### 7.1 启动服务

```bash
# 启动开发服务器
uvicorn app.main:app --reload

# 输出：
# INFO:     Uvicorn running on http://127.0.0.1:8000
# 🚀 CodeStats API v0.1.0 启动
# 📚 API 文档: http://localhost:8000/docs
```

<br/>

### 7.2 访问 API 文档

```
Swagger UI:  http://localhost:8000/docs
ReDoc:       http://localhost:8000/redoc
```

<br/>

### 7.3 测试示例

**使用 curl 测试：**

```bash
# 1. 创建项目
curl -X POST http://localhost:8000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name":"My Project","path":"/Users/admin/my_project"}'

# 响应：
# {"id":1,"name":"My Project","path":"/Users/admin/my_project",...}

# 2. 分析项目
curl -X POST http://localhost:8000/api/projects/1/analyze

# 3. 查看统计
curl http://localhost:8000/api/projects/1

# 4. 查看历史
curl http://localhost:8000/api/projects/1/history

# 5. 对比项目（需要先创建多个项目）
curl "http://localhost:8000/api/projects/compare?project_ids=1,2"
```

<br/>

***

<br/>

## 八、总结

### 8.1 完成的功能

**核心功能：**

```
✅ 项目管理（CRUD）
✅ 代码统计分析
✅ 历史记录保存
✅ 项目对比分析
✅ 自动 API 文档
```

**技术栈：**

```
✅ FastAPI（快速、现代）
✅ SQLAlchemy（ORM）
✅ Pydantic（数据验证）
✅ Uvicorn（ASGI 服务器）
```

<br/>

### 8.2 从 CLI 到 API 的价值

| 特性 | CLI 工具 | Web API |
|------|---------|---------|
| 使用方式 | 手动运行 | 随时访问 |
| 数据管理 | 单次快照 | 持久化存储 |
| 多人协作 | 不支持 | 支持 |
| 历史查询 | 不支持 | 支持 |
| 集成能力 | 独立工具 | 可扩展 |

<br/>

### 8.3 下一步改进

**性能优化：**

```
📋 后台任务（Celery）
📋 缓存（Redis）
📋 增量分析
```

**功能扩展：**

```
📋 用户认证
📋 权限管理
📋 WebSocket 实时更新
📋 导出报告
```

**为下一篇做准备：**

```
🔄 实战03：引入 MCP
   - 连接 GitHub API
   - 连接 GitLab API
   - 实时同步仓库信息
   - 自动触发分析
```

<br/>

***

<br/>

**系列导航**

• 上一篇：实战01：开发命令行工具
• 下一篇：实战03：引入 MCP — 连接外部服务

<br/>

***

本文是《AI Coding 从入门到精通》系列第17篇  
作者：生活助理 | 发布时间：2026-04-06

**从单机工具到服务平台，项目持续进化！** 🚀
