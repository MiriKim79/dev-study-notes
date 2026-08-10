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
  });

  /* ---------- 검색 동의어 사전 ----------
     키(대표어)와 자주 쓰는 다른 표현을 함께 등록해두면, 어느 쪽으로 검색해도
     같은 결과를 찾을 수 있습니다. 필요한 용어가 더 있으면 이 목록에 추가하세요. */
  var SYNONYMS = {
    "저장소": ["repo", "repository", "레포"],
    "브랜치": ["branch"],
    "커밋": ["commit"],
    "병합": ["merge", "머지"],
    "리베이스": ["rebase"],
    "스쿼시": ["squash"],
    "풀리퀘스트": ["pr", "pull request", "풀 리퀘스트"],
    "충돌": ["conflict", "컨플릭트"],
    "되돌리기": ["revert", "reset", "리버트", "리셋"],
    "스태시": ["stash"],
    "태그": ["tag"],
    "원격저장소": ["origin", "remote", "원격"],
    "클론": ["clone"],
    "포크": ["fork"],
    "인증": ["로그인", "login", "authentication", "auth"],
    "토큰": ["jwt", "access token", "액세스 토큰", "리프레시 토큰"],
    "인가": ["authorization", "권한"],
    "해싱": ["bcrypt", "hash", "암호화"],
    "환경변수": ["env", "dotenv", ".env"],
    "컴포넌트": ["component"],
    "상태": ["state"],
    "속성": ["props", "prop"],
    "라우팅": ["routing", "router"],
    "렌더링": ["render", "rendering"],
    "훅": ["hook", "hooks"],
    "데이터베이스": ["db", "database"],
    "마이그레이션": ["migration"],
    "트랜잭션": ["transaction"],
    "엔드포인트": ["endpoint"],
    "미들웨어": ["middleware"],
    "프롬프트": ["prompt"],
    "임베딩": ["embedding"],
    "검색증강생성": ["rag"],
    "환각": ["hallucination"],
    "파인튜닝": ["fine-tuning", "finetuning"],
    "배포": ["deploy", "deployment", "릴리즈", "release"],
    "요청": ["request"],
    "응답": ["response"],
    "검증": ["validation", "유효성"],
    "폴더구조": ["folder structure", "디렉토리 구조", "디렉터리 구조"]
  };
  var SYNONYM_LOOKUP = null;
  function buildSynonymLookup() {
    var map = {};
    Object.keys(SYNONYMS).forEach(function (key) {
      var group = [key].concat(SYNONYMS[key]).map(function (s) { return s.toLowerCase(); });
      group.forEach(function (term) { map[term] = group; });
    });
    return map;
  }
  function expandTerm(term) {
    if (!SYNONYM_LOOKUP) SYNONYM_LOOKUP = buildSynonymLookup();
    return SYNONYM_LOOKUP[term] || [term];
  }

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

    /* 토큰마다 AND, 동의어끼리는 OR. 제목 매치가 가장 높은 점수. */
    function scoreEntry(it, tokenGroups) {
      var hayH = it.h.toLowerCase();
      var hayS = it.s.toLowerCase();
      var hayP = it.p.toLowerCase();
      var score = 0;
      var matchedTerms = [];
      for (var i = 0; i < tokenGroups.length; i++) {
        var terms = tokenGroups[i];
        var inH = terms.filter(function (t) { return hayH.indexOf(t) !== -1; });
        var inS = terms.filter(function (t) { return hayS.indexOf(t) !== -1; });
        var inP = terms.filter(function (t) { return hayP.indexOf(t) !== -1; });
        if (!inH.length && !inS.length && !inP.length) return null;
        if (inH.length) { score += 5; matchedTerms = matchedTerms.concat(inH); }
        if (inP.length) { score += 2; matchedTerms = matchedTerms.concat(inP); }
        if (inS.length) { score += 1; matchedTerms = matchedTerms.concat(inS); }
        if (hayH.indexOf(terms[0]) === 0) score += 2;
      }
      var uniqueTerms = matchedTerms.filter(function (t, i) { return matchedTerms.indexOf(t) === i; });
      return { score: score, terms: uniqueTerms };
    }

    function renderResults(query) {
      results.innerHTML = "";
      var idx = window.SEARCH_INDEX || [];
      var q = query.trim().toLowerCase();
      if (!q) {
        results.innerHTML = '<div class="search-empty">검색어를 입력하세요. 예: 로그인, State, git commit</div>';
        return;
      }
      var tokenGroups = q.split(/\s+/).filter(Boolean).map(expandTerm);
      var scored = [];
      idx.forEach(function (it) {
        var r = scoreEntry(it, tokenGroups);
        if (r) scored.push({ it: it, score: r.score, terms: r.terms });
      });
      scored.sort(function (a, b) { return b.score - a.score; });
      var matched = scored.slice(0, 30);
      if (!matched.length) {
        results.innerHTML = '<div class="search-empty">"' + escapeHtml(query) + '"에 대한 결과가 없습니다. 다른 표현으로도 시도해보세요.</div>';
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
          var a = document.createElement("a");
          a.className = "search-result-item";
          a.href = basePrefix + m.it.u;
          a.innerHTML = '<div class="r-title">' + highlight(m.it.h, m.terms) + '</div><div class="r-snippet">' + highlight(m.it.s, m.terms) + '</div>';
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
})();
