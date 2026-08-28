---
name: independent-knowledge-base-publisher
description: Use this skill to design, build, deploy, optimize SEO, format for WeChat, and manage zero-cost independent static knowledge bases using GitHub + Cloudflare Pages + WeChat Official Account publishing + Baidu/Google SEO automation.
---

# 独立知识库全流程建站、SEO 与微信全渠道发布技能
(Independent Knowledge Base Publisher Skill)

本技能沉淀了一套**“0服务器成本、免备案、全球边缘加速、全网SEO秒级收录、微信公众号100%保真排版与拦截极速解封”**的工业级完整 SOP。

---

## 核心架构与 5 大标准工作流 (Five-Stage Workflow)

```
                       ┌─────────────────────────────────────────────────────────┐
                       │      Independent Knowledge Base Publisher Skill         │
                       └─────────────────────────────────────────────────────────┘
                                                    │
     ┌───────────────────┬───────────────────┬──────┴────────────┬───────────────────┐
     ▼                   ▼                   ▼                   ▼                   ▼
【1. 双轨内容编译】  【2. Cloudflare部署】  【3. SEO 收录矩阵】  【4. 微信保真排版】  【5. 微信拦截解封】
 网站版 + 公众号版    Pages+免费SSL证书      百度API+Google地图   OneDark行内代码染色  3分钟站长txt极速验证
```

---

### 第一阶段：双轨内容构建体系 (Dual-Track Content Architecture)

每篇新文章必须同时生成**两套物理隔离的成果物**：
1. **🌐 网站正式版 (`[序号]-[名称].html`)**：
   - 配备交互式架构图、自适应深浅色主题、阅读进度与站内搜索；
   - 由 `build_site_data.py` 和 `export_dist.py` 压缩打包至 `dist/`，发布上线。
2. **📱 微信公众号版 (`[序号]-[名称]-公众号版.html`)**：
   - 存放在草稿/审阅目录，**严禁混入生产打包目录 `dist/`（物理隔离）**；
   - 采用 100% 纯行内 CSS（Pure Inline Styles），供作者在本地浏览器一键 `Cmd + A` ➔ `Cmd + C` 复制到微信后台。

---

### 第二阶段：Cloudflare + GitHub 零成本全球边缘部署

1. **构建与托管规范**：
   - 托管平台：**Cloudflare Pages**（连接 GitHub 仓库，免费计划）；
   - 输出目录：`dist` 或静态根目录；
   - 触发机制：`git push origin main` ➔ 20 秒全网全球 CDN 自动化分发。
2. **域名与 HTTPS 自动化**：
   - 在 Cloudflare 中同时绑定根域名（`domain.com`）与二级域名（`www.domain.com`）；
   - 自动生成并托管永久免费的 SSL/TLS 证书（免去手动申请与年费续期）。

---

### 第三阶段：全网搜索引擎 SEO 与主动推送矩阵

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

### 第四阶段：微信公众号 100% 格式保真与代码染色标准

微信后台编辑器有一套严格的样式清洗过滤规则，必须严格遵循以下铁律：
1. **禁止 Flexbox 与 Gradient**：
   - 布局全部使用 `block`、`inline-block` 或 `table`；
   - 颜色全部采用原生 Hex 纯色（如 `#00897b`、`#f0fdfa`），防止微信清洗导致背景变白。
2. **OneDark 单行染色机制（解决代码不高亮问题）**：
   - 禁止普通 `<pre><code>`，将每一行代码重构为独立的 `<p style="white-space: pre;">`；
   - 关键字 (`#c678dd`)、注释 (`#5c6370`)、字符串 (`#98c379`)、方法 (`#61afef`) 行内染色，复制粘贴 100% 不丢色。
3. **结构化视觉卡片**：
   - 绿色/红色/黄色高亮卡片（`border-left: 4px solid ...; border-radius: 6px;`）；
   - 序号徽章（`01`、`02`）与文末标准吸粉二维码卡片。

---

### 第五阶段：微信域名拦截与 3 分钟站长极速解封 SOP

当境外免备案域名在微信中提示“非微信官方网页或未备案”时：
1. 在微信拦截页面点击【申请恢复访问】➔ 选择【网站管理员认证】；
2. 获取微信给出的专属认证文件名（如 `[token_hash].txt`）与校验码；
3. **在网站根目录及 `dist/` 目录下创建该 txt 文件**，填入校验码；
4. `git commit` 并 `git push origin main`（Cloudflare 20 秒发布完成）；
5. 回到微信点击【我已部署，立即认证】➔ **当场解除拦截，微信内直接秒开**！

---

## 常用工具与自动化脚本

* **目录与元数据生成器**：`python3 build_site_data.py`
* **生产压缩与打包脚本**：`python3 export_dist.py`
* **本地安全审阅服务器**：`python3 server.py`（访问 `http://localhost:8000/review.html`）
