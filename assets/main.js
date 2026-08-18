/* ==========================================================================
   개발 학습·실전 노트 — 공용 스크립트
   목차 이동 / 다크모드 / 진행도 바 / 모바일 메뉴 / 코드 복사 / 검색
   ========================================================================== */
(function () {
  "use strict";

  /* ---------- 다크모드 ---------- */
  var THEME_KEY = "dev-notes-theme";
  function applyTheme(theme) {
    if (theme === "dark" || theme === "light") {
      document.documentElement.setAttribute("data-theme", theme);
    } else {
      document.documentElement.removeAttribute("data-theme");
    }
  }
  function currentEffectiveTheme() {
    var saved = localStorage.getItem(THEME_KEY);
    if (saved === "dark" || saved === "light") return saved;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  (function initTheme() {
    var saved = localStorage.getItem(THEME_KEY);
    if (saved) applyTheme(saved);
  })();

  function toggleTheme() {
    var next = currentEffectiveTheme() === "dark" ? "light" : "dark";
    localStorage.setItem(THEME_KEY, next);
    applyTheme(next);
  }

  /* ---------- 데스크톱 사이드바 접기 ---------- */
  var SIDEBAR_KEY = "dev-notes-sidebar-collapsed";
  function applySidebarCollapsed(collapsed) {
    document.body.classList.toggle("sidebar-collapsed", collapsed);
  }
  (function initSidebar() {
    if (localStorage.getItem(SIDEBAR_KEY) === "1") applySidebarCollapsed(true);
  })();
  function setSidebarCollapsed(collapsed) {
    applySidebarCollapsed(collapsed);
    localStorage.setItem(SIDEBAR_KEY, collapsed ? "1" : "0");
  }

  document.addEventListener("DOMContentLoaded", function () {
    var themeBtns = document.querySelectorAll(".theme-btn");
    themeBtns.forEach(function (btn) {
      btn.addEventListener("click", toggleTheme);
    });

    /* ---------- 읽기 진행도 바 ---------- */
    var progressEl = document.getElementById("reading-progress");
    if (progressEl) {
      var updateProgress = function () {
        var scrollTop = window.scrollY || document.documentElement.scrollTop;
        var docHeight = document.documentElement.scrollHeight - window.innerHeight;
        var pct = docHeight > 0 ? Math.min(100, Math.max(0, (scrollTop / docHeight) * 100)) : 0;
        progressEl.style.width = pct + "%";
      };
      document.addEventListener("scroll", updateProgress, { passive: true });
      window.addEventListener("resize", updateProgress);
      updateProgress();
    }

    /* ---------- 모바일 사이드바 ---------- */
    var sidebar = document.querySelector(".sidebar");
    var overlay = document.querySelector(".sidebar-overlay");
    var menuBtn = document.querySelector(".menu-btn");
    function openSidebar() {
      if (sidebar) sidebar.classList.add("open");
      if (overlay) overlay.classList.add("open");
    }
    function closeSidebar() {
      if (sidebar) sidebar.classList.remove("open");
      if (overlay) overlay.classList.remove("open");
    }
    if (menuBtn) menuBtn.addEventListener("click", function () {
      if (sidebar && sidebar.classList.contains("open")) closeSidebar(); else openSidebar();
    });
    if (overlay) overlay.addEventListener("click", closeSidebar);
    document.querySelectorAll(".toc a").forEach(function (a) {
      a.addEventListener("click", closeSidebar);
    });

    var collapseBtn = document.querySelector(".sidebar-collapse-btn");
    var reopenBtn = document.querySelector(".sidebar-reopen-btn");
    if (collapseBtn) collapseBtn.addEventListener("click", function () { setSidebarCollapsed(true); });
    if (reopenBtn) reopenBtn.addEventListener("click", function () { setSidebarCollapsed(false); });

    /* ---------- 목차 스크롤스파이 ---------- */
    var headings = Array.prototype.slice.call(document.querySelectorAll(".doc-inner .section-h1[id], .doc-inner .section-h2[id]"));
    var tocLinks = Array.prototype.slice.call(document.querySelectorAll(".toc a"));
    if (headings.length && tocLinks.length && "IntersectionObserver" in window) {
      var linkById = {};
      tocLinks.forEach(function (a) {
        var id = a.getAttribute("href").replace("#", "");
        linkById[id] = a;
      });
      var setActive = function (id) {
        tocLinks.forEach(function (a) { a.classList.remove("active"); });
        var link = linkById[id];
        if (link) {
          link.classList.add("active");
          if (link.scrollIntoView) {
            var rect = link.getBoundingClientRect();
            var sbRect = link.closest(".sidebar") ? link.closest(".sidebar").getBoundingClientRect() : null;
            if (sbRect && (rect.top < sbRect.top || rect.bottom > sbRect.bottom)) {
              link.scrollIntoView({ block: "nearest" });
            }
          }
        }
      };
      var visibleSet = new Map();
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) visibleSet.set(entry.target.id, entry.boundingClientRect ? entry.boundingClientRect.top : 0);
          else visibleSet.delete(entry.target.id);
        });
        if (visibleSet.size > 0) {
          var topId = null, topY = Infinity;
          visibleSet.forEach(function (y, id) { if (y < topY) { topY = y; topId = id; } });
          if (topId) setActive(topId);
        }
      }, { rootMargin: "-90px 0px -70% 0px", threshold: 0 });
      headings.forEach(function (h) { io.observe(h); });
    }

    /* ---------- 코드 복사 버튼 ---------- */
    document.querySelectorAll(".copy-btn").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var wrap = btn.closest(".code-block");
        var codeEl = wrap ? wrap.querySelector("code") : null;
        if (!codeEl) return;
        var text = codeEl.innerText;
        var done = function () {
          var original = btn.textContent;
          btn.textContent = "복사됨";
          btn.classList.add("copied");
          setTimeout(function () { btn.textContent = original; btn.classList.remove("copied"); }, 1400);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(done).catch(function () { fallbackCopy(text, done); });
        } else {
          fallbackCopy(text, done);
        }
      });
    });
    function fallbackCopy(text, done) {
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.style.position = "fixed";
      ta.style.opacity = "0";
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand("copy"); } catch (e) {}
      document.body.removeChild(ta);
      done();
    }

    /* ---------- 체크리스트 상태 표시(원본 [x]/[ ] 반영, 읽기전용) ---------- */
    document.querySelectorAll(".checklist input[type=checkbox]").forEach(function (cb) {
      cb.addEventListener("click", function (e) { e.preventDefault(); });
    });

    /* ---------- 검색 ---------- */
    initSearch();

    /* ---------- 이스터에그 ---------- */
    initConsoleEasterEgg();
    initLogoClickEasterEgg();

    /* ---------- 오늘의 개발 소식(GeekNews) ---------- */
    initNewsFeed();
  });

  /* ---------- 검색 핵심 로직 ----------
     동의어 사전·오타 보정·ranking·snippet 생성 로직은 assets/search-core.js에
     따로 두고 여기서는 그 모듈을 가져다 쓴다. 브라우저와 Node 테스트(scripts/test-search.js)가
     같은 로직을 공유하기 위한 구조로, 이 파일에는 로직을 중복 작성하지 않는다. */
  var SC = window.DevNotesSearchCore;

  function initSearch() {
    var overlay = document.getElementById("search-overlay");
    var input = document.getElementById("search-input");
    var results = document.getElementById("search-results");
    if (!overlay || !input || !results) return;

    var activeIndex = -1;

    function open() {
      overlay.classList.add("open");
      input.value = "";
      activeIndex = -1;
      renderResults("");
      setTimeout(function () { input.focus(); }, 30);
    }
    function close() { overlay.classList.remove("open"); }

    document.querySelectorAll(".search-btn, .search-box-desktop input").forEach(function (el) {
      el.addEventListener(el.tagName === "INPUT" ? "focus" : "click", function (e) {
        e.preventDefault();
        open();
      });
    });
    overlay.addEventListener("click", function (e) { if (e.target === overlay) close(); });
    document.addEventListener("keydown", function (e) {
      if ((e.key === "k" || e.key === "K") && (e.metaKey || e.ctrlKey)) { e.preventDefault(); open(); }
      if (e.key === "Escape") close();
    });

    var basePrefix = document.body.getAttribute("data-root-prefix") || "";

    function highlight(text, terms) {
      var escaped = escapeHtml(text);
      var found = terms.filter(function (t) { return t.length > 1; })
        .sort(function (a, b) { return b.length - a.length; });
      found.forEach(function (t) {
        var re = new RegExp("(" + t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "ig");
        escaped = escaped.replace(re, "$1");
      });
      return escaped.replace(//g, "<mark>").replace(//g, "</mark>");
    }

    function renderResults(query) {
      results.innerHTML = "";
      var idx = window.SEARCH_INDEX || [];
      var q = query.trim();
      if (!q) {
        results.innerHTML = '<div class="search-empty">검색어를 입력하세요. 예: 로그인, State, git commit</div>';
        return;
      }
      var tokenGroups = SC.tokenize(q);
      var scored = [];
      idx.forEach(function (it) {
        var r = SC.scoreEntry(it, tokenGroups);
        if (r) scored.push({ it: it, score: r.score, terms: r.terms });
      });
      scored.sort(function (a, b) { return b.score - a.score; });
      var matched = scored.slice(0, 30);
      if (!matched.length) {
        results.innerHTML =
          '<div class="search-empty">' +
          '<div>"' + escapeHtml(query) + '"에 대한 결과가 없습니다.</div>' +
          '<div class="search-empty-hint">다른 표현이나 더 짧은 검색어로 다시 검색해보세요. (예: 정확한 이름 대신 "로그인", "배포"처럼 키워드만)</div>' +
          '</div>';
        return;
      }
      var byPage = {};
      var order = [];
      matched.forEach(function (m) {
        if (!byPage[m.it.p]) { byPage[m.it.p] = []; order.push(m.it.p); }
        byPage[m.it.p].push(m);
      });
      activeIndex = -1;
      order.forEach(function (page) {
        var group = document.createElement("div");
        group.className = "search-result-group";
        group.textContent = page;
        results.appendChild(group);
        byPage[page].forEach(function (m) {
          var snippet = SC.buildSnippet(m.it.t || "", m.terms, 140);
          var a = document.createElement("a");
          a.className = "search-result-item";
          a.href = basePrefix + m.it.u;
          a.innerHTML = '<div class="r-title">' + highlight(m.it.h, m.terms) + '</div><div class="r-snippet">' + highlight(snippet, m.terms) + '</div>';
          results.appendChild(a);
        });
      });
    }

    function moveActive(delta) {
      var items = Array.prototype.slice.call(results.querySelectorAll(".search-result-item"));
      if (!items.length) return;
      if (activeIndex >= 0 && items[activeIndex]) items[activeIndex].classList.remove("active");
      activeIndex = (activeIndex + delta + items.length) % items.length;
      items[activeIndex].classList.add("active");
      items[activeIndex].scrollIntoView({ block: "nearest" });
    }

    input.addEventListener("input", function () { renderResults(input.value); });
    input.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") { e.preventDefault(); moveActive(1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); moveActive(-1); }
      else if (e.key === "Enter" && activeIndex >= 0) {
        var items = results.querySelectorAll(".search-result-item");
        if (items[activeIndex]) items[activeIndex].click();
      }
    });
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  /* ---------- 이스터에그 1: 콘솔 메시지 ---------- */
  function initConsoleEasterEgg() {
    if (window.__devNotesConsoleEggShown) return;
    window.__devNotesConsoleEggShown = true;
    var art = [
      "  _____             _   _       _            ",
      " |  __ \\           | | | |     | |           ",
      " | |  | | _____   _| |_| |_ __ | | ___ _   _ ",
      " | |  | |/ _ \\ \\ / / __| __/ _ \\| |/ _ \\ | | |",
      " | |__| |  __/\\ V /| |_| || (_) | |  __/ |_| |",
      " |_____/ \\___| \\_/  \\__|\\__\\___/|_|\\___|\\__, |",
      "                                          __/ |",
      "                                         |___/ "
    ].join("\n");
    try {
      console.log("%c" + art, "color:#4F7DF3;font-family:monospace;font-size:11px;");
      console.log("%c개발자 도구까지 열어보시다니, 진짜 개발자시네요 🕵️", "color:#4F7DF3;font-weight:bold;font-size:13px;");
      console.log("이 사이트도 결국 Git·HTML·CSS·JS로 만들어졌습니다. 궁금하면 저장소도 구경해보세요: https://github.com/mirikim79/dev-study-notes");
    } catch (e) { /* 콘솔이 없는 환경이면 조용히 무시 */ }
  }

  /* ---------- 이스터에그 2: 홈에서 로고 연타하면 토스트 ---------- */
  function initLogoClickEasterEgg() {
    var brand = document.querySelector(".brand");
    if (!brand) return;
    var onIndex = /(^|\/)index\.html$/.test(location.pathname) || location.pathname === "/" || location.pathname.endsWith("/dev-study-notes/");
    if (!onIndex) return; // 다른 페이지에서는 로고 클릭이 정상적으로 홈으로 이동해야 하므로 건드리지 않음

    var clickTimes = [];
    var THRESHOLD = 5;
    var WINDOW_MS = 2500;
    brand.addEventListener("click", function (e) {
      e.preventDefault();
      var now = Date.now();
      clickTimes.push(now);
      clickTimes = clickTimes.filter(function (t) { return now - t <= WINDOW_MS; });
      if (clickTimes.length >= THRESHOLD) {
        showToast("🎉 오늘의 이스터에그를 찾으셨습니다! 계속 화이팅하세요.");
        clickTimes = [];
      }
    });
  }

  var toastTimer = null;
  function showToast(message) {
    var el = document.getElementById("dev-notes-toast");
    if (!el) {
      el = document.createElement("div");
      el.id = "dev-notes-toast";
      el.className = "dev-notes-toast";
      document.body.appendChild(el);
    }
    el.textContent = message;
    el.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { el.classList.remove("show"); }, 2600);
  }

  /* ---------- 오늘의 개발 소식: GeekNews 피드(assets/news-feed.json)를 client-side에서 fetch ----------
     news-feed.json은 GitHub Actions가 매일 GeekNews RSS를 읽어 새로 커밋하는 정적 파일이다.
     사이트 자체는 여전히 정적이고, 브라우저가 그 JSON을 그때그때 가져와 그리는 방식이라
     별도 서버나 빌드 재실행 없이도 "매일 갱신"되는 효과를 낸다. */
  function initNewsFeed() {
    var el = document.getElementById("news-feed");
    if (!el) return;
    var src = el.getAttribute("data-src");
    fetch(src, { cache: "no-cache" })
      .then(function (res) { if (!res.ok) throw new Error("news-feed fetch failed"); return res.json(); })
      .then(function (data) {
        var items = (data && data.items) || [];
        if (!items.length) { el.innerHTML = '<div class="news-feed-empty">오늘은 불러올 소식이 없습니다.</div>'; return; }
        el.innerHTML = items.map(function (it) {
          return (
            '<a class="news-item" href="' + encodeURI(it.url) + '" target="_blank" rel="noopener">' +
            '<div class="news-item-top"><span class="news-item-source">' + escapeHtml(it.source || "") + '</span>' +
            '<span class="news-item-date">' + escapeHtml(it.date || "") + '</span></div>' +
            '<div class="news-item-title">' + escapeHtml(it.title || "") + '</div>' +
            (it.summary ? '<div class="news-item-summary">' + escapeHtml(it.summary) + '</div>' : "") +
            '</a>'
          );
        }).join("");
      })
      .catch(function () {
        el.innerHTML = '<div class="news-feed-empty">지금은 소식을 불러올 수 없습니다. 나중에 다시 확인해주세요.</div>';
      });
  }
})();
