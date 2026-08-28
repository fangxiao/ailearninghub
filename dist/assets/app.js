(function(){"use strict";const i={data:window.SITE_DATA||{categories:[],articles:[],stats:{}},activeCategory:"all",searchQuery:"",difficultyFilter:"all",viewMode:"roadmap",roadmapTrack:"tech",theme:localStorage.getItem("ai_hub_theme")||"dark",readerTheme:localStorage.getItem("ai_hub_reader_theme")||"default",readerFontSize:parseInt(localStorage.getItem("ai_hub_reader_fontsize")||"16",10),currentArticle:null,history:JSON.parse(localStorage.getItem("ai_hub_history")||"[]")},t={app:document.getElementById("app"),themeToggle:document.getElementById("theme-toggle"),themeIcon:document.getElementById("theme-icon"),searchInput:document.getElementById("search-input"),searchClear:document.getElementById("search-clear"),categoryTabs:document.getElementById("category-tabs"),categorySelect:document.getElementById("category-select"),viewButtons:document.querySelectorAll("[data-view]"),mainContent:document.getElementById("main-content"),readerModal:document.getElementById("reader-modal"),readerIframeContainer:document.getElementById("reader-iframe-container"),readerMarkdownContainer:document.getElementById("reader-markdown-container"),readerFrame:document.getElementById("reader-frame"),markdownContent:document.getElementById("markdown-content"),readerTitle:document.getElementById("reader-title"),readerCategory:document.getElementById("reader-category"),readerTocList:document.getElementById("reader-toc-list"),readerTocDrawer:document.getElementById("reader-toc-drawer"),wechatModal:document.getElementById("wechat-modal"),btnPrevArticle:document.getElementById("btn-prev-article"),btnNextArticle:document.getElementById("btn-next-article"),btnOpenExternal:document.getElementById("btn-open-external"),btnCloseReader:document.getElementById("btn-close-reader"),btnToggleToc:document.getElementById("btn-toggle-toc"),toast:document.getElementById("toast")};function y(){$(i.theme),H(),R(),N(),c();const e=new URLSearchParams(window.location.search),a=e.get("category"),s=e.get("article"),r=e.get("view");if(r&&["grid","list","tree","shelf","roadmap","my-space"].includes(r)&&(i.viewMode=r,x()),a&&(a==="all"||i.data.categories.some(n=>n.id===a))&&(i.activeCategory=a,h()),s){const n=i.data.articles.find(l=>l.id===s||l.path===s);n&&u(n)}}function $(e){i.theme=e,localStorage.setItem("ai_hub_theme",e),e==="light"?(document.documentElement.classList.add("light-theme"),document.documentElement.classList.remove("dark"),t.themeIcon&&(t.themeIcon.innerHTML="\u2600\uFE0F")):(document.documentElement.classList.remove("light-theme"),document.documentElement.classList.add("dark"),t.themeIcon&&(t.themeIcon.innerHTML="\u{1F319}"))}function I(){$(i.theme==="dark"?"light":"dark")}let k;function b(e,a="\u2728"){t.toast&&(t.toast.innerHTML=`<span class="text-xl">${a}</span><span>${e}</span>`,t.toast.classList.remove("opacity-0","translate-y-4","pointer-events-none"),t.toast.classList.add("opacity-100","translate-y-0"),clearTimeout(k),k=setTimeout(()=>{t.toast.classList.add("opacity-0","translate-y-4","pointer-events-none"),t.toast.classList.remove("opacity-100","translate-y-0")},2400))}function q(){t.statsArticles&&(t.statsArticles.textContent=i.data.articles.length),t.statsCategories&&(t.statsCategories.textContent=i.data.categories.length),t.statsEbooks&&(t.statsEbooks.textContent=i.data.categories.find(e=>e.id==="ebooks")?.count||7)}function H(){if(!t.categoryTabs)return;const e=i.data.categories;let a=`
      <button data-category="all" class="category-tab px-3.5 py-1.5 rounded-xl text-xs font-medium border flex items-center gap-1.5 transition ${i.activeCategory==="all"?"active":"border-white/10 text-slate-400 hover:text-white hover:bg-white/5"}">
        <span>\u{1F310}</span>
        <span>\u5168\u90E8\u5206\u7C7B</span>
      </button>
    `;e.forEach(s=>{const r=i.activeCategory===s.id;a+=`
        <button data-category="${s.id}" class="category-tab px-3.5 py-1.5 rounded-xl text-xs font-medium border flex items-center gap-1.5 transition ${r?"active":"border-white/10 text-slate-400 hover:text-white hover:bg-white/5"}">
          <span>${s.icon}</span>
          <span>${s.name}</span>
        </button>
      `}),t.categoryTabs.innerHTML=a}function R(){if(!t.categorySelect)return;let e=`<option value="all">\u{1F310} \u5168\u90E8\u7CFB\u5217\u5206\u7C7B (${i.data.articles.length} \u7BC7)</option>`;i.data.categories.forEach(a=>{e+=`<option value="${a.id}">${a.icon} ${a.name} (${a.count} \u7BC7)</option>`}),t.categorySelect.innerHTML=e,t.categorySelect.value=i.activeCategory}function h(){document.querySelectorAll(".category-tab").forEach(e=>{e.dataset.category===i.activeCategory?(e.classList.add("active"),e.classList.remove("border-white/10","text-slate-400","hover:bg-white/5")):(e.classList.remove("active"),e.classList.add("border-white/10","text-slate-400","hover:bg-white/5"))}),t.categorySelect&&(t.categorySelect.value=i.activeCategory)}function x(){t.viewButtons.forEach(e=>{e.dataset.view===i.viewMode?(e.classList.add("bg-indigo-600","text-white"),e.classList.remove("text-slate-400","hover:text-white","hover:bg-white/5")):(e.classList.remove("bg-indigo-600","text-white"),e.classList.add("text-slate-400","hover:text-white","hover:bg-white/5"))})}function C(){return i.data.articles.filter(e=>{if(i.activeCategory!=="all"&&e.categoryId!==i.activeCategory)return!1;if(i.searchQuery){const a=i.searchQuery.toLowerCase(),s=e.title.toLowerCase().includes(a),r=(e.subtitle||"").toLowerCase().includes(a),n=(e.summary||"").toLowerCase().includes(a),l=(e.toc||[]).some(d=>d.toLowerCase().includes(a)),o=(e.badge||"").toLowerCase().includes(a);if(!s&&!r&&!n&&!l&&!o)return!1}return!0})}function c(){t.mainContent&&(i.viewMode==="grid"?P():i.viewMode==="list"?D():i.viewMode==="tree"?U():i.viewMode==="shelf"?renderShelfView():i.viewMode==="roadmap"?_():i.viewMode==="my-space"&&renderMySpaceView())}function g(e){if(!i.searchQuery||!e)return e;const a=i.searchQuery.replace(/[.*+?^${}()|[\]\\]/g,"\\$&"),s=new RegExp(`(${a})`,"gi");return e.replace(s,'<mark class="bg-amber-400/30 text-amber-300 px-1 rounded">$1</mark>')}function P(){const e=C(),a=i.data.categories;if(e.length===0){t.mainContent.innerHTML=L();return}if(i.activeCategory!=="all"||i.searchQuery||i.formatFilter!=="all"){const r=a.find(o=>o.id===i.activeCategory);let n="";r&&!i.searchQuery?n=j(r,e):i.searchQuery&&(n=`
          <div class="mb-8 p-6 rounded-2xl glass border border-white/10 flex items-center justify-between">
            <div>
              <div class="text-sm text-indigo-400 font-medium">\u641C\u7D22\u7ED3\u679C</div>
              <h2 class="text-2xl font-bold mt-1 text-white">\u627E\u5230 <span class="text-indigo-400">${e.length}</span> \u7BC7\u5339\u914D\u6587\u6863</h2>
              <p class="text-sm text-slate-400 mt-1">\u5173\u952E\u5B57\uFF1A"${i.searchQuery}"</p>
            </div>
            <button id="btn-clear-search-res" class="px-4 py-2 text-xs rounded-xl bg-white/10 hover:bg-white/20 text-white transition">\u6E05\u7A7A\u641C\u7D22</button>
          </div>
        `),t.mainContent.innerHTML=`
        ${n}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-fade-in">
          ${e.map(A).join("")}
        </div>
      `;const l=document.getElementById("btn-clear-search-res");l&&l.addEventListener("click",()=>{i.searchQuery="",t.searchInput.value="",c()});return}let s="";a.forEach(r=>{const n=i.data.articles.filter(o=>o.categoryId===r.id);if(n.length===0)return;const l=n[0];s+=`
        <div class="mb-14" id="cat-section-${r.id}">
          <!-- Category Header -->
          <div class="p-6 md:p-8 rounded-3xl glass border border-white/10 mb-6 relative overflow-hidden">
            <div class="absolute right-0 top-0 w-64 h-64 bg-${r.theme}-500/10 blur-3xl pointer-events-none"></div>
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 relative z-10">
              <div class="flex items-start md:items-center gap-4">
                <div class="w-14 h-14 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-3xl shadow-inner shrink-0">
                  ${r.icon}
                </div>
                <div>
                  <div class="flex items-center gap-2 flex-wrap">
                    <h2 class="text-2xl font-bold text-white">${r.name}</h2>
                    <span class="badge-chip bg-${r.theme}-500/20 text-${r.theme}-400 border border-${r.theme}-500/30">${r.badge}</span>
                    <span class="text-xs text-slate-400 bg-white/5 px-2.5 py-1 rounded-full border border-white/5">\u5171 ${n.length} \u7BC7</span>
                  </div>
                  <p class="text-sm text-slate-300 mt-2 max-w-2xl">${r.desc}</p>
                </div>
              </div>
              <div class="flex items-center gap-2.5 shrink-0">
                <button onclick="window.AI_HUB.switchCategory('${r.id}')" class="px-4 py-2 text-xs font-semibold rounded-xl bg-white/10 hover:bg-white/20 text-white transition flex items-center gap-1.5 border border-white/10">
                  <span>\u67E5\u770B\u8BE5\u7CFB\u5217\u5168\u90E8</span>
                  <span>\u2192</span>
                </button>
                ${l?`
                  <button onclick="window.AI_HUB.openReaderById('${l.id}')" class="btn-read px-4 py-2 text-xs font-bold rounded-xl shadow-lg flex items-center gap-1.5">
                    <span>\u26A1 \u4ECE\u7B2C 1 \u7AE0\u5F00\u59CB</span>
                  </button>
                `:""}
              </div>
            </div>
          </div>

          <!-- Cards Grid (Top 6) -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            ${n.slice(0,6).map(A).join("")}
          </div>

          ${n.length>6?`
            <div class="text-center mt-6">
              <button onclick="window.AI_HUB.switchCategory('${r.id}')" class="px-6 py-2.5 rounded-2xl glass text-xs font-medium text-slate-300 hover:text-white hover:border-indigo-500/50 transition">
                \u67E5\u770B\u8BE5\u7CFB\u5217\u5269\u4F59 ${n.length-6} \u7BC7\u6587\u6863 \u2193
              </button>
            </div>
          `:""}
        </div>
      `}),t.mainContent.innerHTML=s}function j(e,a){return`
      <div class="p-6 md:p-8 rounded-3xl glass border border-white/10 mb-8 relative overflow-hidden">
        <div class="absolute right-0 top-0 w-80 h-80 bg-${e.theme}-500/15 blur-3xl pointer-events-none"></div>
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-6 relative z-10">
          <div class="flex items-start gap-4">
            <div class="w-16 h-16 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-4xl shadow-inner shrink-0">
              ${e.icon}
            </div>
            <div>
              <div class="flex items-center gap-2 flex-wrap">
                <h2 class="text-2xl md:text-3xl font-bold text-white">${e.name}</h2>
                <span class="badge-chip bg-${e.theme}-500/20 text-${e.theme}-400 border border-${e.theme}-500/30">${e.badge}</span>
                <span class="badge-chip bg-white/5 text-slate-300 border border-white/10">${e.difficulty}</span>
                <span class="text-xs text-slate-400 bg-white/5 px-2.5 py-1 rounded-full border border-white/5">\u5171 ${a.length} \u7BC7\u7CBE\u9009</span>
              </div>
              <p class="text-sm md:text-base text-slate-300 mt-2 max-w-2xl">${e.desc}</p>
            </div>
          </div>

          <div class="flex flex-wrap items-center gap-3 shrink-0">
            <button onclick="window.AI_HUB.openReaderById('${a[0]?.id}')" class="btn-read px-5 py-2.5 rounded-xl font-bold text-sm shadow-lg flex items-center gap-2">
              <span>\u26A1 \u4ECE\u7B2C 1 \u7AE0\u5F00\u59CB\u9605\u8BFB</span>
            </button>
          </div>
        </div>
      </div>
    `}function A(e){const a=i.data.categories.find(r=>r.id===e.categoryId)||{};let s="bg-blue-500/20 text-blue-400 border-blue-500/30";return e.format==="pdf"&&(s="bg-rose-500/20 text-rose-400 border-rose-500/30"),e.format==="md"&&(s="bg-amber-500/20 text-amber-400 border-amber-500/30"),`
      <div class="article-card rounded-2xl glass border border-white/10 p-6 flex flex-col justify-between relative group">
        <div>
          <div class="flex items-center justify-between gap-2 mb-3">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="badge-chip ${s} border">${e.badge}</span>
              <span class="text-xs text-slate-400 flex items-center gap-1">
                <span>\u23F1\uFE0F</span>
                <span>${e.readTime}</span>
              </span>
              <span class="text-xs text-slate-400 bg-white/5 px-2 py-0.5 rounded-md">${e.sizeStr}</span>
            </div>
          </div>

          <h3 class="text-lg font-bold text-white group-hover:text-indigo-400 transition line-clamp-2 cursor-pointer" onclick="window.AI_HUB.openReaderById('${e.id}')">
            ${g(e.title)}
          </h3>

          ${e.subtitle?`
            <div class="text-xs font-medium text-indigo-400/90 mt-1.5 line-clamp-1">
              ${g(e.subtitle)}
            </div>
          `:""}

          <p class="text-xs text-slate-400 mt-2.5 line-clamp-3 leading-relaxed">
            ${g(e.summary||"\u70B9\u51FB\u8FDB\u5165\u9605\u8BFB\u5168\u7BC7\u8BE6\u7EC6\u56FE\u6587\u5185\u5BB9\u4E0E\u6280\u672F\u62C6\u89E3\u3002")}
          </p>
        </div>

        <div class="pt-5 mt-5 border-t border-white/5 flex items-center justify-between gap-3">
          <div class="flex items-center gap-1.5 text-xs text-slate-400">
            <span>${a.icon||"\u{1F4C1}"}</span>
            <span class="truncate max-w-[120px]">${a.name||"\u7CFB\u5217\u6587\u6863"}</span>
          </div>

          <div class="flex items-center gap-2">
            <a href="${e.path}" target="_blank" title="\u65B0\u6807\u7B7E\u9875\u6253\u5F00" class="w-8 h-8 rounded-xl bg-white/5 hover:bg-white/15 text-slate-300 hover:text-white flex items-center justify-center text-xs transition border border-white/10">
              \u2197
            </a>
            <button onclick="window.AI_HUB.openReaderById('${e.id}')" class="btn-read px-3.5 py-1.5 rounded-xl text-xs font-bold shadow-md flex items-center gap-1">
              <span>\u9605\u8BFB</span>
              <span>\u2192</span>
            </button>
          </div>
        </div>
      </div>
    `}function D(){const e=C();if(e.length===0){t.mainContent.innerHTML=L();return}t.mainContent.innerHTML=`
      <div class="rounded-2xl sm:rounded-3xl glass border border-white/10 overflow-hidden animate-fade-in">
        <div class="p-4 sm:p-6 border-b border-white/10 flex items-center justify-between">
          <div>
            <h3 class="text-lg sm:text-xl font-bold text-white">\u6587\u6863\u901F\u67E5\u5217\u8868</h3>
            <p class="text-xs text-slate-400 mt-0.5">\u5171\u627E\u5230 ${e.length} \u7BC7\u76F8\u5173\u8D44\u6599</p>
          </div>
        </div>

        <!-- Mobile Card List View (< 640px) -->
        <div class="block sm:hidden divide-y divide-white/5">
          ${e.map(a=>{const s=i.data.categories.find(r=>r.id===a.categoryId)||{};return`
              <div class="p-4 hover:bg-white/5 transition flex flex-col gap-2.5">
                <div class="flex items-center justify-between gap-2">
                  <span class="inline-flex items-center gap-1 text-[11px] text-slate-300 bg-white/5 px-2 py-0.5 rounded-lg border border-white/5">
                    <span>${s.icon||"\u{1F4C1}"}</span>
                    <span class="truncate max-w-[120px]">${s.name||"\u5176\u4ED6"}</span>
                  </span>
                  <span class="text-[10px] text-slate-400 font-mono">${a.readTime}</span>
                </div>

                <div class="font-bold text-sm text-white hover:text-indigo-400 cursor-pointer line-clamp-2" onclick="window.AI_HUB.openReaderById('${a.id}')">
                  ${g(a.title)}
                </div>

                ${a.subtitle?`<div class="text-xs text-slate-400 line-clamp-1">${g(a.subtitle)}</div>`:""}

                <div class="flex items-center justify-between pt-1">
                  <span class="badge-chip text-[10px] bg-white/5 border border-white/10 text-slate-300 uppercase">${a.format}</span>
                  <div class="flex items-center gap-2">
                    <a href="${a.path}" target="_blank" class="px-2.5 py-1 rounded-lg bg-white/5 hover:bg-white/10 text-slate-300 text-xs border border-white/10">\u2197 \u72EC\u7ACB\u9875</a>
                    <button onclick="window.AI_HUB.openReaderById('${a.id}')" class="btn-read px-3 py-1 rounded-lg text-xs font-bold transition">
                      \u9605\u8BFB \u2192
                    </button>
                  </div>
                </div>
              </div>
            `}).join("")}
        </div>

        <!-- Desktop Table View (>= 640px) -->
        <div class="hidden sm:block overflow-x-auto">
          <table class="w-full text-left text-sm text-slate-300">
            <thead class="text-xs text-slate-400 bg-white/5 uppercase border-b border-white/10">
              <tr>
                <th class="px-6 py-4">\u5206\u7C7B\u7CFB\u5217</th>
                <th class="px-6 py-4">\u7AE0\u8282\u6807\u9898</th>
                <th class="px-6 py-4">\u683C\u5F0F</th>
                <th class="px-6 py-4">\u9884\u4F30\u9605\u8BFB</th>
                <th class="px-6 py-4">\u5927\u5C0F</th>
                <th class="px-6 py-4 text-right">\u64CD\u4F5C</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/5">
              ${e.map(a=>{const s=i.data.categories.find(r=>r.id===a.categoryId)||{};return`
                  <tr class="hover:bg-white/5 transition">
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span class="inline-flex items-center gap-1.5 text-xs text-slate-300 bg-white/5 px-2.5 py-1 rounded-lg border border-white/5">
                        <span>${s.icon||"\u{1F4C1}"}</span>
                        <span>${s.name||"\u5176\u4ED6"}</span>
                      </span>
                    </td>
                    <td class="px-6 py-4">
                      <div class="font-medium text-white hover:text-indigo-400 cursor-pointer" onclick="window.AI_HUB.openReaderById('${a.id}')">
                        ${g(a.title)}
                      </div>
                      ${a.subtitle?`<div class="text-xs text-slate-400 mt-0.5 line-clamp-1">${g(a.subtitle)}</div>`:""}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span class="badge-chip text-xs bg-white/5 border border-white/10 text-slate-300 uppercase">${a.format}</span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-xs text-slate-400">
                      ${a.readTime}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-xs text-slate-400">
                      ${a.sizeStr}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-right">
                      <div class="flex items-center justify-end gap-2">
                        <button onclick="window.AI_HUB.openReaderById('${a.id}')" class="btn-read px-3.5 py-1.5 rounded-lg text-xs font-bold transition">
                          \u9605\u8BFB
                        </button>
                      </div>
                    </td>
                  </tr>
                `}).join("")}
            </tbody>
          </table>
        </div>
      </div>
    `}function U(){const e=i.data.categories;t.mainContent.innerHTML=`
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 sm:gap-8 animate-fade-in">
        <div class="lg:col-span-1 space-y-3">
          <div class="p-4 sm:p-6 rounded-2xl sm:rounded-3xl glass border border-white/10">
            <h3 class="text-base sm:text-lg font-bold text-white mb-3 sm:mb-4">\u{1F4DA} \u7CFB\u5217\u77E5\u8BC6\u5927\u7EB2</h3>
            <div class="grid grid-cols-2 lg:grid-cols-1 gap-1.5">
              ${e.map(a=>{const s=i.data.articles.filter(r=>r.categoryId===a.id).length;return`
                  <a href="#tree-cat-${a.id}" class="flex items-center justify-between p-2 sm:p-2.5 rounded-xl hover:bg-white/10 text-slate-300 hover:text-white text-xs sm:text-sm transition">
                    <span class="flex items-center gap-1.5 sm:gap-2 truncate">
                      <span>${a.icon}</span>
                      <span class="truncate">${a.name}</span>
                    </span>
                    <span class="text-[10px] sm:text-xs bg-white/10 px-1.5 sm:px-2 py-0.5 rounded-full shrink-0">${s}</span>
                  </a>
                `}).join("")}
            </div>
          </div>
        </div>

        <div class="lg:col-span-2 space-y-6">
          ${e.map(a=>{const s=i.data.articles.filter(r=>r.categoryId===a.id);return s.length===0?"":`
              <div id="tree-cat-${a.id}" class="p-4 sm:p-6 md:p-8 rounded-2xl sm:rounded-3xl glass border border-white/10">
                <div class="flex items-center justify-between border-b border-white/10 pb-3 sm:pb-4 mb-4 sm:mb-6">
                  <div class="flex items-center gap-2.5 sm:gap-3">
                    <span class="text-2xl sm:text-3xl">${a.icon}</span>
                    <div>
                      <h4 class="text-lg sm:text-xl font-bold text-white">${a.name}</h4>
                      <p class="text-xs text-slate-400 mt-0.5">${a.desc}</p>
                    </div>
                  </div>
                  <span class="badge-chip bg-${a.theme}-500/20 text-${a.theme}-400 border border-${a.theme}-500/30 text-xs">${a.badge}</span>
                </div>

                <div class="space-y-2.5 sm:space-y-3">
                  ${s.map((r,n)=>`
                      <div class="p-3 sm:p-3.5 rounded-xl hover:bg-white/5 border border-transparent hover:border-white/10 transition flex items-center justify-between gap-3 sm:gap-4 cursor-pointer group" onclick="window.AI_HUB.openReaderById('${r.id}')">
                        <div class="flex items-center gap-2.5 sm:gap-3 min-w-0">
                          <span class="w-5 h-5 sm:w-6 sm:h-6 rounded-md bg-white/5 flex items-center justify-center text-[10px] sm:text-xs font-mono text-slate-400 group-hover:bg-indigo-600 group-hover:text-white transition shrink-0">
                            ${n+1}
                          </span>
                          <div class="min-w-0">
                            <div class="text-xs sm:text-sm font-medium text-slate-200 group-hover:text-indigo-400 transition truncate">
                              ${r.title}
                            </div>
                            ${r.subtitle?`<div class="text-[11px] sm:text-xs text-slate-400 truncate mt-0.5">${r.subtitle}</div>`:""}
                          </div>
                        </div>

                        <div class="flex items-center gap-2 sm:gap-3 shrink-0">
                          <span class="text-[10px] sm:text-xs text-slate-400">${r.readTime}</span>
                          <span class="badge-chip text-[10px] sm:text-xs bg-white/5 border border-white/10 text-slate-300 hidden sm:inline-block">${r.badge}</span>
                        </div>
                      </div>
                    `).join("")}
                </div>
              </div>
            `}).join("")}
        </div>
      </div>
    `}function _(){const e=i.roadmapTrack==="tech",r=e?[{level:"Level 1",title:"\u{1F331} \u57FA\u7840\u901A\u8BC6\u4E0E\u5927\u6A21\u578B\u5E95\u5C42\u539F\u7406",desc:"\u6DF1\u5165\u638C\u63E1\u5927\u6A21\u578B\u6838\u5FC3\u67B6\u6784\u3001\u6CE8\u610F\u529B\u673A\u5236 (Self-Attention)\u3001RoPE \u4E0E\u4F4D\u7F6E\u7F16\u7801\u6570\u5B66\u539F\u7406\u4E0E\u524D\u6CBF\u8109\u7EDC",categories:["ai-science","ai-news","bigmodel","ai-safety"],skills:["Transformer \u67B6\u6784","\u6CE8\u610F\u529B\u673A\u5236\u8BA1\u7B97","Token & \u5D4C\u5165\u5411\u91CF","\u6A21\u578B\u5B89\u5168\u4E0E\u4F26\u7406"]},{level:"Level 2",title:"\u26A1 Agent \u6838\u5FC3\u67B6\u6784\u3001\u624B\u5199\u6846\u67B6\u4E0E\u601D\u8003\u5FAA\u73AF",desc:"\u4ECE\u96F6\u624B\u5199\u8F7B\u91CF\u7EA7 Agent \u601D\u8003\u5FAA\u73AF\uFF0C\u6DF1\u5165 OpenClaw \u667A\u80FD\u4F53\u7CFB\u7EDF\uFF0C\u638C\u63E1\u6709\u9650\u72B6\u6001\u673A\u3001\u610F\u56FE\u611F\u77E5\u4E0E\u8BB0\u5FC6\u7CFB\u7EDF",categories:["myagent","agent-core","openclaw"],skills:["ReAct \u601D\u8003\u5FAA\u73AF","\u77ED/\u957F\u671F\u8BB0\u5FC6\u7CFB\u7EDF","\u5DE5\u5177\u8C03\u7528\u534F\u8BAE","OpenClaw \u667A\u80FD\u4F53"]},{level:"Level 3",title:"\u{1F6E0}\uFE0F \u73B0\u4EE3 AI \u5DE5\u5177\u94FE\u4E0E AI Coding \u5168\u6808\u8FDB\u9636",desc:"\u73A9\u8F6C Claude Code \u5168\u5BB6\u6876\u3001AI Coding 33\u7BC7\u5168\u4F53\u7CFB\u3001MCP Server \u534F\u8BAE\u5F00\u53D1\u3001TDD \u4E0E\u540E\u7AEF\u670D\u52A1\u96C6\u6210",categories:["aitools","ai-coding"],skills:["Claude Code \u5168\u5BB6\u6876","MCP \u534F\u8BAE\u5F00\u53D1","AI \u8F85\u52A9\u67B6\u6784\u8BBE\u8BA1","\u6D4B\u8BD5\u9A71\u52A8\u5F00\u53D1 TDD"]},{level:"Level 4",title:"\u{1F4BC} \u4F01\u4E1A\u7EA7\u5DE5\u7A0B\u843D\u5730\u4E0E\u79C1\u6709\u77E5\u8BC6\u5E93 (RAG)",desc:"\u843D\u5730\u4F01\u4E1A\u667A\u80FD\u5BA2\u670D\u5168\u95ED\u73AF\u3001\u6784\u5EFA\u79C1\u6709\u672C\u5730\u5927\u6A21\u578B\u77E5\u8BC6\u5E93 (Ollama + \u5411\u91CF\u5E93)\u3001\u6253\u9020\u5782\u76F4\u9886\u57DF Agent \u7CFB\u7EDF",categories:["customer-service","customer-service-harness","local-rag","english-agent","quant-agent"],skills:["\u4F01\u4E1A\u5FAE\u4FE1\u667A\u80FD\u5BA2\u670D","\u672C\u5730\u79C1\u6709 RAG","\u5411\u91CF\u68C0\u7D22\u4E0E\u91CD\u6392","\u5782\u76F4 Agent \u843D\u5730"]}]:[{level:"Level 1",title:"\u{1F3AF} \u4E1A\u52A1\u8BA4\u77E5\u4E0E\u9AD8\u9636\u63D0\u793A\u5DE5\u7A0B (Prompt \u8D4B\u80FD\u4E1A\u52A1)",desc:"\u628A\u4E1A\u52A1\u89C4\u5219\u8F6C\u5316\u4E3A\u5927\u6A21\u578B\u80FD\u7CBE\u51C6\u6267\u884C\u7684\u9AD8\u9636 Prompt\uFF0C\u638C\u63E1\u7ED3\u6784\u5316\u8F93\u51FA\u3001\u4E1A\u52A1\u8FB9\u754C\u7EA6\u675F\u4E0E\u5185\u5BB9\u6DA6\u8272",skills:["CRISPE \u7ED3\u6784\u5316\u6846\u67B6","\u4E1A\u52A1\u89C4\u5219\u4E0E\u8FB9\u754C\u7EA6\u675F","\u975E\u7ED3\u6784\u5316\u6570\u636E\u521D\u7B5B","\u81EA\u5A92\u4F53\u56FE\u6587\u751F\u4EA7\u6D41","\u6587\u672C\u53BB AI \u75D5\u6DA6\u8272"],curatedArticles:[{id:"aitools_pm_skills_write_prd_\u6DF1\u5EA6\u5B9E\u6218_\u516C\u4F17\u53F7\u7248_html",tag:"\u{1F3AF} \u4EA7\u54C1PRD\u5B9E\u6218"},{id:"aitools_baoyu_skills_\u4E2D\u6587\u81EA\u5A92\u4F53\u6280\u80FD\u96C6_\u516C\u4F17\u53F7\u7248_html",tag:"\u26A1 \u56FE\u6587\u751F\u4EA7\u6D41"},{id:"aitools_humanizer_skill\u4ECB\u7ECD_\u516C\u4F17\u53F7\u7248_html",tag:"\u{1F4DD} \u6587\u672C\u53BBAI\u75D5"}],inProgressText:"\u{1F331} \u300A\u4E1A\u52A1\u573A\u666F\u9AD8\u9636 Prompt \u7ED3\u6784\u5316\u8BBE\u8BA1\u5168\u6307\u5357\u300B\u5BA1\u6838\u6392\u671F\u4E2D..."},{level:"Level 2",title:"\u{1F4A1} AI \u4EA7\u54C1\u8BBE\u8BA1\u4E0E\u4E1A\u52A1\u6D41\u91CD\u6784 (AI PM \u5B9E\u6218)",desc:"\u638C\u63E1 AI \u539F\u751F\u4EA7\u54C1\u9700\u6C42\u5B9A\u4E49\uFF08AI PRD \u89C4\u8303\uFF09\u3001\u4EBA\u673A\u534F\u540C\u4EA4\u4E92\u6A21\u5F0F\u8BBE\u8BA1\u3001\u5168\u7F51\u7814\u62A5\u8C03\u7814\u4E0E\u4E1A\u52A1\u6D41\u7A0B\u81EA\u52A8\u5316",skills:["AI PRD \u7ED3\u6784\u5316\u64B0\u5199","Copilot vs Agent \u9009\u578B","\u5168\u7F51\u7ADE\u54C1\u6DF1\u5EA6\u8C03\u7814","\u4E1A\u52A1\u6D41\u7A0B\u81EA\u52A8\u5316"],curatedArticles:[{id:"aitools_pm_skills_\u4EA7\u54C1\u7ECF\u7406\u6280\u80FD\u5E02\u573A_\u516C\u4F17\u53F7\u7248_html",tag:"\u{1F3AF} PM \u6280\u80FD\u5E02\u573A"},{id:"aitools_agent_reach_\u8BA9AI\u4E0A\u7F51\u641C\u8D44\u6599_\u516C\u4F17\u53F7\u7248_html",tag:"\u{1F50D} \u5168\u7F51\u7814\u62A5\u641C\u96C6"}],inProgressText:"\u{1F331} \u300AAI \u539F\u751F PRD \u9700\u6C42\u89C4\u8303\u4E0E\u4EBA\u673A\u534F\u540C\u4EA4\u4E92\u8BBE\u8BA1\u300B\u5BA1\u6838\u6392\u671F\u4E2D..."},{level:"Level 3",title:"\u{1F916} \u96F6\u4EE3\u7801\u642D\u5EFA\u4E1A\u52A1\u667A\u80FD\u4F53 (Dify / \u6263\u5B50\u5B9E\u64CD)",desc:"\u65E0\u9700\u7F16\u5199\u590D\u6742\u4EE3\u7801\uFF0C\u901A\u8FC7\u53EF\u89C6\u5316\u754C\u9762\u642D\u5EFA\u4F01\u4E1A\u4E13\u5C5E\u77E5\u8BC6\u95EE\u7B54\u52A9\u624B\u3001\u4E1A\u52A1\u81EA\u52A8\u5316\u5DE5\u4F5C\u6D41\u4E0E\u667A\u80FD\u5BA2\u670D\u673A\u5668\u4EBA",skills:["\u4F01\u4E1A\u79C1\u6709\u77E5\u8BC6\u95EE\u7B54\u5E93","\u53EF\u89C6\u5316\u95EE\u7B54\u4EA4\u4E92\u754C\u9762","\u4E1A\u52A1\u75DB\u70B9\u4E0E\u610F\u56FE\u5206\u6790","\u5FAE\u4FE1/\u4F01\u5FAE\u5BA2\u670D\u63A5\u5165"],curatedArticles:[{id:"local_llm_knowledge_base_\u672C\u5730\u5927\u6A21\u578B\u77E5\u8BC6\u5E93\u7CFB\u5217_01_\u516C\u4F17\u53F7\u7248_html",tag:"\u{1F4DA} \u79C1\u6709\u77E5\u8BC6\u5E93"},{id:"local_llm_knowledge_base_\u672C\u5730\u5927\u6A21\u578B\u77E5\u8BC6\u5E93\u7CFB\u5217_04_\u516C\u4F17\u53F7\u7248_html",tag:"\u{1F5A5}\uFE0F \u53EF\u89C6\u5316\u95EE\u7B54"},{id:"customer_service_agent_\u5BA2\u670DAgent\u5B9E\u6218\u7CFB\u5217_01_html",tag:"\u{1F4AC} \u4E1A\u52A1\u75DB\u70B9\u5206\u6790"}],inProgressText:"\u{1F331} \u300A\u96F6\u4EE3\u7801\u5E73\u53F0\u6DF1\u5EA6\u6A2A\u8BC4\u4E0E\u4F01\u4E1A\u79C1\u6709\u77E5\u8BC6\u5E93 Bot \u5B9E\u64CD\u300B\u5BA1\u6838\u6392\u671F\u4E2D..."},{level:"Level 4",title:"\u{1F4C8} \u4E1A\u52A1 ROI \u8BC4\u4F30\u4E0E\u5546\u4E1A\u5316\u95ED\u73AF (\u51B3\u7B56\u4E0E\u843D\u5730)",desc:"\u638C\u63E1 AI \u9879\u76EE\u6295\u5165\u4EA7\u51FA\u6BD4\uFF08ROI\uFF09\u6D4B\u7B97\u3001\u4E1A\u52A1\u56E2\u961F\u5F15\u5165 SOP\u3001\u4E00\u4EBA\u516C\u53F8\uFF08Solopreneur\uFF09\u95ED\u73AF\u4E0E\u4F01\u4E1A\u843D\u5730\u6307\u5357",skills:["\u4F01\u4E1A AI \u9009\u578B ROI \u8D26\u672C","\u4E1A\u52A1\u56E2\u961F\u5F15\u5165 SOP","\u4E00\u4EBA\u516C\u53F8\u5546\u4E1A\u95ED\u73AF","\u590D\u6742\u4E1A\u52A1\u591A\u4F53\u534F\u540C"],curatedArticles:[{id:"customer_service_agent_\u5BA2\u670DAgent\u5B9E\u6218\u7CFB\u5217_08_\u516C\u4F17\u53F7\u7248_html",tag:"\u{1F91D} \u590D\u6742\u4E1A\u52A1\u4F1A\u8BCA"},{id:"ai_coding_AI_Coding\u7CFB\u5217_25_\u56E2\u961F\u534F\u4F5C_html",tag:"\u{1F465} \u56E2\u961F\u534F\u540C\u843D\u5730"}],inProgressText:"\u{1F331} \u300A\u4F01\u4E1A\u5F15\u5165 AI \u7684 ROI \u6210\u672C\u8D26\u672C\u4E0E\u4E1A\u52A1\u56E2\u961F\u843D\u5730 SOP\u300B\u5BA1\u6838\u6392\u671F\u4E2D..."}];t.mainContent.innerHTML=`
      <div class="max-w-4xl mx-auto animate-fade-in px-1 sm:px-0">
        <!-- Dual Track Switcher Pill -->
        <div class="text-center mb-8 sm:mb-10">
          <div class="inline-flex items-center p-1 rounded-2xl glass border border-white/15 text-xs sm:text-sm mb-5 shadow-lg max-w-full">
            <button onclick="window.AI_HUB.switchRoadmapTrack('tech')" class="px-3.5 sm:px-6 py-2 sm:py-2.5 rounded-xl font-bold transition flex items-center gap-1.5 sm:gap-2 ${e?"bg-indigo-600 text-white shadow-md":"text-slate-400 hover:text-white hover:bg-white/5"}">
              <span>\u{1F6E0}\uFE0F \u6280\u672F\u7814\u53D1\u8DEF\u7EBF</span>
              <span class="text-[10px] sm:text-xs opacity-75 font-normal hidden xs:inline">\uFF08\u5DE5\u7A0B\u5E08/\u67B6\u6784\uFF09</span>
            </button>
            <button onclick="window.AI_HUB.switchRoadmapTrack('business')" class="px-3.5 sm:px-6 py-2 sm:py-2.5 rounded-xl font-bold transition flex items-center gap-1.5 sm:gap-2 ${e?"text-slate-400 hover:text-white hover:bg-white/5":"bg-indigo-600 text-white shadow-md"}">
              <span>\u{1F3AF} \u4E1A\u52A1\u843D\u5730\u8DEF\u7EBF</span>
              <span class="text-[10px] sm:text-xs opacity-75 font-normal hidden xs:inline">\uFF08\u4EA7\u54C1/\u4E1A\u52A1/\u8FD0\u8425\uFF09</span>
            </button>
          </div>

          <h2 class="text-2xl sm:text-3xl font-extrabold text-white">
            ${e?'\u4ECE\u96F6\u5230\u67B6\u6784\u5E08\u7684 <span class="gradient-text">AI \u5F00\u53D1\u8005</span> \u8FDB\u9636\u8DEF\u7EBF':'\u4ECE\u96F6\u5230\u64CD\u76D8\u624B\u7684 <span class="gradient-text">AI \u4EA7\u54C1\u4E0E\u4E1A\u52A1\u843D\u5730</span> \u8DEF\u7EBF'}
          </h2>
          <p class="text-slate-300 text-xs sm:text-sm mt-2 max-w-xl mx-auto leading-relaxed">
            ${e?"\u6309\u7167 4 \u4E2A\u5DE5\u7A0B\u8FDB\u9636\u9636\u6BB5\u5FAA\u5E8F\u6E10\u8FDB\u7814\u8BFB\uFF0C\u638C\u63E1\u4ECE\u5927\u6A21\u578B\u539F\u7406\u5230 Agent \u843D\u5730\u3001AI \u7F16\u7A0B\u5B9E\u6218\u4E0E\u5168\u6808\u5DE5\u7A0B\u4F53\u7CFB\u3002":"\u4E13\u4E3A\u4EA7\u54C1\u7ECF\u7406\u3001\u4E1A\u52A1\u4E13\u5BB6\u4E0E\u8FD0\u8425\u6253\u9020\uFF1A\u4E25\u683C\u5254\u9664\u5E95\u5C42\u4EE3\u7801\u5E72\u6270\uFF0C\u7CBE\u9009\u4E1A\u52A1\u5B9E\u64CD\u4E0E\u4EA7\u54C1\u843D\u5730\u6587\u732E\u3002"}
          </p>
        </div>

        <div class="space-y-6 sm:space-y-8">
          ${r.map(n=>{const l=e?i.data.articles.filter(o=>n.categories.includes(o.categoryId)).length:(n.curatedArticles||[]).length;return`
              <div class="roadmap-step">
                <div class="roadmap-dot"></div>
                <div class="p-4 sm:p-6 md:p-8 rounded-2xl sm:rounded-3xl glass border border-white/10">
                  <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 sm:gap-4 border-b border-white/10 pb-3 sm:pb-4 mb-3 sm:mb-4">
                    <div>
                      <span class="text-[11px] sm:text-xs font-mono font-bold text-indigo-400 bg-indigo-500/10 px-2 py-0.5 sm:px-2.5 sm:py-1 rounded-md border border-indigo-500/20">${n.level}</span>
                      <h3 class="text-lg sm:text-xl font-bold text-white mt-1.5">${n.title}</h3>
                      <p class="text-xs text-slate-300 mt-1">${n.desc}</p>
                    </div>

                    <div class="shrink-0">
                      <span class="text-[11px] sm:text-xs font-medium px-2.5 sm:px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 inline-block">
                        ${e?`\u5171 ${l} \u7BC7\u4E13\u680F\u89E3\u6790`:`\u5DF2\u6536\u5F55 ${l} \u7BC7\u7CBE\u9009\u5B9E\u64CD`}
                      </span>
                    </div>
                  </div>

                  <!-- Key Competencies Skills Badges -->
                  <div class="flex flex-wrap items-center gap-1.5 my-3">
                    ${(n.skills||[]).map(o=>`
                      <span class="text-[10px] sm:text-[11px] px-2 py-0.5 rounded-md bg-white/5 text-slate-300 border border-white/10">
                        \u2713 ${o}
                      </span>
                    `).join("")}
                  </div>

                  ${e?`
                    <!-- Tech Track: Category List -->
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 sm:gap-3 mt-3 sm:mt-4">
                      ${n.categories.map(o=>{const d=i.data.categories.find(f=>f.id===o);if(!d)return"";const m=i.data.articles.filter(f=>f.categoryId===o).length;return`
                          <div onclick="window.AI_HUB.switchCategory('${d.id}')" class="p-3 sm:p-3.5 rounded-xl bg-white/5 hover:bg-white/10 border border-white/5 hover:border-indigo-500/30 transition flex items-center justify-between cursor-pointer group">
                            <span class="flex items-center gap-2 text-xs sm:text-sm text-slate-200 group-hover:text-indigo-400 font-medium">
                              <span class="text-base sm:text-lg">${d.icon}</span>
                              <span>${d.name}</span>
                            </span>
                            <span class="text-[11px] sm:text-xs bg-white/10 px-2 sm:px-2.5 py-0.5 sm:py-1 rounded-full text-slate-300 group-hover:bg-indigo-600 group-hover:text-white transition">${m} \u7BC7</span>
                          </div>
                        `}).join("")}
                    </div>
                  `:`
                    <!-- Business Track: Curated Specific Article Cards -->
                    <div class="space-y-3 mt-3 sm:mt-4">
                      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 sm:gap-3">
                        ${(n.curatedArticles||[]).map(o=>{const d=i.data.articles.find(m=>m.id===o.id);return d?`
                            <div onclick="window.AI_HUB.openReaderById('${d.id}')" class="p-3 sm:p-3.5 rounded-xl bg-white/5 hover:bg-white/10 border border-white/5 hover:border-indigo-500/30 transition flex flex-col justify-between cursor-pointer group shadow-sm">
                              <div>
                                <div class="flex items-center justify-between gap-2 mb-1.5">
                                  <span class="text-[10px] sm:text-[11px] font-bold px-2 py-0.5 rounded-md bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                                    ${o.tag}
                                  </span>
                                  <span class="text-[10px] sm:text-[11px] text-slate-400">\u23F1\uFE0F ${d.readTime}</span>
                                </div>
                                <h4 class="text-xs sm:text-sm font-semibold text-slate-100 group-hover:text-indigo-300 line-clamp-2 transition leading-snug">
                                  ${d.title}
                                </h4>
                              </div>
                              <div class="flex items-center justify-between mt-2.5 pt-2 border-t border-white/5 text-[11px] text-indigo-400 group-hover:text-indigo-300 font-medium">
                                <span>\u{1F4D6} \u7ACB\u5373\u9605\u8BFB</span>
                                <span class="transform group-hover:translate-x-1 transition">\u2192</span>
                              </div>
                            </div>
                          `:""}).join("")}
                      </div>

                      <!-- In-Progress Placeholder Badge -->
                      <div class="p-2.5 sm:p-3 rounded-xl bg-indigo-500/5 border border-dashed border-indigo-500/20 flex items-center justify-between text-xs text-indigo-300">
                        <span class="flex items-center gap-1.5">
                          <span>${n.inProgressText}</span>
                        </span>
                        <span class="text-[10px] text-slate-400 hidden sm:inline">\u516C\u4F17\u53F7\u3010\u5927\u524D\u7AEF\u5DE5\u7A0B\u5E08\u3011\u6BCF\u5468\u9996\u53D1\u540C\u6B65</span>
                      </div>
                    </div>
                  `}
                </div>
              </div>
            `}).join("")}
        </div>
      </div>
    `}function L(){return`
      <div class="text-center py-20 animate-fade-in">
        <div class="text-5xl mb-4">\u{1F50D}</div>
        <h3 class="text-xl font-bold text-white">\u672A\u627E\u5230\u5339\u914D\u7684\u5B66\u4E60\u8D44\u6599</h3>
        <p class="text-slate-400 text-sm mt-2">\u8BF7\u5C1D\u8BD5\u66F4\u6362\u641C\u7D22\u5173\u952E\u5B57\uFF0C\u6216\u8C03\u6574\u5206\u7C7B\u7B5B\u9009\u6761\u4EF6\u3002</p>
        <button onclick="window.AI_HUB.resetFilters()" class="mt-6 px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium transition">
          \u91CD\u7F6E\u6240\u6709\u7B5B\u9009\u6761\u4EF6
        </button>
      </div>
    `}function O(e){return e?e.replace(/^### (.*$)/gim,'<h3 id="$1">$1</h3>').replace(/^## (.*$)/gim,'<h2 id="$1">$1</h2>').replace(/^# (.*$)/gim,'<h1 id="$1">$1</h1>').replace(/^\> (.*$)/gim,"<blockquote>$1</blockquote>").replace(/\*\*(.*)\*\*/gim,"<strong>$1</strong>").replace(/\*(.*)\*/gim,"<em>$1</em>").replace(/```([a-z]*)\n([\s\S]*?)```/gim,"<pre><code>$2</code></pre>").replace(/`([^`]+)`/gim,"<code>$1</code>").replace(/\n\n/gim,"</p><p>").replace(/\[([^\]]+)\]\(([^)]+)\)/gim,'<a href="$2" target="_blank">$1</a>'):""}function u(e){i.currentArticle=e,i.history=[{id:e.id,time:new Date().toLocaleTimeString()},...i.history.filter(s=>s.id!==e.id)],localStorage.setItem("ai_hub_history",JSON.stringify(i.history)),window.history.replaceState(null,"",`?article=${e.id}`),t.readerTitle&&(t.readerTitle.textContent=e.title);const a=i.data.categories.find(s=>s.id===e.categoryId);t.readerCategory&&(t.readerCategory.textContent=a?`${a.icon} ${a.name}`:"\u7CFB\u5217\u6587\u6863"),F(),e.format==="md"?(t.readerIframeContainer&&t.readerIframeContainer.classList.add("hidden"),t.readerMarkdownContainer&&t.readerMarkdownContainer.classList.remove("hidden"),t.markdownContent&&(t.markdownContent.innerHTML='<div class="text-center py-16 text-slate-400">\u6B63\u5728\u89E3\u6790\u5E76\u6E32\u67D3 Markdown \u6587\u6863...</div>'),fetch(e.path).then(s=>s.text()).then(s=>{let r="";window.marked&&typeof window.marked.parse=="function"?r=window.marked.parse(s):r=O(s),t.markdownContent&&(t.markdownContent.innerHTML=r);const n=[];s.split(`
`).forEach(o=>{(o.startsWith("## ")||o.startsWith("### "))&&n.push(o.replace(/^#+\s*/,"").trim())}),e.toc=n.slice(0,15),M(e)}).catch(s=>{t.markdownContent&&(t.markdownContent.innerHTML=`<div class="text-rose-400 p-6">\u52A0\u8F7D Markdown \u6587\u4EF6\u5931\u8D25\uFF1A${s.message}</div>`)})):(t.readerMarkdownContainer&&t.readerMarkdownContainer.classList.add("hidden"),t.readerIframeContainer&&t.readerIframeContainer.classList.remove("hidden"),t.readerFrame&&(t.readerFrame.src=e.path,t.readerFrame.onload=function(){try{const s=t.readerFrame.contentDocument||t.readerFrame.contentWindow.document;if(!s)return;const r=s.createElement("style");r.textContent=`
              body {
                background: #ffffff !important;
                color: #1e293b !important;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
                line-height: 1.8 !important;
                letter-spacing: 0.2px !important;
              }
              .container {
                max-width: 760px !important;
                margin: 0 auto !important;
                background: #ffffff !important;
                box-shadow: none !important;
                padding: 24px 16px !important;
              }
              p {
                color: #334155 !important;
                font-size: 15.5px !important;
                line-height: 1.8 !important;
              }
              h1, h2, h3, h4 {
                color: #0f172a !important;
                font-weight: 700 !important;
              }
              h2 .title-text, h3 .title-text {
                color: #0f172a !important;
              }
              strong, b {
                color: #0f172a !important;
                font-weight: 700 !important;
              }
              a {
                color: #4f46e5 !important;
                text-decoration: underline !important;
                text-underline-offset: 3px !important;
                cursor: pointer !important;
              }
              a:hover {
                color: #4338ca !important;
              }
              blockquote {
                background: #f8fafc !important;
                border-left: 4px solid #6366f1 !important;
                color: #334155 !important;
                border-radius: 0 8px 8px 0 !important;
              }
              blockquote p {
                color: #334155 !important;
              }
              .code-block, pre {
                background: #0f172a !important;
                border-radius: 8px !important;
              }
              .code-block code, pre code {
                color: #f8fafc !important;
              }
              table {
                color: #334155 !important;
              }
              th {
                background: #f1f5f9 !important;
                color: #0f172a !important;
              }
              td {
                color: #334155 !important;
              }
            `,s.head.appendChild(r),s.querySelectorAll("a[href]").forEach(l=>{l.addEventListener("click",function(o){const d=l.getAttribute("href");if(!d)return;if(d.startsWith("#")){o.preventDefault();const p=s.querySelector(d);p&&p.scrollIntoView({behavior:"smooth"});return}if(d.startsWith("http://")||d.startsWith("https://")||d.startsWith("//")){l.target="_blank";return}o.preventDefault();const m=d.split("?")[0].split("#")[0],f=m.split("/").pop(),S=i.data.articles.find(p=>p.path===m||p.path.endsWith(m)||p.path.endsWith(f)||p.id===m.replace(/\.html$/,""));if(S)u(S);else{let p=e.path.substring(0,e.path.lastIndexOf("/")+1),V=new URL(d,window.location.origin+"/"+p).pathname.replace(/^\//,"");t.readerFrame.src=V}})})}catch(s){console.warn("Iframe link handling notice:",s)}}),M(e)),t.readerModal&&(t.readerModal.classList.remove("hidden"),document.body.style.overflow="hidden")}function T(){i.currentArticle=null,t.readerModal&&(t.readerModal.classList.add("hidden"),document.body.style.overflow=""),t.readerFrame&&(t.readerFrame.src="about:blank"),window.history.replaceState(null,"",window.location.pathname),c()}function F(){if(!i.currentArticle)return;const e=i.currentArticle;t.btnOpenExternal&&(t.btnOpenExternal.href=e.path);const a=i.data.articles.filter(r=>r.categoryId===e.categoryId),s=a.findIndex(r=>r.id===e.id);t.btnPrevArticle&&(t.btnPrevArticle.disabled=s<=0,t.btnPrevArticle.classList.toggle("opacity-30",s<=0),t.btnPrevArticle.classList.toggle("cursor-not-allowed",s<=0)),t.btnNextArticle&&(t.btnNextArticle.disabled=s===-1||s>=a.length-1,t.btnNextArticle.classList.toggle("opacity-30",s===-1||s>=a.length-1),t.btnNextArticle.classList.toggle("cursor-not-allowed",s===-1||s>=a.length-1))}function M(e){if(!t.readerTocList)return;const a=e.toc||[];if(a.length===0){t.readerTocList.innerHTML='<div class="text-xs text-slate-400 py-4 text-center">\u672C\u7BC7\u65E0\u591A\u7EA7\u6807\u9898\u7D22\u5F15</div>';return}t.readerTocList.innerHTML=a.map((s,r)=>`
      <button onclick="window.AI_HUB.scrollToHeading('${s}')" class="w-full text-left p-2.5 rounded-xl hover:bg-white/10 text-xs text-slate-300 hover:text-white transition truncate" title="${s}">
        ${r+1}. ${s}
      </button>
    `).join("")}function W(e){if(i.currentArticle&&i.currentArticle.format==="md"&&t.markdownContent){const a=t.markdownContent.querySelectorAll("h1, h2, h3, h4");for(const s of a)if(s.textContent.trim().includes(e)||e.includes(s.textContent.trim())){s.scrollIntoView({behavior:"smooth",block:"start"});break}}}function v(e){if(!i.currentArticle)return;const a=i.data.articles.filter(r=>r.categoryId===i.currentArticle.categoryId),s=a.findIndex(r=>r.id===i.currentArticle.id);e==="prev"&&s>0?u(a[s-1]):e==="next"&&s<a.length-1&&u(a[s+1])}function B(){t.wechatModal&&(t.wechatModal.classList.remove("hidden"),document.body.style.overflow="hidden")}function E(){t.wechatModal&&(t.wechatModal.classList.add("hidden"),document.body.style.overflow="")}function Q(){const e="\u5927\u524D\u7AEF\u5DE5\u7A0B\u5E08";navigator.clipboard&&window.isSecureContext?navigator.clipboard.writeText(e).then(()=>{b("\u5DF2\u590D\u5236\u516C\u4F17\u53F7\u540D\u79F0\uFF1A\u5927\u524D\u7AEF\u5DE5\u7A0B\u5E08","\u{1F4CB}")}).catch(()=>{w(e)}):w(e)}function z(e){navigator.clipboard&&window.isSecureContext?navigator.clipboard.writeText(e).then(()=>{b(`\u5DF2\u590D\u5236\u53E3\u4EE4\u3010${e}\u3011\uFF0C\u8BF7\u5728\u5FAE\u4FE1\u516C\u4F17\u53F7\u540E\u53F0\u76F4\u63A5\u53D1\u9001\uFF01`,"\u{1F4CB}")}).catch(()=>{w(e)}):w(e),B()}function w(e){const a=document.createElement("input");a.value=e,document.body.appendChild(a),a.select();try{document.execCommand("copy"),b("\u5DF2\u590D\u5236\u516C\u4F17\u53F7\u540D\u79F0\uFF1A\u5927\u524D\u7AEF\u5DE5\u7A0B\u5E08","\u{1F4CB}")}catch{b("\u516C\u4F17\u53F7\u540D\u79F0\uFF1A\u5927\u524D\u7AEF\u5DE5\u7A0B\u5E08","\u{1F4AC}")}document.body.removeChild(a)}function N(){t.themeToggle&&t.themeToggle.addEventListener("click",I),t.searchInput&&t.searchInput.addEventListener("input",e=>{i.searchQuery=e.target.value.trim(),t.searchClear&&t.searchClear.classList.toggle("hidden",!i.searchQuery),c()}),t.searchClear&&t.searchClear.addEventListener("click",()=>{i.searchQuery="",t.searchInput.value="",t.searchClear.classList.add("hidden"),c()}),t.categoryTabs&&t.categoryTabs.addEventListener("click",e=>{const a=e.target.closest("[data-category]");a&&(i.activeCategory=a.dataset.category,i.activeCategory!=="all"&&i.viewMode==="roadmap"&&(i.viewMode="grid",x()),h(),c())}),t.categorySelect&&t.categorySelect.addEventListener("change",e=>{i.activeCategory=e.target.value,i.activeCategory!=="all"&&i.viewMode==="roadmap"&&(i.viewMode="grid",x()),h(),c()}),t.viewButtons.forEach(e=>{e.addEventListener("click",()=>{i.viewMode=e.dataset.view,x(),c()})}),t.btnCloseReader&&t.btnCloseReader.addEventListener("click",T),t.btnPrevArticle&&t.btnPrevArticle.addEventListener("click",()=>v("prev")),t.btnNextArticle&&t.btnNextArticle.addEventListener("click",()=>v("next")),t.btnToggleToc&&t.btnToggleToc.addEventListener("click",()=>{t.readerTocDrawer&&t.readerTocDrawer.classList.toggle("hidden")}),document.addEventListener("keydown",e=>{(e.metaKey||e.ctrlKey)&&e.key==="k"&&(e.preventDefault(),t.searchInput?.focus()),e.key==="Escape"&&(i.currentArticle&&T(),t.wechatModal&&!t.wechatModal.classList.contains("hidden")&&E()),i.currentArticle&&!e.target.matches("input, textarea")&&(e.key==="ArrowLeft"&&v("prev"),e.key==="ArrowRight"&&v("next")),(e.key==="t"||e.key==="T")&&!e.target.matches("input, textarea")&&!i.currentArticle&&I()})}window.AI_HUB={openReaderById:function(e){const a=i.data.articles.find(s=>s.id===e);a&&u(a)},switchCategory:function(e){i.activeCategory=e,i.viewMode="grid",h(),x(),c(),window.scrollTo({top:400,behavior:"smooth"})},openWeChatModal:B,closeWeChatModal:E,copyWeChatName:Q,scrollToHeading:W,resetFilters:function(){i.activeCategory="all",i.searchQuery="",t.searchInput&&(t.searchInput.value=""),h(),c()},switchView:function(e){i.viewMode=e,x(),c()},switchRoadmapTrack:function(e){i.roadmapTrack=e,_()}},document.readyState==="loading"?document.addEventListener("DOMContentLoaded",y):y()})();