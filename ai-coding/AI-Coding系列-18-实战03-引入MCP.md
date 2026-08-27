# 实战03：引入 MCP — 连接外部服务

阅读时间：50分钟
难度等级：⭐⭐⭐ 进阶
你将收获：使用 MCP 协议连接 GitHub、GitLab，实现自动同步和触发

<br/>

***

<br/>

## 为什么需要 MCP？

**上篇回顾：**

```
✅ 实战02：codestats Web API
   - 项目管理（CRUD）
   - 代码统计分析
   - 历史记录查询
   - 项目对比分析
```

**当前限制：**

```
❌ 手动创建项目
   每次都要输入项目名称和路径

❌ 手动触发分析
   每次都要调用 /analyze 接口

❌ 数据不同步
   仓库更新后，统计数据过期

❌ 信息不完整
   缺少 GitHub stars、issues 等信息
```

**MCP 能做什么？**

```
Model Context Protocol (MCP)
  └─ 标准化的外部服务连接协议
  └─ 让 AI 应用能访问外部数据源
  └─ 支持实时同步和事件触发

应用到 codestats：
  ✅ 自动发现 GitHub 仓库
  ✅ 实时同步仓库信息（stars、forks、issues）
  ✅ Webhook 触发自动分析
  ✅ 支持多平台（GitHub、GitLab）
```

**本篇目标：**

```
给 codestats-api 引入 MCP

功能：
✅ 连接 GitHub API（获取仓库信息）
✅ 连接 GitLab API（支持多平台）
✅ 自动同步仓库数据（定时任务）
✅ Webhook 触发分析（实时更新）
```

**学习要点：**

- ✅ MCP 协议原理
- ✅ GitHub API 集成
- ✅ GitLab API 集成
- ✅ 定时任务和 Webhook
- ✅ 异步处理

<br/>

***

<br/>

## 一、MCP 简介

### 1.1 什么是 MCP？

**Model Context Protocol（模型上下文协议）**

```
定义：
  一种标准化的协议，让 AI 应用能连接外部数据源

作用：
  - 获取外部数据（API、数据库、文件系统）
  - 执行外部操作（创建、更新、删除）
  - 订阅事件（实时通知）

类似：
  - 就像 API 的标准化框架
  - 类似于 Language Server Protocol（LSP）
```

**MCP 架构：**

```
┌─────────────┐
│   AI 应用   │ (codestats-api)
│             │
│  MCP Client │ ◄────┐
└─────────────┘      │
                     │ MCP 协议
┌─────────────┐      │
│ MCP Server  │ ─────┘
│             │
│  ┌────────┐ │
│  │GitHub  │ │
│  └────────┘ │
│  ┌────────┐ │
│  │GitLab  │ │
│  └────────┘ │
│  ┌────────┐ │
│  │Database│ │
│  └────────┘ │
└─────────────┘
```

<br/>

### 1.2 MCP 在 codestats 中的应用

**场景1：自动发现仓库**

```python
# 不用 MCP（手动）
POST /api/projects
{
  "name": "My Project",
  "path": "/local/path/to/project"
}

# 使用 MCP（自动）
GET /api/github/repos
→ 自动列出所有 GitHub 仓库
→ 选择后自动创建项目
```

**场景2：实时同步信息**

```python
# 不用 MCP（数据静态）
Project:
  - name: "My Project"
  - stars: 100  # 过期的数据

# 使用 MCP（实时同步）
Project:
  - name: "My Project"
  - stars: 123  # 从 GitHub 实时获取
  - forks: 45
  - open_issues: 7
  - last_commit: "2026-04-06"
```

**场景3：Webhook 自动触发**

```python
# 不用 MCP（手动触发）
curl -X POST /api/projects/1/analyze

# 使用 MCP（自动触发）
GitHub Webhook → MCP Server → 自动分析
仓库有 push → 触发 webhook → 更新统计
```

<br/>

***

<br/>

## 二、集成 GitHub MCP

### 2.1 安装 MCP SDK

```bash
# 安装 Python MCP SDK
pip install mcp python-dotenv

# 或者使用 poetry
poetry add mcp python-dotenv
```

<br/>

### 2.2 创建 GitHub MCP Server

**创建 `app/mcp/github_server.py`：**

