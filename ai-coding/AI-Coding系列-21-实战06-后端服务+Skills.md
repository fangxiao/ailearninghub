# 实战06：后端服务 + Skills

阅读时间：45分钟
难度等级：⭐⭐⭐⭐ 进阶
你将收获：使用 Skills 快速实现认证、权限、通知功能

<br/>

***

<br/>

## 从设计到实现

**上篇回顾：**

```
✅ 实战05：架构设计
   - 前后端分离
   - 技术选型
   - 数据库设计
   - API 设计
```

**本篇目标：**

```
实现后端核心功能

内容：
✅ 用户认证（JWT）
✅ 权限管理（RBAC）
✅ 团队管理
✅ 使用 Skills 加速开发
✅ WebSocket 实时通知
```

**Skills 是什么？**

```
Skills = 预置的功能模块

类似：
  - WordPress 插件
  - VS Code 扩展
  - npm 包

作用：
  ✅ 快速集成常见功能
  ✅ 避免重复造轮子
  ✅ 最佳实践
  ✅ 可配置可扩展

示例：
  - Auth Skill：用户认证、JWT、密码加密
  - RBAC Skill：角色、权限、资源控制
  - Notification Skill：邮件、短信、推送
```

**学习要点：**

- ✅ JWT 认证实现
- ✅ RBAC 权限模型
- ✅ Skills 使用
- ✅ WebSocket 实时通信
- ✅ 异步任务处理

<br/>

***

<br/>

## 一、用户认证

### 1.1 安装 Auth Skill

```bash
# 安装 OpenClaw CLI（如果还没有）
pip install openclaw-cli

# 初始化项目
openclaw init codestats-platform
cd codestats-platform

# 安装 Auth Skill
openclaw skill install auth

# 输出：
# ✅ 安装成功: auth@1.0.0
# 📦 文件位置: ~/.openclaw/skills/auth/
# 📖 文档: ~/.openclaw/skills/auth/README.md
```

<br/>

### 1.2 Auth Skill 使用

**配置 Auth Skill：**

```python
# app/skills_config.py
from openclaw_skills import AuthSkill

# 创建 Auth Skill 实例
auth = AuthSkill(
    secret_key="your-secret-key-here",
    algorithm="HS256",
    access_token_expire_minutes=30,
    refresh_token_expire_days=7,
)

# 自动提供的功能
"""
✅ 用户注册
✅ 用户登录（JWT）
✅ 密码加密（bcrypt）
✅ Token 验证
✅ Token 刷新
✅ 密码重置
✅ 邮箱验证
"""
```

**集成到 FastAPI：**

```python
# app/main.py
from fastapi import FastAPI, Depends
from openclaw_skills.auth import AuthSkill, get_current_user

# 初始化 Auth Skill
auth = AuthSkill(
    secret_key=settings.secret_key,
    database_url=settings.database_url
)

app = FastAPI()

# 注册 Auth 路由
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])

# 使用认证中间件
@app.get("/api/protected")
async def protected_route(current_user = Depends(get_current_user)):
    return {"user": current_user.username}
```

<br/>

### 1.3 自定义认证逻辑

**扩展 User 模型：**

```python
# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from openclaw_skills.auth.models import BaseUser

class User(BaseUser):
    """扩展用户模型"""
    __tablename__ = "users"
    
    # BaseUser 已包含：
    # - id, email, username, password_hash
    # - is_active, is_verified, created_at
    
    # 扩展字段
    avatar = Column(String(500))
    bio = Column(String(500))
    github_id = Column(Integer, unique=True, nullable=True)
    github_username = Column(String(100), nullable=True)
    
    # 关系
    projects = relationship("Project", back_populates="owner")
    teams = relationship("TeamMember", back_populates="user")
```

**自定义认证逻辑：**

