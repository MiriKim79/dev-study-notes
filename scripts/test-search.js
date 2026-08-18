/* ==========================================================================
   검색 기능 스모크 테스트 — 프레임워크 없이 순수 Node로 실행한다.
   실행: node scripts/test-search.js

   assets/search-core.js(브라우저·Node 공용 로직)와 assets/search-index.js
   (build_site.py가 생성한 실제 검색 인덱스)를 그대로 불러와, 대표 검색어들이
   상위 결과로 "관련 있는" 문서/heading을 반환하는지 확인한다.
   사이트 콘텐츠가 바뀌어 검색이 망가지면 이 스크립트가 실패해야 한다.
   ========================================================================== */
"use strict";

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const SC = require(path.join(ROOT, "assets", "search-core.js"));

function loadSearchIndex() {
  const raw = fs.readFileSync(path.join(ROOT, "assets", "search-index.js"), "utf-8");
  const m = raw.match(/window\.SEARCH_INDEX\s*=\s*(\[[\s\S]*\]);/);
  if (!m) throw new Error("search-index.js에서 SEARCH_INDEX 배열을 찾지 못했습니다.");
  return JSON.parse(m[1]);
}

function search(idx, query, topN) {
  const tokenGroups = SC.tokenize(query);
  const scored = [];
  idx.forEach(function (it) {
    const r = SC.scoreEntry(it, tokenGroups);
    if (r) scored.push({ it: it, score: r.score });
  });
  scored.sort(function (a, b) { return b.score - a.score; });
  return scored.slice(0, topN || 3);
}

/* 각 케이스: query로 검색했을 때, 상위 topN 결과 중 최소 하나는
   heading(h) 또는 page(p)에 expectAny 중 하나(대소문자 무시)를 포함해야 한다. */
const CASES = [
  // 정확한 기술명
  { query: "Git", expectAny: ["git", "깃"] },
  { query: "GitHub", expectAny: ["github", "깃허브"] },
  { query: "React", expectAny: ["react", "리액트"] },
  { query: "JWT", expectAny: ["jwt"] },
  { query: "RAG", expectAny: ["rag"] },
  { query: "TypeScript", expectAny: ["typescript"] },
  { query: "CI/CD", expectAny: ["ci", "배포", "cd"] },
  // 한글
  { query: "깃허브", expectAny: ["github", "깃허브"] },
  { query: "리액트", expectAny: ["react", "리액트"] },
  { query: "데이터베이스", expectAny: ["데이터베이스", "db", "database"] },
  { query: "인증", expectAny: ["인증", "auth", "login", "로그인"] },
  { query: "배포", expectAny: ["배포", "deploy"] },
  { query: "테스트", expectAny: ["테스트", "test"] },
  { query: "보안", expectAny: ["보안", "security"] },
  // 약어
  { query: "DB", expectAny: ["db", "데이터베이스", "database"] },
  { query: "PR", expectAny: ["pr", "풀리퀘스트", "pull request"] },
  { query: "TS", expectAny: ["typescript", "타입스크립트"] },
  { query: "JS", expectAny: ["javascript", "자바스크립트"] },
  // 유사어
  { query: "merge", expectAny: ["병합", "머지", "merge"] },
  { query: "머지", expectAny: ["병합", "머지", "merge"] },
  { query: "병합", expectAny: ["병합", "머지", "merge"] },
  { query: "login", expectAny: ["인증", "로그인", "login"] },
  { query: "로그인", expectAny: ["인증", "로그인", "login"] },
  { query: "auth", expectAny: ["인증", "auth"] },
  // 흔한 오타
  { query: "리엑트", expectAny: ["react", "리액트"] },
  { query: "깃헙", expectAny: ["github", "깃허브"] },
  { query: "데이타베이스", expectAny: ["데이터베이스", "db", "database"] },
  { query: "자바스크립", expectAny: ["javascript", "자바스크립트"] },
  { query: "타입스크립", expectAny: ["typescript", "타입스크립트"] },
  // 자연어 / 문제 상황
  { query: "로그인 구현", expectAny: ["인증", "로그인"] },
  { query: "로그인 안됨", expectAny: ["인증", "로그인", "401", "403"] },
  { query: "push 안됨", expectAny: ["push"] },
  { query: "코드 합치기", expectAny: ["병합", "머지", "merge"] },
  { query: "Git 충돌", expectAny: ["충돌", "conflict"] },
  { query: "서버 안 켜짐", expectAny: ["실행", "배포"] },
  { query: "페이지 안 뜸", expectAny: ["cors", "네트워크", "요청"] },
  { query: "배포 자동화", expectAny: ["배포", "ci", "cd", "자동"] },
  { query: "사이트 느림", expectAny: ["성능", "최적화"] },
  { query: "React 상태", expectAny: ["state", "상태", "react", "리액트"] }
];

function includesAny(text, needles) {
  const lower = String(text || "").toLowerCase();
  return needles.some(function (n) { return lower.indexOf(n.toLowerCase()) !== -1; });
}

function run() {
  const idx = loadSearchIndex();
  let pass = 0;
  let fail = 0;
  const failures = [];

  CASES.forEach(function (c) {
    const results = search(idx, c.query, 3);
    const ok = results.some(function (r) {
      return includesAny(r.it.h, c.expectAny) || includesAny(r.it.p, c.expectAny);
    });
    if (ok) {
      pass++;
    } else {
      fail++;
      failures.push({
        query: c.query,
        expectAny: c.expectAny,
        got: results.map(function (r) { return r.it.p + " > " + r.it.h + " (score " + r.score + ")"; })
      });
    }
  });

  console.log("검색 테스트: " + pass + "개 통과 / " + fail + "개 실패 (전체 " + CASES.length + "개)");
  if (failures.length) {
    console.log("\n실패한 케이스:");
    failures.forEach(function (f) {
      console.log('  - "' + f.query + '" → 기대: [' + f.expectAny.join(", ") + "]");
      console.log("    실제 상위 결과: " + (f.got.length ? f.got.join(" | ") : "(결과 없음)"));
    });
    process.exitCode = 1;
  }
}

run();
