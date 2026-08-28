---
name: quick-site-builder
description: Use this skill to instantly scaffold, build, configure, and deploy zero-cost, high-performance static websites, blogs, and knowledge bases from scratch in under 3 minutes using pure HTML/CSS/JS + Python compiler + Cloudflare Pages + GitHub.
---

# 极速独立建站技能 (Quick Site Builder Skill)

本技能用于在 **3 分钟内从零一键搭建** 一个现代化、高颜值、零服务器成本、免备案的独立知识库/技术专栏/产品官网。

---

## 🚀 核心建站能力与四步极速工作流

```
                    ┌───────────────────────────────────────────────┐
                    │          Quick Site Builder Workflow          │
                    └───────────────────────────────────────────────┘
                                           │
  ┌───────────────────────┬────────────────┴───────┬───────────────────────┐
  ▼                       ▼                        ▼                       ▼
【1. 脚手架一键初始化】  【2. 内容扫描与编译】    【3. 本地预览与审阅】    【4. 全球边缘极速发布】
 生成完整网站核心骨架     自动提取目录与元数据     server.py 零依赖预览    git push ➔ Cloudflare
```

---

### 第一步：一键生成网站骨架 (Scaffold Site)

当用户说 *“帮我新建一个 [某某主题] 的独立知识库/网站”* 时：
1. 自动在目标目录创建标准化轻量项目结构：
   - `index.html`：现代化交互首页 (SPA分类检索/搜索/深浅色主题)；
   - `review.html`：本地双轨审阅控制台；
   - `assets/`：核心样式与脚本 (`app.css`, `app.js`, `data.json`)；
   - `build_site_data.py`：内容索引与元数据自动提取器；
   - `export_dist.py`：生产环境安全打包与压缩器 (自动生成 `sitemap.xml`)；
   - `server.py`：本地极速预览服务器；
   - `docs/`：用户文档与专栏文章分类目录。
2. 注入高质感现代化 UI（Tailwind/原生 CSS，移动端自适应，极速秒开）。

---

### 第二步：自动化内容编译与索引 (Build & Compile)

1. 用户只需把 Markdown 或 HTML 文章丢进专栏目录（如 `docs/tech/`, `docs/guide/`）；
2. 运行 `python3 build_site_data.py`：
   - 自动提取文章标题、摘要、字数、预估阅读时间；
   - 自动生成轻量索引 `data.json` 与 `data.js`；
   - 自动生成全站 `sitemap.xml` 与 `robots.txt`。

---

### 第三步：本地预览与双轨排版 (Preview & Dual-Track)

1. 启动本地开发服务：`python3 server.py` ➔ 打开 `http://localhost:8000`；
2. 打开 `review.html` 审阅控制台：
   - 📖 **网站正式版**：交互图表、暗黑模式、代码高亮；
   - 📱 **公众号专用版**：100% 纯行内 CSS、OneDark 代码高亮、全选即拷。

---

### 第四步：Cloudflare + GitHub 零成本极速上线 (Deploy)

1. 执行生产打包：`python3 export_dist.py` ➔ 生成轻量 `dist/`；
2. 连接 GitHub 仓库 ➔ 绑定 Cloudflare Pages（输出目录填 `dist`）；
3. 绑定独立域名（如 `.top` / `.com`），自动签发免费 HTTPS SSL 证书，全网 20 秒全球 CDN 分发上线！

---

## 🛠️ 快速建站命令示例

只需一条指令即可触发：
- *“帮我新建一个名为【AI产品经理研习社】的独立知识库”*
- *“帮我新建一个名为【个人技术作品集】的静态网站”*