```python
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import requests
from mcp.server import MCPServer
from mcp.types import Tool, Resource

@dataclass
class GitHubRepo:
    """GitHub 仓库信息"""
    id: int
    name: str
    full_name: str
    description: str
    html_url: str
    clone_url: str
    stars: int
    forks: int
    open_issues: int
    language: str
    topics: List[str]
    updated_at: str

class GitHubMCPServer:
    """GitHub MCP 服务器"""
    
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # 创建 MCP Server
        self.server = MCPServer("github")
        self._register_tools()
        self._register_resources()
    
    def _register_tools(self):
        """注册工具"""
        
        @self.server.tool("list_repos")
        async def list_repos(username: Optional[str] = None) -> List[Dict]:
            """
            列出 GitHub 仓库
            
            Args:
                username: GitHub 用户名（默认为当前认证用户）
            
            Returns:
                仓库列表
            """
            if username:
                url = f"{self.base_url}/users/{username}/repos"
            else:
                url = f"{self.base_url}/user/repos"
            
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            repos = []
            for repo in response.json():
                repos.append({
                    "id": repo["id"],
                    "name": repo["name"],
                    "full_name": repo["full_name"],
                    "description": repo["description"] or "",
                    "html_url": repo["html_url"],
                    "clone_url": repo["clone_url"],
                    "stars": repo["stargazers_count"],
                    "forks": repo["forks_count"],
                    "open_issues": repo["open_issues_count"],
                    "language": repo["language"] or "Unknown",
                    "topics": repo.get("topics", []),
                    "updated_at": repo["updated_at"],
                })
            
            return repos
        
        @self.server.tool("get_repo")
        async def get_repo(owner: str, repo: str) -> Dict:
            """
            获取单个仓库详情
            
            Args:
                owner: 仓库所有者
                repo: 仓库名称
            
            Returns:
                仓库详情
            """
            url = f"{self.base_url}/repos/{owner}/{repo}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            return {
                "id": data["id"],
                "name": data["name"],
                "full_name": data["full_name"],
                "description": data["description"] or "",
                "html_url": data["html_url"],
                "clone_url": data["clone_url"],
                "stars": data["stargazers_count"],
                "forks": data["forks_count"],
                "open_issues": data["open_issues_count"],
                "watchers": data["watchers_count"],
                "language": data["language"] or "Unknown",
                "topics": data.get("topics", []),
                "license": data.get("license", {}).get("spdx_id", ""),
                "created_at": data["created_at"],
                "updated_at": data["updated_at"],
                "pushed_at": data["pushed_at"],
                "size": data["size"],
            }
        
        @self.server.tool("get_latest_commit")
        async def get_latest_commit(owner: str, repo: str) -> Dict:
            """
            获取最新提交信息
            
            Args:
                owner: 仓库所有者
                repo: 仓库名称
            
            Returns:
                最新提交信息
            """
            url = f"{self.base_url}/repos/{owner}/{repo}/commits"
            response = requests.get(url, headers=self.headers, params={"per_page": 1})
            response.raise_for_status()
            
            commits = response.json()
            if not commits:
                return {}
            
            commit = commits[0]
            return {
                "sha": commit["sha"],
                "message": commit["commit"]["message"],
                "author": commit["commit"]["author"]["name"],
                "date": commit["commit"]["author"]["date"],
                "html_url": commit["html_url"],
            }
    
    def _register_resources(self):
        """注册资源"""
        
        @self.server.resource("github://repos")
        async def repos_resource() -> List[Dict]:
            """所有仓库资源"""
            return await list_repos()
        
        @self.server.resource("github://repo/{owner}/{repo}")
        async def repo_resource(owner: str, repo: str) -> Dict:
            """单个仓库资源"""
            return await get_repo(owner, repo)
    
    async def start(self):
        """启动 MCP 服务器"""
        await self.server.start()
    
    async def stop(self):
        """停止 MCP 服务器"""
        await self.server.stop()

# 创建全局实例
github_mcp = GitHubMCPServer()
```

<br/>

### 2.3 配置 GitHub Token

**创建 `.env` 文件：**

```bash
# .env
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx

# 获取 Token：
# 1. 访问 https://github.com/settings/tokens
# 2. Generate new token (classic)
# 3. 选择权限：repo, read:user
# 4. 复制 token
```

<br/>

***

<br/>

## 三、扩展数据模型

### 3.1 添加外部服务字段

**更新 `app/models/project.py`：**