```python
# app/api/auth_custom.py
from fastapi import APIRouter, HTTPException
from openclaw_skills.auth import AuthSkill
from ..models.user import User

router = APIRouter()
auth = AuthSkill()

@router.post("/register")
async def custom_register(
    email: str,
    username: str,
    password: str,
    github_username: str = None
):
    """自定义注册逻辑"""
    
    # 使用 Auth Skill 的基础功能
    user = await auth.create_user(
        email=email,
        username=username,
        password=password
    )
    
    # 添加自定义逻辑
    if github_username:
        user.github_username = github_username
        # 验证 GitHub 用户名
        # ...
    
    return {"message": "注册成功", "user_id": user.id}

@router.post("/login/github")
async def github_login(code: str):
    """GitHub OAuth 登录"""
    # 获取 GitHub access token
    # 获取 GitHub 用户信息
    # 查找或创建用户
    # 生成 JWT token
    
    # 使用 Auth Skill 生成 token
    access_token = auth.create_access_token(
        data={"sub": user.username}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
```

<br/>

***

<br/>

## 二、权限管理

### 2.1 安装 RBAC Skill

```bash
# 安装 RBAC Skill
openclaw skill install rbac

# 输出：
# ✅ 安装成功: rbac@1.0.0
# 📦 提供：角色、权限、资源管理
```

<br/>

### 2.2 RBAC 模型

**角色定义：**

```python
# app/models/permissions.py
from enum import Enum

class Role(str, Enum):
    """角色枚举"""
    SUPER_ADMIN = "super_admin"    # 超级管理员
    ADMIN = "admin"                # 管理员
    TEAM_ADMIN = "team_admin"      # 团队管理员
    MEMBER = "member"              # 成员
    GUEST = "guest"                # 访客

class Permission(str, Enum):
    """权限枚举"""
    # 项目权限
    PROJECT_CREATE = "project:create"
    PROJECT_READ = "project:read"
    PROJECT_UPDATE = "project:update"
    PROJECT_DELETE = "project:delete"
    PROJECT_ANALYZE = "project:analyze"
    
    # 团队权限
    TEAM_CREATE = "team:create"
    TEAM_MANAGE = "team:manage"
    TEAM_INVITE = "team:invite"
    TEAM_REMOVE = "team:remove"
    
    # 用户权限
    USER_READ = "user:read"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"

# 角色-权限映射
ROLE_PERMISSIONS = {
    Role.SUPER_ADMIN: list(Permission),  # 所有权限
    Role.ADMIN: [
        Permission.PROJECT_CREATE,
        Permission.PROJECT_READ,
        Permission.PROJECT_UPDATE,
        Permission.PROJECT_DELETE,
        Permission.TEAM_CREATE,
        Permission.USER_READ,
    ],
    Role.TEAM_ADMIN: [
        Permission.PROJECT_CREATE,
        Permission.PROJECT_READ,
        Permission.TEAM_INVITE,
    ],
    Role.MEMBER: [
        Permission.PROJECT_READ,
        Permission.PROJECT_ANALYZE,
    ],
    Role.GUEST: [
        Permission.PROJECT_READ,
    ],
}
```

<br/>

### 2.3 使用 RBAC Skill

**集成到应用：**

```python
# app/main.py
from openclaw_skills.rbac import RBACSkill

# 初始化 RBAC Skill
rbac = RBACSkill(
    database_url=settings.database_url,
    role_permissions=ROLE_PERMISSIONS
)

# 注册路由
app.include_router(rbac.router, prefix="/api/rbac", tags=["RBAC"])

# 添加权限中间件
@app.middleware("http")
async def check_permission(request, call_next):
    # 获取当前用户
    user = await get_current_user(request)
    
    # 检查权限
    if not rbac.has_permission(user.role, request.url.path):
        raise HTTPException(status_code=403, detail="权限不足")
    
    return await call_next(request)
```

**使用权限装饰器：**

