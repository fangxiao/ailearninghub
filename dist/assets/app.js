(function(){"use strict";const a={data:window.SITE_DATA||{categories:[],articles:[],stats:{}},activeCategory:"all",searchQuery:"",difficultyFilter:"all",viewMode:"roadmap",roadmapTrack:"tech",theme:localStorage.getItem("ai_hub_theme")||"dark",readerTheme:localStorage.getItem("ai_hub_reader_theme")||"default",readerFontSize:parseInt(localStorage.getItem("ai_hub_reader_fontsize")||"16",10),currentArticle:null,history:JSON.parse(localStorage.getItem("ai_hub_history")||"[]")},s={app:document.getElementById("app"),themeToggle:document.getElementById("theme-toggle"),themeIcon:document.getElementById("theme-icon"),searchInput:document.getElementById("search-input"),searchClear:document.getElementById("search-clear"),categoryTabs:document.getElementById("category-tabs"),categorySelect:document.getElementById("category-select"),viewButtons:document.querySelectorAll("[data-view]"),mainContent:document.getElementById("main-content"),readerModal:document.getElementById("reader-modal"),readerIframeContainer:document.getElementById("reader-iframe-container"),readerMarkdownContainer:document.getElementById("reader-markdown-container"),readerFrame:document.getElementById("reader-frame"),markdownContent:document.getElementById("markdown-content"),readerTitle:document.getElementById("reader-title"),readerCategory:document.getElementById("reader-category"),readerTocList:document.getElementById("reader-toc-list"),readerTocDrawer:document.getElementById("reader-toc-drawer"),wechatModal:document.getElementById("wechat-modal"),btnPrevArticle:document.getElementById("btn-prev-article"),btnNextArticle:document.getElementById("btn-next-article"),btnOpenExternal:document.getElementById("btn-open-external"),btnCloseReader:document.getElementById("btn-close-reader"),btnToggleToc:document.getElementById("btn-toggle-toc"),toast:document.getElementById("toast")};function y(){$(a.theme),H(),R(),V(),c();const e=new URLSearchParams(window.location.search),t=e.get("category"),i=e.get("article"),r=e.get("view");if(r&&["grid","list","tree","shelf","roadmap","my-space","showcases","works"].includes(r)&&(a.viewMode=r==="works"?"showcases":r,a.viewMode=r,p()),t&&(t==="all"||a.data.categories.some(o=>o.id===t))&&(a.activeCategory=t,u()),i){const o=a.data.articles.find(d=>d.id===i||d.path===i);o&&g(o)}const n=()=>{const o=window.location.hash;o==="#showcases"||o==="#works"||o==="#tools"?(a.viewMode="showcases",p(),c()):o==="#roadmap"&&(a.viewMode="roadmap",p(),c())};window.addEventListener("hashchange",n),n()}function $(e){a.theme=e,localStorage.setItem("ai_hub_theme",e),e==="light"?(document.documentElement.classList.add("light-theme"),document.documentElement.classList.remove("dark"),s.themeIcon&&(s.themeIcon.innerHTML="\u2600\uFE0F")):(document.documentElement.classList.remove("light-theme"),document.documentElement.classList.add("dark"),s.themeIcon&&(s.themeIcon.innerHTML="\u{1F319}"))}function k(){$(a.theme==="dark"?"light":"dark")}let C;function b(e,t="\u2728"){s.toast&&(s.toast.innerHTML=`<span class="text-xl">${t}</span><span>${e}</span>`,s.toast.classList.remove("opacity-0","translate-y-4","pointer-events-none"),s.toast.classList.add("opacity-100","translate-y-0"),clearTimeout(C),C=setTimeout(()=>{s.toast.classList.add("opacity-0","translate-y-4","pointer-events-none"),s.toast.classList.remove("opacity-100","translate-y-0")},2400))}function G(){s.statsArticles&&(s.statsArticles.textContent=a.data.articles.length),s.statsCategories&&(s.statsCategories.textContent=a.data.categories.length),s.statsEbooks&&(s.statsEbooks.textContent=a.data.categories.find(e=>e.id==="ebooks")?.count||7)}function H(){if(!s.categoryTabs)return;const e=a.data.categories;let t=`
      <button data-category="all" class="category-tab px-3.5 py-1.5 rounded-xl text-xs font-medium border flex items-center gap-1.5 transition ${a.activeCategory==="all"?"active":"border-white/10 text-slate-400 hover:text-white hover:bg-white/5"}">
        <span>\u{1F310}</span>
        <span>\u5168\u90E8\u5206\u7C7B</span>
      </button>
    `;e.forEach(i=>{const r=a.activeCategory===i.id;t+=`
        <button data-category="${i.id}" class="category-tab px-3.5 py-1.5 rounded-xl text-xs font-medium border flex items-center gap-1.5 transition ${r?"active":"border-white/10 text-slate-400 hover:text-white hover:bg-white/5"}">
          <span>${i.icon}</span>
          <span>${i.name}</span>
        </button>
      `}),s.categoryTabs.innerHTML=t}function R(){if(!s.categorySelect)return;let e=`<option value="all">\u{1F310} \u5168\u90E8\u7CFB\u5217\u5206\u7C7B (${a.data.articles.length} \u7BC7)</option>`;a.data.categories.forEach(t=>{e+=`<option value="${t.id}">${t.icon} ${t.name} (${t.count} \u7BC7)</option>`}),s.categorySelect.innerHTML=e,s.categorySelect.value=a.activeCategory}function u(){document.querySelectorAll(".category-tab").forEach(e=>{e.dataset.category===a.activeCategory?(e.classList.add("active"),e.classList.remove("border-white/10","text-slate-400","hover:bg-white/5")):(e.classList.remove("active"),e.classList.add("border-white/10","text-slate-400","hover:bg-white/5"))}),s.categorySelect&&(s.categorySelect.value=a.activeCategory)}function p(){s.viewButtons.forEach(e=>{e.dataset.view===a.viewMode?(e.classList.add("bg-indigo-600","text-white"),e.classList.remove("text-slate-400","hover:text-white","hover:bg-white/5")):(e.classList.remove("bg-indigo-600","text-white"),e.classList.add("text-slate-400","hover:text-white","hover:bg-white/5"))})}function I(){return a.data.articles.filter(e=>{if(a.activeCategory!=="all"&&e.categoryId!==a.activeCategory)return!1;if(a.searchQuery){const t=a.searchQuery.toLowerCase(),i=e.title.toLowerCase().includes(t),r=(e.subtitle||"").toLowerCase().includes(t),n=(e.summary||"").toLowerCase().includes(t),o=(e.toc||[]).some(l=>l.toLowerCase().includes(t)),d=(e.badge||"").toLowerCase().includes(t);if(!i&&!r&&!n&&!o&&!d)return!1}return!0})}function c(){if(!s.mainContent)return;const e=document.getElementById("category-nav-bar"),t=document.getElementById("hero-banner-section");e&&(["grid","list"].includes(a.viewMode)?e.classList.remove("hidden"):e.classList.add("hidden")),t&&(a.viewMode==="showcases"?t.classList.add("hidden"):t.classList.remove("hidden")),a.viewMode==="grid"?j():a.viewMode==="list"?D():a.viewMode==="tree"?U():a.viewMode==="shelf"?renderShelfView():a.viewMode==="roadmap"?L():a.viewMode==="my-space"?renderMySpaceView():a.viewMode==="showcases"&&N()}function x(e){if(!a.searchQuery||!e)return e;const t=a.searchQuery.replace(/[.*+?^${}()|[\]\\]/g,"\\$&"),i=new RegExp(`(${t})`,"gi");return e.replace(i,'<mark class="bg-amber-400/30 text-amber-300 px-1 rounded">$1</mark>')}function j(){const e=I(),t=a.data.categories;if(e.length===0){s.mainContent.innerHTML=_();return}if(a.activeCategory!=="all"||a.searchQuery||a.formatFilter!=="all"){const r=t.find(d=>d.id===a.activeCategory);let n="";r&&!a.searchQuery?n=P(r,e):a.searchQuery&&(n=`
          <div class="mb-8 p-6 rounded-2xl glass border border-white/10 flex items-center justify-between">
            <div>
              <div class="text-sm text-indigo-400 font-medium">\u641C\u7D22\u7ED3\u679C</div>
              <h2 class="text-2xl font-bold mt-1 text-white">\u627E\u5230 <span class="text-indigo-400">${e.length}</span> \u7BC7\u5339\u914D\u6587\u6863</h2>
              <p class="text-sm text-slate-400 mt-1">\u5173\u952E\u5B57\uFF1A"${a.searchQuery}"</p>
            </div>
            <button id="btn-clear-search-res" class="px-4 py-2 text-xs rounded-xl bg-white/10 hover:bg-white/20 text-white transition">\u6E05\u7A7A\u641C\u7D22</button>
          </div>
        `),s.mainContent.innerHTML=`
        ${n}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-fade-in">
          ${e.map(A).join("")}
        </div>
      `;const o=document.getElementById("btn-clear-search-res");o&&o.addEventListener("click",()=>{a.searchQuery="",s.searchInput.value="",c()});return}let i="";t.forEach(r=>{const n=a.data.articles.filter(d=>d.categoryId===r.id);if(n.length===0)return;const o=n[0];i+=`
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
                ${o?`
                  <button onclick="window.AI_HUB.openReaderById('${o.id}')" class="btn-read px-4 py-2 text-xs font-bold rounded-xl shadow-lg flex items-center gap-1.5">
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
      `}),s.mainContent.innerHTML=i}function P(e,t){return`
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
                <span class="text-xs text-slate-400 bg-white/5 px-2.5 py-1 rounded-full border border-white/5">\u5171 ${t.length} \u7BC7\u7CBE\u9009</span>
              </div>
              <p class="text-sm md:text-base text-slate-300 mt-2 max-w-2xl">${e.desc}</p>
            </div>
          </div>

          <div class="flex flex-wrap items-center gap-3 shrink-0">
            <button onclick="window.AI_HUB.openReaderById('${t[0]?.id}')" class="btn-read px-5 py-2.5 rounded-xl font-bold text-sm shadow-lg flex items-center gap-2">
              <span>\u26A1 \u4ECE\u7B2C 1 \u7AE0\u5F00\u59CB\u9605\u8BFB</span>
            </button>
          </div>
        </div>
      </div>
    `}function A(e){const t=a.data.categories.find(r=>r.id===e.categoryId)||{};let i="bg-blue-500/20 text-blue-400 border-blue-500/30";return e.format==="pdf"&&(i="bg-rose-500/20 text-rose-400 border-rose-500/30"),e.format==="md"&&(i="bg-amber-500/20 text-amber-400 border-amber-500/30"),`
      <div class="article-card rounded-2xl glass border border-white/10 p-6 flex flex-col justify-between relative group">
        <div>
          <div class="flex items-center justify-between gap-2 mb-3">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="badge-chip ${i} border">${e.badge}</span>
              <span class="text-xs text-slate-400 flex items-center gap-1">
                <span>\u23F1\uFE0F</span>
                <span>${e.readTime}</span>
              </span>
              <span class="text-xs text-slate-400 bg-white/5 px-2 py-0.5 rounded-md">${e.sizeStr}</span>
            </div>
          </div>

          <h3 class="text-lg font-bold text-white group-hover:text-indigo-400 transition line-clamp-2 cursor-pointer" onclick="window.AI_HUB.openReaderById('${e.id}')">
            ${x(e.title)}
          </h3>

          ${e.subtitle?`
            <div class="text-xs font-medium text-indigo-400/90 mt-1.5 line-clamp-1">
              ${x(e.subtitle)}
            </div>
          `:""}

          <p class="text-xs text-slate-400 mt-2.5 line-clamp-3 leading-relaxed">
            ${x(e.summary||"\u70B9\u51FB\u8FDB\u5165\u9605\u8BFB\u5168\u7BC7\u8BE6\u7EC6\u56FE\u6587\u5185\u5BB9\u4E0E\u6280\u672F\u62C6\u89E3\u3002")}
          </p>
        </div>

        <div class="pt-5 mt-5 border-t border-white/5 flex items-center justify-between gap-3">
          <div class="flex items-center gap-1.5 text-xs text-slate-400">
            <span>${t.icon||"\u{1F4C1}"}</span>
            <span class="truncate max-w-[120px]">${t.name||"\u7CFB\u5217\u6587\u6863"}</span>
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
    `}function D(){const e=I();if(e.length===0){s.mainContent.innerHTML=_();return}s.mainContent.innerHTML=`
      <div class="rounded-2xl sm:rounded-3xl glass border border-white/10 overflow-hidden animate-fade-in">
        <div class="p-4 sm:p-6 border-b border-white/10 flex items-center justify-between">
          <div>
            <h3 class="text-lg sm:text-xl font-bold text-white">\u6587\u6863\u901F\u67E5\u5217\u8868</h3>
            <p class="text-xs text-slate-400 mt-0.5">\u5171\u627E\u5230 ${e.length} \u7BC7\u76F8\u5173\u8D44\u6599</p>
          </div>
        </div>

        <!-- Mobile Card List View (< 640px) -->
        <div class="block sm:hidden divide-y divide-white/5">
          ${e.map(t=>{const i=a.data.categories.find(r=>r.id===t.categoryId)||{};return`
              <div class="p-4 hover:bg-white/5 transition flex flex-col gap-2.5">
                <div class="flex items-center justify-between gap-2">
                  <span class="inline-flex items-center gap-1 text-[11px] text-slate-300 bg-white/5 px-2 py-0.5 rounded-lg border border-white/5">
                    <span>${i.icon||"\u{1F4C1}"}</span>
                    <span class="truncate max-w-[120px]">${i.name||"\u5176\u4ED6"}</span>
                  </span>
                  <span class="text-[10px] text-slate-400 font-mono">${t.readTime}</span>
                </div>

                <div class="font-bold text-sm text-white hover:text-indigo-400 cursor-pointer line-clamp-2" onclick="window.AI_HUB.openReaderById('${t.id}')">
                  ${x(t.title)}
                </div>

                ${t.subtitle?`<div class="text-xs text-slate-400 line-clamp-1">${x(t.subtitle)}</div>`:""}

                <div class="flex items-center justify-between pt-1">
                  <span class="badge-chip text-[10px] bg-white/5 border border-white/10 text-slate-300 uppercase">${t.format}</span>
                  <div class="flex items-center gap-2">
                    <a href="${t.path}" target="_blank" class="px-2.5 py-1 rounded-lg bg-white/5 hover:bg-white/10 text-slate-300 text-xs border border-white/10">\u2197 \u72EC\u7ACB\u9875</a>
                    <button onclick="window.AI_HUB.openReaderById('${t.id}')" class="btn-read px-3 py-1 rounded-lg text-xs font-bold transition">
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
              ${e.map(t=>{const i=a.data.categories.find(r=>r.id===t.categoryId)||{};return`
                  <tr class="hover:bg-white/5 transition">
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span class="inline-flex items-center gap-1.5 text-xs text-slate-300 bg-white/5 px-2.5 py-1 rounded-lg border border-white/5">
                        <span>${i.icon||"\u{1F4C1}"}</span>
                        <span>${i.name||"\u5176\u4ED6"}</span>
                      </span>
                    </td>
                    <td class="px-6 py-4">
                      <div class="font-medium text-white hover:text-indigo-400 cursor-pointer" onclick="window.AI_HUB.openReaderById('${t.id}')">
                        ${x(t.title)}
                      </div>
                      ${t.subtitle?`<div class="text-xs text-slate-400 mt-0.5 line-clamp-1">${x(t.subtitle)}</div>`:""}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span class="badge-chip text-xs bg-white/5 border border-white/10 text-slate-300 uppercase">${t.format}</span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-xs text-slate-400">
                      ${t.readTime}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-xs text-slate-400">
                      ${t.sizeStr}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-right">
                      <div class="flex items-center justify-end gap-2">
                        <button onclick="window.AI_HUB.openReaderById('${t.id}')" class="btn-read px-3.5 py-1.5 rounded-lg text-xs font-bold transition">
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
    `}function U(){const e=a.data.categories;s.mainContent.innerHTML=`
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 sm:gap-8 animate-fade-in">
        <div class="lg:col-span-1 space-y-3">
          <div class="p-4 sm:p-6 rounded-2xl sm:rounded-3xl glass border border-white/10">
            <h3 class="text-base sm:text-lg font-bold text-white mb-3 sm:mb-4">\u{1F4DA} \u7CFB\u5217\u77E5\u8BC6\u5927\u7EB2</h3>
            <div class="grid grid-cols-2 lg:grid-cols-1 gap-1.5">
              ${e.map(t=>{const i=a.data.articles.filter(r=>r.categoryId===t.id).length;return`
                  <a href="#tree-cat-${t.id}" class="flex items-center justify-between p-2 sm:p-2.5 rounded-xl hover:bg-white/10 text-slate-300 hover:text-white text-xs sm:text-sm transition">
                    <span class="flex items-center gap-1.5 sm:gap-2 truncate">
                      <span>${t.icon}</span>
                      <span class="truncate">${t.name}</span>
                    </span>
                    <span class="text-[10px] sm:text-xs bg-white/10 px-1.5 sm:px-2 py-0.5 rounded-full shrink-0">${i}</span>
                  </a>
                `}).join("")}
            </div>
          </div>
        </div>

        <div class="lg:col-span-2 space-y-6">
          ${e.map(t=>{const i=a.data.articles.filter(r=>r.categoryId===t.id);return i.length===0?"":`
              <div id="tree-cat-${t.id}" class="p-4 sm:p-6 md:p-8 rounded-2xl sm:rounded-3xl glass border border-white/10">
                <div class="flex items-center justify-between border-b border-white/10 pb-3 sm:pb-4 mb-4 sm:mb-6">
                  <div class="flex items-center gap-2.5 sm:gap-3">
                    <span class="text-2xl sm:text-3xl">${t.icon}</span>
                    <div>
                      <h4 class="text-lg sm:text-xl font-bold text-white">${t.name}</h4>
                      <p class="text-xs text-slate-400 mt-0.5">${t.desc}</p>
                    </div>
                  </div>
                  <span class="badge-chip bg-${t.theme}-500/20 text-${t.theme}-400 border border-${t.theme}-500/30 text-xs">${t.badge}</span>
                </div>

                <div class="space-y-2.5 sm:space-y-3">
                  ${i.map((r,n)=>`
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
    `}function L(){const e=a.roadmapTrack==="tech",r=e?[{level:"Level 1",title:"\u{1F331} \u57FA\u7840\u901A\u8BC6\u4E0E\u5927\u6A21\u578B\u5E95\u5C42\u539F\u7406",desc:"\u6DF1\u5165\u638C\u63E1\u5927\u6A21\u578B\u6838\u5FC3\u67B6\u6784\u3001\u6CE8\u610F\u529B\u673A\u5236 (Self-Attention)\u3001RoPE \u4E0E\u4F4D\u7F6E\u7F16\u7801\u6570\u5B66\u539F\u7406\u4E0E\u524D\u6CBF\u8109\u7EDC",categories:["ai-science","ai-news","bigmodel","ai-safety"],skills:["Transformer \u67B6\u6784","\u6CE8\u610F\u529B\u673A\u5236\u8BA1\u7B97","Token & \u5D4C\u5165\u5411\u91CF","\u6A21\u578B\u5B89\u5168\u4E0E\u4F26\u7406"]},{level:"Level 2",title:"\u26A1 Agent \u6838\u5FC3\u67B6\u6784\u3001\u624B\u5199\u6846\u67B6\u4E0E\u601D\u8003\u5FAA\u73AF",desc:"\u4ECE\u96F6\u624B\u5199\u8F7B\u91CF\u7EA7 Agent \u601D\u8003\u5FAA\u73AF\uFF0C\u6DF1\u5165 OpenClaw \u667A\u80FD\u4F53\u7CFB\u7EDF\uFF0C\u638C\u63E1\u6709\u9650\u72B6\u6001\u673A\u3001\u610F\u56FE\u611F\u77E5\u4E0E\u8BB0\u5FC6\u7CFB\u7EDF",categories:["myagent","agent-core","openclaw"],skills:["ReAct \u601D\u8003\u5FAA\u73AF","\u77ED/\u957F\u671F\u8BB0\u5FC6\u7CFB\u7EDF","\u5DE5\u5177\u8C03\u7528\u534F\u8BAE","OpenClaw \u667A\u80FD\u4F53"]},{level:"Level 3",title:"\u{1F6E0}\uFE0F \u73B0\u4EE3 AI \u5DE5\u5177\u94FE\u4E0E AI Coding \u5168\u6808\u8FDB\u9636",desc:"\u73A9\u8F6C Claude Code \u5168\u5BB6\u6876\u3001AI Coding 33\u7BC7\u5168\u4F53\u7CFB\u3001MCP Server \u534F\u8BAE\u5F00\u53D1\u3001TDD \u4E0E\u540E\u7AEF\u670D\u52A1\u96C6\u6210",categories:["aitools","ai-coding"],skills:["Claude Code \u5168\u5BB6\u6876","MCP \u534F\u8BAE\u5F00\u53D1","AI \u8F85\u52A9\u67B6\u6784\u8BBE\u8BA1","\u6D4B\u8BD5\u9A71\u52A8\u5F00\u53D1 TDD"]},{level:"Level 4",title:"\u{1F4BC} \u4F01\u4E1A\u7EA7\u5DE5\u7A0B\u843D\u5730\u4E0E\u79C1\u6709\u77E5\u8BC6\u5E93 (RAG)",desc:"\u843D\u5730\u4F01\u4E1A\u667A\u80FD\u5BA2\u670D\u5168\u95ED\u73AF\u3001\u6784\u5EFA\u79C1\u6709\u672C\u5730\u5927\u6A21\u578B\u77E5\u8BC6\u5E93 (Ollama + \u5411\u91CF\u5E93)\u3001\u6253\u9020\u5782\u76F4\u9886\u57DF Agent \u7CFB\u7EDF",categories:["customer-service","customer-service-harness","local-rag","english-agent","quant-agent"],skills:["\u4F01\u4E1A\u5FAE\u4FE1\u667A\u80FD\u5BA2\u670D","\u672C\u5730\u79C1\u6709 RAG","\u5411\u91CF\u68C0\u7D22\u4E0E\u91CD\u6392","\u5782\u76F4 Agent \u843D\u5730"]}]:[{level:"Level 1",title:"\u{1F3AF} \u4E1A\u52A1\u8BA4\u77E5\u4E0E\u9AD8\u9636\u63D0\u793A\u5DE5\u7A0B (Prompt \u8D4B\u80FD\u4E1A\u52A1)",desc:"\u628A\u4E1A\u52A1\u89C4\u5219\u8F6C\u5316\u4E3A\u5927\u6A21\u578B\u80FD\u7CBE\u51C6\u6267\u884C\u7684\u9AD8\u9636 Prompt\uFF0C\u638C\u63E1\u7ED3\u6784\u5316\u8F93\u51FA\u3001\u4E1A\u52A1\u8FB9\u754C\u7EA6\u675F\u4E0E\u5185\u5BB9\u6DA6\u8272",skills:["CRISPE \u7ED3\u6784\u5316\u6846\u67B6","\u4E1A\u52A1\u89C4\u5219\u4E0E\u8FB9\u754C\u7EA6\u675F","\u975E\u7ED3\u6784\u5316\u6570\u636E\u521D\u7B5B","\u81EA\u5A92\u4F53\u56FE\u6587\u751F\u4EA7\u6D41","\u6587\u672C\u53BB AI \u75D5\u6DA6\u8272"],curatedArticles:[{id:"aitools_pm_skills_write_prd_\u6DF1\u5EA6\u5B9E\u6218_\u516C\u4F17\u53F7\u7248_html",tag:"\u{1F3AF} \u4EA7\u54C1PRD\u5B9E\u6218"},{id:"aitools_baoyu_skills_\u4E2D\u6587\u81EA\u5A92\u4F53\u6280\u80FD\u96C6_\u516C\u4F17\u53F7\u7248_html",tag:"\u26A1 \u56FE\u6587\u751F\u4EA7\u6D41"},{id:"aitools_humanizer_skill\u4ECB\u7ECD_\u516C\u4F17\u53F7\u7248_html",tag:"\u{1F4DD} \u6587\u672C\u53BBAI\u75D5"}],inProgressText:"\u{1F331} \u300A\u4E1A\u52A1\u573A\u666F\u9AD8\u9636 Prompt \u7ED3\u6784\u5316\u8BBE\u8BA1\u5168\u6307\u5357\u300B\u5BA1\u6838\u6392\u671F\u4E2D..."},{level:"Level 2",title:"\u{1F4A1} AI \u4EA7\u54C1\u8BBE\u8BA1\u4E0E\u4E1A\u52A1\u6D41\u91CD\u6784 (AI PM \u5B9E\u6218)",desc:"\u638C\u63E1 AI \u539F\u751F\u4EA7\u54C1\u9700\u6C42\u5B9A\u4E49\uFF08AI PRD \u89C4\u8303\uFF09\u3001\u4EBA\u673A\u534F\u540C\u4EA4\u4E92\u6A21\u5F0F\u8BBE\u8BA1\u3001\u5168\u7F51\u7814\u62A5\u8C03\u7814\u4E0E\u4E1A\u52A1\u6D41\u7A0B\u81EA\u52A8\u5316",skills:["AI PRD \u7ED3\u6784\u5316\u64B0\u5199","Copilot vs Agent \u9009\u578B","\u5168\u7F51\u7ADE\u54C1\u6DF1\u5EA6\u8C03\u7814","\u4E1A\u52A1\u6D41\u7A0B\u81EA\u52A8\u5316"],curatedArticles:[{id:"aitools_pm_skills_\u4EA7\u54C1\u7ECF\u7406\u6280\u80FD\u5E02\u573A_\u516C\u4F17\u53F7\u7248_html",tag:"\u{1F3AF} PM \u6280\u80FD\u5E02\u573A"},{id:"aitools_agent_reach_\u8BA9AI\u4E0A\u7F51\u641C\u8D44\u6599_\u516C\u4F17\u53F7\u7248_html",tag:"\u{1F50D} \u5168\u7F51\u7814\u62A5\u641C\u96C6"}],inProgressText:"\u{1F331} \u300AAI \u539F\u751F PRD \u9700\u6C42\u89C4\u8303\u4E0E\u4EBA\u673A\u534F\u540C\u4EA4\u4E92\u8BBE\u8BA1\u300B\u5BA1\u6838\u6392\u671F\u4E2D..."},{level:"Level 3",title:"\u{1F916} \u96F6\u4EE3\u7801\u642D\u5EFA\u4E1A\u52A1\u667A\u80FD\u4F53 (Dify / \u6263\u5B50\u5B9E\u64CD)",desc:"\u65E0\u9700\u7F16\u5199\u590D\u6742\u4EE3\u7801\uFF0C\u901A\u8FC7\u53EF\u89C6\u5316\u754C\u9762\u642D\u5EFA\u4F01\u4E1A\u4E13\u5C5E\u77E5\u8BC6\u95EE\u7B54\u52A9\u624B\u3001\u4E1A\u52A1\u81EA\u52A8\u5316\u5DE5\u4F5C\u6D41\u4E0E\u667A\u80FD\u5BA2\u670D\u673A\u5668\u4EBA",skills:["\u4F01\u4E1A\u79C1\u6709\u77E5\u8BC6\u95EE\u7B54\u5E93","\u53EF\u89C6\u5316\u95EE\u7B54\u4EA4\u4E92\u754C\u9762","\u4E1A\u52A1\u75DB\u70B9\u4E0E\u610F\u56FE\u5206\u6790","\u5FAE\u4FE1/\u4F01\u5FAE\u5BA2\u670D\u63A5\u5165"],curatedArticles:[{id:"local_llm_knowledge_base_\u672C\u5730\u5927\u6A21\u578B\u77E5\u8BC6\u5E93\u7CFB\u5217_01_\u516C\u4F17\u53F7\u7248_html",tag:"\u{1F4DA} \u79C1\u6709\u77E5\u8BC6\u5E93"},{id:"local_llm_knowledge_base_\u672C\u5730\u5927\u6A21\u578B\u77E5\u8BC6\u5E93\u7CFB\u5217_04_\u516C\u4F17\u53F7\u7248_html",tag:"\u{1F5A5}\uFE0F \u53EF\u89C6\u5316\u95EE\u7B54"},{id:"customer_service_agent_\u5BA2\u670DAgent\u5B9E\u6218\u7CFB\u5217_01_html",tag:"\u{1F4AC} \u4E1A\u52A1\u75DB\u70B9\u5206\u6790"}],inProgressText:"\u{1F331} \u300A\u96F6\u4EE3\u7801\u5E73\u53F0\u6DF1\u5EA6\u6A2A\u8BC4\u4E0E\u4F01\u4E1A\u79C1\u6709\u77E5\u8BC6\u5E93 Bot \u5B9E\u64CD\u300B\u5BA1\u6838\u6392\u671F\u4E2D..."},{level:"Level 4",title:"\u{1F4C8} \u4E1A\u52A1 ROI \u8BC4\u4F30\u4E0E\u5546\u4E1A\u5316\u95ED\u73AF (\u51B3\u7B56\u4E0E\u843D\u5730)",desc:"\u638C\u63E1 AI \u9879\u76EE\u6295\u5165\u4EA7\u51FA\u6BD4\uFF08ROI\uFF09\u6D4B\u7B97\u3001\u4E1A\u52A1\u56E2\u961F\u5F15\u5165 SOP\u3001\u4E00\u4EBA\u516C\u53F8\uFF08Solopreneur\uFF09\u95ED\u73AF\u4E0E\u4F01\u4E1A\u843D\u5730\u6307\u5357",skills:["\u4F01\u4E1A AI \u9009\u578B ROI \u8D26\u672C","\u4E1A\u52A1\u56E2\u961F\u5F15\u5165 SOP","\u4E00\u4EBA\u516C\u53F8\u5546\u4E1A\u95ED\u73AF","\u590D\u6742\u4E1A\u52A1\u591A\u4F53\u534F\u540C"],curatedArticles:[{id:"customer_service_agent_\u5BA2\u670DAgent\u5B9E\u6218\u7CFB\u5217_08_\u516C\u4F17\u53F7\u7248_html",tag:"\u{1F91D} \u590D\u6742\u4E1A\u52A1\u4F1A\u8BCA"},{id:"ai_coding_AI_Coding\u7CFB\u5217_25_\u56E2\u961F\u534F\u4F5C_html",tag:"\u{1F465} \u56E2\u961F\u534F\u540C\u843D\u5730"}],inProgressText:"\u{1F331} \u300A\u4F01\u4E1A\u5F15\u5165 AI \u7684 ROI \u6210\u672C\u8D26\u672C\u4E0E\u4E1A\u52A1\u56E2\u961F\u843D\u5730 SOP\u300B\u5BA1\u6838\u6392\u671F\u4E2D..."}];s.mainContent.innerHTML=`
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
          ${r.map(n=>{const o=e?a.data.articles.filter(d=>n.categories.includes(d.categoryId)).length:(n.curatedArticles||[]).length;return`
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
                        ${e?`\u5171 ${o} \u7BC7\u4E13\u680F\u89E3\u6790`:`\u5DF2\u6536\u5F55 ${o} \u7BC7\u7CBE\u9009\u5B9E\u64CD`}
                      </span>
                    </div>
                  </div>

                  <!-- Key Competencies Skills Badges -->
                  <div class="flex flex-wrap items-center gap-1.5 my-3">
                    ${(n.skills||[]).map(d=>`
                      <span class="text-[10px] sm:text-[11px] px-2 py-0.5 rounded-md bg-white/5 text-slate-300 border border-white/10">
                        \u2713 ${d}
                      </span>
                    `).join("")}
                  </div>

                  ${e?`
                    <!-- Tech Track: Category List -->
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 sm:gap-3 mt-3 sm:mt-4">
                      ${n.categories.map(d=>{const l=a.data.categories.find(f=>f.id===d);if(!l)return"";const h=a.data.articles.filter(f=>f.categoryId===d).length;return`
                          <div onclick="window.AI_HUB.switchCategory('${l.id}')" class="p-3 sm:p-3.5 rounded-xl bg-white/5 hover:bg-white/10 border border-white/5 hover:border-indigo-500/30 transition flex items-center justify-between cursor-pointer group">
                            <span class="flex items-center gap-2 text-xs sm:text-sm text-slate-200 group-hover:text-indigo-400 font-medium">
                              <span class="text-base sm:text-lg">${l.icon}</span>
                              <span>${l.name}</span>
                            </span>
                            <span class="text-[11px] sm:text-xs bg-white/10 px-2 sm:px-2.5 py-0.5 sm:py-1 rounded-full text-slate-300 group-hover:bg-indigo-600 group-hover:text-white transition">${h} \u7BC7</span>
                          </div>
                        `}).join("")}
                    </div>
                  `:`
                    <!-- Business Track: Curated Specific Article Cards -->
                    <div class="space-y-3 mt-3 sm:mt-4">
                      <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 sm:gap-3">
                        ${(n.curatedArticles||[]).map(d=>{const l=a.data.articles.find(h=>h.id===d.id);return l?`
                            <div onclick="window.AI_HUB.openReaderById('${l.id}')" class="p-3 sm:p-3.5 rounded-xl bg-white/5 hover:bg-white/10 border border-white/5 hover:border-indigo-500/30 transition flex flex-col justify-between cursor-pointer group shadow-sm">
                              <div>
                                <div class="flex items-center justify-between gap-2 mb-1.5">
                                  <span class="text-[10px] sm:text-[11px] font-bold px-2 py-0.5 rounded-md bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                                    ${d.tag}
                                  </span>
                                  <span class="text-[10px] sm:text-[11px] text-slate-400">\u23F1\uFE0F ${l.readTime}</span>
                                </div>
                                <h4 class="text-xs sm:text-sm font-semibold text-slate-100 group-hover:text-indigo-300 line-clamp-2 transition leading-snug">
                                  ${l.title}
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
    `}function _(){return`
      <div class="text-center py-20 animate-fade-in">
        <div class="text-5xl mb-4">\u{1F50D}</div>
        <h3 class="text-xl font-bold text-white">\u672A\u627E\u5230\u5339\u914D\u7684\u5B66\u4E60\u8D44\u6599</h3>
        <p class="text-slate-400 text-sm mt-2">\u8BF7\u5C1D\u8BD5\u66F4\u6362\u641C\u7D22\u5173\u952E\u5B57\uFF0C\u6216\u8C03\u6574\u5206\u7C7B\u7B5B\u9009\u6761\u4EF6\u3002</p>
        <button onclick="window.AI_HUB.resetFilters()" class="mt-6 px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium transition">
          \u91CD\u7F6E\u6240\u6709\u7B5B\u9009\u6761\u4EF6
        </button>
      </div>
    `}function O(e){return e?e.replace(/^### (.*$)/gim,'<h3 id="$1">$1</h3>').replace(/^## (.*$)/gim,'<h2 id="$1">$1</h2>').replace(/^# (.*$)/gim,'<h1 id="$1">$1</h1>').replace(/^\> (.*$)/gim,"<blockquote>$1</blockquote>").replace(/\*\*(.*)\*\*/gim,"<strong>$1</strong>").replace(/\*(.*)\*/gim,"<em>$1</em>").replace(/```([a-z]*)\n([\s\S]*?)```/gim,"<pre><code>$2</code></pre>").replace(/`([^`]+)`/gim,"<code>$1</code>").replace(/\n\n/gim,"</p><p>").replace(/\[([^\]]+)\]\(([^)]+)\)/gim,'<a href="$2" target="_blank">$1</a>'):""}function g(e){a.currentArticle=e,a.history=[{id:e.id,time:new Date().toLocaleTimeString()},...a.history.filter(i=>i.id!==e.id)],localStorage.setItem("ai_hub_history",JSON.stringify(a.history)),window.history.replaceState(null,"",`?article=${e.id}`),s.readerTitle&&(s.readerTitle.textContent=e.title);const t=a.data.categories.find(i=>i.id===e.categoryId);s.readerCategory&&(s.readerCategory.textContent=t?`${t.icon} ${t.name}`:"\u7CFB\u5217\u6587\u6863"),F(),e.format==="md"?(s.readerIframeContainer&&s.readerIframeContainer.classList.add("hidden"),s.readerMarkdownContainer&&s.readerMarkdownContainer.classList.remove("hidden"),s.markdownContent&&(s.markdownContent.innerHTML='<div class="text-center py-16 text-slate-400">\u6B63\u5728\u89E3\u6790\u5E76\u6E32\u67D3 Markdown \u6587\u6863...</div>'),fetch(e.path).then(i=>i.text()).then(i=>{let r="";window.marked&&typeof window.marked.parse=="function"?r=window.marked.parse(i):r=O(i),s.markdownContent&&(s.markdownContent.innerHTML=r);const n=[];i.split(`
`).forEach(d=>{(d.startsWith("## ")||d.startsWith("### "))&&n.push(d.replace(/^#+\s*/,"").trim())}),e.toc=n.slice(0,15),M(e)}).catch(i=>{s.markdownContent&&(s.markdownContent.innerHTML=`<div class="text-rose-400 p-6">\u52A0\u8F7D Markdown \u6587\u4EF6\u5931\u8D25\uFF1A${i.message}</div>`)})):(s.readerMarkdownContainer&&s.readerMarkdownContainer.classList.add("hidden"),s.readerIframeContainer&&s.readerIframeContainer.classList.remove("hidden"),s.readerFrame&&(s.readerFrame.src=e.path,s.readerFrame.onload=function(){try{const i=s.readerFrame.contentDocument||s.readerFrame.contentWindow.document;if(!i)return;const r=i.createElement("style");r.textContent=`
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
            `,i.head.appendChild(r),i.querySelectorAll("a[href]").forEach(o=>{o.addEventListener("click",function(d){const l=o.getAttribute("href");if(!l)return;if(l.startsWith("#")){d.preventDefault();const m=i.querySelector(l);m&&m.scrollIntoView({behavior:"smooth"});return}if(l.startsWith("http://")||l.startsWith("https://")||l.startsWith("//")){o.target="_blank";return}d.preventDefault();const h=l.split("?")[0].split("#")[0],f=h.split("/").pop(),S=a.data.articles.find(m=>m.path===h||m.path.endsWith(h)||m.path.endsWith(f)||m.id===h.replace(/\.html$/,""));if(S)g(S);else{let m=e.path.substring(0,e.path.lastIndexOf("/")+1),z=new URL(l,window.location.origin+"/"+m).pathname.replace(/^\//,"");s.readerFrame.src=z}})})}catch(i){console.warn("Iframe link handling notice:",i)}}),M(e)),s.readerModal&&(s.readerModal.classList.remove("hidden"),document.body.style.overflow="hidden")}function T(){a.currentArticle=null,s.readerModal&&(s.readerModal.classList.add("hidden"),document.body.style.overflow=""),s.readerFrame&&(s.readerFrame.src="about:blank"),window.history.replaceState(null,"",window.location.pathname),c()}function F(){if(!a.currentArticle)return;const e=a.currentArticle;s.btnOpenExternal&&(s.btnOpenExternal.href=e.path);const t=document.getElementById("btn-open-wechat-version");if(t)if(e.path&&(e.path.includes("business-review/")||e.path.includes("-\u516C\u4F17\u53F7\u7248.html"))){const n=e.path.includes("-\u516C\u4F17\u53F7\u7248.html")?e.path:e.path.replace(/\.html$/,"-\u516C\u4F17\u53F7\u7248.html");t.href=n,t.classList.remove("hidden")}else t.classList.add("hidden");const i=a.data.articles.filter(n=>n.categoryId===e.categoryId),r=i.findIndex(n=>n.id===e.id);s.btnPrevArticle&&(s.btnPrevArticle.disabled=r<=0,s.btnPrevArticle.classList.toggle("opacity-30",r<=0),s.btnPrevArticle.classList.toggle("cursor-not-allowed",r<=0)),s.btnNextArticle&&(s.btnNextArticle.disabled=r===-1||r>=i.length-1,s.btnNextArticle.classList.toggle("opacity-30",r===-1||r>=i.length-1),s.btnNextArticle.classList.toggle("cursor-not-allowed",r===-1||r>=i.length-1))}function M(e){if(!s.readerTocList)return;const t=e.toc||[];if(t.length===0){s.readerTocList.innerHTML='<div class="text-xs text-slate-400 py-4 text-center">\u672C\u7BC7\u65E0\u591A\u7EA7\u6807\u9898\u7D22\u5F15</div>';return}s.readerTocList.innerHTML=t.map((i,r)=>`
      <button onclick="window.AI_HUB.scrollToHeading('${i}')" class="w-full text-left p-2.5 rounded-xl hover:bg-white/10 text-xs text-slate-300 hover:text-white transition truncate" title="${i}">
        ${r+1}. ${i}
      </button>
    `).join("")}function W(e){if(a.currentArticle&&a.currentArticle.format==="md"&&s.markdownContent){const t=s.markdownContent.querySelectorAll("h1, h2, h3, h4");for(const i of t)if(i.textContent.trim().includes(e)||e.includes(i.textContent.trim())){i.scrollIntoView({behavior:"smooth",block:"start"});break}}}function v(e){if(!a.currentArticle)return;const t=a.data.articles.filter(r=>r.categoryId===a.currentArticle.categoryId),i=t.findIndex(r=>r.id===a.currentArticle.id);e==="prev"&&i>0?g(t[i-1]):e==="next"&&i<t.length-1&&g(t[i+1])}function B(){s.wechatModal&&(s.wechatModal.classList.remove("hidden"),document.body.style.overflow="hidden")}function E(){s.wechatModal&&(s.wechatModal.classList.add("hidden"),document.body.style.overflow="")}function Q(){const e="\u5927\u524D\u7AEF\u5DE5\u7A0B\u5E08";navigator.clipboard&&window.isSecureContext?navigator.clipboard.writeText(e).then(()=>{b("\u5DF2\u590D\u5236\u516C\u4F17\u53F7\u540D\u79F0\uFF1A\u5927\u524D\u7AEF\u5DE5\u7A0B\u5E08","\u{1F4CB}")}).catch(()=>{w(e)}):w(e)}function K(e){navigator.clipboard&&window.isSecureContext?navigator.clipboard.writeText(e).then(()=>{b(`\u5DF2\u590D\u5236\u53E3\u4EE4\u3010${e}\u3011\uFF0C\u8BF7\u5728\u5FAE\u4FE1\u516C\u4F17\u53F7\u540E\u53F0\u76F4\u63A5\u53D1\u9001\uFF01`,"\u{1F4CB}")}).catch(()=>{w(e)}):w(e),B()}function w(e){const t=document.createElement("input");t.value=e,document.body.appendChild(t),t.select();try{document.execCommand("copy"),b("\u5DF2\u590D\u5236\u516C\u4F17\u53F7\u540D\u79F0\uFF1A\u5927\u524D\u7AEF\u5DE5\u7A0B\u5E08","\u{1F4CB}")}catch{b("\u516C\u4F17\u53F7\u540D\u79F0\uFF1A\u5927\u524D\u7AEF\u5DE5\u7A0B\u5E08","\u{1F4AC}")}document.body.removeChild(t)}function V(){s.themeToggle&&s.themeToggle.addEventListener("click",k),s.searchInput&&s.searchInput.addEventListener("input",t=>{a.searchQuery=t.target.value.trim(),s.searchClear&&s.searchClear.classList.toggle("hidden",!a.searchQuery),a.searchQuery&&a.viewMode!=="grid"&&a.viewMode!=="list"&&(a.viewMode="grid",p()),c()}),s.searchClear&&s.searchClear.addEventListener("click",()=>{a.searchQuery="",s.searchInput.value="",s.searchClear.classList.add("hidden"),s.searchInput.focus(),c()}),document.querySelectorAll(".hot-tag-btn").forEach(t=>{t.addEventListener("click",()=>{const i=t.dataset.keyword;i&&s.searchInput&&(s.searchInput.value=i,a.searchQuery=i,s.searchClear&&s.searchClear.classList.remove("hidden"),a.viewMode!=="grid"&&a.viewMode!=="list"&&(a.viewMode="grid",p()),c(),s.mainContent?.scrollIntoView({behavior:"smooth",block:"start"}))})});function e(){if(!s.mainContent)return;if(a.viewMode==="showcases"){window.scrollTo({top:0,behavior:"smooth"});return}const t=document.getElementById("category-nav-bar");if(t&&!t.classList.contains("hidden")){const i=t.getBoundingClientRect(),r=window.pageYOffset+i.top-65;window.scrollTo({top:Math.max(0,r),behavior:"smooth"})}else{const i=s.mainContent.getBoundingClientRect(),r=window.pageYOffset+i.top-70;window.scrollTo({top:Math.max(0,r),behavior:"smooth"})}}s.categoryTabs&&s.categoryTabs.addEventListener("click",t=>{const i=t.target.closest("[data-category]");i&&(a.activeCategory=i.dataset.category,a.activeCategory!=="all"&&a.viewMode==="roadmap"&&(a.viewMode="grid",p()),u(),c(),e())}),s.categorySelect&&s.categorySelect.addEventListener("change",t=>{a.activeCategory=t.target.value,a.activeCategory!=="all"&&a.viewMode==="roadmap"&&(a.viewMode="grid",p()),u(),c(),e()}),s.viewButtons.forEach(t=>{t.addEventListener("click",()=>{a.viewMode=t.dataset.view,p(),c(),e()})}),s.btnCloseReader&&s.btnCloseReader.addEventListener("click",T),s.btnPrevArticle&&s.btnPrevArticle.addEventListener("click",()=>v("prev")),s.btnNextArticle&&s.btnNextArticle.addEventListener("click",()=>v("next")),s.btnToggleToc&&s.btnToggleToc.addEventListener("click",()=>{s.readerTocDrawer&&s.readerTocDrawer.classList.toggle("hidden")}),document.addEventListener("keydown",t=>{(t.metaKey||t.ctrlKey)&&(t.key==="k"||t.key==="K")&&(t.preventDefault(),s.searchInput?.focus(),s.searchInput?.select()),t.key==="Escape"&&(a.currentArticle&&T(),s.wechatModal&&!s.wechatModal.classList.contains("hidden")&&E()),a.currentArticle&&!t.target.matches("input, textarea")&&(t.key==="ArrowLeft"&&v("prev"),t.key==="ArrowRight"&&v("next")),(t.key==="t"||t.key==="T")&&!t.target.matches("input, textarea")&&!a.currentArticle&&k()})}function N(){let t=`
      <div class="mb-10 animate-fade-in pt-4 sm:pt-6">
        
        <!-- Clean Section Header -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-8 pb-4 border-b border-white/10">
          <div>
            <div class="flex items-center gap-2.5">
              <span class="text-2xl sm:text-3xl">\u{1F916}</span>
              <h2 class="text-2xl sm:text-3xl font-black text-white tracking-tight">AI Agent & Claude Code \u4E13\u6709\u6280\u80FD\u5E93</h2>
            </div>
            <p class="text-xs sm:text-sm text-slate-400 mt-1.5">
              \u5F00\u7BB1\u5373\u7528\u7684\u81EA\u52A8\u5316\u667A\u80FD\u4F53 Skills\uFF0C\u652F\u6301\u5728 Claude Code \u4E2D\u901A\u8FC7\u5355\u884C\u547D\u4EE4\u6309\u9700\u5B89\u88C5\u4E0E\u5BF9\u8BDD\u8C03\u7528\u3002
            </p>
          </div>
        </div>

        <!-- Showcase Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 sm:gap-8">
          ${(a.data.showcases||[]).map(q).join("")}
        </div>

      </div>
    `;s.mainContent.innerHTML=t}function q(e){const t=e.theme||"emerald",i=(e.features||[]).map(o=>`
      <li class="flex items-start gap-2 text-xs text-slate-300 leading-relaxed">
        <span class="text-emerald-400 shrink-0 mt-0.5">\u2713</span>
        <span>${o}</span>
      </li>
    `).join(""),r=(e.tags||[]).map(o=>`
      <span class="text-[11px] px-2 py-0.5 rounded-md bg-white/5 text-slate-300 border border-white/10 font-mono">${o}</span>
    `).join(""),n=e.docsUrl?`
      <a href="${e.docsUrl}" target="_blank" class="flex-1 py-2 rounded-xl bg-white/5 hover:bg-white/10 text-slate-200 hover:text-white border border-white/10 text-xs font-bold text-center transition flex items-center justify-center gap-1">
        <span>\u{1F4D6}</span>
        <span>\u5B9E\u64CD\u590D\u76D8</span>
      </a>
    `:"";return`
      <div class="rounded-3xl glass border border-white/10 p-6 sm:p-7 flex flex-col justify-between hover:border-emerald-500/40 hover:shadow-xl hover:shadow-emerald-500/10 transition-all group relative overflow-hidden bg-gradient-to-b from-white/[0.04] to-transparent">
        <div class="absolute top-0 right-0 w-32 h-32 bg-${t}-500/10 rounded-full blur-2xl pointer-events-none group-hover:scale-150 transition-transform"></div>
        
        <div>
          <!-- Card Header -->
          <div class="flex items-start justify-between gap-3 mb-4">
            <div class="w-12 h-12 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-2xl shadow-inner shrink-0 group-hover:scale-110 transition-transform">
              ${e.icon||"\u{1F6E0}\uFE0F"}
            </div>
            <div class="flex items-center gap-2">
              <span class="badge-chip bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-[10px] font-bold">
                ${e.badge||"\u81EA\u7814\u51FA\u54C1"}
              </span>
            </div>
          </div>

          <!-- Title & Subtitle -->
          <h3 class="text-xl font-bold text-white group-hover:text-emerald-300 transition-colors tracking-tight mb-1">
            ${e.title}
          </h3>
          <div class="text-xs font-mono text-emerald-400 font-medium mb-3">
            \u{1F4E6} ${e.name}
          </div>

          <!-- Description -->
          <p class="text-xs sm:text-sm text-slate-300 leading-relaxed mb-4">
            ${e.description}
          </p>

          <!-- Feature Bullets -->
          <div class="p-3.5 rounded-2xl bg-white/[0.02] border border-white/5 mb-5">
            <div class="text-[11px] font-bold text-slate-400 mb-2 uppercase tracking-wider">\u{1F4A1} \u6838\u5FC3\u4EAE\u70B9</div>
            <ul class="space-y-1.5">
              ${i}
            </ul>
          </div>

          <!-- Tags -->
          <div class="flex flex-wrap gap-1.5 mb-6">
            ${r}
          </div>
        </div>

        <!-- Footer Action Box -->
        <div>
          ${e.type==="tool"?`
            <!-- Web Tool Direct Action Button -->
            <div class="mb-4">
              <a href="${e.toolUrl}" target="_blank" class="w-full py-3 px-4 rounded-2xl bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:from-indigo-500 hover:to-pink-500 text-white text-xs sm:text-sm font-bold text-center transition flex items-center justify-center gap-2 shadow-lg shadow-indigo-500/25 cursor-pointer">
                <span>\u26A1</span>
                <span>\u7ACB\u5373\u5728\u7EBF\u6253\u5F00\u4F7F\u7528 (\u514D\u5B89\u88C5) \u2794</span>
              </a>
            </div>
            ${e.docsUrl?`
              <div class="flex items-center gap-2">
                <a href="${e.docsUrl}" target="_blank" class="w-full py-2 rounded-xl bg-white/5 hover:bg-white/10 text-slate-200 hover:text-white border border-white/10 text-xs font-bold text-center transition flex items-center justify-center gap-1.5">
                  <span>\u{1F4D6}</span>
                  <span>\u9605\u8BFB\u914D\u5957\u5B9E\u6218\u4E13\u680F</span>
                </a>
              </div>
            `:""}
          `:`
            <!-- Install Command Box for Skills -->
            <div class="p-2.5 rounded-xl bg-slate-950/80 border border-white/10 mb-4 flex items-center justify-between gap-2 shadow-inner">
              <code class="text-[10px] sm:text-[11px] text-emerald-300 font-mono truncate select-all">
                ${e.installCmd}
              </code>
              <button onclick="window.AI_HUB.copyInstallCmd('${e.installCmd}')" class="px-2.5 py-1 rounded-lg bg-emerald-500/20 hover:bg-emerald-500 text-emerald-300 hover:text-slate-950 text-[10px] font-bold transition shrink-0 cursor-pointer" title="\u70B9\u51FB\u590D\u5236\u5B89\u88C5\u547D\u4EE4">
                \u590D\u5236
              </button>
            </div>

            <!-- Action Buttons -->
            <div class="flex items-center gap-2">
              <a href="${e.githubUrl||"https://github.com/fangxiao/myskills"}" target="_blank" class="flex-1 py-2 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white text-xs font-bold text-center transition flex items-center justify-center gap-1.5 shadow-md shadow-emerald-900/30">
                <span>\u2B50</span>
                <span>GitHub \u5F00\u6E90</span>
              </a>
              ${n}
            </div>
          `}
        </div>

      </div>
    `}window.AI_HUB={openReaderById:function(e){const t=a.data.articles.find(i=>i.id===e);t&&g(t)},openReaderByPath:function(e){if(!e)return;const t=e.split("#")[0],i=a.data.articles.find(r=>r.path===t||r.path.endsWith(t)||t.endsWith(r.path));i&&g(i)},switchCategory:function(e){a.activeCategory=e,a.viewMode="grid",u(),p(),c(),scrollToMainContent()},openWeChatModal:B,closeWeChatModal:E,copyWeChatName:Q,scrollToHeading:W,resetFilters:function(){a.activeCategory="all",a.searchQuery="",s.searchInput&&(s.searchInput.value=""),u(),c()},switchView:function(e){a.viewMode=e,p(),c(),scrollToMainContent()},switchRoadmapTrack:function(e){a.roadmapTrack=e,L()}},document.readyState==="loading"?document.addEventListener("DOMContentLoaded",y):y()})();