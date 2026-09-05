/**
 * AI 全系列学习智库 · 智能知识库助手 (Vector RAG + Cloudflare Worker AI 网关)
 * 具备端侧语义向量混合检索、流式打字生成、站内文献精准引证与无缝阅读器联动能力。
 */

(function () {
  'use strict';

  // 1. 网关端点配置：直连 Cloudflare AI 网关 (动态防伪时间戳签名 + 边缘频控鉴权)
  const RAG_CONFIG = {
    endpoint: 'https://api.ailearning.top/v1/chat/completions',
    model: 'auto',
    topK: 4,
    maxHistory: 6
  };

  // 动态防伪时间戳签名 (防重放、防盗刷、防外部爬虫调用)
  async function generateSecuritySign(path) {
    const ts = Date.now();
    const SALT = "ai_hub_sec_982f10";
    const raw = `${ts}:${path}:${SALT}`;
    try {
      const encoder = new TextEncoder();
      const data = encoder.encode(raw);
      const hashBuffer = await crypto.subtle.digest("SHA-256", data);
      const hashArray = Array.from(new Uint8Array(hashBuffer));
      const sign = hashArray.map(b => b.toString(16).padStart(2, "0")).join("").substring(0, 32);
      return { ts: String(ts), sign };
    } catch (e) {
      return { ts: String(ts), sign: "" };
    }
  }

  // 2. 状态管理
  const state = {
    isOpen: false,
    isMaximized: false,
    isGenerating: false,
    abortController: null,
    messages: [], // { role, content, references, timestamp }
    chunks: null, // 知识切片缓存
    isLoadingChunks: false
  };

  // 3. 停用词库（提升关键词提取与语义匹配召回率）
  const STOPWORDS = new Set([
    "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你",
    "会", "着", "没有", "看", "好", "自己", "这", "如何", "怎么", "什么", "可以", "这个", "那个", "因为", "所以", "如果", "我们",
    "他们", "它们", "由于", "同时", "并且", "以及", "通过", "进行", "对于", "关于", "之中", "其中", "或者", "还是", "为了", "而且",
    "请问", "帮我", "介绍", "讲讲", "解析", "一下", "怎样", "吗", "呢", "吧", "呀"
  ]);

  // 4. 异步加载知识切片库
  async function loadKnowledgeChunks() {
    if (state.chunks && state.chunks.length > 0) return state.chunks;
    if (window.KNOWLEDGE_CHUNKS && Array.isArray(window.KNOWLEDGE_CHUNKS)) {
      state.chunks = window.KNOWLEDGE_CHUNKS;
      return state.chunks;
    }
    if (state.isLoadingChunks) {
      // 等待加载完成
      while (state.isLoadingChunks) {
        await new Promise(r => setTimeout(r, 100));
      }
      return state.chunks || [];
    }

    state.isLoadingChunks = true;
    try {
      const resp = await fetch('assets/knowledge_chunks.json');
      if (resp.ok) {
        state.chunks = await resp.json();
      } else {
        console.warn('⚠️ 加载 assets/knowledge_chunks.json 失败，尝试等待 window.KNOWLEDGE_CHUNKS');
        state.chunks = window.KNOWLEDGE_CHUNKS || [];
      }
    } catch (e) {
      console.warn('⚠️ 读取 knowledge_chunks 出错，降级至 window.KNOWLEDGE_CHUNKS', e);
      state.chunks = window.KNOWLEDGE_CHUNKS || [];
    } finally {
      state.isLoadingChunks = false;
    }
    return state.chunks || [];
  }

  // 5. 端侧高精混合向量与语义检索器 (Vector / BM25 Hybrid Retriever)
  function retrieveRelevantChunks(query, chunks, topK = 4) {
    if (!chunks || chunks.length === 0 || !query.trim()) return [];

    // 分词：提取中文字词 (2~6字) 与 英文/代码符号 (>=2字符)
    const rawTerms = query.match(/[a-zA-Z0-9_\-\.]{2,}|[\u4e00-\u9fa5]{2,6}/g) || [];
    const queryTerms = rawTerms
      .map(t => t.toLowerCase().trim())
      .filter(t => t.length > 1 && !STOPWORDS.has(t));

    // 如果没有任何分词（如输入特殊符号），直接降级全字符匹配
    if (queryTerms.length === 0) {
      queryTerms.push(query.toLowerCase().trim());
    }

    // 针对用户查询中的核心领域专词做加权增强（Agent, RAG, Ollama, Claude, Transformer, Prompt 等）
    const techBoostMap = {
      'agent': ['agent', '智能体', '智能客服', 'react', '感知', '决策', '记忆', '工具调用', 'mcp'],
      'react': ['react', '思考', '行动', '观察', '循环', '推理'],
      'rag': ['rag', '知识库', '向量', '切片', '检索', 'embedding', 'ollama'],
      'ollama': ['ollama', '本地大模型', '私有化', '量化', 'gguf'],
      'claude': ['claude', 'claude code', 'prompt', 'coding', '编程'],
      'transformer': ['transformer', 'attention', '注意力', '自注意力', 'qkv', 'decoder', 'encoder']
    };

    const expandedTerms = new Set(queryTerms);
    for (const qt of queryTerms) {
      for (const [key, related] of Object.entries(techBoostMap)) {
        if (qt.includes(key) || key.includes(qt)) {
          related.forEach(r => expandedTerms.add(r));
        }
      }
    }

    const scored = [];
    const lowerQuery = query.toLowerCase();

    for (const chunk of chunks) {
      let score = 0.0;
      const cTitle = (chunk.title || '').toLowerCase();
      const cSec = (chunk.section || '').toLowerCase();
      const cCat = (chunk.category || '').toLowerCase();
      const cContent = (chunk.content || '').toLowerCase();
      const cKw = (chunk.keywords || []).map(k => k.toLowerCase());

      // 1. 完整 Query 连续子串匹配（极高权重）
      if (lowerQuery.length >= 3) {
        if (cTitle.includes(lowerQuery)) score += 25.0;
        if (cSec.includes(lowerQuery)) score += 15.0;
        if (cContent.includes(lowerQuery)) score += 8.0;
      }

      // 2. 词袋与关键词相关度匹配
      for (const term of expandedTerms) {
        const isOriginalTerm = queryTerms.includes(term);
        const weightMult = isOriginalTerm ? 1.0 : 0.4;

        if (cTitle.includes(term)) score += 12.0 * weightMult;
        if (cSec.includes(term)) score += 7.0 * weightMult;
        if (cCat.includes(term)) score += 4.0 * weightMult;
        if (cKw.some(k => k.includes(term))) score += 5.0 * weightMult;

        // 正文中出现频次计算 (带封顶抑制)
        if (cContent.includes(term)) {
          const count = (cContent.match(new RegExp(term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g')) || []).length;
          score += Math.min(count * 1.5, 6.0) * weightMult;
        }
      }

      if (score > 1.5) {
        scored.push({ score, chunk });
      }
    }

    // 按得分倒序排序
    scored.sort((a, b) => b.score - a.score);

    // 文档多样性去重：优先避免同一篇文章的连续重复切片霸榜
    const results = [];
    const seenArticles = new Map();

    for (const item of scored) {
      const artPath = item.chunk.path;
      const currentCount = seenArticles.get(artPath) || 0;
      // 每篇文章最多提供 2 个最精粹切片
      if (currentCount < 2) {
        results.push(item.chunk);
        seenArticles.set(artPath, currentCount + 1);
        if (results.length >= topK) break;
      }
    }

    // 如果多样性去重后不足 topK，再用得分最高的切片补齐
    if (results.length < topK) {
      for (const item of scored) {
        if (!results.includes(item.chunk)) {
          results.push(item.chunk);
          if (results.length >= topK) break;
        }
      }
    }

    return results;
  }

  // 6. 构造 RAG 增强 Prompt
  function buildRAGSystemPrompt(chunks) {
    let contextStr = '';
    if (chunks && chunks.length > 0) {
      contextStr = chunks.map((c, i) => {
        return `[参考资料 ${i + 1}] 《${c.title}》 - 章节：${c.section}\n专栏：${c.category} | 路径：${c.path}\n内容要点：${c.content}`;
      }).join('\n\n------------------------\n\n');
    }

    return `你是由微信公众号【大前端工程师】打造的「AI 全系列学习智库」(ailearning.top) 专属 AI 知识伴学专家。
你的职责是基于本站 167 篇权威体系化文献为读者提供准确、专业、通俗的答疑与技术辅导。

【🚨 核心话题边界与限制（严格执行）】：
- 你是专注于人工智能与计算机编程的专属技术导师。
- 你【仅被授权】探讨和解答与以下领域相关的问题：
  1. 人工智能 (AI)、机器学习、深度学习；
  2. 大语言模型 (LLM)、Transformer / Attention 底层原理、数学与算法；
  3. Agent 智能体核心架构（ReAct、感知决策、Memory 记忆机制、工具调用、多智能体协作、企业客服 Agent）；
  4. RAG 检索增强生成、向量数据库、Embeddings、切片策略、Ollama 本地私有化部署；
  5. AI Coding / AI 编程全栈实战（Claude Code、Cursor、Copilot、MCP 协议、Prompt 结构化工程）；
  6. 相关的计算机编程、代码实现、软件工程与技术落地。
- 【严禁回答与 AI 及计算机技术无关的生活话题】：
  如果用户的提问完全脱离 AI 与技术（例如：做菜食谱、天气预报、生活琐事、情感咨询、娱乐八卦、非技术类医疗健康、彩票占卜等日常生活非技术话题）：
  你必须【坚决拒绝回答该生活内容】，并礼貌回应：
  "抱歉，我是「AI 全系列学习智库」的专属技术学伴，专注于大模型、智能体 (Agent)、RAG 知识库、AI Coding 等人工智能技术领域。日常生活与非技术类问题不在我的解答范围内。欢迎向我咨询任何 AI 与技术落地相关的问题！"
  严禁在拒绝后顺带解答该非技术内容。

${contextStr ? `【智库实时检索到的高相关内容如下】：\n------------------------\n${contextStr}\n------------------------\n` : ''}

【回答指导原则】：
1. 优先根据上述智库检索切片的内容进行深度解答。讲透原理、底层机制与实战落地方法。
2. 格式请使用专业排版的 Markdown：善于使用 ### 小标题、**粗体**、有序/无序列表、以及带有语言标识的代码块（\`\`\`python, \`\`\`bash, \`\`\`json 等）。
3. 语言风格：专业、清晰、极客范儿且温暖有温度，像一位手把手带徒弟的资深架构师。
4. 在回答中，可以自然引用参考文章的专栏和章节名称，方便用户后续研读。
5. 请全程使用中文回答。`;
  }

  // 7. 轻量且安全的 Markdown 渲染器（支持标题、粗体、行内代码、语法代码块与链接）
  function renderMarkdown(md) {
    if (!md) return '';
    let html = md;

    // 保护代码块
    const codeBlocks = [];
    html = html.replace(/```([a-zA-Z0-9_\-\+]*)\n([\s\S]*?)```/g, (match, lang, code) => {
      const id = `__CODE_BLOCK_${codeBlocks.length}__`;
      codeBlocks.push({ lang: lang || 'text', code: code.trim() });
      return id;
    });

    // 保护行内代码
    const inlineCodes = [];
    html = html.replace(/`([^`\n]+)`/g, (match, code) => {
      const id = `__INLINE_CODE_${inlineCodes.length}__`;
      inlineCodes.push(escapeHtml(code));
      return id;
    });

    // 转义 HTML 标签（防止注入）
    html = escapeHtml(html);

    // 还原代码块
    codeBlocks.forEach((b, idx) => {
      const escapedCode = escapeHtml(b.code);
      const blockHtml = `
        <div class="my-3 rounded-xl overflow-hidden border border-white/10 bg-slate-950 text-xs shadow-md">
          <div class="flex items-center justify-between px-3 py-1.5 bg-slate-900/80 border-b border-white/10 text-[11px] text-slate-400 font-mono">
            <span class="uppercase tracking-wider font-semibold text-indigo-400">${b.lang}</span>
            <button onclick="window.AI_ASSISTANT.copyCode(this)" class="hover:text-white transition flex items-center gap-1 cursor-pointer">
              <span>📋</span><span>复制</span>
            </button>
          </div>
          <pre class="p-3 overflow-x-auto text-slate-200 font-mono leading-relaxed"><code>${escapedCode}</code></pre>
        </div>
      `;
      html = html.replace(`__CODE_BLOCK_${idx}__`, blockHtml);
    });

    // 还原行内代码
    inlineCodes.forEach((c, idx) => {
      html = html.replace(`__INLINE_CODE_${idx}__`, `<code class="px-1.5 py-0.5 mx-0.5 rounded bg-indigo-500/10 text-indigo-300 font-mono text-[12px] border border-indigo-500/20">${c}</code>`);
    });

    // 标题
    html = html.replace(/^### (.*$)/gim, '<h4 class="text-sm sm:text-base font-bold text-white mt-4 mb-2 flex items-center gap-1.5"><span class="text-indigo-400">✦</span>$1</h4>');
    html = html.replace(/^## (.*$)/gim, '<h3 class="text-base sm:text-lg font-black text-white mt-5 mb-2.5 flex items-center gap-2 pb-1 border-b border-white/10"><span class="text-indigo-500">▶</span>$1</h3>');
    html = html.replace(/^# (.*$)/gim, '<h2 class="text-lg sm:text-xl font-black text-white mt-6 mb-3">$1</h2>');

    // 粗体 & 斜体
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong class="font-bold text-indigo-300">$1</strong>');
    html = html.replace(/\*(.*?)\*/g, '<em class="italic text-slate-300">$1</em>');

    // 引用块
    html = html.replace(/^\> (.*$)/gim, '<blockquote class="border-l-2 border-indigo-500 pl-3 my-2 text-slate-400 italic text-xs sm:text-sm bg-indigo-500/5 py-1 rounded-r-lg">$1</blockquote>');

    // 无序列表
    html = html.replace(/^\s*[\-\*]\s+(.*$)/gim, '<li class="ml-4 list-disc text-slate-300 my-1 leading-relaxed">$1</li>');

    // 有序列表
    html = html.replace(/^\s*(\d+)\.\s+(.*$)/gim, '<li class="ml-4 list-decimal text-slate-300 my-1 leading-relaxed">$2</li>');

    // 段落换行
    html = html.split('\n\n').map(p => {
      p = p.trim();
      if (!p) return '';
      if (p.startsWith('<h') || p.startsWith('<div') || p.startsWith('<blockquote') || p.startsWith('<li')) {
        return p;
      }
      return `<p class="my-2 leading-relaxed text-slate-200 text-xs sm:text-sm">${p.replace(/\n/g, '<br>')}</p>`;
    }).join('');

    return html;
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // 8. 挂载 UI 结构
  function mountUI() {
    // 浮动唤醒按钮 (移动端胶囊化更紧凑，避免遮挡页面内容)
    const triggerBtn = document.createElement('div');
    triggerBtn.id = 'ai-assistant-trigger';
    triggerBtn.className = 'fixed bottom-5 right-4 sm:right-5 z-40 flex items-center group cursor-pointer transition-all duration-300';
    triggerBtn.innerHTML = `
      <div class="relative flex items-center gap-1.5 sm:gap-2 px-3 sm:px-4 py-2 sm:py-2.5 rounded-full bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white shadow-2xl hover:shadow-indigo-500/50 hover:scale-105 active:scale-95 transition-all duration-300 border border-white/20 select-none">
        <span class="text-base sm:text-xl animate-bounce">🤖</span>
        <span class="text-xs sm:text-sm font-bold tracking-wide">智库 AI</span>
        <span class="hidden sm:inline text-xs sm:text-sm font-bold tracking-wide">助手</span>
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
      </div>
    `;
    triggerBtn.addEventListener('click', toggleChat);
    document.body.appendChild(triggerBtn);

    // 聊天主体悬浮窗口 (移动端全屏无边框抽屉式体验，PC端悬浮卡片)
    const modal = document.createElement('div');
    modal.id = 'ai-assistant-modal';
    modal.className = 'fixed inset-0 sm:inset-auto sm:bottom-5 sm:right-5 z-50 flex flex-col glass sm:border sm:border-white/20 sm:rounded-3xl shadow-2xl overflow-hidden transition-all duration-300 opacity-0 pointer-events-none translate-y-6 bg-slate-900/95 backdrop-blur-2xl w-full sm:w-[460px] h-[100dvh] sm:h-[660px] sm:max-h-[90vh]';
    modal.innerHTML = `
      <!-- Mobile Drag Handle -->
      <div class="sm:hidden pt-2 pb-1 bg-slate-950/80 flex justify-center items-center cursor-pointer" id="ai-mobile-handle">
        <div class="w-10 h-1 bg-white/25 rounded-full"></div>
      </div>

      <!-- Header -->
      <div class="flex items-center justify-between px-3.5 sm:px-4 py-2.5 sm:py-3.5 bg-slate-950/70 border-b border-white/10 shrink-0">
        <div class="flex items-center gap-2 sm:gap-2.5 min-w-0">
          <div class="w-7 h-7 sm:w-8 sm:h-8 rounded-xl bg-gradient-to-tr from-indigo-600 to-purple-500 flex items-center justify-center text-sm sm:text-base shadow-inner shrink-0">
            🤖
          </div>
          <div class="min-w-0">
            <div class="font-bold text-xs sm:text-sm text-white flex items-center gap-1.5 truncate">
              <span>智库 AI 伴学助手</span>
              <span class="text-[9px] px-1.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 font-mono font-medium border border-emerald-500/30">Vector RAG</span>
            </div>
            <div class="text-[10px] text-slate-400 flex items-center gap-1 truncate">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 inline-block"></span>
              <span>Cloudflare AI 网关 · 167 篇智库</span>
            </div>
          </div>
        </div>

        <div class="flex items-center gap-1 shrink-0 text-slate-400">
          <!-- Clear History / New Chat -->
          <button id="ai-clear-btn" title="新建会话 (清空历史与上下文)" class="w-7 h-7 rounded-lg hover:bg-white/10 hover:text-white flex items-center justify-center text-xs transition cursor-pointer">
            🔄
          </button>
          <!-- Maximize Toggle (PC Only) -->
          <button id="ai-max-btn" title="最大化 / 还原" class="w-7 h-7 rounded-lg hover:bg-white/10 hover:text-white items-center justify-center text-xs transition hidden sm:flex cursor-pointer">
            ⛶
          </button>
          <!-- Close / Back -->
          <button id="ai-close-btn" title="关闭" class="w-7 h-7 rounded-lg hover:bg-white/10 hover:text-white flex items-center justify-center text-sm sm:text-base transition cursor-pointer">
            ✕
          </button>
        </div>
      </div>

      <!-- Chat Messages Container -->
      <div id="ai-messages-container" class="flex-1 overflow-y-auto p-3.5 sm:p-4 space-y-4 text-xs sm:text-sm scroll-smooth">
        ${getWelcomeCardHTML()}
      </div>

      <!-- Input Area with Safe Area Bottom Padding -->
      <div class="p-2.5 sm:p-3 bg-slate-950/90 border-t border-white/10 shrink-0 space-y-2 ai-safe-bottom">
        <div class="relative flex items-end gap-2">
          <textarea 
            id="ai-user-input" 
            rows="1" 
            placeholder="向 AI 智库提问技术问题... (仅限 AI / 编程技术)" 
            class="flex-1 max-h-32 min-h-[42px] px-3.5 py-2.5 rounded-2xl bg-white/5 border border-white/15 text-xs sm:text-sm text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition resize-none leading-relaxed"
          ></textarea>

          <!-- Action Button (Send / Stop) -->
          <button id="ai-send-btn" class="w-10 h-10 rounded-2xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 active:scale-95 text-white flex items-center justify-center transition shadow-lg shrink-0 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed" title="发送提问">
            <span id="ai-send-icon" class="text-base">🚀</span>
          </button>
        </div>

        <div class="flex items-center justify-between text-[10px] text-slate-500 px-1">
          <span class="flex items-center gap-1 text-indigo-400">
            <span>🛡️</span>
            <span>仅限 AI 与技术开发交流</span>
          </span>
          <span class="text-slate-400 font-mono">文献精准引证</span>
        </div>
      </div>
    `;
    document.body.appendChild(modal);

    // 移动端顶部把手支持下拉关闭
    const mobileHandle = document.getElementById('ai-mobile-handle');
    if (mobileHandle) {
      mobileHandle.addEventListener('click', closeChat);
    }


    // 绑定事件
    document.getElementById('ai-close-btn').addEventListener('click', (e) => {
      e.stopPropagation();
      closeChat();
    });
    document.getElementById('ai-clear-btn').addEventListener('click', clearHistory);
    document.getElementById('ai-max-btn').addEventListener('click', toggleMaximize);

    // 支持按下 ESC 键快捷关闭
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && state.isOpen) {
        closeChat();
      }
    });

    const inputEl = document.getElementById('ai-user-input');
    const sendBtn = document.getElementById('ai-send-btn');

    sendBtn.addEventListener('click', () => {
      if (state.isGenerating) {
        stopGenerating();
      } else {
        handleUserSubmit();
      }
    });

    inputEl.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleUserSubmit();
      }
    });

    // 自动高度调整
    inputEl.addEventListener('input', () => {
      inputEl.style.height = 'auto';
      inputEl.style.height = Math.min(inputEl.scrollHeight, 128) + 'px';
    });

    // 主页搜索框打通联动：在顶部搜索框右侧加入“问问 AI”便捷入口
    enhanceGlobalSearchBar();
  }

  // 9. 主页顶部搜索栏增强联动
  function enhanceGlobalSearchBar() {
    const searchContainer = document.querySelector('#hero-banner-section .max-w-2xl .relative.group');
    if (!searchContainer) return;

    // 添加快捷按钮
    const aiSearchBtn = document.createElement('button');
    aiSearchBtn.type = 'button';
    aiSearchBtn.className = 'hidden sm:flex items-center gap-1 px-2.5 py-1 rounded-xl bg-indigo-600/30 hover:bg-indigo-600 text-indigo-200 hover:text-white border border-indigo-500/40 transition text-xs font-semibold cursor-pointer mr-1 z-20';
    aiSearchBtn.innerHTML = `<span>🤖</span><span>AI 解答</span>`;
    aiSearchBtn.title = '用 AI 智库伴学助手深度解答该问题';

    aiSearchBtn.addEventListener('click', () => {
      const searchInput = document.getElementById('search-input');
      const val = searchInput ? searchInput.value.trim() : '';
      if (val) {
        openChatWithQuery(val);
      } else {
        toggleChat(true);
      }
    });

    const kbd = searchContainer.querySelector('kbd');
    if (kbd && kbd.parentElement) {
      kbd.parentElement.insertBefore(aiSearchBtn, kbd);
    }
  }

  // 10. 交互控制器
  function closeChat() {
    toggleChat(false);
  }

  function openChat() {
    toggleChat(true);
  }

  function toggleChat(forceOpen) {
    if (typeof forceOpen === 'boolean') {
      state.isOpen = forceOpen;
    } else {
      state.isOpen = !state.isOpen;
    }
    const modal = document.getElementById('ai-assistant-modal');
    const trigger = document.getElementById('ai-assistant-trigger');
    if (!modal) return;

    if (state.isOpen) {
      modal.classList.remove('opacity-0', 'pointer-events-none', 'translate-y-6');
      if (trigger) {
        trigger.classList.add('scale-0', 'opacity-0');
        trigger.classList.remove('scale-100', 'opacity-100');
      }
      // 预加载知识切片
      loadKnowledgeChunks();
      setTimeout(() => {
        const input = document.getElementById('ai-user-input');
        if (input) input.focus();
      }, 200);
    } else {
      modal.classList.add('opacity-0', 'pointer-events-none', 'translate-y-6');
      if (trigger) {
        trigger.classList.remove('scale-0', 'opacity-0');
        trigger.classList.add('scale-100', 'opacity-100');
      }
    }
  }

  function toggleMaximize() {
    state.isMaximized = !state.isMaximized;
    const modal = document.getElementById('ai-assistant-modal');
    const maxBtn = document.getElementById('ai-max-btn');
    if (!modal) return;

    if (state.isMaximized) {
      modal.classList.remove('sm:bottom-5', 'sm:right-5', 'sm:w-[460px]', 'sm:h-[660px]', 'sm:rounded-3xl');
      modal.classList.add('sm:inset-4', 'sm:w-auto', 'sm:h-auto', 'sm:rounded-2xl');
      if (maxBtn) maxBtn.textContent = '❐';
    } else {
      modal.classList.remove('sm:inset-4', 'sm:w-auto', 'sm:h-auto', 'sm:rounded-2xl');
      modal.classList.add('sm:bottom-5', 'sm:right-5', 'sm:w-[460px]', 'sm:h-[660px]', 'sm:rounded-3xl');
      if (maxBtn) maxBtn.textContent = '⛶';
    }
  }

  function getWelcomeCardHTML() {
    return `
      <div id="ai-welcome-card" class="p-4 rounded-2xl bg-white/5 border border-white/10 space-y-3">
        <div class="flex items-start gap-2.5">
          <span class="text-2xl">✨</span>
          <div>
            <h4 class="font-bold text-white text-sm">欢迎来到 AI 全系列学习智库！</h4>
            <p class="text-slate-300 text-xs mt-1 leading-relaxed">
              本站 167 篇深度专栏已通过标准 <strong class="text-indigo-400">Vector RAG</strong> 进行知识切片索引。你可以向我咨询任何大模型原理、Agent 手写、客服智能体、本地知识库、AI Coding 或 OpenClaw 体系知识！
            </p>
          </div>
        </div>

        <div class="pt-2 border-t border-white/10">
          <div class="text-[11px] font-bold text-slate-400 mb-2 flex items-center gap-1">
            <span>💡</span><span>猜你想问（点击直接提问）：</span>
          </div>
          <div class="flex flex-col gap-1.5">
            <button onclick="window.AI_ASSISTANT.askPreset('什么是 Agent 的 ReAct 决策与思考模式？')" class="text-left px-3 py-2 rounded-xl bg-white/5 hover:bg-indigo-600/30 hover:border-indigo-500/40 border border-white/5 text-slate-300 hover:text-white transition text-xs flex items-center justify-between group">
              <span>🤖 什么是 Agent 的 ReAct 决策模式？</span>
              <span class="text-slate-500 group-hover:text-indigo-400 group-hover:translate-x-0.5 transition">→</span>
            </button>
            <button onclick="window.AI_ASSISTANT.askPreset('如何使用 Ollama + RAG 快速搭建本地私有知识库？')" class="text-left px-3 py-2 rounded-xl bg-white/5 hover:bg-indigo-600/30 hover:border-indigo-500/40 border border-white/5 text-slate-300 hover:text-white transition text-xs flex items-center justify-between group">
              <span>📚 如何用 Ollama 搭建本地私有知识库？</span>
              <span class="text-slate-500 group-hover:text-indigo-400 group-hover:translate-x-0.5 transition">→</span>
            </button>
            <button onclick="window.AI_ASSISTANT.askPreset('Transformer 自注意力机制 (Self-Attention) 是如何计算的？')" class="text-left px-3 py-2 rounded-xl bg-white/5 hover:bg-indigo-600/30 hover:border-indigo-500/40 border border-white/5 text-slate-300 hover:text-white transition text-xs flex items-center justify-between group">
              <span>🧠 Transformer 自注意力机制计算流程是什么？</span>
              <span class="text-slate-500 group-hover:text-indigo-400 group-hover:translate-x-0.5 transition">→</span>
            </button>
            <button onclick="window.AI_ASSISTANT.askPreset('Claude Code 在实际开发中有哪些高效实战技巧与工作流？')" class="text-left px-3 py-2 rounded-xl bg-white/5 hover:bg-indigo-600/30 hover:border-indigo-500/40 border border-white/5 text-slate-300 hover:text-white transition text-xs flex items-center justify-between group">
              <span>⚡ Claude Code 最佳实战技巧与高产工作流？</span>
              <span class="text-slate-500 group-hover:text-indigo-400 group-hover:translate-x-0.5 transition">→</span>
            </button>
          </div>
        </div>
      </div>
    `;
  }

  function showToast(msg) {
    const toast = document.getElementById('toast');
    if (toast) {
      toast.innerHTML = `<span>✨</span><span>${escapeHtml(msg)}</span>`;
      toast.classList.remove('opacity-0', 'translate-y-4', 'pointer-events-none');
      setTimeout(() => {
        toast.classList.add('opacity-0', 'translate-y-4', 'pointer-events-none');
      }, 2000);
    }
  }

  function clearHistory() {
    const hasMessages = state.messages.length > 0;
    if (state.isGenerating) stopGenerating();
    state.messages = [];
    const container = document.getElementById('ai-messages-container');
    if (container) {
      container.innerHTML = getWelcomeCardHTML();
    }
    const inputEl = document.getElementById('ai-user-input');
    if (inputEl) {
      inputEl.value = '';
      inputEl.style.height = 'auto';
    }
    if (hasMessages) {
      showToast('✨ 已开启新对话，上下文已重置');
    } else {
      showToast('💡 当前已是初始会话，可直接提问');
    }
  }

  function openChatWithQuery(query) {
    toggleChat(true);
    const input = document.getElementById('ai-user-input');
    if (input) {
      input.value = query;
      handleUserSubmit();
    }
  }

  // 话题边界探测：检查是否属于明显脱离 AI / 计算机技术的日常生活话题
  function isObviousNonTechQuery(query) {
    const q = query.toLowerCase().trim();
    // 基础礼貌与问候放行
    if (/^(你好|您好|hi|hello|hey|在吗|早安|晚上好|你是谁|自我介绍)$/i.test(q)) {
      return false;
    }

    // 包含常见科技与 AI 核心词汇，直接放行
    const techAllowList = /ai|agent|rag|llm|gpt|claude|deepseek|qwen|ollama|model|prompt|code|coding|transformer|attention|python|js|vue|react|node|docker|api|mcp|linux|git|token|cuda|bge|embedding|智能|大模型|算法|向量|模型|代码|编程|框架|函数|数据库|知识库|架构|部署|前端|后端|分布式|嵌入|权重|梯度|微调|开源|开发|教程/i;
    if (techAllowList.test(q)) return false;

    // 常见与 AI/编程无关的日常生活话题模式
    const nonTechPatterns = [
      /做菜|食谱|菜谱|烹饪|食材|好吃的|西红柿|番茄|炒蛋|炒鸡蛋|红烧|蛋炒饭|火锅|怎么煮|炒菜|煲汤|怎么做饭|烧烤|烘焙|下厨房|买菜|好吃吗/,
      /今天天气|明天下雨|穿什么衣服|气温|多少度|冷不冷|热不热|防晒|天气预报/,
      /星座|八字|算命|运势|占卜|塔罗牌|属相|看相|风水/,
      /八卦|明星|出轨|绯闻|电视剧|电影推荐|演过什么|演唱会门票|周杰伦|王力宏/,
      /彩票|双色球|大乐透|中奖号码|刮刮乐|买彩票/,
      /肚子疼|头疼|感冒吃什么药|怀孕|挂什么科|吃什么药|生病怎么办/
    ];

    for (const pat of nonTechPatterns) {
      if (pat.test(q)) return true;
    }
    return false;
  }

  // 11. 处理用户发送提问
  async function handleUserSubmit() {
    const inputEl = document.getElementById('ai-user-input');
    const query = inputEl.value.trim();
    if (!query || state.isGenerating) return;

    inputEl.value = '';
    inputEl.style.height = 'auto';

    // 隐藏默认欢迎卡片
    const welcome = document.getElementById('ai-welcome-card');
    if (welcome) welcome.remove();

    // 1. 渲染用户消息
    appendUserMessage(query);

    // 2. 话题边界拦截：非 AI / 非技术类日常话题友好拒绝并重定向
    if (isObviousNonTechQuery(query)) {
      const refusalNotice = `抱歉，我是**「AI 全系列学习智库」**的专属技术伴学导师，专注于**大模型底层原理、Agent 智能体手写架构、本地知识库 (RAG)、AI Coding 编程实战与 OpenClaw 体系**等人工智能核心技术领域。\n\n日常生活琐事、娱乐八卦或非技术类问题不在本智库的解答范围内。\n\n你可以向我提问任何 AI 相关的技术问题，例如：\n- 🤖 *“什么是 Agent 的 ReAct 决策模式与核心循环？”*\n- 📚 *“如何使用 Ollama + RAG 快速搭建本地私有知识库？”*\n- 🧠 *“Transformer 自注意力机制 (Self-Attention) 是如何计算的？”*\n- ⚡ *“Claude Code 在日常开发中有哪些提效工作流？”*`;
      const botMsgObj = appendAssistantMessage('', []);
      botMsgObj.elem.innerHTML = renderMarkdown(refusalNotice);
      state.messages.push({ role: 'assistant', content: refusalNotice });
      return;
    }

    // 3. 检索相关知识切片
    const chunks = await loadKnowledgeChunks();
    const relevantChunks = retrieveRelevantChunks(query, chunks, RAG_CONFIG.topK);

    // 4. 准备助手回复气泡
    const botMsgObj = appendAssistantMessage('', relevantChunks);

    // 5. 调用 Cloudflare Worker AI 网关流式接口
    await streamChatCompletion(query, relevantChunks, botMsgObj);
  }

  // 12. 渲染用户消息
  function appendUserMessage(text) {
    const container = document.getElementById('ai-messages-container');
    const msgDiv = document.createElement('div');
    msgDiv.className = 'flex justify-end items-start gap-2.5';
    msgDiv.innerHTML = `
      <div class="max-w-[85%] px-4 py-2.5 rounded-2xl rounded-tr-sm bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-md leading-relaxed break-words">
        ${escapeHtml(text)}
      </div>
      <div class="w-7 h-7 rounded-xl bg-white/10 flex items-center justify-center text-xs shrink-0 mt-0.5 border border-white/10">
        👤
      </div>
    `;
    container.appendChild(msgDiv);
    container.scrollTop = container.scrollHeight;

    state.messages.push({ role: 'user', content: text });
  }

  // 13. 渲染助手流式消息容器
  function appendAssistantMessage(initialText, references) {
    const container = document.getElementById('ai-messages-container');
    const msgDiv = document.createElement('div');
    msgDiv.className = 'flex items-start gap-2.5';

    const msgId = 'bot-msg-' + Date.now();

    msgDiv.innerHTML = `
      <div class="w-7 h-7 rounded-xl bg-gradient-to-tr from-indigo-600 to-purple-500 flex items-center justify-center text-xs text-white shrink-0 mt-0.5 shadow-md">
        🤖
      </div>
      <div class="flex-1 min-w-0 max-w-[88%] space-y-2">
        <div id="${msgId}" class="px-4 py-3 rounded-2xl rounded-tl-sm bg-white/5 border border-white/10 text-slate-100 shadow-md">
          <div class="bot-content prose prose-invert max-w-none">
            <span class="inline-flex items-center gap-1.5 text-indigo-400 text-xs animate-pulse">
              <span>⚡</span><span>智库知识切片匹配中，正在构思回答...</span>
            </span>
          </div>
        </div>

        <!-- 引用文献卡片组 -->
        ${references && references.length > 0 ? `
          <div class="p-2.5 rounded-xl bg-slate-950/60 border border-white/10 space-y-1.5 text-[11px]">
            <div class="font-bold text-slate-400 flex items-center justify-between">
              <span class="flex items-center gap-1">
                <span>📚</span><span>参考智库文献 (${references.length} 篇)：</span>
              </span>
              <span class="text-[9px] text-emerald-400">已引证</span>
            </div>
            <div class="space-y-1">
              ${references.map((ref, idx) => `
                <div class="flex items-center justify-between gap-2 p-1.5 rounded-lg bg-white/5 hover:bg-indigo-600/20 border border-white/5 transition group">
                  <div class="min-w-0 flex items-center gap-1.5 truncate">
                    <span class="w-4 h-4 rounded-full bg-indigo-500/20 text-indigo-300 flex items-center justify-center text-[10px] shrink-0 font-bold">${idx + 1}</span>
                    <span class="text-slate-300 group-hover:text-white truncate font-medium">${escapeHtml(ref.title)}</span>
                    <span class="text-slate-500 text-[10px] shrink-0">· ${escapeHtml(ref.section)}</span>
                  </div>
                  <button onclick="window.AI_ASSISTANT.openArticle('${ref.path}')" class="px-2 py-0.5 rounded-md bg-indigo-600/30 hover:bg-indigo-600 text-indigo-300 hover:text-white text-[10px] font-semibold shrink-0 transition flex items-center gap-0.5 cursor-pointer">
                    <span>阅读</span><span>↗</span>
                  </button>
                </div>
              `).join('')}
            </div>
          </div>
        ` : ''}
      </div>
    `;

    container.appendChild(msgDiv);
    container.scrollTop = container.scrollHeight;

    return {
      id: msgId,
      elem: msgDiv.querySelector(`#${msgId} .bot-content`),
      references
    };
  }

  // 14. 调用 Cloudflare AI 网关并进行流式打字输出
  async function streamChatCompletion(userQuery, references, botMsgObj) {
    state.isGenerating = true;
    updateSendButtonState(true);

    const container = document.getElementById('ai-messages-container');
    state.abortController = new AbortController();

    // 组装历史消息
    const recentHistory = state.messages.slice(-RAG_CONFIG.maxHistory);
    const systemPrompt = buildRAGSystemPrompt(references);

    const apiMessages = [
      { role: 'system', content: systemPrompt },
      ...recentHistory
    ];

    let fullAnswer = '';

    try {
      const sig = await generateSecuritySign('/v1/chat/completions');
      const response = await fetch(RAG_CONFIG.endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-request-time': sig.ts,
          'x-request-sign': sig.sign
        },
        body: JSON.stringify({
          model: RAG_CONFIG.model,
          messages: apiMessages,
          stream: true,
          temperature: 0.6
        }),
        signal: state.abortController.signal
      });

      if (!response.ok) {
        throw new Error(`网关响应异常 HTTP ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let buffer = '';
      let isFirstChunk = true;

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed || !trimmed.startsWith('data:')) continue;
          if (trimmed === 'data: [DONE]') break;

          try {
            const dataStr = trimmed.replace(/^data:\s*/, '');
            const parsed = JSON.parse(dataStr);
            const delta = parsed.choices?.[0]?.delta;
            if (delta) {
              // 严格只提取最终回答 content，绝对不提取或拼接大模型内部思考过程 reasoning_content
              const textChunk = (delta.content !== undefined && delta.content !== null) ? delta.content : '';
              if (textChunk) {
                if (isFirstChunk) {
                  botMsgObj.elem.innerHTML = '';
                  isFirstChunk = false;
                }
                fullAnswer += textChunk;
                botMsgObj.elem.innerHTML = renderMarkdown(fullAnswer) + '<span class="inline-block w-1.5 h-3.5 bg-indigo-400 ml-0.5 animate-pulse align-middle"></span>';
                container.scrollTop = container.scrollHeight;
              }
            }
          } catch (err) {
            // ignore partial JSON parse error
          }
        }
      }

      // 渲染最终结果
      botMsgObj.elem.innerHTML = renderMarkdown(fullAnswer || '抱歉，暂时未能生成有效回答，请重试。');
      state.messages.push({ role: 'assistant', content: fullAnswer });

    } catch (err) {
      if (err.name === 'AbortError') {
        botMsgObj.elem.innerHTML = renderMarkdown(fullAnswer + '\n\n*(已手动停止生成)*');
      } else {
        console.error('AI Gateway Error:', err);
        botMsgObj.elem.innerHTML = `
          <div class="p-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-xs space-y-1">
            <div class="font-bold flex items-center gap-1"><span>⚠️</span><span>网关请求失败</span></div>
            <div>${escapeHtml(err.message || '网络异常，无法连接至 Cloudflare AI 网关。')}</div>
          </div>
        `;
      }
    } finally {
      state.isGenerating = false;
      state.abortController = null;
      updateSendButtonState(false);
      container.scrollTop = container.scrollHeight;
    }
  }

  function stopGenerating() {
    if (state.abortController) {
      state.abortController.abort();
    }
  }

  function updateSendButtonState(generating) {
    const icon = document.getElementById('ai-send-icon');
    const btn = document.getElementById('ai-send-btn');
    if (!icon || !btn) return;

    if (generating) {
      icon.textContent = '⏹';
      btn.title = '停止生成';
      btn.classList.add('from-red-600', 'to-rose-600');
      btn.classList.remove('from-indigo-600', 'to-purple-600');
    } else {
      icon.textContent = '🚀';
      btn.title = '发送提问';
      btn.classList.remove('from-red-600', 'to-rose-600');
      btn.classList.add('from-indigo-600', 'to-purple-600');
    }
  }

  // 15. 导出供全局调用的方法
  window.AI_ASSISTANT = {
    toggle: toggleChat,
    open: openChat,
    close: closeChat,
    askPreset: function (query) {
      openChatWithQuery(query);
    },
    openArticle: function (path) {
      if (window.AI_HUB && typeof window.AI_HUB.openReaderByPath === 'function') {
        window.AI_HUB.openReaderByPath(path);
      } else {
        window.open(path, '_blank');
      }
    },
    copyCode: function (btn) {
      const pre = btn.closest('.my-3').querySelector('pre code');
      if (pre) {
        navigator.clipboard.writeText(pre.innerText).then(() => {
          const original = btn.innerHTML;
          btn.innerHTML = '<span>✅</span><span>已复制</span>';
          setTimeout(() => { btn.innerHTML = original; }, 2000);
        });
      }
    }
  };

  // 16. 初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mountUI);
  } else {
    mountUI();
  }

})();
