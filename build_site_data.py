#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 学习智库 · 知识库数据索引与元数据生成器
支持 exclude_config.json 排除规则、草稿自动忽略与分类动态统计。
"""

import os
import glob
import fnmatch
import re
import json

# Load Exclude Configuration
EXCLUDE_CONFIG_PATH = "exclude_config.json"
exclude_config = {
    "hidden_categories": [],
    "hidden_files": [],
    "hidden_patterns": ["*draft*", "*草稿*", "*wip*", "*temp*", "_*"],
    "coming_soon_articles": []
}

if os.path.exists(EXCLUDE_CONFIG_PATH):
    try:
        with open(EXCLUDE_CONFIG_PATH, "r", encoding="utf-8") as f:
            user_config = json.load(f)
            exclude_config.update(user_config)
    except Exception as e:
        print(f"⚠️ 读取 {EXCLUDE_CONFIG_PATH} 失败: {e}")

def should_exclude_file(rel_path):
    fn = os.path.basename(rel_path)
    
    # 1. Exact file match
    if rel_path in exclude_config.get("hidden_files", []):
        return True
    if fn in exclude_config.get("hidden_files", []):
        return True
        
    # 2. Pattern match (like _*, *draft*, *草稿*, etc.)
    for pattern in exclude_config.get("hidden_patterns", []):
        if fnmatch.fnmatch(fn, pattern) or fnmatch.fnmatch(rel_path, pattern):
            return True
            
    # 3. Hidden directory/file prefix (_, ., beta-, todo-)
    for part in rel_path.split("/"):
        if part.startswith("_") or part.startswith(".") or part.startswith("beta-") or part.startswith("todo-"):
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

categories_data = [
    {
        "id": "bigmodel",
        "name": "大模型底层原理",
        "icon": "🧠",
        "badge": "核心原理",
        "desc": "深入剖析 Transformer、位置编码、多头注意力、RoPE、KV Cache、MoE 及对齐原理",
        "theme": "purple",
        "accent": "#8b5cf6",
        "color": "purple",
        "difficulty": "进阶",
        "tags": ["Transformer", "Attention", "RoPE", "KV Cache", "MoE"]
    },
    {
        "id": "agent-core",
        "name": "Agent 核心开发进阶",
        "icon": "⚡",
        "badge": "智能体系统",
        "desc": "感知-决策-执行全循环、四层记忆架构、向量 RAG、Tool 工具编排、多 Agent 团队与可观测性",
        "theme": "blue",
        "accent": "#3b82f6",
        "color": "blue",
        "difficulty": "核心实战",
        "tags": ["Agent循环", "记忆架构", "RAG", "Function Calling", "多Agent"]
    },
    {
        "id": "myagent",
        "name": "myAgent 架构手写实战",
        "icon": "🤖",
        "badge": "轻量手写",
        "desc": "手把手从零手写轻量级 Agent 框架：有限状态机、意图感知、任务规划与反思执行",
        "theme": "indigo",
        "accent": "#6366f1",
        "color": "indigo",
        "difficulty": "实战开发",
        "tags": ["手写Agent", "状态机", "意图解析", "反思机制"]
    },
    {
        "id": "customer-service",
        "name": "智能客服 Agent 实战落地",
        "icon": "🎧",
        "badge": "企业落地",
        "desc": "企业级智能客服系统：意图识别、工单流转、知识库检索、情感分析与多 Agent 协同",
        "theme": "emerald",
        "accent": "#10b981",
        "color": "emerald",
        "difficulty": "生产项目",
        "tags": ["客服实战", "意图流转", "工单系统", "多Agent协同"]
    },
    {
        "id": "customer-service-harness",
        "name": "客服 Agent 进化论 (强化版)",
        "icon": "🚀",
        "badge": "Skill架构",
        "desc": "基于 BaseSkill 规范、SkillRegistry 注册中心、智能 Router 路由与混合检索的高阶重构",
        "theme": "teal",
        "accent": "#14b8a6",
        "color": "teal",
        "difficulty": "高阶架构",
        "tags": ["BaseSkill", "SkillRegistry", "Router", "混合检索"]
    },
    {
        "id": "local-rag",
        "name": "本地大模型与知识库 (RAG)",
        "icon": "📚",
        "badge": "私有化部署",
        "desc": "Ollama 本地部署、文档切分、Embedding 向量化、Top-K 语义召回、重排序与 Web 问答",
        "theme": "amber",
        "accent": "#f59e0b",
        "color": "amber",
        "difficulty": "热门实战",
        "tags": ["Ollama", "私有知识库", "RAG", "向量检索", "WebUI"]
    },
    {
        "id": "aitools",
        "name": "AI 工具与 Agent 技能实战",
        "icon": "🛠️",
        "badge": "开发生态",
        "desc": "Claude Code 全家桶、MCP Server、Dify 编排、TDD 先行、Superpowers 与生产级 Agent 技能库",
        "theme": "sky",
        "accent": "#0ea5e9",
        "color": "sky",
        "difficulty": "效率神器",
        "tags": ["Claude Code", "MCP", "Dify", "TDD", "Superpowers"]
    },
    {
        "id": "ai-coding",
        "name": "AI Coding 编程全套实战",
        "icon": "💻",
        "badge": "AI编程体系",
        "desc": "涵盖命令基础、多文件重构、TDD、调试、MCP扩展、全栈实战与 Claude Code 源码级架构解析",
        "theme": "blue",
        "accent": "#2563eb",
        "color": "blue",
        "difficulty": "实战到源码",
        "tags": ["AI Coding", "Claude Code", "MCP", "TDD", "全栈实战", "源码架构"]
    },
    {
        "id": "openclaw",
        "name": "OpenClaw 智能体从入门到精通",
        "icon": "🦞",
        "badge": "Agent框架",
        "desc": "从零部署第一只龙虾、技能系统、多 Agent 协作、核心循环、记忆系统与企业级架构解析",
        "theme": "orange",
        "accent": "#f97316",
        "color": "orange",
        "difficulty": "体系实战",
        "tags": ["OpenClaw", "Skills", "多Agent", "核心循环", "记忆系统", "企业部署"]
    },
    {
        "id": "english-agent",
        "name": "英语学习 Agent 智能导师",
        "icon": "🗣️",
        "badge": "垂直AI",
        "desc": "词汇艾宾浩斯记忆、知识图谱语法教学、自适应难度分级阅读与 AI 对话口语实训系统",
        "theme": "rose",
        "accent": "#f43f5e",
        "color": "rose",
        "difficulty": "垂直实战",
        "tags": ["英语学习", "知识图谱", "自适应阅读", "AI口语"]
    },
    {
        "id": "ai-safety",
        "name": "AI 安全与伦理规范",
        "icon": "🛡️",
        "badge": "安全合规",
        "desc": "大模型幻觉治理、数据隐私脱敏合规、算法偏见消除、Deepfake 防御与伦理安全底线",
        "theme": "red",
        "accent": "#ef4444",
        "color": "red",
        "difficulty": "安全规范",
        "tags": ["幻觉治理", "数据隐私", "算法偏见", "Deepfake"]
    },
    {
        "id": "ai-engineering",
        "name": "AI 工程化实践",
        "icon": "⚙️",
        "badge": "架构落地",
        "desc": "大模型生产级部署、高并发微服务架构、模型推理加速与全链路可观测性监控",
        "theme": "slate",
        "accent": "#64748b",
        "color": "slate",
        "difficulty": "工程落地",
        "tags": ["生产部署", "高并发", "推理加速", "工程监控"]
    },
    {
        "id": "ai-monetization",
        "name": "AI 商业化与变现之路",
        "icon": "💰",
        "badge": "商业落地",
        "desc": "AI 时代 5 条变现路径：独立开发出海、垂直行业解决方案、技术咨询服务与私域变现",
        "theme": "orange",
        "accent": "#ea580c",
        "color": "orange",
        "difficulty": "商业认知",
        "tags": ["商业变现", "独立开发", "垂直方案", "出海产品"]
    },
    {
        "id": "ai-science",
        "name": "AI 通识与混知科普",
        "icon": "🌱",
        "badge": "零门槛科普",
        "desc": "用通俗生动的混知漫画风格拆解 AI 底层概念，零基础读者也能秒懂的人工智能科普",
        "theme": "green",
        "accent": "#84cc16",
        "color": "green",
        "difficulty": "零门槛入门",
        "tags": ["通俗科普", "混知风格", "零基础", "图解AI"]
    },
    {
        "id": "ai-news",
        "name": "AI 资讯周刊与前沿动态",
        "icon": "📰",
        "badge": "前沿动态",
        "desc": "追踪全球大模型技术突破、开源框架发布、顶会前沿论文与行业变革深度观察",
        "theme": "cyan",
        "accent": "#06b6d4",
        "color": "cyan",
        "difficulty": "行业资讯",
        "tags": ["资讯周刊", "前沿追踪", "开源趋势"]
    },
    {
        "id": "quant-agent",
        "name": "量化交易 Agent 实战",
        "icon": "📈",
        "badge": "金融量化",
        "desc": "市场情绪量化感知、多因子策略回测与自动化交易智能体架构设计与实操",
        "theme": "violet",
        "accent": "#7c3aed",
        "color": "violet",
        "difficulty": "量化实战",
        "tags": ["量化金融", "策略回测", "交易Agent", "情绪感知"]
    },
    {
        "id": "business-growth",
        "name": "业务落地与轻量建站",
        "icon": "🚀",
        "badge": "实战复盘",
        "desc": "零成本独立建站、SEO 流量矩阵、微信生态闭环、Prompt 业务工程与超级个体实战",
        "theme": "teal",
        "accent": "#0d9488",
        "color": "teal",
        "difficulty": "商业落地",
        "tags": ["零成本建站", "Cloudflare", "免备案", "SEO矩阵", "业务落地"]
    }
]

def build_data():
    all_articles = []
    excluded_count = 0

    def add_article(cat_id, rel_path, custom_title=None, custom_badge=None, sort_order=100):
        nonlocal excluded_count
        if not os.path.exists(rel_path):
            return
        
        # Check if excluded
        if should_exclude_file(rel_path):
            excluded_count += 1
            return

        meta = extract_meta(rel_path)
        if custom_title:
            meta['title'] = custom_title
        ext = os.path.splitext(rel_path)[1].lower().replace('.', '')
        
        item_id = rel_path.replace('/', '_').replace('.', '_').replace('-', '_')
        
        badge = custom_badge or ext.upper()
        if rel_path in exclude_config.get("coming_soon_articles", []):
            badge = "编写中"

        all_articles.append({
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

    # 1. Big Model
    bm_files = [
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
    ]
    for p, t, b, o in bm_files: add_article("bigmodel", p, t, b, o)

    # 2. Agent Core
    agent_core_files = [
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
    ]
    for p, t, b, o in agent_core_files: add_article("agent-core", p, t, b, o)

    # 3. myAgent
    myagent_files = [
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
    ]
    for p, t, b, o in myagent_files: add_article("myagent", p, t, b, o)

    # 4. Customer Service
    cs_files = [
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
    ]
    for p, t, b, o in cs_files: add_article("customer-service", p, t, b, o)

    # 5. Customer Service Harness
    csh_files = [
        ("customer-service-agent-harness-skill/客服Agent加强版-01.html", "客服 Agent 进化论 ① | 别再写 if/else 了！模块解耦初探", "进化01", 1),
        ("customer-service-agent-harness-skill/客服Agent加强版-02.html", "客服 Agent 进化论 ② | BaseSkill：给 Agent 发张身份证", "进化02", 2),
        ("customer-service-agent-harness-skill/客服Agent加强版-03.html", "客服 Agent 进化论 ③ | Registry+Router：Skill的生存哲学", "进化03", 3),
        ("customer-service-agent-harness-skill/客服Agent加强版-04.html", "客服 Agent 进化论 ④ | OrderSkill：订单查询的正确姿势", "进化04", 4),
        ("customer-service-agent-harness-skill/客服Agent加强版-05.html", "客服 Agent 进化论 ⑤ | FAQ检索：关键词和向量为啥都不能少", "进化05", 5),
        ("customer-service-agent-harness-skill/客服Agent加强版-06.html", "客服 Agent 进化论 ⑥ | TicketSkill：工单系统的自动化跃迁", "进化06", 6),
        ("customer-service-agent-harness-skill/客服Agent加强版-07.html", "客服 Agent 进化论 ⑦ | Web 集成：从后端架构到现代化前端", "进化07", 7),
        ("customer-service-agent-harness-skill/客服Agent加强版-08.html", "客服 Agent 进化论 ⑧ | 总结与展望：打造可扩展的技能生态", "进化08", 8),
    ]
    for p, t, b, o in csh_files: add_article("customer-service-harness", p, t, b, o)

    # 6. Local RAG
    local_rag_files = [
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
    ]
    for p, t, b, o in local_rag_files: add_article("local-rag", p, t, b, o)

    # 7. AI Tools
    aitools_list = [f for f in sorted(glob.glob("aitools/*.html")) if not f.endswith('template.html') and not f.endswith('images.html')]
    order = 1
    for f in aitools_list:
        meta = extract_meta(f)
        title = meta['title']
        badge = "实战"
        if "claude" in f.lower(): badge = "Claude"
        elif "skills" in f.lower() or "skill" in f.lower(): badge = "Skill"
        elif "dify" in f.lower(): badge = "Dify"
        elif "tdd" in f.lower(): badge = "TDD"
        elif "prd" in f.lower(): badge = "PRD"
        add_article("aitools", f, title, badge, order)
        order += 1

    if os.path.exists("aitools/写作规范.md"):
        add_article("aitools", "aitools/写作规范.md", "AI 知识库写作规范与排版指南", "规范", order)

    # 8. AI Coding Series (33 articles)
    ai_coding_files = [
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
    ]
    for p, t, b, o in ai_coding_files: add_article("ai-coding", p, t, b, o)
    if os.path.exists("ai-coding/AI-Coding-系列大纲.md"):
        add_article("ai-coding", "ai-coding/AI-Coding-系列大纲.md", "AI Coding 体系全套实战大纲", "大纲", 34)

    # 9. OpenClaw Series (18 articles)
    openclaw_files = [
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
    ]
    for p, t, b, o in openclaw_files: add_article("openclaw", p, t, b, o)
    if os.path.exists("openclaw/OpenClaw-大纲.md"):
        add_article("openclaw", "openclaw/OpenClaw-大纲.md", "OpenClaw 架构体系全景大纲", "大纲", 19)

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
    eng_files = [f for f in sorted(glob.glob("english-learning-agent/*.html") + glob.glob("beta-english-learning-agent/*.html"))]
    for idx, f in enumerate(eng_files, 1):
        meta = extract_meta(f)
        add_article("english-agent", f, f"英语学习 Agent {idx:02d} · {meta['title']}", f"{idx:02d}章", idx)

    # 11. AI Safety
    safety_files = [
        ("ai-safety/AI安全与伦理系列-01.html", "AI安全与伦理 01 · AI 幻觉的成因与工程治理", "01 幻觉", 1),
        ("ai-safety/AI安全与伦理系列-02.html", "AI安全与伦理 02 · 数据隐私脱敏与合规底线", "02 隐私", 2),
        ("ai-safety/AI安全与伦理系列-03.html", "AI安全与伦理 03 · 算法偏见识别与公平性对齐", "03 偏见", 3),
        ("ai-safety/AI安全与伦理系列-04.html", "AI安全与伦理 04 · 深度伪造（Deepfake）检测与防范", "04 深伪", 4),
        ("ai-safety/AI安全与伦理系列-05.html", "AI安全与伦理 05 · 提示注入攻击与模型防御对抗", "05 防御", 5),
        ("ai-safety/AI安全与伦理系列-06.html", "AI安全与伦理 06 · AI 伦理治理体系与国际规范", "06 伦理", 6),
        ("ai-safety/AI安全与伦理系列-总结.html", "AI安全与伦理 07 · 总结：构建可信赖的负责任 AI", "07 总结", 7),
    ]
    for p, t, b, o in safety_files:
        actual_p = get_existing_path(p)
        if actual_p: add_article("ai-safety", actual_p, t, b, o)

    # 12. AI Engineering
    p_eng = get_existing_path("ai-engineering/AI工程化系列-01.html")
    if p_eng:
        add_article("ai-engineering", p_eng, "AI工程化 01 · 大模型生产级部署与性能调优", "01 部署", 1)

    # 13. AI Monetization
    p_mon = get_existing_path("ai-monetization/AI变现之路-01.html")
    if p_mon:
        add_article("ai-monetization", p_mon, "AI变现之路 01 · AI时代个人与团队的5条变现黄金路径", "01 商业", 1)

    # 14. AI Science
    p_sci_readme = get_existing_path("ai-popular-science-series/README.md")
    if p_sci_readme:
        add_article("ai-science", p_sci_readme, "AI科普系列 · 混知漫画风格通俗图解提纲（全本大纲）", "大纲", 1)
    p_sci_01 = get_existing_path("ai-popular-science-series/AI科普系列-01-公众号版.html")
    if p_sci_01:
        add_article("ai-science", p_sci_01, "AI科普 01 · 通俗图解：大模型到底是怎么思考的？", "01 科普", 2)

    # 15. AI News
    p_news = get_existing_path("ai-news/AI资讯周刊-2026年第28期.html")
    if p_news:
        add_article("ai-news", p_news, "AI资讯周刊 · 2026 年第 28 期：大模型前沿突破与开源动态", "第28期", 1)

    # 16. Quant Trading
    p_quant = get_existing_path("quant-trading-agent/量化交易Agent系列-01-公众号版.html")
    if p_quant:
        add_article("quant-agent", p_quant, "量化交易 Agent 01 · 架构设计与自动化交易系统", "01 架构", 1)

    # 17. Business Growth
    p_bg = get_existing_path("business-growth/01-不用买服务器免备案搭建独立知识库.html")
    if p_bg:
        add_article("business-growth", p_bg, "独立知识库搭建复盘 · 不用买服务器、免备案：用 Cloudflare + GitHub 搭建知识库与 SEO 实战", "01 建站复盘", 1)
    p_bg2 = get_existing_path("business-growth/02-纯静态网站秒变智能知识库-Vector-RAG实战.html")
    if p_bg2:
        add_article("business-growth", p_bg2, "知识库 RAG 实战 · 纯静态站点秒变智能智库：用 Cloudflare Workers + Vector RAG 零成本打造 AI 伴学助手", "02 RAG实战", 2)

    # Filter categories: Remove explicitly hidden categories or categories with 0 published articles
    hidden_cats = exclude_config.get("hidden_categories", [])
    active_categories = []
    
    for cat in categories_data:
        if cat['id'] in hidden_cats:
            continue
        cat_items = [a for a in all_articles if a['categoryId'] == cat['id']]
        if len(cat_items) > 0:
            cat['count'] = len(cat_items)
            active_categories.append(cat)

    # Also remove articles whose category was hidden
    active_cat_ids = {c['id'] for c in active_categories}
    all_articles = [a for a in all_articles if a['categoryId'] in active_cat_ids]

    os.makedirs("assets", exist_ok=True)

    # Load Showcases / Works / Tools
    showcases_list = []
    if os.path.exists("showcases.json"):
        try:
            with open("showcases.json", "r", encoding="utf-8") as f:
                showcases_list = json.load(f)
        except Exception as e:
            print(f"⚠️ 读取 showcases.json 失败: {e}")

    site_data = {
        "siteTitle": "AI 全系列学习智库 · 体系化知识库",
        "siteSubtitle": "涵盖大模型底层原理、Agent 核心架构、智能客服实战、本地知识库 (RAG) 与 AI 编程实战工具链",
        "stats": {
            "totalCategories": len(active_categories),
            "totalArticles": len(all_articles),
            "totalShowcases": len(showcases_list)
        },
        "categories": active_categories,
        "articles": all_articles,
        "showcases": showcases_list
    }

    with open("assets/data.json", "w", encoding="utf-8") as f:
        json.dump(site_data, f, ensure_ascii=False, indent=2)

    with open("assets/data.js", "w", encoding="utf-8") as f:
        f.write("window.SITE_DATA = " + json.dumps(site_data, ensure_ascii=False, indent=2) + ";")

    # Generate SEO files (sitemap.xml and robots.txt)
    generate_seo_files(site_data)

    print(f"✅ 数据构建完成！")
    print(f"   - 生效系列分类: {len(active_categories)} 个")
    print(f"   - 展现文献篇目: {len(all_articles)} 篇")
    print(f"   - 原创作品工具: {len(showcases_list)} 款")
    print(f"   - 过滤排除文献: {excluded_count} 篇")
    return site_data

def generate_seo_files(site_data):
    base_url = "https://ailearning.top"
    now_date = "2026-08-28"
    
    # 1. robots.txt
    robots_content = f"""User-agent: *