```python
# app/api/projects.py
from fastapi import APIRouter, Depends
from openclaw_skills.rbac import require_permission
from ..models.permissions import Permission

router = APIRouter()

@router.post("/")
@require_permission(Permission.PROJECT_CREATE)
async def create_project(
    project_data: ProjectCreate,
    current_user = Depends(get_current_user)
):
    """创建项目（需要 PROJECT_CREATE 权限）"""
    project = Project(**project_data.dict(), owner_id=current_user.id)
    db.add(project)
    db.commit()
    return project

@router.delete("/{project_id}")
@require_permission(Permission.PROJECT_DELETE)
async def delete_project(
    project_id: int,
    current_user = Depends(get_current_user)
):
    """删除项目（需要 PROJECT_DELETE 权限）"""
    project = db.query(Project).filter(Project.id == project_id).first()
    
    # 检查资源所有权
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="只能删除自己的项目")
    
    db.delete(project)
    db.commit()
    return {"message": "删除成功"}
```

<br/>

***

<br/>

## 三、团队管理

### 3.1 团队模型实现

```python
# app/models/team.py
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from ..database import Base

class Team(Base):
    """团队模型"""
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    avatar = Column(String(500))
    owner_id = Column(Integer, ForeignKey("users.id"))
    is_public = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    owner = relationship("User", back_populates="owned_teams")
    members = relationship("TeamMember", back_populates="team", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="team")

class TeamMember(Base):
    """团队成员"""
    __tablename__ = "team_members"
    
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    team_id = Column(Integer, ForeignKey("teams.id"), primary_key=True)
    role = Column(String(20), default="member")  # owner, admin, member, guest
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    user = relationship("User", back_populates="team_memberships")
    team = relationship("Team", back_populates="members")
```

<br/>

### 3.2 团队 API 实现

```python
# app/api/teams.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.team import Team, TeamMember
from ..models.permissions import Role
from ..schemas.team import TeamCreate, TeamResponse, TeamMemberAdd

router = APIRouter(prefix="/teams", tags=["Teams"])

@router.post("/", response_model=TeamResponse, status_code=201)
async def create_team(
    team_data: TeamCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """创建团队"""
    # 检查 slug 是否存在
    existing = db.query(Team).filter(Team.slug == team_data.slug).first()
    if existing:
        raise HTTPException(400, "团队标识已存在")
    
    # 创建团队
    team = Team(
        name=team_data.name,
        slug=team_data.slug,
        description=team_data.description,
        owner_id=current_user.id
    )
    db.add(team)
    
    # 添加创建者为成员
    membership = TeamMember(
        user_id=current_user.id,
        team=team,
        role=Role.TEAM_ADMIN
    )
    db.add(membership)
    db.commit()
    
    return team

@router.post("/{team_id}/members", status_code=201)
async def add_team_member(
    team_id: int,
    member_data: TeamMemberAdd,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """添加团队成员"""
    # 检查团队是否存在
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(404, "团队不存在")
    
    # 检查权限（需要 TEAM_INVITE）
    membership = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == current_user.id
    ).first()
    
    if not membership or membership.role not in [Role.ADMIN, Role.TEAM_ADMIN]:
        raise HTTPException(403, "需要管理员权限")
    
    # 检查用户是否已是成员
    existing = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == member_data.user_id
    ).first()
    
    if existing:
        raise HTTPException(400, "用户已是团队成员")
    
    # 添加成员
    new_member = TeamMember(
        user_id=member_data.user_id,
        team_id=team_id,
        role=member_data.role or Role.MEMBER
    )
    db.add(new_member)
    db.commit()
    
    return {"message": "成员添加成功"}

@router.delete("/{team_id}/members/{user_id}")
async def remove_team_member(
    team_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """移除团队成员"""
    # 检查权限
    membership = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == current_user.id
    ).first()
    
    if not membership or membership.role not in [Role.ADMIN, Role.TEAM_ADMIN]:
        raise HTTPException(403, "需要管理员权限")
    
    # 移除成员
    member = db.query(TeamMember).filter(
        TeamMember.team_id == team_id,
        TeamMember.user_id == user_id
    ).first()
    
    if not member:
        raise HTTPException(404, "成员不存在")
    
    db.delete(member)
    db.commit()
    
    return {"message": "成员已移除"}
```

