#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 学习智库 · 知识库切块与向量 RAG 索引构建器
扫描所有 167 篇专栏文章，按大纲/语义切片，提取关键词并输出静态可加载的知识库切块数据。
"""

import os
import re
import json
from collections import Counter

DATA_JSON_PATH = "assets/data.json"
OUTPUT_CHUNKS_JSON = "assets/knowledge_chunks.json"
OUTPUT_CHUNKS_JS = "assets/knowledge_chunks.js"

# Common stopwords in Chinese & technical text for better keyword extraction
STOPWORDS = set([
    "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你",
    "会", "着", "没有", "看", "好", "自己", "这", "如何", "怎么", "什么", "可以", "这个", "那个", "因为", "所以", "如果", "我们",
    "他们", "它们", "由于", "同时", "并且", "以及", "通过", "进行", "对于", "关于", "之中", "其中", "或者", "还是", "为了", "而且"
])

def clean_html_content(raw_html):
    """Clean styles, scripts and HTML tags from raw html."""
    if not raw_html:
        return ""
    text = re.sub(r'<style.*?</style>', '', raw_html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<head.*?</head>', '', text, flags=re.DOTALL | re.IGNORECASE)
    # Extract headers and paragraphs with spacing
    text = re.sub(r'</(h[1-6]|p|div|li|tr|blockquote)>', '\n\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<[^>]+>', '', text)
    # Decode basic entities
    text = text.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&').replace('&quot;', '"')
    return text.strip()

def extract_sections(raw_content, is_html=True):
    """Split article into section-level blocks based on headers."""
    sections = []
    
    if is_html:
        # Regex to find headings h2, h3
        header_pattern = re.compile(r'<(h[2-4])[^>]*>(.*?)</\1>', flags=re.DOTALL | re.IGNORECASE)
        pos = 0
        current_header = "前言与概述"
        
        for match in header_pattern.finditer(raw_content):
            start, end = match.span()
            prev_content = raw_content[pos:start]
            clean_prev = clean_html_content(prev_content)
            if clean_prev and len(clean_prev) > 80:
                sections.append({
                    "section": current_header,
                    "text": clean_prev
                })
            header_text = re.sub(r'<[^>]+>', '', match.group(2)).strip()
            current_header = header_text or current_header
            pos = end
            
        remaining = raw_content[pos:]
        clean_rem = clean_html_content(remaining)
        if clean_rem and len(clean_rem) > 80:
            sections.append({
                "section": current_header,
                "text": clean_rem
            })
    else:
        lines = raw_content.split('\n')
        current_header = "前言与概述"
        current_lines = []
        for line in lines:
            if re.match(r'^#{2,4}\s+(.+)', line):
                if current_lines:
                    text_block = '\n'.join(current_lines).strip()
                    if len(text_block) > 60:
                        sections.append({
                            "section": current_header,
                            "text": text_block
                        })
                    current_lines = []
                current_header = re.sub(r'^#{2,4}\s+', '', line).strip()
            else:
                current_lines.append(line)
        if current_lines:
            text_block = '\n'.join(current_lines).strip()
            if len(text_block) > 60:
                sections.append({
                    "section": current_header,
                    "text": text_block
                })

    return sections

def chunk_text(text, max_len=600, overlap=100):
    """Chunk long text into overlapping blocks of max_len characters."""
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    chunks = []
    curr = ""
    for p in paragraphs:
        if len(curr) + len(p) > max_len and curr:
            chunks.append(curr.strip())
            curr = curr[-overlap:] + " " + p if len(curr) > overlap else p
        else:
            curr = (curr + "\n" + p).strip() if curr else p
    if curr and len(curr) > 50:
        chunks.append(curr.strip())
    return chunks

def extract_keywords(text, top_k=8):
    """Extract Chinese & English technical terms as chunk keywords."""
    words = re.findall(r'[a-zA-Z0-9_\-\.]{2,}|[\u4e00-\u9fa5]{2,6}', text)
    filtered = [w for w in words if w.lower() not in STOPWORDS and len(w) > 1]
    counts = Counter(filtered)
    return [w for w, _ in counts.most_common(top_k)]

def build_knowledge_base():
    if not os.path.exists(DATA_JSON_PATH):
        print(f"Error: {DATA_JSON_PATH} not found!")
        return

    with open(DATA_JSON_PATH, "r", encoding="utf-8") as f:
        site_data = json.load(f)

    articles = site_data.get("articles", [])
    categories = {c["id"]: c["name"] for c in site_data.get("categories", [])}

    print(f"Loaded {len(articles)} articles from {DATA_JSON_PATH}. Processing...")

    all_chunks = []
    chunk_id = 1

    for art in articles:
        p = art.get("path", "")
        if not os.path.exists(p):
            continue

        cat_id = art.get("categoryId", "")
        cat_name = categories.get(cat_id, "综合技术")
        art_title = art.get("title", "")
        is_html = p.endswith(".html")

        with open(p, "r", encoding="utf-8", errors="ignore") as f:
            raw_content = f.read()

        sections = extract_sections(raw_content, is_html=is_html)
        if not sections:
            clean_body = clean_html_content(raw_content) if is_html else raw_content
            sections = [{"section": "全篇要点", "text": clean_body}]

        for sec in sections:
            sec_title = sec["section"]
            sec_text = sec["text"]

            sub_chunks = chunk_text(sec_text, max_len=600, overlap=80)
            for sub in sub_chunks:
                clean_chunk_text = ' '.join(sub.split())
                if len(clean_chunk_text) < 40:
                    continue

                keywords = extract_keywords(art_title + " " + sec_title + " " + clean_chunk_text, top_k=6)

                all_chunks.append({
                    "id": chunk_id,
                    "title": art_title,
                    "section": sec_title,
                    "category": cat_name,
                    "path": p,
                    "keywords": keywords,
                    "content": clean_chunk_text[:500]
                })
                chunk_id += 1

    print(f"Generated {len(all_chunks)} knowledge chunks!")

    # Write JSON
    os.makedirs(os.path.dirname(OUTPUT_CHUNKS_JSON), exist_ok=True)
    with open(OUTPUT_CHUNKS_JSON, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=None)

    # Write JS format for static usage
    with open(OUTPUT_CHUNKS_JS, "w", encoding="utf-8") as f:
        f.write("window.KNOWLEDGE_CHUNKS = ")
        json.dump(all_chunks, f, ensure_ascii=False, indent=None)
        f.write(";\n")

    json_size = os.path.getsize(OUTPUT_CHUNKS_JSON)
    js_size = os.path.getsize(OUTPUT_CHUNKS_JS)
    print(f"Saved: {OUTPUT_CHUNKS_JSON} ({json_size / 1024:.1f} KB)")
    print(f"Saved: {OUTPUT_CHUNKS_JS} ({js_size / 1024:.1f} KB)")

if __name__ == "__main__":
    build_knowledge_base()