Allow: /

Sitemap: {base_url}/sitemap.xml
"""
    with open("robots.txt", "w", encoding="utf-8") as f:
        f.write(robots_content)
        
    # 2. sitemap.xml
    urls = []
    # Homepage
    urls.append(f"""  <url>
    <loc>{base_url}/</loc>
    <lastmod>{now_date}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>\n""")
    
    # Roadmap
    urls.append(f"""  <url>
    <loc>{base_url}/#roadmap</loc>
    <lastmod>{now_date}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>\n""")
    
    # Categories
    for cat in site_data.get('categories', []):
        cat_id = cat.get('id')
        urls.append(f"""  <url>
    <loc>{base_url}/#cat={cat_id}</loc>
    <lastmod>{now_date}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>\n""")
        
    # Articles
    for art in site_data.get('articles', []):
        art_id = art.get('id')
        art_path = art.get('path', '')
        urls.append(f"""  <url>
    <loc>{base_url}/?id={art_id}</loc>
    <lastmod>{now_date}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>\n""")
        if art_path and art_path.endswith('.html'):
            urls.append(f"""  <url>
    <loc>{base_url}/{art_path}</loc>
    <lastmod>{now_date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>\n""")
            
    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{"".join(urls)}</urlset>"""

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_xml)
        
    print(f"   - 🌐 全球 SEO 索引已生成: robots.txt, sitemap.xml (收录 {len(urls)} 个独立页面链接)")
    
    # 自动同步更新 Vector RAG 知识库索引
    try:
        from build_rag_index import build_knowledge_base
        print("   - 🤖 正在同步构建 Vector RAG 知识库切片...")
        build_knowledge_base()
    except Exception as e:
        print(f"   - ⚠️ 构建 RAG 知识库切片失败: {e}")

if __name__ == '__main__':
    build_data()
