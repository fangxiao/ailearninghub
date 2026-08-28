---
name: quick-site-builder
description: Use this skill to scaffold, build, compile, preview, deploy, and manage zero-cost independent static websites, blogs, and knowledge bases using pure HTML/CSS/JS + Python compiler + Cloudflare Pages + GitHub + Baidu/Google SEO automation + WeChat webmaster verification.
---

# 极速独立建站与发布技能 (Quick Site Builder Skill)

本技能用于在 **3 分钟内从零一键搭建、编译并发布** 一个现代化、高颜值、零服务器成本、免备案的独立知识库/技术专栏/产品官网。

---

## 🚀 核心建站闭环与 4 步标准工作流

```
                    ┌───────────────────────────────────────────────┐
                    │          Quick Site Builder Workflow          │
                    └───────────────────────────────────────────────┘
                                           │
  ┌───────────────────────┬────────────────┴───────┬───────────────────────┐
  ▼                       ▼                        ▼                       ▼
【1. 脚手架一键初始化】  【2. 自动化内容编译】    【3. Cloudflare边缘部署】  【4. SEO收录与微信解封】
 现代化SPA首页+编译器    自动提取目录与元数据     Pages+GitHub+免费SSL     百度API+Sitemap+txt验证
```

---

### 第一步：一键生成网站骨架 (Scaffold Site)

当用户说 *“帮我新建一个 [某某主题] 的独立知识库/网站”* 时：
1. 自动在目标目录创建标准化轻量项目结构：
   - `index.html`：极速交互首页（SPA 分类过滤 / 全局模糊搜索 / 深浅色主题切换 / 移动端自适应）；
   - `assets/`：核心样式与脚本 (`app.css`, `app.js`, `data.json`)；
   - `build_site_data.py`：内容索引与元数据自动提取器；
   - `export_dist.py`：生产环境安全打包与压缩器 (自动生成 `sitemap.xml`)；
   - `server.py`：本地极速预览服务器；
   - `docs/`：用户文档与专栏文章分类目录。
2. 注入高质感现代化 UI（Tailwind/原生 CSS，移动端自适应，极速秒开）。

---

### 第二步：自动化内容编译与索引 (Build & Index)

1. 用户只需把 Markdown 或 HTML 文章放入对应专栏目录（如 `docs/tech/`, `docs/guide/`）；
2. 运行 `python3 build_site_data.py`：
   - 自动提取文章标题、摘要、字数、预估阅读时间；
   - 自动生成轻量索引 `data.json` 与 `data.js`；
   - 自动生成全站 `sitemap.xml` 与 `robots.txt`。

---

### 第三步：Cloudflare + GitHub 零成本全球边缘托管 (Deploy)

1. **构建与托管规范**：
   - 托管平台：**Cloudflare Pages**（连接 GitHub 仓库，免费计划）；
   - 输出目录：`dist` 或静态根目录；
   - 触发机制：`git push origin main` ➔ 20 秒全网全球 CDN 自动化分发。
2. **域名与 HTTPS 自动化**：
   - 在 Cloudflare 中同时绑定根域名（`domain.com`）与二级域名（`www.domain.com`）；
   - 自动生成并托管永久免费的 SSL/TLS 证书（免去手动申请与年费续期）。

---

### 第四步：全网 SEO 主动推送与微信解封 (SEO & Webmaster Verify)

1. **全网搜索引擎 SEO 矩阵**：
   - Google Search Console 提交 `sitemap.xml`；
   - Bing Webmaster Tools 通过 Google 账号一键直接同步导入；
   - 使用 5 行 Python 脚本调用百度站长 API 批量主动推送种子链接（突破新站 0 配额）。
2. **微信拦截 3 分钟极速解封 SOP**：
   - 当境外免备案域名在微信中提示未备案时，在根目录及 `dist/` 创建管理员 `[token_hash].txt` 文件；
   - 推送部署生效后，在微信点击【立即认证】当场秒级恢复正常访问。

---

## 🛠️ 常用指令示例

只需在 Claude Code / Antigravity 中发送自然语言：
* *“用 quick-site-builder 帮我在 ./my-docs 目录搭建一个名为【AI 产品经理实战智库】的独立网站”*
* *“用 quick-site-builder 帮我重新扫描全站生成 sitemap 并推送到百度 API”*
* *“微信提示需要验证文件 fb59...txt，用 quick-site-builder 帮我完成 20 秒自动化部署解封”*
