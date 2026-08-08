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
  });

  function initSearch() {
    var overlay = document.getElementById("search-overlay");
    var input = document.getElementById("search-input");
    var results = document.getElementById("search-results");
    if (!overlay || !input || !results) return;

    function open() {
      overlay.classList.add("open");
      input.value = "";
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

    function renderResults(query) {
      results.innerHTML = "";
      var idx = window.SEARCH_INDEX || [];
      var q = query.trim().toLowerCase();
      if (!q) {
        results.innerHTML = '<div class="search-empty">검색어를 입력하세요. 예: JWT, State, git commit</div>';
        return;
      }
      var matched = idx.filter(function (it) {
        return it.h.toLowerCase().indexOf(q) !== -1 || it.s.toLowerCase().indexOf(q) !== -1 || it.p.toLowerCase().indexOf(q) !== -1;
      }).slice(0, 30);
      if (!matched.length) {
        results.innerHTML = '<div class="search-empty">"' + escapeHtml(query) + '"에 대한 결과가 없습니다.</div>';
        return;
      }
      var byPage = {};
      var order = [];
      matched.forEach(function (it) {
        if (!byPage[it.p]) { byPage[it.p] = []; order.push(it.p); }
        byPage[it.p].push(it);
      });
      order.forEach(function (page) {
        var group = document.createElement("div");
        group.className = "search-result-group";
        group.textContent = page;
        results.appendChild(group);
        byPage[page].forEach(function (it) {
          var a = document.createElement("a");
          a.className = "search-result-item";
          a.href = basePrefix + it.u;
          a.innerHTML = '<div class="r-title">' + escapeHtml(it.h) + '</div><div class="r-snippet">' + escapeHtml(it.s) + '</div>';
          results.appendChild(a);
        });
      });
    }

    input.addEventListener("input", function () { renderResults(input.value); });
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
})();
