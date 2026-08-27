# 🚀 AI 全系列学习智库 · 部署与发布指南

本网站为纯静态、高性能架构，零构建依赖，可直接部署在任意公网服务器或企业内网环境中。

---

## 📱 微信公众号信息与二维码替换

网站已经全方位集成了 **微信公众号【大前端工程师】** 的品牌展示：
- 顶部导航栏专属公众号入口
- Banner 显眼提示徽章与弹窗关注
- 页脚专属公众号介绍卡片与一键复制名称
- 浮层高清二维码弹窗（支持一键复制「大前端工程师」）

### 如何放入你真实的微信公众号二维码：
只需将你的公众号二维码图片保存并覆盖到：
```bash
/assets/qrcode.png
```
（或者 `assets/qrcode.jpg`）即可！网站会自动优先加载真实二维码图片，未放置时会自动展示优雅的 SVG 占位图标。

---

## 一、发布到公网（互联网访问）

### 方案 1：Vercel / Cloudflare Pages / Netlify（免费且极速，推荐）
1. 将当前项目推送到 GitHub / GitLab 仓库。
2. 登录 [Vercel](https://vercel.com) 或 [Cloudflare Pages](https://pages.cloudflare.com/)。
3. 点击 **Import Project**，选择该仓库。
4. 保持默认配置（无需构建命令，Framework 选 Other），点击 **Deploy**。
5. 30 秒内即可获得全球 CDN 加速的公网访问域名（支持自定义域名和免费 HTTPS）。
> 项目已内置 `vercel.json`，自动优化了字体、大文件 PDF 流式缓存和跨域头。

### 方案 2：自建云服务器（Nginx）
在 Linux 服务器（如腾讯云 / 阿里云）上执行：
```bash
# 1. 安装 Nginx
sudo apt update && sudo apt install -y nginx

# 2. 将当前目录内容上传至 /var/www/ai-hub
# 3. 将项目中的 nginx.conf 复制到 /etc/nginx/conf.d/ai-hub.conf
sudo cp nginx.conf /etc/nginx/conf.d/ai-hub.conf

# 4. 修改 root 路径为 /var/www/ai-hub 并重启 Nginx
sudo nginx -t && sudo systemctl reload nginx
```

---

## 二、发布到公司内网（局域网 / 私有部署）

### 方案 1：Docker 一键容器化部署（最简单、最稳健）
内网服务器只需安装 Docker，进入本目录后执行：
```bash
# 启动容器
docker compose up -d --build
```
启动后，内网同事即可通过 `http://<服务器内网IP>:8088` 极速访问！

### 方案 2：内网局域网共享预览（开发机直接共享）
在本机运行：
```bash
python3 server.py
```
终端会输出当前局域网 IP，同一 Wi-Fi 或局域网下的同事直接访问 `http://<你的电脑局域网IP>:8000` 即可共同阅读。

---

## 三、文档数据同步与自动更新

如果后续在知识库中添加了新的 HTML 或 Markdown 文档，只需运行：
```bash
python3 build_site_data.py
```
脚本会自动扫描所有目录、提取文章元数据并更新 `assets/data.json` 和 `assets/data.js`。
