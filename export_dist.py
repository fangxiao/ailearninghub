#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 学习智库 · 生产环境安全打包与导出脚本 (export_dist.py)
1. 严格根据 exclude_config.json 过滤全部草稿和未成熟资料；
2. 仅将正式发布的文档、图片与前端资源复制到 dist/ 目录；
3. 草稿和未公开文件物理隔离，完全无法通过 URL 路径探测；
4. 可选自动生成 zip 压缩包供一键上传。
"""

import os
import shutil
import zipfile
import fnmatch
import json
import re
import subprocess

DIST_DIR = "dist"
EXCLUDE_CONFIG_PATH = "exclude_config.json"

def minify_css_content(css_str):
    """Minify CSS using esbuild with pure-python fallback"""
    try:
        proc = subprocess.run(
            ["npx", "--yes", "esbuild", "--loader=css", "--minify"],
            input=css_str.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return proc.stdout.decode('utf-8').strip()
    except Exception:
        pass
        
    # High-efficiency Python Fallback
    css = re.sub(r'/\*[\s\S]*?\*/', '', css_str)
    css = re.sub(r'\s+', ' ', css)
    css = re.sub(r'\s*([\{\}\:\;\,\>\+\~\(\)])\s*', r'\1', css)
    css = re.sub(r';\}', '}', css)
    return css.strip()

def minify_js_content(js_str):
    """Minify JavaScript using esbuild with syntax-safe python tokenizer fallback"""
    try:
        proc = subprocess.run(
            ["npx", "--yes", "esbuild", "--loader=js", "--minify"],
            input=js_str.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return proc.stdout.decode('utf-8').strip()
    except Exception:
        pass

    # Tokenizer-based Python Fallback preserving strings & template literals
    res = []
    i = 0
    n = len(js_str)
    in_str = None
    
    while i < n:
        c = js_str[i]
        if in_str:
            res.append(c)
            if c == '\\':
                if i + 1 < n:
                    res.append(js_str[i+1])
                    i += 2
                    continue
            elif c == in_str:
                in_str = None
            i += 1
            continue
            
        if c in ('"', "'", '`'):
            in_str = c
            res.append(c)
            i += 1
            continue
            
        if c == '/' and i + 1 < n:
            if js_str[i+1] == '/':
                end = js_str.find('\n', i)
                if end == -1: break
                i = end + 1
                res.append('\n')
                continue
            elif js_str[i+1] == '*':
                end = js_str.find('*/', i + 2)
                if end == -1: break
                i = end + 2
                continue
                
        res.append(c)
        i += 1
        
    code = ''.join(res)
    lines = [l.strip() for l in code.splitlines() if l.strip()]
    return '\n'.join(lines)

def minify_html_content(html_str):
    """Minify HTML structure by removing comments and trimming space"""
    html = re.sub(r'<!--(?!\s*(?:\[if [^\]]+]|<!|>))(?:(?!-->)[\s\S])*-->', '', html_str)
    return html.strip()

def load_exclude_config():
    config = {
        "hidden_categories": [],
        "hidden_files": [],
        "hidden_patterns": ["*draft*", "*草稿*", "*wip*", "*temp*", "_*"],
        "coming_soon_articles": []
    }
    if os.path.exists(EXCLUDE_CONFIG_PATH):
        try:
            with open(EXCLUDE_CONFIG_PATH, "r", encoding="utf-8") as f:
                config.update(json.load(f))
        except Exception as e:
            print(f"⚠️ 读取 {EXCLUDE_CONFIG_PATH} 失败: {e}")
    return config

def should_exclude_file(rel_path, config):
    fn = os.path.basename(rel_path)
    
    # 1. Exact match
    if rel_path in config.get("hidden_files", []) or fn in config.get("hidden_files", []):
        return True
        
    # 2. Pattern match
    for pattern in config.get("hidden_patterns", []):
        if fnmatch.fnmatch(fn, pattern) or fnmatch.fnmatch(rel_path, pattern):
            return True
            
    # 3. Path parts with _, ., beta-, todo-
    for part in rel_path.split("/"):
        if part.startswith("_") or part.startswith("beta-") or part.startswith("todo-") or (part.startswith(".") and part != "."):
            return True
            
    return False

def clean_html(raw_html):
    if not raw_html:
        return ""
    cleanr = re.compile(r"<.*?>")
    cleantext = re.sub(cleanr, "", raw_html)
    return " ".join(cleantext.split()).strip()

def format_size(bytes_size):
    if bytes_size < 1024:
        return f"{bytes_size} B"
    elif bytes_size < 1024 * 1024:
        return f"{bytes_size / 1024:.1f} KB"
    else:
        return f"{bytes_size / (1024 * 1024):.1f} MB"

def extract_meta(fp):
    ext = os.path.splitext(fp)[1].lower()
    fn = os.path.basename(fp)
    size = os.path.getsize(fp)
    title = fn
    subtitle = ""
    summary = ""
    toc = []
    
    if ext == '.html':
        try:
            with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                tm = re.search(r'<title>(.*?)</title>', content, re.I | re.S)
                if tm and tm.group(1).strip():
                    title = clean_html(tm.group(1))
                else:
                    h1m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.I | re.S)
                    if h1m:
                        title = clean_html(h1m.group(1))
                
                h2s = re.findall(r'<h[23][^>]*>(.*?)</h[23]>', content, re.I | re.S)
                clean_h2s = [clean_html(h) for h in h2s if clean_html(h)]
                if clean_h2s:
                    subtitle = " · ".join(clean_h2s[:2])
                    toc = clean_h2s[:12]
                
                ps = re.findall(r'<p[^>]*>(.*?)</p>', content, re.I | re.S)
                good_ps = [clean_html(p) for p in ps if len(clean_html(p)) > 20 and not clean_html(p).startswith('©') and 'function' not in clean_html(p)]
                if good_ps:
                    summary = good_ps[0][:160] + ("..." if len(good_ps[0]) > 160 else "")
                
                text_len = len(clean_html(content))
                mins = max(2, round(text_len / 450))
                read_time = f"{mins} 分钟"
        except Exception:
            pass
            
    elif ext == '.md':
        try:
            with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.splitlines()
                for l in lines:
                    l_str = l.strip()
                    if l_str.startswith('# ') and (not title or title == fn):
                        title = l_str.lstrip('# ').strip()
                    elif l_str.startswith('## '):
                        toc.append(l_str.lstrip('## ').strip())
                if toc:
                    subtitle = " · ".join(toc[:2])
                good_ls = [clean_html(l.strip()) for l in lines if l.strip() and not l.startswith('#') and not l.startswith('```') and not l.startswith('|') and len(clean_html(l.strip())) > 20]
                if good_ls:
                    summary = good_ls[0][:160] + ("..." if len(good_ls[0]) > 160 else "")
                mins = max(2, round(len(content) / 450))
                read_time = f"{mins} 分钟"
        except Exception:
            pass
            
    elif ext == '.pdf':
        title = os.path.splitext(fn)[0]
        subtitle = "PDF 完整版电子书"
        summary = f"包含全套完整章节的高清 PDF 电子书，支持离线阅读与全本查阅。"
        read_time = f"约 {max(12, round(size / (120 * 1024)))} 页"
        
    return {
        "title": title,
        "subtitle": subtitle,
        "summary": summary,
        "size_str": format_size(size),
        "size_bytes": size,
        "read_time": read_time,
        "toc": toc
    }

def build_dist():
    print("=" * 65)
    print(" 📦 开始执行生产环境安全打包 (Build Dist)...")
    print("=" * 65)

    config = load_exclude_config()
    
    # 1. Clean dist directory
    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    os.makedirs(DIST_DIR, exist_ok=True)
    os.makedirs(os.path.join(DIST_DIR, "assets"), exist_ok=True)

    # 2. Copy static entry & assets
    shutil.copy2("index.html", os.path.join(DIST_DIR, "index.html"))
    if os.path.exists("favicon.ico"): shutil.copy2("favicon.ico", os.path.join(DIST_DIR, "favicon.ico"))
    if os.path.exists("favicon.svg"): shutil.copy2("favicon.svg", os.path.join(DIST_DIR, "favicon.svg"))

    # Copy assets folder (css, js, qrcode, etc.)
    for item in os.listdir("assets"):
        if item.startswith(".") or item in ["data.js", "data.json"]: continue
        src_p = os.path.join("assets", item)
        dst_p = os.path.join(DIST_DIR, "assets", item)
        if os.path.isdir(src_p):
            shutil.copytree(src_p, dst_p)
        else:
            shutil.copy2(src_p, dst_p)

    # 3. Read site data config and copy published files ONLY
    from build_site_data import categories_data
    
    all_published_articles = []
    skipped_count = 0
    copied_files_count = 0

    # Build articles database
    def process_article(cat_id, rel_path, custom_title=None, custom_badge=None, sort_order=100):
        nonlocal skipped_count, copied_files_count
        if not os.path.exists(rel_path):
            return
            
        if should_exclude_file(rel_path, config):
            skipped_count += 1
            return
            
        meta = extract_meta(rel_path)
        if custom_title: meta['title'] = custom_title
        ext = os.path.splitext(rel_path)[1].lower().replace('.', '')
        item_id = rel_path.replace('/', '_').replace('.', '_').replace('-', '_')
        badge = custom_badge or ext.upper()

        all_published_articles.append({
            "id": item_id,
            "categoryId": cat_id,
            "path": rel_path,
            "filename": os.path.basename(rel_path),
            "format": ext,
            "title": meta['title'],
            "subtitle": meta['subtitle'],
            "summary": meta['summary'],
            "readTime": meta['read_time'],
            "sizeStr": meta['size_str'],
            "sizeBytes": meta['size_bytes'],
            "badge": badge,
            "sortOrder": sort_order,
            "toc": meta['toc']
        })

        # Copy this file to dist
        target_path = os.path.join(DIST_DIR, rel_path)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        shutil.copy2(rel_path, target_path)
        copied_files_count += 1

    # Load article lists from build_site_data rules
    import glob
    # 1. Bigmodel
    for p, t, b, o in [
        ("bigmodel/大模型原理系列-开篇.html", "大模型原理 00 · 开篇词：探寻智能涌现的本质", "开篇", 1),
        ("bigmodel/大模型原理系列-01.html", "大模型原理 01 · Transformer 架构原理拆解", "01章", 2),
        ("bigmodel/大模型原理系列-03.html", "大模型原理 03 · 位置编码（Positional Encoding）详解", "03章", 3),
        ("bigmodel/大模型原理系列-04.html", "大模型原理 04 · 多头注意力与自注意力机制", "04章", 4),
        ("bigmodel/大模型原理系列-05.html", "大模型原理 05 · Encoder-Decoder 架构全解析", "05章", 5),
        ("bigmodel/大模型原理系列-06.html", "大模型原理 06 · RoPE 旋转位置编码与长文本外推", "06章", 6),
        ("bigmodel/大模型原理系列-07.html", "大模型原理 07 · KV Cache 缓存加速与推理优化", "07章", 7),
        ("bigmodel/大模型原理系列-08.html", "大模型原理 08 · MoE 混合专家模型与稀疏激活", "08章", 8),
        ("bigmodel/大模型原理系列-总结.html", "大模型原理 09 · 总结与大模型技术全景展望", "总结", 9),
        ("bigmodel/大模型原理系列-03-公众号版.html", "大模型原理 03 · 位置编码 (公众号图文版)", "公众号", 10),
    ]: process_article("bigmodel", p, t, b, o)

    # 2. Agent Core
    for p, t, b, o in [
        ("Agent开发系列-01.html", "Agent开发 01-02 · 从用户到创造者：Agent核心四环节", "01-02", 1),
        ("Agent开发系列-03.html", "Agent开发 03-04 · 最小可行 Agent：感知与决策的骨架", "03-04", 2),
        ("Agent开发系列-05.html", "Agent开发 05-06 · 思考机制：Agent 是怎么\"想\"的", "05-06", 3),
        ("Agent开发系列-07.html", "Agent开发 07-08 · 反思机制：Agent 是怎么\"反省\"的", "07-08", 4),
        ("Agent开发系列-08.html", "Agent开发 · 核心循环篇总结：Agent 是怎么思考的", "循环总结", 5),
        ("Agent开发系列-09.html", "Agent开发 09-10 · 四层记忆架构与上下文窗口管理", "09-10", 6),
        ("Agent开发系列-11.html", "Agent开发 11-12 · 向量数据库与 RAG 检索增强实战", "11-12", 7),
        ("Agent开发系列-13.html", "Agent开发 13-14 · Tool 接口设计与内置工具实现", "13-14", 8),
        ("Agent开发系列-15.html", "Agent开发 15-16 · Function Calling 与工具安全沙箱", "15-16", 9),
        ("Agent开发系列-17.html", "Agent开发 17-18 · 复杂任务分解与执行引擎架构", "17-18", 10),
        ("Agent开发系列-19.html", "Agent开发 19-20 · 动态规划调整与容错自愈机制", "19-20", 11),
        ("Agent开发系列-21.html", "Agent开发 21-22 · 消息总线与多智能体团队编排", "21-22", 12),
        ("Agent开发系列-23.html", "Agent开发 23-24 · 内容生产团队多 Agent 协同实战", "23-24", 13),
        ("Agent开发系列-25.html", "Agent开发 25-26 · Agent 系统可观测性与链路追踪", "25-26", 14),
        ("Agent开发系列-27.html", "Agent开发 27-28 · 实战篇 01：个人助手智能体全流程实现", "27-28", 15),
        ("Agent开发系列-29.html", "Agent开发 29-30 · 主流 Agent 框架横评与终极总结", "29-30", 16),
        ("Agent开发系列-电子书.html", "Agent开发系列 · 完整全本在线电子书", "全本Web", 17),
    ]: process_article("agent-core", p, t, b, o)

    # 3. myAgent
    for p, t, b, o in [
        ("myagent/myAgent开发系列大纲-公众号版.html", "myAgent 架构系列大纲与全景导读", "大纲", 1),
        ("myagent/myAgent开发系列-01.html", "myAgent 01 · 架构设计与环境搭建", "01章", 2),
        ("myagent/myAgent开发系列-02.html", "myAgent 02 · 意图感知模块手写实现", "02章", 3),
        ("myagent/myAgent开发系列-03.html", "myAgent 03 · 决策规划器与状态转移", "03章", 4),
        ("myagent/myAgent开发系列-04.html", "myAgent 04 · 工具注册表与执行调度", "04章", 5),
        ("myagent/myAgent开发系列-05.html", "myAgent 05 · 短期与长期记忆管理机制", "05章", 6),
        ("myagent/myAgent开发系列-06.html", "myAgent 06 · 自省反馈与动态错误修正", "06章", 7),
        ("myagent/myAgent开发系列-07.html", "myAgent 07 · 向量召回与知识注入实战", "07章", 8),
        ("myagent/myAgent开发系列-08.html", "myAgent 08 · 工具调用参数自动校验与安全", "08章", 9),
        ("myagent/myAgent开发系列-09.html", "myAgent 09 · 多步推理与长链任务执行", "09章", 10),
        ("myagent/myAgent开发系列-10.html", "myAgent 10 · 消息通道与事件驱动架构", "10章", 11),
        ("myagent/myAgent开发系列-11.html", "myAgent 11 · 运行监控、日志与性能调优", "11章", 12),
        ("myagent/myAgent开发系列-12.html", "myAgent 12 · 综合场景落地与实测验证", "12章", 13),
        ("myagent/myAgent开发系列-13.html", "myAgent 13 · 框架封装、总结与演进路线", "13章", 14),
    ]: process_article("myagent", p, t, b, o)

    # 4. Customer Service
    for p, t, b, o in [
        ("customer-service-agent/README.md", "智能客服 Agent 实战项目架构与说明文档", "项目文档", 1),
        ("customer-service-agent/客服Agent实战系列-01.html", "客服 Agent 实战 01 · 为什么需要智能客服与业务痛点", "01章", 2),
        ("customer-service-agent/客服Agent实战系列-02.html", "客服 Agent 实战 02 · 整体系统架构与模块划分", "02章", 3),
        ("customer-service-agent/客服Agent实战系列-03.html", "客服 Agent 实战 03 · 意图识别算法与分类流水线", "03章", 4),
        ("customer-service-agent/客服Agent实战系列-04.html", "客服 Agent 实战 04 · 知识库构建与 FAQ 语义匹配", "04章", 5),
        ("customer-service-agent/客服Agent实战系列-05.html", "客服 Agent 实战 05 · 订单状态查询与 API 插件接入", "05章", 6),
        ("customer-service-agent/客服Agent实战系列-06.html", "客服 Agent 实战 06 · 智能工单流转与自动化流向处理", "06章", 7),
        ("customer-service-agent/客服Agent实战系列-07-公众号版.html", "客服 Agent 实战 07 · 情感分析与客户满意度监控", "07章", 8),
        ("customer-service-agent/客服Agent实战系列-08-公众号版.html", "客服 Agent 实战 08 · 多 Agent 协同与复杂诉求会诊", "08章", 9),
        ("customer-service-agent/客服Agent实战系列-09-公众号版.html", "客服 Agent 实战 09 · Web 交互终端与前端接入", "09章", 10),
        ("customer-service-agent/客服Agent实战系列-10-公众号版.html", "客服 Agent 实战 10 · 评测指标与业务效果量化", "10章", 11),
        ("customer-service-agent/客服Agent实战系列-11-公众号版.html", "客服 Agent 实战 11 · 容灾降级与人工转接机制", "11章", 12),
        ("customer-service-agent/客服Agent实战系列-12-公众号版.html", "客服 Agent 实战 12 · 成本优化与高并发请求压测", "12章", 13),
        ("customer-service-agent/客服Agent实战系列-13-公众号版.html", "客服 Agent 实战 13 · 运维部署与生产环境发布", "13章", 14),
        ("customer-service-agent/客服Agent实战系列-14-公众号版.html", "客服 Agent 实战 14 · 全系列终极复盘与未来展望", "14章", 15),
    ]: process_article("customer-service", p, t, b, o)

    # 5. Customer Service Harness
    for p, t, b, o in [
        ("customer-service-agent-harness-skill/客服Agent加强版-01.html", "客服 Agent 进化论 ① | 别再写 if/else 了！模块解耦初探", "进化01", 1),
        ("customer-service-agent-harness-skill/客服Agent加强版-02.html", "客服 Agent 进化论 ② | BaseSkill：给 Agent 发张身份证", "进化02", 2),
        ("customer-service-agent-harness-skill/客服Agent加强版-03.html", "客服 Agent 进化论 ③ | Registry+Router：Skill的生存哲学", "进化03", 3),
        ("customer-service-agent-harness-skill/客服Agent加强版-04.html", "客服 Agent 进化论 ④ | OrderSkill：订单查询的正确姿势", "进化04", 4),
        ("customer-service-agent-harness-skill/客服Agent加强版-05.html", "客服 Agent 进化论 ⑤ | FAQ检索：关键词和向量为啥都不能少", "进化05", 5),
        ("customer-service-agent-harness-skill/客服Agent加强版-06.html", "客服 Agent 进化论 ⑥ | TicketSkill：工单系统的自动化跃迁", "进化06", 6),
        ("customer-service-agent-harness-skill/客服Agent加强版-07.html", "客服 Agent 进化论 ⑦ | Web 集成：从后端架构到现代化前端", "进化07", 7),
        ("customer-service-agent-harness-skill/客服Agent加强版-08.html", "客服 Agent 进化论 ⑧ | 总结与展望：打造可扩展的技能生态", "进化08", 8),
    ]: process_article("customer-service-harness", p, t, b, o)

    # 6. Local RAG
    for p, t, b, o in [
        ("local-llm-knowledge-base/README.md", "本地大模型知识库实战项目说明文档", "项目文档", 1),
        ("local-llm-knowledge-base/本地大模型知识库系列-01-公众号版.html", "本地知识库 01 · 为什么要自己搭建本地大模型知识库？", "01章", 2),
        ("local-llm-knowledge-base/本地大模型知识库系列-02-公众号版.html", "本地知识库 02 · 搭建 Ollama 环境：三步搞定本地大模型", "02章", 3),
        ("local-llm-knowledge-base/本地大模型知识库系列-03-公众号版.html", "本地知识库 03 · 构建本地知识库：从文档分块到智能问答", "03章", 4),
        ("local-llm-knowledge-base/本地大模型知识库系列-04-公众号版.html", "本地知识库 04 · 打造智能问答界面：让你的知识库更易用", "04章", 5),
        ("local-llm-knowledge-base/本地大模型知识库系列-05-公众号版.html", "本地知识库 05 · 多源文档导入与复杂格式智能解析", "05章", 6),
        ("local-llm-knowledge-base/本地大模型知识库系列-06-公众号版.html", "本地知识库 06 · 向量嵌入与 Top-K 语义召回深度优化", "06章", 7),
        ("local-llm-knowledge-base/本地大模型知识库系列-07-公众号版.html", "本地知识库 07 · 混合检索与重排序（Reranking）实战", "07章", 8),
        ("local-llm-knowledge-base/本地大模型知识库系列-08-公众号版.html", "本地知识库 08 · 提示词工程与上下文注入策略优化", "08章", 9),
        ("local-llm-knowledge-base/本地大模型知识库系列-09-公众号版.html", "本地知识库 09 · 权限隔离与多租户知识库架构", "09章", 10),
        ("local-llm-knowledge-base/本地大模型知识库系列-10-公众号版.html", "本地知识库 10 · 知识库持续更新与增量同步机制", "10章", 11),
        ("local-llm-knowledge-base/本地大模型知识库系列-11-公众号版.html", "本地知识库 11 · 性能调优、显存压榨与量化部署", "11章", 12),
        ("local-llm-knowledge-base/本地大模型知识库系列-12-公众号版.html", "本地知识库 12 · 企业级落地总结与开源方案选型指南", "12章", 13),
    ]: process_article("local-rag", p, t, b, o)

    # 7. AI Tools
    aitools_list = [f for f in sorted(glob.glob("aitools/*.html")) if not f.endswith('template.html') and not f.endswith('images.html')]
    order = 1
    for f in aitools_list:
        meta = extract_meta(f)
        badge = "实战"
        if "claude" in f.lower(): badge = "Claude"
        elif "skills" in f.lower() or "skill" in f.lower(): badge = "Skill"
        elif "dify" in f.lower(): badge = "Dify"
        elif "tdd" in f.lower(): badge = "TDD"
        elif "prd" in f.lower(): badge = "PRD"
        process_article("aitools", f, meta['title'], badge, order)
        order += 1
    if os.path.exists("aitools/写作规范.md"):
        process_article("aitools", "aitools/写作规范.md", "AI 知识库写作规范与排版指南", "规范", order)

    # 8. AI Coding Series (33 articles)
    for p, t, b, o in [
        ("ai-coding/AI-Coding系列-00-系列导航.html", "AI Coding 新手篇 00 · 完整导航与学习指南", "导航", 1),
        ("ai-coding/AI-Coding系列-01-AI-Coding是什么.html", "AI Coding 01 · 从手动编程到 AI 辅助革命", "01章", 2),
        ("ai-coding/AI-Coding系列-02-10分钟安装配置.html", "AI Coding 02 · 10分钟安装配置与环境准备", "02章", 3),
        ("ai-coding/AI-Coding系列-03-基础操作.html", "AI Coding 03 · 基础操作与 5 个必会命令", "03章", 4),
        ("ai-coding/AI-Coding系列-04-提示词技巧.html", "AI Coding 04 · 提示词技巧：让 Claude 更懂你", "04章", 5),
        ("ai-coding/AI-Coding系列-05-新手总结.html", "AI Coding 05 · 新手篇总结：从入门到日常使用", "05章", 6),
        ("ai-coding/AI-Coding系列-06-代码库理解.html", "AI Coding 06 · 代码库理解：让 AI 认识你的项目", "06章", 7),
        ("ai-coding/AI-Coding系列-07-多文件编辑.html", "AI Coding 07 · 多文件编辑：复杂重构不求人", "07章", 8),
        ("ai-coding/AI-Coding系列-08-测试驱动.html", "AI Coding 08 · 测试驱动开发：AI 帮你写测试", "08章", 9),
        ("ai-coding/AI-Coding系列-09-调试高手.html", "AI Coding 09 · 调试高手：快速定位和修复 Bug", "09章", 10),
        ("ai-coding/AI-Coding系列-10-文档生成.html", "AI Coding 10 · 文档生成：自动生成工程级代码文档", "10章", 11),
        ("ai-coding/AI-Coding系列-11-进阶总结.html", "AI Coding 11 · 进阶总结：成为 AI 编程高手", "11章", 12),
        ("ai-coding/AI-Coding系列-12-代码补全原理.html", "AI Coding 12 · 代码补全原理：AI 如何\"读懂\"代码", "12章", 13),
        ("ai-coding/AI-Coding系列-13-上下文管理.html", "AI Coding 13 · 上下文管理：AI 如何记住你的代码", "13章", 14),
        ("ai-coding/AI-Coding系列-14-AI-Coding架构.html", "AI Coding 14 · AI Coding 架构：技术实现全景揭秘", "14章", 15),
        ("ai-coding/AI-Coding系列-15-安全与隐私.html", "AI Coding 15 · 安全与隐私：代码安全性与隐私防护", "15章", 16),
        ("ai-coding/AI-Coding系列-16-实战01-开发命令行工具.html", "AI Coding 16 · 实战 01：开发命令行工具 CLI", "实战01", 17),
        ("ai-coding/AI-Coding系列-17-实战02-开发Web-API.html", "AI Coding 17 · 实战 02：开发 Web API 后端服务", "实战02", 18),
        ("ai-coding/AI-Coding系列-18-实战03-引入MCP.html", "AI Coding 18 · 实战 03：引入 MCP 连接外部生态服务", "实战03", 19),
        ("ai-coding/AI-Coding系列-19-实战04-打包发布.html", "AI Coding 19 · 实战 04：工程打包与多端自动化发布", "实战04", 20),
        ("ai-coding/AI-Coding系列-20-实战05-设计全栈应用架构.html", "AI Coding 20 · 实战 05：设计全栈应用架构全景", "实战05", 21),
        ("ai-coding/AI-Coding系列-21-实战06-后端服务+Skills.html", "AI Coding 21 · 实战 06：后端微服务 + Skills 插件", "实战06", 22),
        ("ai-coding/AI-Coding系列-22-实战07-前端界面.html", "AI Coding 22 · 实战 07：现代化前端交互界面开发", "实战07", 23),
        ("ai-coding/AI-Coding系列-23-实战08-数据分析+AI特性.html", "AI Coding 23 · 实战 08：数据分析与 AI 特性深度整合", "实战08", 24),
        ("ai-coding/AI-Coding系列-24-多语言开发.html", "AI Coding 24 · 专题篇：多语言开发 (Python/JS/Go/Rust)", "多语言", 25),
        ("ai-coding/AI-Coding系列-25-团队协作.html", "AI Coding 25 · 专题篇：团队协作与企业级落地指南", "企业落地", 26),
        ("ai-coding/AI-Coding系列-26-系列总结.html", "AI Coding 26 · 全系列总结：从入门到精通演进之路", "系列总结", 27),
        ("ai-coding/AI-Coding系列-27-Claude-Code架构概览.html", "AI Coding 27 · Claude Code 源码架构核心剖析", "源码01", 28),
        ("ai-coding/AI-Coding系列-28-Agent核心实现.html", "AI Coding 28 · Agent 核心实现：消息循环与工具调用", "源码02", 29),
        ("ai-coding/AI-Coding系列-29-工具系统.html", "AI Coding 29 · 工具系统 (Tool System)：能力边界扩展", "源码03", 30),
        ("ai-coding/AI-Coding系列-30-上下文管理.html", "AI Coding 30 · 上下文管理 (Context Management) 机制", "源码04", 31),
        ("ai-coding/AI-Coding系列-31-安全与性能.html", "AI Coding 31 · 安全与性能 (Security & Performance) 优化", "源码05", 32),
        ("ai-coding/AI-Coding系列-32-实战改造与扩展.html", "AI Coding 32 · 实战改造与扩展：从源码到二次开发", "源码06", 33),
    ]: process_article("ai-coding", p, t, b, o)
    if os.path.exists("ai-coding/AI-Coding-系列大纲.md"):
        process_article("ai-coding", "ai-coding/AI-Coding-系列大纲.md", "AI Coding 体系全套实战大纲", "大纲", 34)

    # 9. OpenClaw Series (18 articles)
    for p, t, b, o in [
        ("openclaw/OpenClaw系列-00-系列导航.html", "OpenClaw 00 · 系列导航：从入门到精通完整指引", "导航", 1),
        ("openclaw/OpenClaw系列-01-OpenClaw是什么.html", "OpenClaw 01 · 5分钟看懂 AI Agent 与龙虾架构", "01 概述", 2),
        ("openclaw/OpenClaw系列-02-10分钟部署.html", "OpenClaw 02 · 10分钟部署你的第一只\"龙虾\"", "02 部署", 3),
        ("openclaw/OpenClaw系列-03-10个实用任务.html", "OpenClaw 03 · 新手必学的 10 个实用任务", "03 任务", 4),
        ("openclaw/OpenClaw系列-04-基础配置指南.html", "OpenClaw 04 · 让龙虾更懂你：基础配置指南", "04 配置", 5),
        ("openclaw/OpenClaw系列-05-默认Skills与管理.html", "OpenClaw 05 · 认识 Skills 系统：默认 Skills 与管理", "05 Skills", 6),
        ("openclaw/OpenClaw系列-06-第一个自定义Skill.html", "OpenClaw 06 · 从 0 到 1：开发你的第一个自定义 Skill", "06 自定义", 7),
        ("openclaw/OpenClaw系列-07-Agent工作流.html", "OpenClaw 07 · Agent 工作流：让龙虾自动化协同干活", "07 工作流", 8),
        ("openclaw/OpenClaw系列-08-多Agent协作.html", "OpenClaw 08 · 多 Agent 协作：1+1>2 的编排魔法", "08 多Agent", 9),
        ("openclaw/OpenClaw系列-09-工具与API集成.html", "OpenClaw 09 · 接入外部世界：工具与 API 深度集成", "09 API", 10),
        ("openclaw/OpenClaw系列-10-进阶篇总结.html", "OpenClaw 10 · 进阶篇总结：打造全能智能助手", "10 进阶总结", 11),
        ("openclaw/OpenClaw系列-11-核心循环.html", "OpenClaw 11 · 核心循环：感知-思考-行动-反思闭环", "11 核心循环", 12),
        ("openclaw/OpenClaw系列-12-记忆系统.html", "OpenClaw 12 · 记忆系统：Agent 如何\"记住\"关键信息", "12 记忆", 13),
        ("openclaw/OpenClaw系列-13-架构解析.html", "OpenClaw 13 · OpenClaw 架构解析：设计哲学与演进", "13 架构", 14),
        ("openclaw/OpenClaw系列-14-企业级部署.html", "OpenClaw 14 · 企业级部署：从开发环境到生产高可用", "14 企业部署", 15),
        ("openclaw/OpenClaw系列-15-原理篇总结.html", "OpenClaw 15 · 原理篇总结：掌握智能体核心精髓", "15 原理总结", 16),
        ("openclaw/OpenClaw系列-16-实战01-设计专属AI助手.html", "OpenClaw 16 · 实战篇 01：设计你的专属 AI 助手", "16 实战", 17),
        ("openclaw/OpenClaw系列-17-全系列终极总结.html", "OpenClaw 17 · 全系列终极总结：从入门到精通的完整旅程", "17 终极总结", 18),
    ]: process_article("openclaw", p, t, b, o)
    if os.path.exists("openclaw/OpenClaw-大纲.md"):
        process_article("openclaw", "openclaw/OpenClaw-大纲.md", "OpenClaw 架构体系全景大纲", "大纲", 19)

    def get_existing_path(p):
        if os.path.exists(p):
            return p
        parts = p.split("/", 1)
        if len(parts) == 2:
            beta_p = f"beta-{parts[0]}/{parts[1]}"
            if os.path.exists(beta_p):
                return beta_p
        return None

    # 10. English Agent
    for idx, f in enumerate(sorted(glob.glob("english-learning-agent/*.html") + glob.glob("beta-english-learning-agent/*.html")), 1):
        meta = extract_meta(f)
        process_article("english-agent", f, f"英语学习 Agent {idx:02d} · {meta['title']}", f"{idx:02d}章", idx)

    # 11. AI Safety
    for p, t, b, o in [
        ("ai-safety/AI安全与伦理系列-01.html", "AI安全与伦理 01 · AI 幻觉的成因与工程治理", "01 幻觉", 1),
        ("ai-safety/AI安全与伦理系列-02.html", "AI安全与伦理 02 · 数据隐私脱敏与合规底线", "02 隐私", 2),
        ("ai-safety/AI安全与伦理系列-03.html", "AI安全与伦理 03 · 算法偏见识别与公平性对齐", "03 偏见", 3),
        ("ai-safety/AI安全与伦理系列-04.html", "AI安全与伦理 04 · 深度伪造（Deepfake）检测与防范", "04 深伪", 4),
        ("ai-safety/AI安全与伦理系列-05.html", "AI安全与伦理 05 · 提示注入攻击与模型防御对抗", "05 防御", 5),
        ("ai-safety/AI安全与伦理系列-06.html", "AI安全与伦理 06 · AI 伦理治理体系与国际规范", "06 伦理", 6),
        ("ai-safety/AI安全与伦理系列-总结.html", "AI安全与伦理 07 · 总结：构建可信赖的负责任 AI", "07 总结", 7),
    ]:
        actual_p = get_existing_path(p)
        if actual_p: process_article("ai-safety", actual_p, t, b, o)

    # 12. AI Engineering
    p_eng = get_existing_path("ai-engineering/AI工程化系列-01.html")
    if p_eng:
        process_article("ai-engineering", p_eng, "AI工程化 01 · 大模型生产级部署与性能调优", "01 部署", 1)

    # 13. AI Monetization
    p_mon = get_existing_path("ai-monetization/AI变现之路-01.html")
    if p_mon:
        process_article("ai-monetization", p_mon, "AI变现之路 01 · AI时代个人与团队的5条变现黄金路径", "01 商业", 1)

    # 14. AI Science
    p_sci_readme = get_existing_path("ai-popular-science-series/README.md")
    if p_sci_readme:
        process_article("ai-science", p_sci_readme, "AI科普系列 · 混知漫画风格通俗图解提纲（全本大纲）", "大纲", 1)
    p_sci_01 = get_existing_path("ai-popular-science-series/AI科普系列-01-公众号版.html")
    if p_sci_01:
        process_article("ai-science", p_sci_01, "AI科普 01 · 通俗图解：大模型到底是怎么思考的？", "01 科普", 2)

    # 15. AI News
    p_news = get_existing_path("ai-news/AI资讯周刊-2026年第28期.html")
    if p_news:
        process_article("ai-news", p_news, "AI资讯周刊 · 2026 年第 28 期：大模型前沿突破与开源动态", "第28期", 1)

    # 16. Quant Trading
    p_quant = get_existing_path("quant-trading-agent/量化交易Agent系列-01-公众号版.html")
    if p_quant:
        process_article("quant-agent", p_quant, "量化交易 Agent 01 · 架构设计与自动化交易系统", "01 架构", 1)

    # 4. Copy image assets (mermaid images, diagrams, etc.) referenced by articles
    for img_dir in ["mermaid", "bigmodel/mermaid", "customer-service-agent/mermaid-img", "aitools/diagram", "local-llm-knowledge-base/mermaid-img"]:
        if os.path.exists(img_dir):
            dst_img_dir = os.path.join(DIST_DIR, img_dir)
            os.makedirs(os.path.dirname(dst_img_dir), exist_ok=True)
            if not os.path.exists(dst_img_dir):
                shutil.copytree(img_dir, dst_img_dir)

    # Filter categories for dist
    hidden_cats = config.get("hidden_categories", [])
    active_categories = []
    for cat in categories_data:
        if cat['id'] in hidden_cats: continue
        cat_items = [a for a in all_published_articles if a['categoryId'] == cat['id']]
        if len(cat_items) > 0:
            cat['count'] = len(cat_items)
            active_categories.append(cat)

    active_cat_ids = {c['id'] for c in active_categories}
    final_articles = [a for a in all_published_articles if a['categoryId'] in active_cat_ids]

    # Write dist/assets/data.json and dist/assets/data.js
    dist_site_data = {
        "siteTitle": "AI 全系列学习智库 · 体系化知识库",
        "siteSubtitle": "涵盖大模型底层原理、Agent 核心架构、智能客服实战、本地知识库 (RAG) 与 AI 编程实战工具链",
        "stats": {
            "totalCategories": len(active_categories),
            "totalArticles": len(final_articles)
        },
        "categories": active_categories,
        "articles": final_articles
    }

    with open(os.path.join(DIST_DIR, "assets", "data.json"), "w", encoding="utf-8") as f:
        json.dump(dist_site_data, f, ensure_ascii=False, indent=2)

    # Write CloudBase Dockerfile & nginx.conf directly inside DIST_DIR for 1-click cloud deploy
    cloud_dockerfile = '''FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY . /usr/share/nginx/html/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
'''
    with open(os.path.join(DIST_DIR, "Dockerfile"), "w", encoding="utf-8") as f:
        f.write(cloud_dockerfile)

    if os.path.exists("nginx.conf"):
        shutil.copy2("nginx.conf", os.path.join(DIST_DIR, "nginx.conf"))
    if os.path.exists(".dockerignore"):
        shutil.copy2(".dockerignore", os.path.join(DIST_DIR, ".dockerignore"))

    # 5. Minify CSS, JS, HTML, and JSON Assets for Production
    print("-" * 65)
    print(" ⚡ 正在执行专业级静态资源深度压缩 (Minification)...")
    
    min_stats = []

    # 5.1 Minify app.css
    dist_css_path = os.path.join(DIST_DIR, "assets", "app.css")
    if os.path.exists(dist_css_path):
        with open(dist_css_path, "r", encoding="utf-8") as f:
            orig_css = f.read()
        min_css = minify_css_content(orig_css)
        with open(dist_css_path, "w", encoding="utf-8") as f:
            f.write(min_css)
        min_stats.append(("assets/app.css", len(orig_css), len(min_css)))

    # 5.2 Minify app.js
    dist_js_path = os.path.join(DIST_DIR, "assets", "app.js")
    if os.path.exists(dist_js_path):
        with open(dist_js_path, "r", encoding="utf-8") as f:
            orig_js = f.read()
        min_js = minify_js_content(orig_js)
        with open(dist_js_path, "w", encoding="utf-8") as f:
            f.write(min_js)
        min_stats.append(("assets/app.js", len(orig_js), len(min_js)))

    # 5.3 Write Ultra-Compact data.json & data.js
    dist_json_path = os.path.join(DIST_DIR, "assets", "data.json")
    dist_data_js_path = os.path.join(DIST_DIR, "assets", "data.js")
    
    compact_json = json.dumps(dist_site_data, separators=(',', ':'), ensure_ascii=False)
    compact_data_js = "window.SITE_DATA=" + compact_json + ";"
    
    with open(dist_json_path, "w", encoding="utf-8") as f:
        f.write(compact_json)
    with open(dist_data_js_path, "w", encoding="utf-8") as f:
        f.write(compact_data_js)
        
    orig_data_len = len(json.dumps(dist_site_data, indent=2, ensure_ascii=False))
    min_stats.append(("assets/data.json", orig_data_len, len(compact_json)))
    min_stats.append(("assets/data.js", orig_data_len + 25, len(compact_data_js)))

    # 5.4 Minify index.html
    dist_index_path = os.path.join(DIST_DIR, "index.html")
    if os.path.exists(dist_index_path):
        with open(dist_index_path, "r", encoding="utf-8") as f:
            orig_html = f.read()
        min_html = minify_html_content(orig_html)
        with open(dist_index_path, "w", encoding="utf-8") as f:
            f.write(min_html)
        min_stats.append(("index.html", len(orig_html), len(min_html)))

    for name, orig_len, new_len in min_stats:
        saved_pct = ((orig_len - new_len) / orig_len) * 100 if orig_len > 0 else 0
        print(f"    ✓ {name:<18}: {format_size(orig_len):>8} -> {format_size(new_len):>8} (体积缩减 {saved_pct:.1f}%)")

    # 6. Create zip bundle
    zip_path = "ai_learning_hub_dist.zip"
    print("-" * 65)
    print(" 📦 正在生成一键发布压缩包: ai_learning_hub_dist.zip ...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(DIST_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, DIST_DIR)
                zipf.write(file_path, arcname)

    print("-" * 65)
    print(" 🎉 打包完成！输出目录: ./dist/")
    print(f"    - 发布分类数: {len(active_categories)} 个")
    print(f"    - 正式收录文献: {len(final_articles)} 篇")
    print(f"    - 物理过滤草稿: {skipped_count} 篇")
    print(f"    - 静态资源压缩: 已全部完成 (CSS/JS/JSON/HTML Minified)")
    print(f"    - 生成部署 ZIP: {zip_path} ({os.path.getsize(zip_path) // 1024} KB)")
    print("=" * 65)
    print(" 💡 提示：部署时只需将 dist/ 文件夹内容（或解压后的 ZIP）上传到服务器即可！")
    print("    草稿与未成熟文件绝不会包含在 dist/ 中，从物理层面杜绝直接路径探测。")
    print("=" * 65)

if __name__ == '__main__':
    build_dist()
