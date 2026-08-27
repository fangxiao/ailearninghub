# 实战05：设计全栈应用架构

阅读时间：40分钟
难度等级：⭐⭐⭐⭐ 进阶
你将收获：前后端分离架构、技术选型、系统设计

<br/>

***

<br/>

## 从服务到平台

**之前完成：**

```
✅ 实战01-04：单机版 codestats
   - CLI 工具
   - Web API
   - MCP 集成
   - Docker 部署

核心功能：
   - 代码统计
   - GitHub 同步
   - 项目管理
```

**当前限制：**

```
❌ 单用户设计
   没有用户系统，无法区分不同用户

❌ 缺少前端
   只有 API，需要用 curl 测试

❌ 功能简单
   只能统计和同步，缺少协作功能

❌ 无法扩展
   架构设计不支持团队使用
```

**平台化需求：**

```
✅ 多用户系统
   - 注册/登录
   - 个人项目
   - 团队协作

✅ 完整前端
   - Vue 3 界面
   - 数据可视化
   - 实时更新

✅ 高级功能
   - 项目分组
   - 标签管理
   - 数据导出

✅ 可扩展架构
   - 微服务准备
   - 插件系统
```

**本篇目标：**

```
设计 codestats 平台架构

内容：
✅ 架构演进路线
✅ 技术栈选型
✅ 数据库设计
✅ API 设计
✅ 前端设计
✅ 部署架构
```

**学习要点：**

- ✅ 架构设计思维
- ✅ 技术选型决策
- ✅ 数据库设计
- ✅ 前后端分离
- ✅ 可扩展性设计

<br/>

***

<br/>

## 一、架构演进

### 1.1 三个阶段

**阶段1：单机版（已完成）**

```
架构：
  CLI → 本地文件
  API → SQLite

特点：
  ✅ 快速开发
  ✅ 简单部署
  ❌ 单用户
  ❌ 无前端
```

**阶段2：团队版（本篇设计）**

```
架构：
  前端 (Vue) → 后端 (FastAPI) → PostgreSQL
                      ↓
                   MCP (GitHub/GitLab)

特点：
  ✅ 多用户
  ✅ 前端界面
  ✅ 团队协作
  ✅ 数据持久化
```

**阶段3：企业版（未来）**

```
架构：
  前端 → API 网关 → 微服务集群
                    ├─ 用户服务
                    ├─ 项目服务
                    ├─ 分析服务
                    └─ 通知服务

特点：
  ✅ 高可用
  ✅ 可扩展
  ✅ 企业级
```

<br/>

### 1.2 本次设计范围

**包含功能：**

```
用户管理
  - 注册/登录
  - 个人信息
  - 密码重置

项目管理
  - 创建项目
  - GitHub 导入
  - 项目分组
  - 标签管理

统计分析
  - 代码统计
  - 历史趋势
  - 项目对比
  - 数据导出

团队协作
  - 创建团队
  - 邀请成员
  - 权限管理
  - 项目共享

数据可视化
  - 仪表盘
  - 图表展示
  - 实时更新
```

<br/>

***

<br/>

## 二、技术栈选型

### 2.1 前端技术栈

**框架选择：Vue 3**

```
为什么选 Vue 3？

优点：
  ✅ 组合式 API（逻辑复用）
  ✅ TypeScript 支持好
  ✅ 性能优秀
  ✅ 生态成熟（Element Plus）
  ✅ 学习曲线平缓

对比 React：
  React: 更灵活，但需要更多配置
  Vue 3: 开箱即用，适合快速开发

对比 Angular：
  Angular: 更完整，但更重
  Vue 3: 轻量级，够用即可
```

**UI 库：Element Plus**

```
为什么选 Element Plus？

优点：
  ✅ 组件丰富（80+）
  ✅ Vue 3 原生支持
  ✅ 文档完善
  ✅ 社区活跃
  ✅ 设计统一

包含组件：
  - 表单、表格、图表
  - 导航、布局、对话框
  - 通知、加载、动画
```

**其他工具：**

```
状态管理：Pinia
  - Vue 3 官方推荐
  - TypeScript 友好
  - DevTools 支持

路由：Vue Router 4
  - 官方路由
  - 支持嵌套路由
  - 路由守卫

HTTP：Axios
  - 拦截器
  - 请求取消
  - 自动转换

图表：ECharts
  - 功能强大
  - 配置灵活
  - 性能优秀

构建：Vite
  - 快速启动
  - HMR 热更新
  - 生产优化
```

<br/>

### 2.2 后端技术栈

**保持现有技术栈，增加：**