```python
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class Project(Base):
    """项目模型"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    path = Column(String(500), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    
    # 统计数据（本地分析）
    total_files = Column(Integer, default=0)
    code_files = Column(Integer, default=0)
    total_lines = Column(Integer, default=0)
    code_lines = Column(Integer, default=0)
    comment_lines = Column(Integer, default=0)
    blank_lines = Column(Integer, default=0)
    language_stats = Column(JSON, default=dict)
    
    # 外部服务信息（MCP 同步）
    github_repo_id = Column(Integer, nullable=True, unique=True)
    github_full_name = Column(String(255), nullable=True)
    github_url = Column(String(500), nullable=True)
    github_stars = Column(Integer, default=0)
    github_forks = Column(Integer, default=0)
    github_open_issues = Column(Integer, default=0)
    github_language = Column(String(50), nullable=True)
    github_last_commit = Column(DateTime, nullable=True)
    
    # 同步状态
    auto_sync = Column(Boolean, default=False)
    last_sync_at = Column(DateTime, nullable=True)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_analyzed_at = Column(DateTime, nullable=True)
    
    # 关联历史记录
    history = relationship("AnalysisHistory", back_populates="project", cascade="all, delete-orphan")
    
    @property
    def is_github_project(self):
        return self.github_repo_id is not None
```

<br/>

### 3.2 更新 Pydantic 模型

**更新 `app/schemas/project.py`：**

```python
from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    path: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectCreateFromGitHub(BaseModel):
    """从 GitHub 创建项目"""
    owner: str = Field(..., description="仓库所有者")
    repo: str = Field(..., description="仓库名称")
    auto_sync: bool = Field(True, description="是否自动同步")
    clone_to: Optional[str] = Field(None, description="克隆到的本地路径")

class ProjectResponse(ProjectBase):
    id: int
    
    # 本地统计
    total_files: int = 0
    code_files: int = 0
    total_lines: int = 0
    code_lines: int = 0
    comment_lines: int = 0
    blank_lines: int = 0
    language_stats: Dict[str, int] = {}
    
    # GitHub 信息
    github_full_name: Optional[str] = None
    github_url: Optional[str] = None
    github_stars: int = 0
    github_forks: int = 0
    github_open_issues: int = 0
    github_language: Optional[str] = None
    is_github_project: bool = False
    
    # 同步状态
    auto_sync: bool = False
    last_sync_at: Optional[datetime] = None
    last_analyzed_at: Optional[datetime] = None
    
    # 时间戳
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class GitHubRepoResponse(BaseModel):
    """GitHub 仓库响应"""
    id: int
    name: str
    full_name: str
    description: str
    html_url: str
    clone_url: str
    stars: int
    forks: int
    open_issues: int
    language: str
    topics: List[str]
    updated_at: str

class SyncResponse(BaseModel):
    """同步响应"""
    project_id: int
    project_name: str
    sync_type: str
    synced_at: datetime
    changes: Dict[str, Any]
```

<br/>

***

<br/>

## 四、GitHub 集成 API

### 4.1 GitHub 仓库 API

**创建 `app/api/github.py`：**