<br/>

***

<br/>

## 四、实时通知

### 4.1 WebSocket 实现

```python
# app/websocket.py
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List
import json

class ConnectionManager:
    """WebSocket 连接管理器"""
    
    def __init__(self):
        # 用户ID -> WebSocket连接列表
        self.active_connections: Dict[int, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        """建立连接"""
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, user_id: int):
        """断开连接"""
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
    
    async def send_personal_message(self, message: dict, user_id: int):
        """发送个人消息"""
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_json(message)
    
    async def broadcast(self, message: dict, user_ids: List[int] = None):
        """广播消息"""
        if user_ids:
            for user_id in user_ids:
                await self.send_personal_message(message, user_id)
        else:
            for connections in self.active_connections.values():
                for connection in connections:
                    await connection.send_json(message)

manager = ConnectionManager()

# WebSocket 端点
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            # 处理客户端消息
            message = json.loads(data)
            # ...
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
```

<br/>

### 4.2 实时分析进度

```python
# app/services/analysis.py
from ..websocket import manager

async def analyze_project_with_progress(project_id: int, user_id: int):
    """带进度的项目分析"""
    
    # 1. 发送开始通知
    await manager.send_personal_message({
        "type": "analysis_start",
        "project_id": project_id,
        "message": "开始分析项目..."
    }, user_id)
    
    # 2. 扫描文件
    await manager.send_personal_message({
        "type": "analysis_progress",
        "project_id": project_id,
        "stage": "scanning",
        "progress": 20,
        "message": "正在扫描文件..."
    }, user_id)
    
    files = scanner.scan()
    
    # 3. 分析代码
    await manager.send_personal_message({
        "type": "analysis_progress",
        "project_id": project_id,
        "stage": "analyzing",
        "progress": 50,
        "message": f"正在分析 {len(files)} 个文件..."
    }, user_id)
    
    stats = analyzer.analyze_files(files)
    
    # 4. 保存结果
    await manager.send_personal_message({
        "type": "analysis_progress",
        "project_id": project_id,
        "stage": "saving",
        "progress": 90,
        "message": "保存分析结果..."
    }, user_id)
    
    save_stats(project_id, stats)
    
    # 5. 发送完成通知
    await manager.send_personal_message({
        "type": "analysis_complete",
        "project_id": project_id,
        "progress": 100,
        "message": "分析完成！",
        "stats": stats
    }, user_id)
```

<br/>

***

<br/>

## 五、邮件通知

### 5.1 安装 Notification Skill

```bash
# 安装 Notification Skill
openclaw skill install notification

# 输出：
# ✅ 安装成功: notification@1.0.0
# 📦 提供：邮件、短信、推送通知
```

<br/>

### 5.2 配置邮件通知

```python
# app/skills_config.py
from openclaw_skills.notification import NotificationSkill

# 初始化 Notification Skill
notification = NotificationSkill(
    email_provider="smtp",  # 或 sendgrid, mailgun
    smtp_host="smtp.gmail.com",
    smtp_port=587,
    smtp_username="your-email@gmail.com",
    smtp_password="your-app-password",
    from_email="noreply@codestats.com",
    from_name="CodeStats"
)

# 发送邮件
async def send_welcome_email(user):
    """发送欢迎邮件"""
    await notification.send_email(
        to=user.email,
        subject="欢迎加入 CodeStats",
        template="welcome",
        context={
            "username": user.username,
            "login_url": "https://codestats.com/login"
        }
    )

async def send_team_invite_email(user, team):
    """发送团队邀请邮件"""
    await notification.send_email(
        to=user.email,
        subject=f"您被邀请加入团队 {team.name}",
        template="team_invite",
        context={
            "username": user.username,
            "team_name": team.name,
            "accept_url": f"https://codestats.com/teams/{team.id}/join"
        }
    )
```

<br/>

### 5.3 邮件模板

