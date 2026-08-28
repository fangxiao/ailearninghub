/**
 * AI 全系列学习智库 - 交互核心逻辑 (app.js)
 */

(function () {
  'use strict';

  // State Management
  const state = {
    data: window.SITE_DATA || { categories: [], articles: [], stats: {} },
    activeCategory: 'all',
    searchQuery: '',
    difficultyFilter: 'all',
    viewMode: 'roadmap', // 'roadmap' (default) | 'grid' | 'tree' | 'list'
    theme: localStorage.getItem('ai_hub_theme') || 'dark',
    readerTheme: localStorage.getItem('ai_hub_reader_theme') || 'default',
    readerFontSize: parseInt(localStorage.getItem('ai_hub_reader_fontsize') || '16', 10),
    currentArticle: null,
    bookmarks: JSON.parse(localStorage.getItem('ai_hub_bookmarks') || '[]'),
    history: JSON.parse(localStorage.getItem('ai_hub_history') || '[]'),
  };

  // DOM Elements
  const el = {
    app: document.getElementById('app'),
    themeToggle: document.getElementById('theme-toggle'),
    themeIcon: document.getElementById('theme-icon'),
    searchInput: document.getElementById('search-input'),
    searchClear: document.getElementById('search-clear'),
    categoryTabs: document.getElementById('category-tabs'),
    categorySelect: document.getElementById('category-select'),
    viewButtons: document.querySelectorAll('[data-view]'),
    mainContent: document.getElementById('main-content'),
    statsArticles: document.getElementById('stat-articles'),
    statsCategories: document.getElementById('stat-categories'),
    readerModal: document.getElementById('reader-modal'),
    readerIframeContainer: document.getElementById('reader-iframe-container'),
    readerMarkdownContainer: document.getElementById('reader-markdown-container'),
    readerFrame: document.getElementById('reader-frame'),
    markdownContent: document.getElementById('markdown-content'),
    readerTitle: document.getElementById('reader-title'),
    readerCategory: document.getElementById('reader-category'),
    readerTocList: document.getElementById('reader-toc-list'),
    readerTocDrawer: document.getElementById('reader-toc-drawer'),
    wechatModal: document.getElementById('wechat-modal'),
    btnPrevArticle: document.getElementById('btn-prev-article'),
    btnNextArticle: document.getElementById('btn-next-article'),
    btnBookmark: document.getElementById('btn-bookmark'),
    btnOpenExternal: document.getElementById('btn-open-external'),
    btnCloseReader: document.getElementById('btn-close-reader'),
    btnToggleToc: document.getElementById('btn-toggle-toc'),
    toast: document.getElementById('toast'),
  };

  // Initialize App
  function init() {
    applyTheme(state.theme);
    renderStats();
    renderCategoryTabs();
    renderCategorySelect();
    bindEvents();
    renderMainView();

    // Check URL parameters for direct link to article or category
    const urlParams = new URLSearchParams(window.location.search);
    const catParam = urlParams.get('category');
    const articleParam = urlParams.get('article');
    const viewParam = urlParams.get('view');

    if (viewParam && ['grid', 'list', 'tree', 'shelf', 'roadmap', 'my-space'].includes(viewParam)) {
      state.viewMode = viewParam;
      updateViewButtons();
    }

    if (catParam && (catParam === 'all' || state.data.categories.some(c => c.id === catParam))) {
      state.activeCategory = catParam;
      updateCategoryTabs();
    }

    if (articleParam) {
      const art = state.data.articles.find(a => a.id === articleParam || a.path === articleParam);
      if (art) {
        openReader(art);
      }
    }
  }

  // Theme Management
  function applyTheme(theme) {
    state.theme = theme;
    localStorage.setItem('ai_hub_theme', theme);
    if (theme === 'light') {
      document.documentElement.classList.add('light-theme');
      document.documentElement.classList.remove('dark');
      if (el.themeIcon) el.themeIcon.innerHTML = '☀️';
    } else {
      document.documentElement.classList.remove('light-theme');
      document.documentElement.classList.add('dark');
      if (el.themeIcon) el.themeIcon.innerHTML = '🌙';
    }
  }

  function toggleTheme() {
    applyTheme(state.theme === 'dark' ? 'light' : 'dark');
  }

  // Toast Notification
  let toastTimeout;
  function showToast(msg, icon = '✨') {
    if (!el.toast) return;
    el.toast.innerHTML = `<span class="text-xl">${icon}</span><span>${msg}</span>`;
    el.toast.classList.remove('opacity-0', 'translate-y-4', 'pointer-events-none');
    el.toast.classList.add('opacity-100', 'translate-y-0');
    clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => {
      el.toast.classList.add('opacity-0', 'translate-y-4', 'pointer-events-none');
      el.toast.classList.remove('opacity-100', 'translate-y-0');
    }, 2400);
  }

  // Statistics
  function renderStats() {
    if (el.statsArticles) el.statsArticles.textContent = state.data.articles.length;
    if (el.statsCategories) el.statsCategories.textContent = state.data.categories.length;
    if (el.statsEbooks) el.statsEbooks.textContent = state.data.categories.find(c => c.id === 'ebooks')?.count || 7;
  }

  // Category Tabs Navigation (Pure clean labels without numbers, multi-row flex-wrap)
  function renderCategoryTabs() {
    if (!el.categoryTabs) return;
    const categories = state.data.categories;

    let html = `
      <button data-category="all" class="category-tab px-3.5 py-1.5 rounded-xl text-xs font-medium border flex items-center gap-1.5 transition ${state.activeCategory === 'all' ? 'active' : 'border-white/10 text-slate-400 hover:text-white hover:bg-white/5'}">
        <span>🌐</span>
        <span>全部分类</span>
      </button>
    `;

    categories.forEach(cat => {
      const isActive = state.activeCategory === cat.id;
      html += `
        <button data-category="${cat.id}" class="category-tab px-3.5 py-1.5 rounded-xl text-xs font-medium border flex items-center gap-1.5 transition ${isActive ? 'active' : 'border-white/10 text-slate-400 hover:text-white hover:bg-white/5'}">
          <span>${cat.icon}</span>
          <span>${cat.name}</span>
        </button>
      `;
    });

    el.categoryTabs.innerHTML = html;
  }

  function renderCategorySelect() {
    if (!el.categorySelect) return;
    let html = `<option value="all">🌐 全部系列分类 (${state.data.articles.length} 篇)</option>`;
    state.data.categories.forEach(cat => {
      html += `<option value="${cat.id}">${cat.icon} ${cat.name} (${cat.count} 篇)</option>`;
    });
    el.categorySelect.innerHTML = html;
    el.categorySelect.value = state.activeCategory;
  }

  function updateCategoryTabs() {
    document.querySelectorAll('.category-tab').forEach(tab => {
      if (tab.dataset.category === state.activeCategory) {
        tab.classList.add('active');
        tab.classList.remove('border-white/10', 'text-slate-400', 'hover:bg-white/5');
      } else {
        tab.classList.remove('active');
        tab.classList.add('border-white/10', 'text-slate-400', 'hover:bg-white/5');
      }
    });
    if (el.categorySelect) el.categorySelect.value = state.activeCategory;
  }

  function updateViewButtons() {
    el.viewButtons.forEach(btn => {
      if (btn.dataset.view === state.viewMode) {
        btn.classList.add('bg-indigo-600', 'text-white');
        btn.classList.remove('text-slate-400', 'hover:text-white', 'hover:bg-white/5');
      } else {
        btn.classList.remove('bg-indigo-600', 'text-white');
        btn.classList.add('text-slate-400', 'hover:text-white', 'hover:bg-white/5');
      }
    });
  }

  // Filter Articles
  function getFilteredArticles() {
    return state.data.articles.filter(art => {
      if (state.activeCategory !== 'all' && art.categoryId !== state.activeCategory) {
        return false;
      }
      if (state.searchQuery) {
        const q = state.searchQuery.toLowerCase();
        const titleMatch = art.title.toLowerCase().includes(q);
        const subMatch = (art.subtitle || '').toLowerCase().includes(q);
        const summaryMatch = (art.summary || '').toLowerCase().includes(q);
        const tocMatch = (art.toc || []).some(t => t.toLowerCase().includes(q));
        const badgeMatch = (art.badge || '').toLowerCase().includes(q);
        if (!titleMatch && !subMatch && !summaryMatch && !tocMatch && !badgeMatch) {
          return false;
        }
      }
      return true;
    });
  }

  // Main View Dispatcher
  function renderMainView() {
    if (!el.mainContent) return;

    if (state.viewMode === 'grid') {
      renderGridView();
    } else if (state.viewMode === 'list') {
      renderListView();
    } else if (state.viewMode === 'tree') {
      renderTreeView();
    } else if (state.viewMode === 'shelf') {
      renderShelfView();
    } else if (state.viewMode === 'roadmap') {
      renderRoadmapView();
    } else if (state.viewMode === 'my-space') {
      renderMySpaceView();
    }
  }

  // Helper: Highlight text
  function highlight(text) {
    if (!state.searchQuery || !text) return text;
    const escaped = state.searchQuery.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const regex = new RegExp(`(${escaped})`, 'gi');
    return text.replace(regex, '<mark class="bg-amber-400/30 text-amber-300 px-1 rounded">$1</mark>');
  }

  // 1. Grid View (卡片矩阵视图)
  function renderGridView() {
    const articles = getFilteredArticles();
    const categories = state.data.categories;

    if (articles.length === 0) {
      el.mainContent.innerHTML = renderEmptyState();
      return;
    }

    if (state.activeCategory !== 'all' || state.searchQuery || state.formatFilter !== 'all') {
      const currentCat = categories.find(c => c.id === state.activeCategory);
      let headerHtml = '';

      if (currentCat && !state.searchQuery) {
        headerHtml = renderCategoryHeader(currentCat, articles);
      } else if (state.searchQuery) {
        headerHtml = `
          <div class="mb-8 p-6 rounded-2xl glass border border-white/10 flex items-center justify-between">
            <div>
              <div class="text-sm text-indigo-400 font-medium">搜索结果</div>
              <h2 class="text-2xl font-bold mt-1 text-white">找到 <span class="text-indigo-400">${articles.length}</span> 篇匹配文档</h2>
              <p class="text-sm text-slate-400 mt-1">关键字："${state.searchQuery}"</p>
            </div>
            <button id="btn-clear-search-res" class="px-4 py-2 text-xs rounded-xl bg-white/10 hover:bg-white/20 text-white transition">清空搜索</button>
          </div>
        `;
      }

      el.mainContent.innerHTML = `
        ${headerHtml}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-fade-in">
          ${articles.map(renderArticleCard).join('')}
        </div>
      `;

      const clearBtn = document.getElementById('btn-clear-search-res');
      if (clearBtn) {
        clearBtn.addEventListener('click', () => {
          state.searchQuery = '';
          el.searchInput.value = '';
          renderMainView();
        });
      }
      return;
    }

    let html = '';
    categories.forEach(cat => {
      const catArticles = state.data.articles.filter(a => a.categoryId === cat.id);
      if (catArticles.length === 0) return;

      const firstArticle = catArticles[0];

      html += `
        <div class="mb-14" id="cat-section-${cat.id}">
          <!-- Category Header -->
          <div class="p-6 md:p-8 rounded-3xl glass border border-white/10 mb-6 relative overflow-hidden">
            <div class="absolute right-0 top-0 w-64 h-64 bg-${cat.theme}-500/10 blur-3xl pointer-events-none"></div>
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 relative z-10">
              <div class="flex items-start md:items-center gap-4">
                <div class="w-14 h-14 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-3xl shadow-inner shrink-0">
                  ${cat.icon}
                </div>
                <div>
                  <div class="flex items-center gap-2 flex-wrap">
                    <h2 class="text-2xl font-bold text-white">${cat.name}</h2>
                    <span class="badge-chip bg-${cat.theme}-500/20 text-${cat.theme}-400 border border-${cat.theme}-500/30">${cat.badge}</span>
                    <span class="text-xs text-slate-400 bg-white/5 px-2.5 py-1 rounded-full border border-white/5">共 ${catArticles.length} 篇</span>
                  </div>
                  <p class="text-sm text-slate-300 mt-2 max-w-2xl">${cat.desc}</p>
                </div>
              </div>
              <div class="flex items-center gap-2.5 shrink-0">
                <button onclick="window.AI_HUB.switchCategory('${cat.id}')" class="px-4 py-2 text-xs font-semibold rounded-xl bg-white/10 hover:bg-white/20 text-white transition flex items-center gap-1.5 border border-white/10">
                  <span>查看该系列全部</span>
                  <span>→</span>
                </button>
                ${firstArticle ? `
                  <button onclick="window.AI_HUB.openReaderById('${firstArticle.id}')" class="px-4 py-2 text-xs font-semibold rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white transition shadow-lg shadow-indigo-500/20 flex items-center gap-1.5">
                    <span>⚡ 从第 1 章开始</span>
                  </button>
                ` : ''}
              </div>
            </div>
          </div>

          <!-- Cards Grid (Top 6) -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            ${catArticles.slice(0, 6).map(renderArticleCard).join('')}
          </div>

          ${catArticles.length > 6 ? `
            <div class="text-center mt-6">
              <button onclick="window.AI_HUB.switchCategory('${cat.id}')" class="px-6 py-2.5 rounded-2xl glass text-xs font-medium text-slate-300 hover:text-white hover:border-indigo-500/50 transition">
                查看该系列剩余 ${catArticles.length - 6} 篇文档 ↓
              </button>
            </div>
          ` : ''}
        </div>
      `;
    });

    el.mainContent.innerHTML = html;
  }

  function renderCategoryHeader(cat, articles) {
    return `
      <div class="p-6 md:p-8 rounded-3xl glass border border-white/10 mb-8 relative overflow-hidden">
        <div class="absolute right-0 top-0 w-80 h-80 bg-${cat.theme}-500/15 blur-3xl pointer-events-none"></div>
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-6 relative z-10">
          <div class="flex items-start gap-4">
            <div class="w-16 h-16 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-4xl shadow-inner shrink-0">
              ${cat.icon}
            </div>
            <div>
              <div class="flex items-center gap-2 flex-wrap">
                <h2 class="text-2xl md:text-3xl font-bold text-white">${cat.name}</h2>
                <span class="badge-chip bg-${cat.theme}-500/20 text-${cat.theme}-400 border border-${cat.theme}-500/30">${cat.badge}</span>
                <span class="badge-chip bg-white/5 text-slate-300 border border-white/10">${cat.difficulty}</span>
                <span class="text-xs text-slate-400 bg-white/5 px-2.5 py-1 rounded-full border border-white/5">共 ${articles.length} 篇精选</span>
              </div>
              <p class="text-sm md:text-base text-slate-300 mt-2 max-w-2xl">${cat.desc}</p>
            </div>
          </div>

          <div class="flex flex-wrap items-center gap-3 shrink-0">
            <button onclick="window.AI_HUB.openReaderById('${articles[0]?.id}')" class="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm transition shadow-lg shadow-indigo-500/20 flex items-center gap-2">
              <span>⚡ 从第 1 章开始阅读</span>
            </button>
          </div>
        </div>
      </div>
    `;
  }

  function renderArticleCard(art) {
    const isBookmarked = state.bookmarks.includes(art.id);
    const cat = state.data.categories.find(c => c.id === art.categoryId) || {};

    let formatBadgeColor = 'bg-blue-500/20 text-blue-400 border-blue-500/30';
    if (art.format === 'pdf') formatBadgeColor = 'bg-rose-500/20 text-rose-400 border-rose-500/30';
    if (art.format === 'md') formatBadgeColor = 'bg-amber-500/20 text-amber-400 border-amber-500/30';

    return `
      <div class="article-card rounded-2xl glass border border-white/10 p-6 flex flex-col justify-between relative group">
        <div>
          <div class="flex items-center justify-between gap-2 mb-3">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="badge-chip ${formatBadgeColor} border">${art.badge}</span>
              <span class="text-xs text-slate-400 flex items-center gap-1">
                <span>⏱️</span>
                <span>${art.readTime}</span>
              </span>
              <span class="text-xs text-slate-400 bg-white/5 px-2 py-0.5 rounded-md">${art.sizeStr}</span>
            </div>
            <div class="flex items-center gap-1.5">
              <button onclick="window.AI_HUB.toggleBookmark('${art.id}', event)" title="${isBookmarked ? '取消收藏' : '加入收藏'}" class="w-8 h-8 rounded-lg flex items-center justify-center transition ${isBookmarked ? 'bg-amber-400/20 text-amber-300' : 'text-slate-400 hover:bg-white/10 hover:text-white'}">
                ${isBookmarked ? '★' : '☆'}
              </button>
            </div>
          </div>

          <h3 class="text-lg font-bold text-white group-hover:text-indigo-400 transition line-clamp-2 cursor-pointer" onclick="window.AI_HUB.openReaderById('${art.id}')">
            ${highlight(art.title)}
          </h3>

          ${art.subtitle ? `
            <div class="text-xs font-medium text-indigo-400/90 mt-1.5 line-clamp-1">
              ${highlight(art.subtitle)}
            </div>
          ` : ''}

          <p class="text-xs text-slate-400 mt-2.5 line-clamp-3 leading-relaxed">
            ${highlight(art.summary || '点击进入阅读全篇详细图文内容与技术拆解。')}
          </p>
        </div>

        <div class="pt-5 mt-5 border-t border-white/5 flex items-center justify-between gap-3">
          <div class="flex items-center gap-1.5 text-xs text-slate-400">
            <span>${cat.icon || '📁'}</span>
            <span class="truncate max-w-[120px]">${cat.name || '系列文档'}</span>
          </div>

          <div class="flex items-center gap-2">
            <a href="${art.path}" target="_blank" title="新标签页打开" class="w-8 h-8 rounded-xl bg-white/5 hover:bg-white/15 text-slate-300 hover:text-white flex items-center justify-center text-xs transition border border-white/10">
              ↗
            </a>
            <button onclick="window.AI_HUB.openReaderById('${art.id}')" class="px-3.5 py-1.5 rounded-xl bg-indigo-600/90 hover:bg-indigo-500 text-white text-xs font-medium transition shadow-md shadow-indigo-500/10 flex items-center gap-1">
              <span>阅读</span>
              <span>→</span>
            </button>
          </div>
        </div>
      </div>
    `;
  }

  // 2. List View (精简清单表格与移动端自适应卡片)
  function renderListView() {
    const articles = getFilteredArticles();
    if (articles.length === 0) {
      el.mainContent.innerHTML = renderEmptyState();
      return;
    }

    el.mainContent.innerHTML = `
      <div class="rounded-2xl sm:rounded-3xl glass border border-white/10 overflow-hidden animate-fade-in">
        <div class="p-4 sm:p-6 border-b border-white/10 flex items-center justify-between">
          <div>
            <h3 class="text-lg sm:text-xl font-bold text-white">文档速查列表</h3>
            <p class="text-xs text-slate-400 mt-0.5">共找到 ${articles.length} 篇相关资料</p>
          </div>
        </div>

        <!-- Mobile Card List View (< 640px) -->
        <div class="block sm:hidden divide-y divide-white/5">
          ${articles.map(art => {
            const isBookmarked = state.bookmarks.includes(art.id);
            const cat = state.data.categories.find(c => c.id === art.categoryId) || {};

            return `
              <div class="p-4 hover:bg-white/5 transition flex flex-col gap-2.5">
                <div class="flex items-center justify-between gap-2">
                  <span class="inline-flex items-center gap-1 text-[11px] text-slate-300 bg-white/5 px-2 py-0.5 rounded-lg border border-white/5">
                    <span>${cat.icon || '📁'}</span>
                    <span class="truncate max-w-[120px]">${cat.name || '其他'}</span>
                  </span>
                  <div class="flex items-center gap-2">
                    <span class="text-[10px] text-slate-400 font-mono">${art.readTime}</span>
                    <button onclick="window.AI_HUB.toggleBookmark('${art.id}', event)" class="w-6 h-6 rounded-md flex items-center justify-center ${isBookmarked ? 'text-amber-300 bg-amber-400/20' : 'text-slate-400 hover:bg-white/10'}">
                      ${isBookmarked ? '★' : '☆'}
                    </button>
                  </div>
                </div>

                <div class="font-bold text-sm text-white hover:text-indigo-400 cursor-pointer line-clamp-2" onclick="window.AI_HUB.openReaderById('${art.id}')">
                  ${highlight(art.title)}
                </div>

                ${art.subtitle ? `<div class="text-xs text-slate-400 line-clamp-1">${highlight(art.subtitle)}</div>` : ''}

                <div class="flex items-center justify-between pt-1">
                  <span class="badge-chip text-[10px] bg-white/5 border border-white/10 text-slate-300 uppercase">${art.format}</span>
                  <div class="flex items-center gap-2">
                    <a href="${art.path}" target="_blank" class="px-2.5 py-1 rounded-lg bg-white/5 hover:bg-white/10 text-slate-300 text-xs border border-white/10">↗ 独立页</a>
                    <button onclick="window.AI_HUB.openReaderById('${art.id}')" class="px-3 py-1 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium transition">
                      阅读 →
                    </button>
                  </div>
                </div>
              </div>
            `;
          }).join('')}
        </div>

        <!-- Desktop Table View (>= 640px) -->
        <div class="hidden sm:block overflow-x-auto">
          <table class="w-full text-left text-sm text-slate-300">
            <thead class="text-xs text-slate-400 bg-white/5 uppercase border-b border-white/10">
              <tr>
                <th class="px-6 py-4">分类系列</th>
                <th class="px-6 py-4">章节标题</th>
                <th class="px-6 py-4">格式</th>
                <th class="px-6 py-4">预估阅读</th>
                <th class="px-6 py-4">大小</th>
                <th class="px-6 py-4 text-right">操作</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/5">
              ${articles.map(art => {
                const isBookmarked = state.bookmarks.includes(art.id);
                const cat = state.data.categories.find(c => c.id === art.categoryId) || {};

                return `
                  <tr class="hover:bg-white/5 transition">
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span class="inline-flex items-center gap-1.5 text-xs text-slate-300 bg-white/5 px-2.5 py-1 rounded-lg border border-white/5">
                        <span>${cat.icon || '📁'}</span>
                        <span>${cat.name || '其他'}</span>
                      </span>
                    </td>
                    <td class="px-6 py-4">
                      <div class="font-medium text-white hover:text-indigo-400 cursor-pointer" onclick="window.AI_HUB.openReaderById('${art.id}')">
                        ${highlight(art.title)}
                      </div>
                      ${art.subtitle ? `<div class="text-xs text-slate-400 mt-0.5 line-clamp-1">${highlight(art.subtitle)}</div>` : ''}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span class="badge-chip text-xs bg-white/5 border border-white/10 text-slate-300 uppercase">${art.format}</span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-xs text-slate-400">
                      ${art.readTime}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-xs text-slate-400">
                      ${art.sizeStr}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-right">
                      <div class="flex items-center justify-end gap-2">
                        <button onclick="window.AI_HUB.toggleBookmark('${art.id}', event)" class="w-7 h-7 rounded-lg flex items-center justify-center ${isBookmarked ? 'text-amber-300 bg-amber-400/20' : 'text-slate-400 hover:bg-white/10'}">
                          ${isBookmarked ? '★' : '☆'}
                        </button>
                        <button onclick="window.AI_HUB.openReaderById('${art.id}')" class="px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium transition">
                          阅读
                        </button>
                      </div>
                    </td>
                  </tr>
                `;
              }).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
  }

  // 3. Tree View (系列目录树视图 - 响应式优化)
  function renderTreeView() {
    const categories = state.data.categories;

    el.mainContent.innerHTML = `
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 sm:gap-8 animate-fade-in">
        <div class="lg:col-span-1 space-y-3">
          <div class="p-4 sm:p-6 rounded-2xl sm:rounded-3xl glass border border-white/10">
            <h3 class="text-base sm:text-lg font-bold text-white mb-3 sm:mb-4">📚 系列知识大纲</h3>
            <div class="grid grid-cols-2 lg:grid-cols-1 gap-1.5">
              ${categories.map(cat => {
                const count = state.data.articles.filter(a => a.categoryId === cat.id).length;
                return `
                  <a href="#tree-cat-${cat.id}" class="flex items-center justify-between p-2 sm:p-2.5 rounded-xl hover:bg-white/10 text-slate-300 hover:text-white text-xs sm:text-sm transition">
                    <span class="flex items-center gap-1.5 sm:gap-2 truncate">
                      <span>${cat.icon}</span>
                      <span class="truncate">${cat.name}</span>
                    </span>
                    <span class="text-[10px] sm:text-xs bg-white/10 px-1.5 sm:px-2 py-0.5 rounded-full shrink-0">${count}</span>
                  </a>
                `;
              }).join('')}
            </div>
          </div>
        </div>

        <div class="lg:col-span-2 space-y-6">
          ${categories.map(cat => {
            const catArticles = state.data.articles.filter(a => a.categoryId === cat.id);
            if (catArticles.length === 0) return '';

            return `
              <div id="tree-cat-${cat.id}" class="p-4 sm:p-6 md:p-8 rounded-2xl sm:rounded-3xl glass border border-white/10">
                <div class="flex items-center justify-between border-b border-white/10 pb-3 sm:pb-4 mb-4 sm:mb-6">
                  <div class="flex items-center gap-2.5 sm:gap-3">
                    <span class="text-2xl sm:text-3xl">${cat.icon}</span>
                    <div>
                      <h4 class="text-lg sm:text-xl font-bold text-white">${cat.name}</h4>
                      <p class="text-xs text-slate-400 mt-0.5">${cat.desc}</p>
                    </div>
                  </div>
                  <span class="badge-chip bg-${cat.theme}-500/20 text-${cat.theme}-400 border border-${cat.theme}-500/30 text-xs">${cat.badge}</span>
                </div>

                <div class="space-y-2.5 sm:space-y-3">
                  ${catArticles.map((art, idx) => {
                    return `
                      <div class="p-3 sm:p-3.5 rounded-xl hover:bg-white/5 border border-transparent hover:border-white/10 transition flex items-center justify-between gap-3 sm:gap-4 cursor-pointer group" onclick="window.AI_HUB.openReaderById('${art.id}')">
                        <div class="flex items-center gap-2.5 sm:gap-3 min-w-0">
                          <span class="w-5 h-5 sm:w-6 sm:h-6 rounded-md bg-white/5 flex items-center justify-center text-[10px] sm:text-xs font-mono text-slate-400 group-hover:bg-indigo-600 group-hover:text-white transition shrink-0">
                            ${idx + 1}
                          </span>
                          <div class="min-w-0">
                            <div class="text-xs sm:text-sm font-medium text-slate-200 group-hover:text-indigo-400 transition truncate">
                              ${art.title}
                            </div>
                            ${art.subtitle ? `<div class="text-[11px] sm:text-xs text-slate-400 truncate mt-0.5">${art.subtitle}</div>` : ''}
                          </div>
                        </div>

                        <div class="flex items-center gap-2 sm:gap-3 shrink-0">
                          <span class="text-[10px] sm:text-xs text-slate-400">${art.readTime}</span>
                          <span class="badge-chip text-[10px] sm:text-xs bg-white/5 border border-white/10 text-slate-300 hidden sm:inline-block">${art.badge}</span>
                        </div>
                      </div>
                    `;
                  }).join('')}
                </div>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;
  }

  // 4. Learning Roadmap View (体系化进阶路线图)
  function renderRoadmapView() {
    const roadmapData = [
      {
        level: "Level 1",
        title: "🌱 基础通识与大模型底层原理",
        desc: "建立 AI 技术全貌认知，深入理解大模型架构、注意力机制、RoPE 与位置编码",
        categories: ["ai-science", "ai-news", "bigmodel", "ai-safety"],
      },
      {
        level: "Level 2",
        title: "⚡ Agent 核心架构、手写框架与 OpenClaw 实战",
        desc: "从零手写轻量级 Agent，深入 OpenClaw 智能体系统，掌握有限状态机、意图感知、记忆与核心思考循环",
        categories: ["myagent", "agent-core", "openclaw"],
      },
      {
        level: "Level 3",
        title: "🛠️ 现代 AI 工具链与 AI Coding 编程实战",
        desc: "玩转 Claude Code 全家桶、AI Coding 33篇全体系、MCP Server 协议开发、Dify 编排与 TDD 先行",
        categories: ["aitools", "ai-coding"],
      },
      {
        level: "Level 4",
        title: "💼 垂直行业与企业级项目实战",
        desc: "落地企业智能客服、构建私有本地大模型知识库 (RAG)、打造英语智能导师与量化交易系统",
        categories: ["customer-service", "customer-service-harness", "local-rag", "english-agent", "quant-agent"],
      }
    ];

    el.mainContent.innerHTML = `
      <div class="max-w-4xl mx-auto animate-fade-in px-1 sm:px-0">
        <div class="text-center mb-8 sm:mb-10">
          <span class="badge-chip bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 mb-2 sm:mb-3">🗺️ 体系化学习路线</span>
          <h2 class="text-2xl sm:text-3xl font-extrabold text-white">从零到专家的 AI 开发者成长路径</h2>
          <p class="text-slate-300 text-xs sm:text-sm mt-2 max-w-xl mx-auto">
            按照 4 个进阶阶段循序渐进研读，掌握从底层原理到 Agent 落地、AI 编程实战与全栈工程落地。
          </p>
        </div>

        <div class="space-y-6 sm:space-y-8">
          ${roadmapData.map(step => {
            const stepArticles = state.data.articles.filter(a => step.categories.includes(a.categoryId));

            return `
              <div class="roadmap-step">
                <div class="roadmap-dot"></div>
                <div class="p-4 sm:p-6 md:p-8 rounded-2xl sm:rounded-3xl glass border border-white/10">
                  <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 sm:gap-4 border-b border-white/10 pb-3 sm:pb-4 mb-3 sm:mb-4">
                    <div>
                      <span class="text-[11px] sm:text-xs font-mono font-bold text-indigo-400 bg-indigo-500/10 px-2 py-0.5 sm:px-2.5 sm:py-1 rounded-md border border-indigo-500/20">${step.level}</span>
                      <h3 class="text-lg sm:text-xl font-bold text-white mt-1.5">${step.title}</h3>
                      <p class="text-xs text-slate-300 mt-1">${step.desc}</p>
                    </div>

                    <div class="shrink-0">
                      <span class="text-[11px] sm:text-xs font-medium px-2.5 sm:px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 inline-block">
                        共 ${stepArticles.length} 篇深度解析
                      </span>
                    </div>
                  </div>

                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 sm:gap-3 mt-3 sm:mt-4">
                    ${step.categories.map(catId => {
                      const cat = state.data.categories.find(c => c.id === catId);
                      if (!cat) return '';
                      const count = state.data.articles.filter(a => a.categoryId === catId).length;
                      return `
                        <div onclick="window.AI_HUB.switchCategory('${cat.id}')" class="p-3 sm:p-3.5 rounded-xl bg-white/5 hover:bg-white/10 border border-white/5 hover:border-indigo-500/30 transition flex items-center justify-between cursor-pointer group">
                          <span class="flex items-center gap-2 text-xs sm:text-sm text-slate-200 group-hover:text-indigo-400 font-medium">
                            <span class="text-base sm:text-lg">${cat.icon}</span>
                            <span>${cat.name}</span>
                          </span>
                          <span class="text-[11px] sm:text-xs bg-white/10 px-2 sm:px-2.5 py-0.5 sm:py-1 rounded-full text-slate-300 group-hover:bg-indigo-600 group-hover:text-white transition">${count} 篇</span>
                        </div>
                      `;
                    }).join('')}
                  </div>
                </div>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;
  }

  function renderEmptyState() {
    return `
      <div class="text-center py-20 animate-fade-in">
        <div class="text-5xl mb-4">🔍</div>
        <h3 class="text-xl font-bold text-white">未找到匹配的学习资料</h3>
        <p class="text-slate-400 text-sm mt-2">请尝试更换搜索关键字，或调整分类筛选条件。</p>
        <button onclick="window.AI_HUB.resetFilters()" class="mt-6 px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium transition">
          重置所有筛选条件
        </button>
      </div>
    `;
  }

  // Fallback simple markdown parser if marked CDN is not loaded
  function simpleMarkdownParse(md) {
    if (!md) return '';
    return md
      .replace(/^### (.*$)/gim, '<h3 id="$1">$1</h3>')
      .replace(/^## (.*$)/gim, '<h2 id="$1">$1</h2>')
      .replace(/^# (.*$)/gim, '<h1 id="$1">$1</h1>')
      .replace(/^\> (.*$)/gim, '<blockquote>$1</blockquote>')
      .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
      .replace(/\*(.*)\*/gim, '<em>$1</em>')
      .replace(/```([a-z]*)\n([\s\S]*?)```/gim, '<pre><code>$2</code></pre>')
      .replace(/`([^`]+)`/gim, '<code>$1</code>')
      .replace(/\n\n/gim, '</p><p>')
      .replace(/\[([^\]]+)\]\(([^)]+)\)/gim, '<a href="$2" target="_blank">$1</a>');
  }

  // Reader Modal Operations (Hybrid: HTML / Markdown / PDF)
  function openReader(article) {
    state.currentArticle = article;

    state.history = [{ id: article.id, time: new Date().toLocaleTimeString() }, ...state.history.filter(h => h.id !== article.id)];
    localStorage.setItem('ai_hub_history', JSON.stringify(state.history));

    window.history.replaceState(null, '', `?article=${article.id}`);

    if (el.readerTitle) el.readerTitle.textContent = article.title;
    const cat = state.data.categories.find(c => c.id === article.categoryId);
    if (el.readerCategory) el.readerCategory.textContent = cat ? `${cat.icon} ${cat.name}` : '系列文档';

    updateReaderButtons();

    // 1. Markdown (.md)
    if (article.format === 'md') {
      if (el.readerIframeContainer) el.readerIframeContainer.classList.add('hidden');
      if (el.readerMarkdownContainer) el.readerMarkdownContainer.classList.remove('hidden');

      if (el.markdownContent) {
        el.markdownContent.innerHTML = `<div class="text-center py-16 text-slate-400">正在解析并渲染 Markdown 文档...</div>`;
      }

      fetch(article.path)
        .then(res => res.text())
        .then(text => {
          let html = '';
          if (window.marked && typeof window.marked.parse === 'function') {
            html = window.marked.parse(text);
          } else {
            html = simpleMarkdownParse(text);
          }
          if (el.markdownContent) {
            el.markdownContent.innerHTML = html;
          }

          // Auto extract headings for TOC in markdown
          const headings = [];
          const lines = text.split('\n');
          lines.forEach(l => {
            if (l.startsWith('## ') || l.startsWith('### ')) {
              headings.push(l.replace(/^#+\s*/, '').trim());
            }
          });
          article.toc = headings.slice(0, 15);
          renderReaderToc(article);
        })
        .catch(err => {
          if (el.markdownContent) {
            el.markdownContent.innerHTML = `<div class="text-rose-400 p-6">加载 Markdown 文件失败：${err.message}</div>`;
          }
        });

    // 2. HTML (.html)
    } else {
      if (el.readerMarkdownContainer) el.readerMarkdownContainer.classList.add('hidden');
      if (el.readerIframeContainer) el.readerIframeContainer.classList.remove('hidden');

      if (el.readerFrame) {
        el.readerFrame.src = article.path;
      }
      renderReaderToc(article);
    }

    if (el.readerModal) {
      el.readerModal.classList.remove('hidden');
      document.body.style.overflow = 'hidden';
    }
  }

  function closeReader() {
    state.currentArticle = null;
    if (el.readerModal) {
      el.readerModal.classList.add('hidden');
      document.body.style.overflow = '';
    }
    if (el.readerFrame) {
      el.readerFrame.src = 'about:blank';
    }
    window.history.replaceState(null, '', window.location.pathname);
    renderMainView();
  }

  function updateReaderButtons() {
    if (!state.currentArticle) return;
    const art = state.currentArticle;
    const isBookmarked = state.bookmarks.includes(art.id);

    if (el.btnBookmark) {
      el.btnBookmark.innerHTML = isBookmarked ? '<span>★ 已收藏</span>' : '<span>☆ 收藏</span>';
      el.btnBookmark.className = `px-3 py-1.5 rounded-xl text-xs font-medium transition flex items-center gap-1.5 ${isBookmarked ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' : 'bg-white/10 hover:bg-white/20 text-slate-300'}`;
    }

    if (el.btnOpenExternal) {
      el.btnOpenExternal.href = art.path;
    }

    const catArticles = state.data.articles.filter(a => a.categoryId === art.categoryId);
    const currentIndex = catArticles.findIndex(a => a.id === art.id);

    if (el.btnPrevArticle) {
      el.btnPrevArticle.disabled = currentIndex <= 0;
      el.btnPrevArticle.classList.toggle('opacity-30', currentIndex <= 0);
      el.btnPrevArticle.classList.toggle('cursor-not-allowed', currentIndex <= 0);
    }

    if (el.btnNextArticle) {
      el.btnNextArticle.disabled = currentIndex === -1 || currentIndex >= catArticles.length - 1;
      el.btnNextArticle.classList.toggle('opacity-30', currentIndex === -1 || currentIndex >= catArticles.length - 1);
      el.btnNextArticle.classList.toggle('cursor-not-allowed', currentIndex === -1 || currentIndex >= catArticles.length - 1);
    }
  }

  function renderReaderToc(article) {
    if (!el.readerTocList) return;
    const toc = article.toc || [];

    if (toc.length === 0) {
      el.readerTocList.innerHTML = `<div class="text-xs text-slate-400 py-4 text-center">本篇无多级标题索引</div>`;
      return;
    }

    el.readerTocList.innerHTML = toc.map((item, idx) => `
      <button onclick="window.AI_HUB.scrollToHeading('${item}')" class="w-full text-left p-2.5 rounded-xl hover:bg-white/10 text-xs text-slate-300 hover:text-white transition truncate" title="${item}">
        ${idx + 1}. ${item}
      </button>
    `).join('');
  }

  function scrollToHeading(text) {
    if (state.currentArticle && state.currentArticle.format === 'md' && el.markdownContent) {
      const headings = el.markdownContent.querySelectorAll('h1, h2, h3, h4');
      for (const h of headings) {
        if (h.textContent.trim().includes(text) || text.includes(h.textContent.trim())) {
          h.scrollIntoView({ behavior: 'smooth', block: 'start' });
          break;
        }
      }
    }
  }

  function navigateChapter(direction) {
    if (!state.currentArticle) return;
    const catArticles = state.data.articles.filter(a => a.categoryId === state.currentArticle.categoryId);
    const idx = catArticles.findIndex(a => a.id === state.currentArticle.id);
    if (direction === 'prev' && idx > 0) {
      openReader(catArticles[idx - 1]);
    } else if (direction === 'next' && idx < catArticles.length - 1) {
      openReader(catArticles[idx + 1]);
    }
  }

  // Toggle Read Status
  // Toggle Bookmark
  function toggleBookmark(articleId, event) {
    if (event) event.stopPropagation();
    if (state.bookmarks.includes(articleId)) {
      state.bookmarks = state.bookmarks.filter(id => id !== articleId);
      showToast('已移出收藏夹', '☆');
    } else {
      state.bookmarks.push(articleId);
      showToast('已加入收藏夹！', '★');
    }
    localStorage.setItem('ai_hub_bookmarks', JSON.stringify(state.bookmarks));
    if (state.currentArticle && state.currentArticle.id === articleId) {
      updateReaderButtons();
    }
    renderMainView();
  }

  // WeChat Modal Operations
  function openWeChatModal() {
    if (el.wechatModal) {
      el.wechatModal.classList.remove('hidden');
      document.body.style.overflow = 'hidden';
    }
  }

  function closeWeChatModal() {
    if (el.wechatModal) {
      el.wechatModal.classList.add('hidden');
      document.body.style.overflow = '';
    }
  }

  // PDF E-Book Unlock Modal Operations
  let pendingPdfTarget = null;

  function openPdfUnlockModal(targetPdf) {
    pendingPdfTarget = targetPdf || null;
    if (el.pdfUnlockModal) {
      el.pdfUnlockModal.classList.remove('hidden');
      document.body.style.overflow = 'hidden';
      if (el.pdfUnlockCode) {
        el.pdfUnlockCode.value = '';
        setTimeout(() => el.pdfUnlockCode.focus(), 150);
      }
    }
  }

  function copyWeChatName() {
    const text = '大前端工程师';
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(() => {
        showToast('已复制公众号名称：大前端工程师', '📋');
      }).catch(() => {
        promptCopy(text);
      });
    } else {
      promptCopy(text);
    }
  }

  function promptCopy(text) {
    const input = document.createElement('input');
    input.value = text;
    document.body.appendChild(input);
    input.select();
    try {
      document.execCommand('copy');
      showToast('已复制公众号名称：大前端工程师', '📋');
    } catch (e) {
      showToast('公众号名称：大前端工程师', '💬');
    }
    document.body.removeChild(input);
  }

  // Event Bindings
  function bindEvents() {
    if (el.themeToggle) el.themeToggle.addEventListener('click', toggleTheme);

    if (el.searchInput) {
      el.searchInput.addEventListener('input', (e) => {
        state.searchQuery = e.target.value.trim();
        if (el.searchClear) {
          el.searchClear.classList.toggle('hidden', !state.searchQuery);
        }
        renderMainView();
      });
    }

    if (el.searchClear) {
      el.searchClear.addEventListener('click', () => {
        state.searchQuery = '';
        el.searchInput.value = '';
        el.searchClear.classList.add('hidden');
        renderMainView();
      });
    }

    if (el.categoryTabs) {
      el.categoryTabs.addEventListener('click', (e) => {
        const tab = e.target.closest('[data-category]');
        if (!tab) return;
        state.activeCategory = tab.dataset.category;
        if (state.activeCategory !== 'all' && state.viewMode === 'roadmap') {
          state.viewMode = 'grid';
          updateViewButtons();
        }
        updateCategoryTabs();
        renderMainView();
      });
    }

    if (el.categorySelect) {
      el.categorySelect.addEventListener('change', (e) => {
        state.activeCategory = e.target.value;
        if (state.activeCategory !== 'all' && state.viewMode === 'roadmap') {
          state.viewMode = 'grid';
          updateViewButtons();
        }
        updateCategoryTabs();
        renderMainView();
      });
    }

    el.viewButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        state.viewMode = btn.dataset.view;
        updateViewButtons();
        renderMainView();
      });
    });

    if (el.btnCloseReader) el.btnCloseReader.addEventListener('click', closeReader);
    if (el.btnPrevArticle) el.btnPrevArticle.addEventListener('click', () => navigateChapter('prev'));
    if (el.btnNextArticle) el.btnNextArticle.addEventListener('click', () => navigateChapter('next'));
    if (el.btnBookmark) el.btnBookmark.addEventListener('click', () => {
      if (state.currentArticle) toggleBookmark(state.currentArticle.id);
    });
    if (el.btnToggleToc) {
      el.btnToggleToc.addEventListener('click', () => {
        if (el.readerTocDrawer) el.readerTocDrawer.classList.toggle('hidden');
      });
    }

    document.addEventListener('keydown', (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        el.searchInput?.focus();
      }
      if (e.key === 'Escape') {
        if (state.currentArticle) closeReader();
        if (el.wechatModal && !el.wechatModal.classList.contains('hidden')) closeWeChatModal();
      }
      if (state.currentArticle && !e.target.matches('input, textarea')) {
        if (e.key === 'ArrowLeft') navigateChapter('prev');
        if (e.key === 'ArrowRight') navigateChapter('next');
      }
      if ((e.key === 't' || e.key === 'T') && !e.target.matches('input, textarea') && !state.currentArticle) {
        toggleTheme();
      }
    });
  }

  // Global API exposed to HTML
  window.AI_HUB = {
    openReaderById: function (id) {
      const art = state.data.articles.find(a => a.id === id);
      if (art) openReader(art);
    },
    switchCategory: function (catId) {
      state.activeCategory = catId;
      state.viewMode = 'grid';
      updateCategoryTabs();
      updateViewButtons();
      renderMainView();
      window.scrollTo({ top: 400, behavior: 'smooth' });
    },
    toggleBookmark: toggleBookmark,
    openWeChatModal: openWeChatModal,
    closeWeChatModal: closeWeChatModal,
    copyWeChatName: copyWeChatName,
    scrollToHeading: scrollToHeading,
    resetFilters: function () {
      state.activeCategory = 'all';
      state.searchQuery = '';
      if (el.searchInput) el.searchInput.value = '';
      updateCategoryTabs();
      renderMainView();
    },
    switchView: function (mode) {
      state.viewMode = mode;
      updateViewButtons();
      renderMainView();
    }
  };

  // Launch on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