```python
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.project import Project
from ..schemas.project import (
    ProjectCreateFromGitHub,
    ProjectResponse,
    GitHubRepoResponse,
    SyncResponse,
    MessageResponse
)
from ..mcp.github_server import github_mcp

router = APIRouter(prefix="/github", tags=["GitHub"])

@router.get("/repos", response_model=List[GitHubRepoResponse])
async def list_github_repos(
    username: str = Query(None, description="GitHub 用户名（默认为当前用户）")
):
    """
    列出 GitHub 仓库
    
    - **username**: 可选，查看其他用户的公开仓库
    """
    try:
        repos = await github_mcp.server.call_tool("list_repos", {"username": username})
        return repos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取仓库失败: {str(e)}")

@router.get("/repos/{owner}/{repo}", response_model=GitHubRepoResponse)
async def get_github_repo(owner: str, repo: str):
    """
    获取 GitHub 仓库详情
    
    - **owner**: 仓库所有者
    - **repo**: 仓库名称
    """
    try:
        repo_data = await github_mcp.server.call_tool("get_repo", {
            "owner": owner,
            "repo": repo
        })
        return repo_data
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"仓库不存在: {str(e)}")

@router.post("/import", response_model=ProjectResponse, status_code=201)
async def import_from_github(
    project_data: ProjectCreateFromGitHub,
    db: Session = Depends(get_db)
):
    """
    从 GitHub 导入项目
    
    - **owner**: 仓库所有者
    - **repo**: 仓库名称
    - **auto_sync**: 是否自动同步（默认 True）
    - **clone_to**: 克隆到的本地路径（可选）
    """
    try:
        # 获取仓库信息
        repo_info = await github_mcp.server.call_tool("get_repo", {
            "owner": project_data.owner,
            "repo": project_data.repo
        })
        
        # 检查是否已导入
        existing = db.query(Project).filter(
            Project.github_repo_id == repo_info["id"]
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"仓库已导入: {existing.name}"
            )
        
        # 确定本地路径
        local_path = project_data.clone_to or f"/tmp/{repo_info['full_name']}"
        
        # 如果指定了克隆路径，克隆仓库
        if project_data.clone_to:
            import subprocess
            subprocess.run(
                ["git", "clone", repo_info["clone_url"], local_path],
                check=True,
                capture_output=True
            )
        
        # 创建项目
        project = Project(
            name=repo_info["name"],
            path=local_path,
            description=repo_info["description"],
            github_repo_id=repo_info["id"],
            github_full_name=repo_info["full_name"],
            github_url=repo_info["html_url"],
            github_stars=repo_info["stars"],
            github_forks=repo_info["forks"],
            github_open_issues=repo_info["open_issues"],
            github_language=repo_info["language"],
            auto_sync=project_data.auto_sync,
        )
        
        db.add(project)
        db.commit()
        db.refresh(project)
        
        return project
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导入失败: {str(e)}")

@router.post("/sync/{project_id}", response_model=SyncResponse)
async def sync_github_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    同步 GitHub 项目信息
    
    - **project_id**: 项目 ID
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    if not project.is_github_project:
        raise HTTPException(status_code=400, detail="不是 GitHub 项目")
    
    try:
        # 同步仓库信息
        owner, repo = project.github_full_name.split("/")
        repo_info = await github_mcp.server.call_tool("get_repo", {
            "owner": owner,
            "repo": repo
        })
        
        # 获取最新提交
        commit_info = await github_mcp.server.call_tool("get_latest_commit", {
            "owner": owner,
            "repo": repo
        })
        
        # 记录变更
        changes = {}
        if project.github_stars != repo_info["stars"]:
            changes["stars"] = {
                "old": project.github_stars,
                "new": repo_info["stars"]
            }
        
        if project.github_forks != repo_info["forks"]:
            changes["forks"] = {
                "old": project.github_forks,
                "new": repo_info["forks"]
            }
        
        # 更新项目
        project.github_stars = repo_info["stars"]
        project.github_forks = repo_info["forks"]
        project.github_open_issues = repo_info["open_issues"]
        
        from datetime import datetime
        if commit_info:
            project.github_last_commit = datetime.fromisoformat(
                commit_info["date"].replace("Z", "+00:00")
            )
        
        project.last_sync_at = datetime.utcnow()
        
        db.commit()
        db.refresh(project)
        
        return SyncResponse(
            project_id=project.id,
            project_name=project.name,
            sync_type="github",
            synced_at=project.last_sync_at,
            changes=changes
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"同步失败: {str(e)}")

@router.post("/sync-all", response_model=List[SyncResponse])
async def sync_all_github_projects(db: Session = Depends(get_db)):
    """
    同步所有 GitHub 项目
    """
    projects = db.query(Project).filter(
        Project.github_repo_id.isnot(None),
        Project.auto_sync == True
    ).all()
    
    results = []
    for project in projects:
        try:
            result = await sync_github_project(project.id, db)
            results.append(result)
        except Exception as e:
            results.append(SyncResponse(
                project_id=project.id,
                project_name=project.name,
                sync_type="github",
                synced_at=datetime.utcnow(),
                changes={"error": str(e)}
            ))
    
    return results
```

<br/>

***

<br/>

## 五、定时同步任务

### 5.1 创建后台任务

**创建 `app/tasks/sync_tasks.py`：**