```
认证：JWT
  - 无状态认证
  - 跨域支持
  - 安全可靠

权限：RBAC
  - 角色管理
  - 权限控制
  - 资源保护

缓存：Redis
  - Session 存储
  - API 缓存
  - 频率限制

队列：Celery
  - 异步任务
  - 定时任务
  - 任务监控

搜索：Elasticsearch（可选）
  - 全文搜索
  - 项目搜索
  - 日志分析
```

<br/>

### 2.3 数据库选择

**PostgreSQL vs MySQL**

```
选择：PostgreSQL

理由：
  ✅ JSON 支持更好（存储 language_stats）
  ✅ 全文搜索内置
  ✅ 扩展性强
  ✅ 开源免费
  ✅ 社区活跃

MySQL:
  - 更流行
  - 性能稍好
  - 但功能不如 PG 丰富
```

<br/>

***

<br/>

## 三、数据库设计

### 3.1 ER 图

```
┌─────────────┐       ┌──────────────┐
│   User      │       │    Team      │
├─────────────┤       ├──────────────┤
│ id          │       │ id           │
│ email       │       │ name         │
│ username    │       │ description  │
│ password    │       │ owner_id     │
│ avatar      │──┐    │ created_at   │
│ created_at  │  │    └──────┬───────┘
└──────┬──────┘  │           │
       │         │           │
       │    ┌────▼───────────▼─────┐
       │    │   team_members       │
       │    ├──────────────────────┤
       │    │ user_id              │
       │    │ team_id              │
       │    │ role                 │
       │    └──────────────────────┘
       │
       │    ┌──────────────────┐
       └────►   Project        │
            ├──────────────────┤
            │ id               │
            │ name             │
            │ path             │
            │ owner_id         │
            │ team_id          │
            │ group_id         │
            │ is_public        │
            │ github_repo_id   │
            │ stats...         │
            │ created_at       │
            └──────┬───────────┘
                   │
       ┌───────────▼────────┐
       │   ProjectTag       │
       ├────────────────────┤
       │ project_id         │
       │ tag_id             │
       └────────────────────┘
                   │
       ┌───────────▼────────┐
       │   Tag              │
       ├────────────────────┤
       │ id                 │
       │ name               │
       │ color              │
       │ user_id            │
       └────────────────────┘
```

<br/>

### 3.2 数据表设计

**用户表（users）：**

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    avatar VARCHAR(500),
    bio TEXT,
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
```

**团队表（teams）：**

```sql
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    avatar VARCHAR(500),
    owner_id INTEGER REFERENCES users(id),
    is_public BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_teams_slug ON teams(slug);
CREATE INDEX idx_teams_owner ON teams(owner_id);
```

**团队成员表（team_members）：**

```sql
CREATE TYPE team_role AS ENUM ('owner', 'admin', 'member', 'guest');

CREATE TABLE team_members (
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    team_id INTEGER REFERENCES teams(id) ON DELETE CASCADE,
    role team_role DEFAULT 'member',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, team_id)
);
```

**项目表（projects）：**

```sql
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    path VARCHAR(500),
    description TEXT,
    
    -- 所有者
    owner_id INTEGER REFERENCES users(id),
    team_id INTEGER REFERENCES teams(id),
    group_id INTEGER REFERENCES project_groups(id),
    
    -- 访问控制
    is_public BOOLEAN DEFAULT false,
    
    -- 统计数据
    total_files INTEGER DEFAULT 0,
    code_files INTEGER DEFAULT 0,
    total_lines INTEGER DEFAULT 0,
    code_lines INTEGER DEFAULT 0,
    comment_lines INTEGER DEFAULT 0,
    blank_lines INTEGER DEFAULT 0,
    language_stats JSONB DEFAULT '{}',
    
    -- GitHub 信息
    github_repo_id INTEGER UNIQUE,
    github_full_name VARCHAR(255),
    github_url VARCHAR(500),
    github_stars INTEGER DEFAULT 0,
    github_forks INTEGER DEFAULT 0,
    github_open_issues INTEGER DEFAULT 0,
    github_language VARCHAR(50),
    github_last_commit TIMESTAMP,
    
    -- 同步状态
    auto_sync BOOLEAN DEFAULT false,
    last_sync_at TIMESTAMP,
    last_analyzed_at TIMESTAMP,
    
    -- 时间戳
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- 唯一约束
    UNIQUE(owner_id, slug),
    UNIQUE(team_id, slug)
);

CREATE INDEX idx_projects_owner ON projects(owner_id);
CREATE INDEX idx_projects_team ON projects(team_id);
CREATE INDEX idx_projects_github ON projects(github_repo_id);
CREATE INDEX idx_projects_public ON projects(is_public);
```

**标签表（tags）：**

```sql
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    slug VARCHAR(50) NOT NULL,
    color VARCHAR(7) DEFAULT '#409EFF',
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, slug)
);

