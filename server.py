#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 学习智库 · 本地静态与文档服务器 (server.py)
1. 支持 --dist 模式预览打包后的生产目录；
2. 内置路径安全拦截器：拦截任何未公开草稿文件的直接探测访问；
3. 支持 Range 请求（流式传输 85MB PDF）与自动端口探测。
"""

import os
import sys
import socket
import webbrowser
import mimetypes
import fnmatch
import json
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

# Ensure correct MIME types
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('application/json', '.json')
mimetypes.add_type('text/markdown', '.md')
mimetypes.add_type('application/pdf', '.pdf')
mimetypes.add_type('image/svg+xml', '.svg')

def is_blocked_path(path):
    # Check if requesting a hidden draft or config
    clean_p = path.split('?')[0].strip('/')
    fn = os.path.basename(clean_p)

    if clean_p in ['build_site_data.py', 'export_dist.py', 'server.py', 'exclude_config.json', 'Dockerfile', 'docker-compose.yml']:
        return True

    if os.path.exists("exclude_config.json"):
        try:
            with open("exclude_config.json", "r", encoding="utf-8") as f:
                cfg = json.load(f)
                if clean_p in cfg.get("hidden_files", []) or fn in cfg.get("hidden_files", []):
                    return True
                for pat in cfg.get("hidden_patterns", []):
                    if fnmatch.fnmatch(fn, pat) or fnmatch.fnmatch(clean_p, pat):
                        return True
        except Exception:
            pass

    for part in clean_p.split('/'):
        if part.startswith('_') or part.startswith('beta-') or part.startswith('todo-') or (part.startswith('.') and part not in ['.', '']):
            return True
            
    return False

class KnowledgeBaseHandler(SimpleHTTPRequestHandler):
    def do_HEAD(self):
        if is_blocked_path(self.path):
            self.send_error(404, "File not found")
            return
        super().do_HEAD()

    def do_GET(self):
        if is_blocked_path(self.path):
            self.send_error(404, "File not found")
            return
        super().do_GET()

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cache-Control', 'no-cache, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.end_headers()

def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def find_available_port(start_port=8000):
    port = start_port
    while port < start_port + 100:
        if not is_port_in_use(port):
            return port
        port += 1
    return 8000

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if previewing dist/
    if '--dist' in sys.argv or '-d' in sys.argv:
        dist_dir = os.path.join(root_dir, "dist")
        if not os.path.exists(dist_dir):
            print("⚠️ 未找到 dist 目录，正在为你自动执行打包...")
            import subprocess
            subprocess.run([sys.executable, "export_dist.py"], cwd=root_dir)
        os.chdir(dist_dir)
        serving_mode = "📦 生产打包预览模式 (dist/)"
    else:
        os.chdir(root_dir)
        serving_mode = "🛠️ 开发直连模式 (带草稿安全拦截)"

    port = find_available_port(8000)
    server_address = ('', port)
    
    httpd = ThreadingHTTPServer(server_address, KnowledgeBaseHandler)
    local_url = f"http://localhost:{port}"
    lan_ip = get_lan_ip()
    lan_url = f"http://{lan_ip}:{port}"

    print("=" * 65)
    print(" 🚀 AI 全系列学习智库 · 本地服务已启动！")
    print("=" * 65)
    print(f" 模式:             {serving_mode}")
    print(f" 💻 本机访问地址:   {local_url}")
    print(f" 📱 局域网内网访问: {lan_url}")
    print(f" 💬 官方公众号:     大前端工程师")
    print(f" 💡 提示:           按 Ctrl+C 可停止服务")
    print("=" * 65)

    if '--no-browser' not in sys.argv:
        try:
            webbrowser.open(local_url)
        except Exception:
            pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 服务已停止。")
        sys.exit(0)

if __name__ == '__main__':
    main()
