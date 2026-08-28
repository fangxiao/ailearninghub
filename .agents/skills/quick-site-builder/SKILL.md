---
name: quick-site-builder
description: Use this skill to scaffold, build, compile, preview, deploy, and manage zero-cost independent static websites, blogs, and knowledge bases using pure HTML/CSS/JS + Python compiler + Cloudflare Pages + GitHub + Baidu/Google SEO automation + WeChat webmaster verification.
---

# 极速独立建站与全流程发布技能 (Quick Site Builder & Publisher Skill)

本技能沉淀了一套**“3分钟零成本极速建站、全自动内容编译、Cloudflare全球边缘托管、全网SEO秒级收录与微信生态无缝直连”**的端到端完整工业级工作流。

---

## 🚀 核心架构与 5 大闭环工作流 (End-to-End Workflow)

```
                    ┌─────────────────────────────────────────────────────────┐
                    │          Quick Site Builder & Publisher Skill           │
                    └─────────────────────────────────────────────────────────┘
                                                 │
  ┌───────────────────┬───────────────────┬──────┴────────────┬───────────────────┐
  ▼                   ▼                   ▼                   ▼                   ▼
【1. 脚手架一键初始化】 【2. 双轨内容编译】  【3. Cloudflare部署】 【4. SEO 收录矩阵】  【5. 微信拦截解封】
 现代化SPA首页+编译器   网站版 + 公众号版    Pages+免费SSL证书     百度API+Google地图   3分钟站长txt极速验证
```

---

### 第一阶段：一键生成网站骨架 (Scaffold Site)

当用户说 *“帮我新建一个 [某某主题] 的独立知识库/网站”* 时：
1. 自动在目标目录创建标准化轻量项目结构：
   - `index.html`：极速交互首页（SPA 分类过滤 / 全局模糊搜索 / 深浅色主题切换 / 移动端自适应）；
   - `review.html`：本地双轨审阅台（网站正式版 + 公众号全选即拷版）；
   - `assets/`：核心样式与脚本 (`app.css`, `app.js`, `data.json`)；
   - `build_site_data.py`：内容索引与元数据自动提取器；
   - `export_dist.py`：生产环境安全打包与压缩器 (自动生成 `sitemap.xml`)；
   - `server.py`：本地极速预览服务器；
   - `docs/`：用户文档与专栏文章分类目录。
2. 注入高质感现代化 UI（Tailwind/原生 CSS，移动端自适应，极速秒开）。

---

### 第二阶段：自动化内容编译与双轨排版 (Build & Dual-Track)

1. 用户只需把 Markdown 或 HTML 文章丢进专栏目录（如 `docs/tech/`, `docs/guide/`）；
2. 运行 `python3 build_site_data.py`：
   - 自动提取文章标题、摘要、字数、预估阅读时间；
   - 自动生成轻量索引 `data.json` 与 `data.js`；
   - 自动生成全站 `sitemap.xml` 与 `robots.txt`。
3. 每篇新文章支持**双轨输出**：
   - 🌐 **网站正式版**：交互图表、暗黑模式、SEO 优化；
   - 📱 **公众号专用版**：100% 纯行内 CSS、OneDark 代码高亮、全选即拷（物理隔离不混入 `dist/`）。

---

### 第三阶段：Cloudflare + GitHub 零成本全球边缘托管 (Deploy)

1. **构建与托管规范**：
   - 托管平台：**Cloudflare Pages**（连接 GitHub 仓库，免费计划）；
   - 输出目录：`dist` 或静态根目录；
   - 触发机制：`git push origin main` ➔ 20 秒全网全球 CDN 自动化分发。
2. **域名与 HTTPS 自动化**：
   - 在 Cloudflare 中同时绑定根域名（`domain.com`）与二级域名（`www.domain.com`）；
   - 自动生成并托管永久免费的 SSL/TLS 证书（免去手动申请与年费续期）。

---

### 第四阶段：全网搜索引擎 SEO 与主动推送矩阵 (SEO Matrix)

1. **自动生成全站索引地图**：
   - 运行自动化脚本生成全量 `sitemap.xml`（收录全部分类与独立文章 URL）及 `robots.txt`；
2. **Google & Bing 站长平台**：
   - Google Search Console 提交 `sitemap.xml`；
   - Bing Webmaster Tools 通过 Google 账号一键直接同步导入；
3. **百度搜索资源平台（新站 API 极速推送）**：
   - 针对新站 Sitemap 0 配额问题，使用 Python 脚本调用百度站长 API 批量主动推送种子链接：
   ```python
   import urllib.request
   api = "http://data.zz.baidu.com/urls?site=https://www.yourdomain.top&token=YOUR_TOKEN"
   urls = "\n".join(["https://www.yourdomain.top/", "https://www.yourdomain.top/#roadmap"])
   req = urllib.request.Request(api, data=urls.encode("utf-8"), headers={"Content-Type": "text/plain"})
   print(urllib.request.urlopen(req).read().decode("utf-8"))
   ```

---

### 第五阶段：微信域名拦截与 3 分钟站长极速解封 SOP (WeChat Unblock)

当境外免备案域名在微信中提示“非微信官方网页或未备案”时：
1. 在微信拦截页面点击【申请恢复访问】➔ 选择【网站管理员认证】；
2. 获取微信给出的专属认证文件名（如 `[token_hash].txt`）与校验码；
3. **在网站根目录及 `dist/` 目录下创建该 txt 文件**，填入校验码；
4. `git commit` 并 `git push origin main`（Cloudflare 20 秒发布完成）；
5. 回到微信点击【我已部署，立即认证】➔ **当场解除拦截，微信内直接秒开**！

---

## 🛠️ 常用指令示例

只需在 Claude Code / Antigravity 中发送自然语言：
* *“用 quick-site-builder 帮我在 ./my-docs 目录搭建一个名为【AI 产品经理研习社】的独立网站”*
* *“用 quick-site-builder 帮我重新扫描全站生成 sitemap 并推送到百度 API”*
* *“微信提示需要验证文件 fb59...txt，用 quick-site-builder 帮我完成 20 秒自动化部署解封”*