```python
import asyncio
from datetime import datetime
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models.project import Project
from ..mcp.github_server import github_mcp

class SyncScheduler:
    """同步调度器"""
    
    def __init__(self):
        self.running = False
        self.interval = 3600  # 1小时
    
    async def start(self):
        """启动定时任务"""
        self.running = True
        print("🔄 同步任务启动")
        
        while self.running:
            try:
                await self.sync_all_projects()
            except Exception as e:
                print(f"❌ 同步失败: {e}")
            
            await asyncio.sleep(self.interval)
    
    def stop(self):
        """停止定时任务"""
        self.running = False
        print("⏸️  同步任务停止")
    
    async def sync_all_projects(self):
        """同步所有项目"""
        print(f"🔄 开始同步: {datetime.now()}")
        
        db = SessionLocal()
        try:
            projects = db.query(Project).filter(
                Project.github_repo_id.isnot(None),
                Project.auto_sync == True
            ).all()
            
            print(f"📊 需要同步 {len(projects)} 个项目")
            
            for project in projects:
                try:
                    await self.sync_project(db, project)
                    print(f"  ✅ {project.name}")
                except Exception as e:
                    print(f"  ❌ {project.name}: {e}")
            
        finally:
            db.close()
    
    async def sync_project(self, db: Session, project: Project):
        """同步单个项目"""
        owner, repo = project.github_full_name.split("/")
        
        # 获取最新信息
        repo_info = await github_mcp.server.call_tool("get_repo", {
            "owner": owner,
            "repo": repo
        })
        
        commit_info = await github_mcp.server.call_tool("get_latest_commit", {
            "owner": owner,
            "repo": repo
        })
        
        # 更新项目
        project.github_stars = repo_info["stars"]
        project.github_forks = repo_info["forks"]
        project.github_open_issues = repo_info["open_issues"]
        
        if commit_info:
            project.github_last_commit = datetime.fromisoformat(
                commit_info["date"].replace("Z", "+00:00")
            )
        
        project.last_sync_at = datetime.utcnow()
        db.commit()

# 全局调度器
sync_scheduler = SyncScheduler()
```

<br/>

### 5.2 在应用中启动任务

**更新 `app/main.py`：**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .config import settings
from .database import engine, Base
from .api import projects, github
from .mcp.github_server import github_mcp
from .tasks.sync_tasks import sync_scheduler

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 生命周期管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时
    await github_mcp.start()
    asyncio.create_task(sync_scheduler.start())
    
    print(f"🚀 {settings.app_name} v{settings.app_version} 启动")
    print(f"📚 API 文档: http://localhost:8000/docs")
    print(f"🔄 GitHub 同步已启动")
    
    yield
    
    # 关闭时
    sync_scheduler.stop()
    await github_mcp.stop()
    print(f"👋 {settings.app_name} 关闭")

