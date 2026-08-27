# 基础镜像使用超轻量 Nginx Alpine
FROM nginx:alpine

# 复制自定义 Nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 复制已打包的站点静态文件
COPY dist/ /usr/share/nginx/html/

# 暴露 80 端口（微信云托管默认监听端口）
EXPOSE 80

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]