-- 项目-标签关联表
CREATE TABLE project_tags (
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (project_id, tag_id)
);
```

**分析历史表（analysis_history）：**

```sql
CREATE TABLE analysis_history (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    
    total_files INTEGER DEFAULT 0,
    code_files INTEGER DEFAULT 0,
    total_lines INTEGER DEFAULT 0,
    code_lines INTEGER DEFAULT 0,
    comment_lines INTEGER DEFAULT 0,
    blank_lines INTEGER DEFAULT 0,
    language_stats JSONB DEFAULT '{}',
    
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_history_project ON analysis_history(project_id);
CREATE INDEX idx_history_time ON analysis_history(analyzed_at DESC);
```

<br/>

***

<br/>

## 四、API 设计

### 4.1 RESTful API 规范

**URL 设计：**

```
资源命名：
  ✅ 复数形式：/api/users, /api/projects
  ✅ 嵌套资源：/api/projects/{id}/stats
  ✅ 过滤参数：/api/projects?tag=python&sort=stars

HTTP 方法：
  GET    - 获取资源
  POST   - 创建资源
  PATCH  - 部分更新
  PUT    - 完整更新（少用）
  DELETE - 删除资源
```

**响应格式：**

```json
// 成功响应
{
  "data": { ... },
  "message": "操作成功"
}

// 列表响应
{
  "data": [ ... ],
  "total": 100,
  "page": 1,
  "page_size": 20
}

// 错误响应
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "验证失败",
    "details": {
      "email": ["邮箱格式不正确"]
    }
  }
}
```

<br/>

### 4.2 API 端点设计

**认证相关：**

```
POST   /api/auth/register        # 注册
POST   /api/auth/login           # 登录
POST   /api/auth/logout          # 登出
POST   /api/auth/refresh         # 刷新 token
POST   /api/auth/forgot-password # 忘记密码
POST   /api/auth/reset-password  # 重置密码
GET    /api/auth/me              # 当前用户信息
PATCH  /api/auth/me              # 更新个人信息
```

**项目管理：**

```
GET    /api/projects                 # 项目列表
POST   /api/projects                 # 创建项目
GET    /api/projects/{id}            # 项目详情
PATCH  /api/projects/{id}            # 更新项目
DELETE /api/projects/{id}            # 删除项目
POST   /api/projects/{id}/analyze    # 分析项目
GET    /api/projects/{id}/history    # 历史记录
GET    /api/projects/{id}/stats      # 统计数据
POST   /api/projects/{id}/tags       # 添加标签
DELETE /api/projects/{id}/tags/{tag} # 移除标签
```

**GitHub 集成：**

```
GET    /api/github/repos             # GitHub 仓库列表
POST   /api/github/import            # 导入仓库
POST   /api/github/sync/{id}         # 同步项目
POST   /api/github/sync-all          # 同步所有
```

**团队管理：**

```
GET    /api/teams                    # 团队列表
POST   /api/teams                    # 创建团队
GET    /api/teams/{id}               # 团队详情
PATCH  /api/teams/{id}               # 更新团队
DELETE /api/teams/{id}               # 删除团队
POST   /api/teams/{id}/members       # 邀请成员
DELETE /api/teams/{id}/members/{uid} # 移除成员
PATCH  /api/teams/{id}/members/{uid} # 更新角色
```

**统计对比：**

```
POST   /api/stats/compare            # 项目对比
GET    /api/stats/trends             # 趋势分析
GET    /api/stats/languages          # 语言统计
POST   /api/stats/export             # 导出报告
```

<br/>

***

<br/>

## 五、前端架构

### 5.1 目录结构

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── main.ts                 # 入口文件
│   ├── App.vue                 # 根组件
│   ├── router/                 # 路由配置
│   │   ├── index.ts
│   │   └── routes.ts
│   ├── store/                  # 状态管理
│   │   ├── index.ts
│   │   ├── modules/
│   │   │   ├── auth.ts
│   │   │   ├── project.ts
│   │   │   └── team.ts
│   ├── views/                  # 页面组件
│   │   ├── auth/
│   │   │   ├── Login.vue
│   │   │   └── Register.vue
│   │   ├── dashboard/
│   │   │   └── Dashboard.vue
│   │   ├── projects/
│   │   │   ├── ProjectList.vue
│   │   │   ├── ProjectDetail.vue
│   │   │   └── ProjectCreate.vue
│   │   └── teams/
│   │       ├── TeamList.vue
│   │       └── TeamDetail.vue
│   ├── components/             # 通用组件
│   │   ├── common/
│   │   │   ├── Navbar.vue
│   │   │   └── Footer.vue
│   │   ├── project/
│   │   │   ├── ProjectCard.vue
│   │   │   └── StatsChart.vue
│   │   └── stats/
│   │       ├── LanguagePie.vue
│   │       └── TrendLine.vue
│   ├── api/                    # API 接口
│   │   ├── request.ts          # Axios 配置
│   │   ├── auth.ts
│   │   ├── project.ts
│   │   └── team.ts
│   ├── composables/            # 组合式函数
│   │   ├── useAuth.ts
│   │   └── useProject.ts
│   ├── utils/                  # 工具函数
│   │   ├── format.ts
│   │   └── storage.ts
│   └── styles/                 # 样式文件
│       ├── main.scss
│       └── variables.scss
├── .env
├── vite.config.ts
├── tsconfig.json
└── package.json
```