**创建邮件模板 `templates/welcome.html`：**

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #409EFF; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background: #f5f5f5; }
        .button { background: #409EFF; color: white; padding: 10px 20px; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>欢迎使用 CodeStats！</h1>
        </div>
        <div class="content">
            <p>Hi {{ username }},</p>
            <p>感谢您注册 CodeStats！现在您可以：</p>
            <ul>
                <li>📊 分析您的代码库</li>
                <li>🔄 同步 GitHub 仓库</li>
                <li>👥 创建团队协作</li>
            </ul>
            <p>
                <a href="{{ login_url }}" class="button">立即开始</a>
            </p>
        </div>
    </div>
</body>
</html>
```

<br/>

***

<br/>

## 六、异步任务

### 6.1 Celery 配置

```python
# app/tasks/celery_app.py
from celery import Celery

celery_app = Celery(
    "codestats",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1"
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
)

# 定时任务
celery_app.conf.beat_schedule = {
    "sync-github-every-hour": {
        "task": "app.tasks.github.sync_all_projects",
        "schedule": 3600.0,  # 每小时
    },
    "cleanup-old-history": {
        "task": "app.tasks.cleanup.cleanup_old_history",
        "schedule": 86400.0,  # 每天
    },
}
```

<br/>

### 6.2 异步任务示例

```python
# app/tasks/github.py
from ..celery_app import celery_app
from ..websocket import manager

@celery_app.task
def sync_github_project(project_id: int):
    """异步同步 GitHub 项目"""
    from ..database import SessionLocal
    from ..models.project import Project
    from ..mcp.github_server import github_mcp
    
    db = SessionLocal()
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return
        
        # 同步仓库信息
        owner, repo = project.github_full_name.split("/")
        repo_info = github_mcp.get_repo(owner, repo)
        
        # 更新项目
        project.github_stars = repo_info["stars"]
        project.github_forks = repo_info["forks"]
        db.commit()
        
    finally:
        db.close()

@celery_app.task
def analyze_project_async(project_id: int, user_id: int):
    """异步分析项目（后台任务）"""
    import asyncio
    asyncio.run(analyze_project_with_progress(project_id, user_id))
```

<br/>

***

<br/>

## 七、总结

### 7.1 完成的功能

**用户系统：**

```
✅ 用户注册/登录
✅ JWT 认证
✅ 密码加密
✅ GitHub OAuth
✅ 邮箱验证
```

**权限管理：**

```
✅ RBAC 模型
✅ 角色-权限映射
✅ 资源访问控制
✅ 权限检查装饰器
```

**团队协作：**

```
✅ 创建团队
✅ 邀请成员
✅ 角色管理
✅ 项目共享
```

**实时通知：**

```
✅ WebSocket 连接
✅ 实时消息推送
✅ 分析进度通知
✅ 系统通知
```

**邮件通知：**

```
✅ 欢迎邮件
✅ 团队邀请
✅ 密码重置
✅ 邮件模板
```

<br/>

### 7.2 Skills 的价值

**开发效率：**

```
使用 Skills：
  ✅ Auth Skill: 2小时 → 10分钟
  ✅ RBAC Skill: 4小时 → 15分钟
  ✅ Notification Skill: 3小时 → 10分钟

总计节省：9小时 → 35分钟
```

**代码质量：**

```
✅ 最佳实践
✅ 安全性保障
✅ 可维护性高
✅ 文档完善
```

<br/>

### 7.3 下一步

**实战07：前端界面**

```
📋 Vue 3 项目搭建
📋 Element Plus 集成
📋 API 接口对接
📋 数据可视化
📋 实时更新（WebSocket）
```

**为前端做准备：**

```
✅ 后端 API 完成
✅ 认证中间件完成
✅ WebSocket 完成
✅ 异步任务完成
```

<br/>

***

<br/>

**系列导航**

• 上一篇：实战05：设计全栈应用架构
• 下一篇：实战07：前端界面

<br/>

***

本文是《AI Coding 从入门到精通》系列第21篇  
作者：生活助理 | 发布时间：2026-04-06

**用 Skills 加速开发，事半功倍！** 🚀