# 创建应用
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
    description="""
## CodeStats API

代码统计分析 API 服务（支持 GitHub 集成）

### 功能特性

- ✅ 管理多个项目
- ✅ 代码统计分析
- ✅ GitHub 仓库导入
- ✅ 自动同步仓库信息
- ✅ 项目对比分析

### GitHub 集成

1. 列出仓库：GET /api/github/repos
2. 导入项目：POST /api/github/import
3. 同步信息：POST /api/github/sync/{id}
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
app.include_router(github.router, prefix=settings.api_prefix)

# 健康检查
@app.get("/")
def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "features": ["github_integration", "auto_sync"]
    }

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "mcp": "github_connected",
        "scheduler": "running" if sync_scheduler.running else "stopped"
    }

import asyncio
```

<br/>

***

<br/>

## 六、GitLab 集成（可选）

### 6.1 创建 GitLab MCP Server

**创建 `app/mcp/gitlab_server.py`：**

```python
import os
from typing import List, Dict, Optional
import requests
from mcp.server import MCPServer

class GitLabMCPServer:
    """GitLab MCP 服务器"""
    
    def __init__(self):
        self.token = os.getenv("GITLAB_TOKEN")
        self.base_url = os.getenv("GITLAB_URL", "https://gitlab.com/api/v4")
        self.headers = {"Private-Token": self.token}
        
        self.server = MCPServer("gitlab")
        self._register_tools()
    
    def _register_tools(self):
        """注册工具"""
        
        @self.server.tool("list_projects")
        async def list_projects(
            owned: bool = True,
            search: Optional[str] = None
        ) -> List[Dict]:
            """
            列出 GitLab 项目
            
            Args:
                owned: 只显示自己的项目
                search: 搜索关键词
            
            Returns:
                项目列表
            """
            params = {"owned": owned}
            if search:
                params["search"] = search
            
            url = f"{self.base_url}/projects"
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            projects = []
            for proj in response.json():
                projects.append({
                    "id": proj["id"],
                    "name": proj["name"],
                    "path_with_namespace": proj["path_with_namespace"],
                    "description": proj["description"] or "",
                    "web_url": proj["web_url"],
                    "http_url_to_repo": proj["http_url_to_repo"],
                    "star_count": proj["star_count"],
                    "forks_count": proj["forks_count"],
                    "open_issues_count": proj["open_issues_count"],
                    "topics": proj.get("topics", []),
                })
            
            return projects
        
        @self.server.tool("get_project")
        async def get_project(project_id: int) -> Dict:
            """
            获取项目详情
            
            Args:
                project_id: 项目 ID
            
            Returns:
                项目详情
            """
            url = f"{self.base_url}/projects/{project_id}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            return {
                "id": data["id"],
                "name": data["name"],
                "path_with_namespace": data["path_with_namespace"],
                "description": data["description"] or "",
                "web_url": data["web_url"],
                "http_url_to_repo": data["http_url_to_repo"],
                "star_count": data["star_count"],
                "forks_count": data["forks_count"],
                "open_issues_count": data["open_issues_count"],
                "last_activity_at": data["last_activity_at"],
            }
    
    async def start(self):
        await self.server.start()
    
    async def stop(self):
        await self.server.stop()

gitlab_mcp = GitLabMCPServer()
```

<br/>

***

<br/>

## 七、测试集成

### 7.1 测试 GitHub 集成

```bash
# 1. 启动服务
uvicorn app.main:app --reload

# 2. 列出 GitHub 仓库
curl http://localhost:8000/api/github/repos

# 响应：
# [
#   {
#     "id": 123456,
#     "name": "my-project",
#     "full_name": "user/my-project",
#     "stars": 10,
#     ...
#   }
# ]

# 3. 导入项目
curl -X POST http://localhost:8000/api/github/import \
  -H "Content-Type: application/json" \
  -d '{"owner":"user","repo":"my-project","clone_to":"/tmp/my-project"}'

# 4. 同步项目
curl -X POST http://localhost:8000/api/github/sync/1

# 5. 同步所有项目
curl -X POST http://localhost:8000/api/github/sync-all

# 6. 查看项目（包含 GitHub 信息）
curl http://localhost:8000/api/projects/1
```

<br/>

### 7.2 检查同步状态

```bash
# 查看健康状态
curl http://localhost:8000/health

# 响应：
# {
#   "status": "ok",
#   "mcp": "github_connected",
#   "scheduler": "running"
# }
```

<br/>

***

<br/>

## 八、总结

### 8.1 完成的功能

**MCP 集成：**

```
✅ GitHub API 连接
✅ GitLab API 连接（可选）
✅ 仓库信息同步
✅ 自动发现仓库
✅ 定时同步任务
```

**扩展功能：**

```
✅ 从 GitHub 导入项目
✅ 自动克隆仓库
✅ 实时同步 stars/forks/issues
✅ 后台定时任务
✅ 批量同步
```

<br/>

### 8.2 MCP 的价值

| 功能 | 不用 MCP | 使用 MCP |
|------|---------|----------|
| **数据来源** | 手动输入 | 自动获取 |
| **信息同步** | 静态数据 | 实时更新 |
| **项目发现** | 手动创建 | 自动导入 |
| **触发方式** | 手动触发 | Webhook 自动 |
| **数据完整性** | 只有代码统计 | 包含仓库元数据 |

<br/>

### 8.3 性能优化

**缓存策略：**

```python
# 使用 Redis 缓存 GitHub API 响应
from redis import Redis
import json

redis = Redis()

async def get_cached_repo(owner: str, repo: str):
    cache_key = f"github:repo:{owner}/{repo}"
    cached = redis.get(cache_key)
    
    if cached:
        return json.loads(cached)
    
    repo_data = await github_mcp.server.call_tool("get_repo", {
        "owner": owner,
        "repo": repo
    })
    
    # 缓存 5 分钟
    redis.setex(cache_key, 300, json.dumps(repo_data))
    return repo_data
```

<br/>

### 8.4 下一步改进

**Webhook 集成：**

```
📋 GitHub Webhook 接收器
📋 自动触发分析
📋 实时通知（WebSocket）
```

**更多平台：**

```
📋 Bitbucket 集成
📋 Gitee 集成
📋 自定义 Git 服务器
```

**为下一篇做准备：**

```
🔄 实战04：打包发布
   - Docker 化部署
   - CI/CD 自动化
   - 发布到 PyPI
   - 配置 MCP 环境变量
```

<br/>

***

<br/>

**系列导航**

• 上一篇：实战02：开发 Web API
• 下一篇：实战04：打包发布

<br/>

***

本文是《AI Coding 从入门到精通》系列第18篇  
作者：生活助理 | 发布时间：2026-04-06

**用 MCP 连接世界，让项目自动同步！** 🌐