<br/>

### 5.2 页面流程

```
用户访问
  │
  ├─ 未登录 → 登录页
  │            ├─ 登录成功 → 仪表盘
  │            └─ 注册 → 登录页
  │
  └─ 已登录 → 仪表盘
              ├─ 项目列表
              │   ├─ 查看项目
              │   ├─ 创建项目
              │   ├─ GitHub 导入
              │   └─ 分析项目
              │
              ├─ 团队管理
              │   ├─ 我的团队
              │   ├─ 创建团队
              │   └─ 邀请成员
              │
              └─ 个人设置
                  ├─ 个人信息
                  ├─ 修改密码
                  └─ API Token
```

<br/>

***

<br/>

## 六、部署架构

### 6.1 生产环境架构

```
┌─────────────────────────────────────────┐
│           CDN (静态资源)                 │
│      CSS/JS/Images/Fonts                │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│        Nginx (反向代理 + HTTPS)          │
│   - SSL 终结                             │
│   - Gzip 压缩                            │
│   - 静态文件服务                         │
└────────┬───────────────────┬────────────┘
         │                   │
    ┌────▼─────┐       ┌────▼──────┐
    │  前端     │       │  后端 API  │
    │  (静态)   │       │  (Uvicorn) │
    └──────────┘       └─────┬──────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   ┌────▼─────┐        ┌─────▼──────┐      ┌────▼─────┐
   │PostgreSQL│        │   Redis    │      │ Celery   │
   │ (主数据库)│        │  (缓存)    │      │(异步任务)│
   └──────────┘        └────────────┘      └────┬─────┘
                                                  │
                                             ┌────▼─────┐
                                             │  MCP     │
                                             │(外部服务)│
                                             └──────────┘
```

<br/>

### 6.2 扩展性设计

**水平扩展：**

```yaml
# docker-compose.scale.yml
version: '3.8'

services:
  api:
    deploy:
      replicas: 3  # 3个API实例
    environment:
      - DATABASE_URL=postgresql://...
    
  nginx:
    volumes:
      - ./nginx-loadbalance.conf:/etc/nginx/nginx.conf
```

**负载均衡配置：**

```nginx
# nginx-loadbalance.conf
upstream api_servers {
    least_conn;
    server api-1:8000;
    server api-2:8000;
    server api-3:8000;
}

server {
    listen 80;
    
    location /api/ {
        proxy_pass http://api_servers;
        proxy_set_header Host $host;
    }
}
```

<br/>

***

<br/>

## 七、总结

### 7.1 架构设计原则

**简单优先：**

```
✅ 不过度设计
✅ 选择成熟技术
✅ 优先解决问题
✅ 逐步演进
```

**可扩展性：**

```
✅ 模块化设计
✅ 接口抽象
✅ 配置外置
✅ 无状态服务
```

**可维护性：**

```
✅ 代码规范
✅ 文档完善
✅ 测试覆盖
✅ 日志完善
```

<br/>

### 7.2 技术栈总结

**前端：**

```
Vue 3 + TypeScript + Vite
Element Plus + ECharts
Pinia + Vue Router
Axios
```

**后端：**

```
FastAPI + SQLAlchemy
PostgreSQL + Redis
JWT + RBAC
Celery
```

**部署：**

```
Docker + Nginx
GitHub Actions
Let's Encrypt
```

<br/>

### 7.3 下一步

**实战06：后端服务 + Skills**

```
📋 实现用户认证
📋 实现团队管理
📋 使用 Skills 加速开发
   - Auth Skill（认证）
   - RBAC Skill（权限）
   - Notification Skill（通知）
```

**为前端做准备：**

```
📋 完整的 API
📋 认证中间件
📋 WebSocket 支持
📋 文件上传
```

<br/>

***

<br/>

**系列导航**

• 上一篇：实战04：打包发布
• 下一篇：实战06：后端服务 + Skills

<br/>

***

本文是《AI Coding 从入门到精通》系列第20篇  
作者：生活助理 | 发布时间：2026-04-06

**好的架构是成功的一半！** 🏗️
