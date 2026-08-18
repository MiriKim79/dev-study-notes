/* ==========================================================================
   개발 학습·실전 노트 — 검색 핵심 로직 (동의어·오타 보정·ranking·snippet)

   브라우저(main.js)와 Node 자동 테스트(scripts/test-search.js)가 이 파일 하나를
   함께 사용한다. 로직을 두 곳에 나눠 베끼지 않기 위한 목적의 아주 작은 모듈이며,
   외부 의존성은 없다(UMD 패턴으로 <script> 로드와 require() 둘 다 지원).
   ========================================================================== */
(function (root, factory) {
  if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.DevNotesSearchCore = factory();
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  /* ---------- 검색 동의어 사전 ----------
     키(대표어)와 자주 쓰는 다른 표현을 함께 등록해두면, 어느 쪽으로 검색해도
     같은 결과를 찾을 수 있습니다. 필요한 용어가 더 있으면 이 목록에 추가하세요. */
  var SYNONYMS = {
    "저장소": ["repo", "repository", "레포"],
    "브랜치": ["branch"],
    "커밋": ["commit"],
    "병합": ["merge", "머지", "합치기"],
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
    "인증": ["로그인", "login", "authentication", "auth", "sign in", "signin"],
    "토큰": ["jwt", "access token", "액세스 토큰", "리프레시 토큰"],
    "인가": ["authorization", "권한"],
    "해싱": ["bcrypt", "hash", "암호화"],
    "환경변수": ["env", "dotenv", ".env", "environment variable"],
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
    "검색증강생성": ["rag", "retrieval augmented generation"],
    "환각": ["hallucination"],
    "파인튜닝": ["fine-tuning", "finetuning"],
    "배포": ["deploy", "deployment", "릴리즈", "release"],
    "요청": ["request"],
    "응답": ["response"],
    "검증": ["validation", "유효성"],
    "폴더구조": ["folder structure", "디렉토리 구조", "디렉터리 구조"],
    /* 아래부터는 Git 외 분야(프론트/백엔드/DB/보안/성능/AI 등) 동의어 —
       실제 문서 내용을 확인한 뒤, 실제로 쓰이는 표현만 추가했다. */
    "프론트엔드": ["frontend", "front-end", "화면"],
    "백엔드": ["backend", "back-end", "서버"],
    "회원가입": ["signup", "sign up", "register", "가입"],
    "테스트": ["test", "testing"],
    "오류": ["error", "에러"],
    "버그": ["bug"],
    "보안": ["security"],
    "성능": ["performance", "최적화", "느림", "느려요", "느려"],
    "캐시": ["cache", "caching"],
    "비밀번호": ["password", "패스워드"],
    "생성형ai": ["generative ai", "genai", "생성형"],
    "인공지능": ["ai", "artificial intelligence"],
    "에이전트": ["agent"],
    "도구호출": ["tool calling", "function calling", "도구 호출"],
    "타입스크립트": ["typescript", "ts"],
    "자바스크립트": ["javascript", "js"],
    "리액트": ["react"],
    "깃허브": ["github"],
    "cicd": ["ci/cd", "ci-cd", "ci·cd", "continuous integration", "continuous deployment", "자동배포", "자동 배포"]
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

  /* ---------- 흔한 오타 보정 ----------
     검색어를 토큰화하기 전에, 자주 틀리는 표기를 올바른 표기로 바꿔치기한다.
     (fuzzy-matching 라이브러리 없이도 실제로 자주 나오는 오타만 가볍게 대응한다) */
  var TYPO_ALIASES = {
    "리엑트": "리액트",
    "리엑": "리액트",
    "깃헙": "깃허브",
    "깃허부": "깃허브",
    "데이타베이스": "데이터베이스",
    "자바스크립": "자바스크립트",
    "자바스크맆트": "자바스크립트",
    "타입스크립": "타입스크립트",
    "타입스크맆트": "타입스크립트"
  };
  function fixTypo(token) {
    return TYPO_ALIASES[token] || token;
  }

  /* ---------- 검색어 normalization ----------
     대소문자는 이미 처리하고 있었지만 "CI/CD"↔"cicd", "front-end"↔"frontend" 같은
     하이픈/슬래시/가운뎃점 표기 차이는 대응하지 못했다. 특수문자를 전부 지우면
     C++·C#·.NET 같은 실제 기술명이 망가지므로, 하이픈·슬래시·가운뎃점만 선택적으로
     제거하는 "느슨한 비교용" 버전을 만들어 원본과 함께(OR로) 비교한다.
     공백은 지우지 않는다 — 공백까지 지우면 "5단계. Network"처럼 서로 무관한 두 단어가
     들러붙어 ".NET" 같은 검색어와 우연히 겹치는 오탐이 생길 수 있기 때문이다. */
  function looseForm(s) {
    return s.replace(/[\-\/·]+/g, "");
  }

  /* ---------- 문제 상황 표현 대응 ----------
     정확한 기술명을 몰라도 "OO 안 됨/안 뜸/느림" 같은 자연어로 검색할 수 있게,
     실제로 관련 문서가 있는 표현만 골라 대상 키워드로 연결한다.
     "서버 안 켜짐"처럼 뒤 절만 떼어내면 지나치게 넓은 범위(예: "서버" 단독)를
     매칭하게 되는 경우는 여기서 구체적인 키워드로 직접 지정해 과다 노출을 막는다. */
  var PROBLEM_PHRASES = [
    { match: "서버 안 켜짐", terms: ["실행", "배포"] },
    { match: "서버가 안 켜짐", terms: ["실행", "배포"] },
    { match: "서버 안켜짐", terms: ["실행", "배포"] },
    { match: "페이지 안 뜸", terms: ["cors", "네트워크", "요청"] },
    { match: "페이지 안뜸", terms: ["cors", "네트워크", "요청"] },
    { match: "화면 안 뜸", terms: ["cors", "네트워크", "요청"] },
    /* "사이트/화면 느림"도 뒤 낱말만 떼면 "사이트"처럼 지나치게 넓은 범위가 되므로
       구체적인 키워드로 직접 연결한다. */
    { match: "사이트 느림", terms: ["성능", "최적화"] },
    { match: "사이트가 느림", terms: ["성능", "최적화"] },
    { match: "사이트 느려", terms: ["성능", "최적화"] },
    { match: "화면 느림", terms: ["성능", "최적화"] },
    { match: "화면 느려", terms: ["성능", "최적화"] },
    /* "OO 구현" 같은 방법을 묻는 자연어 표현 — 실제 관련 헤딩에 "구현"이라는
       단어가 항상 붙어 있지는 않으므로(예: 인증 섹션), 대표 표현만 직접 연결한다. */
    { match: "로그인 구현", terms: ["인증", "로그인"] }
  ];
  /* 위 목록에 없는 일반적인 "OO 안 됨/안 돼요/안 열림/안 켜짐" 류의 문제 서술어는
     검색에 도움이 안 되는 꼬리이므로 핵심 키워드만 남기고 잘라낸다.
     예: "로그인 안됨" → "로그인", "push 안됨" → "push" */
  var PROBLEM_SUFFIX_RE = /\s*(이|가)?\s*안\s*(되나요|되요|됩니다|됨|돼요|돼|열림|켜짐|뜸|올라옴|올라감)\s*[.?!]?\s*$/i;

  /* 문제 상황 문구를 검색 가능한 토큰 그룹으로 바꾼다.
     PROBLEM_PHRASES에 매치되면 그 keyword들을 하나의 OR 그룹으로 반환하고(각 키워드 중
     하나만 있어도 됨), 아니면 꼬리만 잘라낸 뒤 평소처럼 공백 기준으로 토큰화한다. */
  function tokenize(query) {
    var q = String(query || "").trim().toLowerCase();
    if (!q) return [];
    for (var i = 0; i < PROBLEM_PHRASES.length; i++) {
      if (q.indexOf(PROBLEM_PHRASES[i].match) !== -1) {
        return [PROBLEM_PHRASES[i].terms.slice()];
      }
    }
    var stripped = q.replace(PROBLEM_SUFFIX_RE, "").trim();
    if (stripped) q = stripped;
    return q.split(/\s+/).filter(Boolean).map(function (tok) {
      return expandTerm(fixTypo(tok));
    });
  }

  /* 토큰 그룹마다 AND, 그룹 안 동의어끼리는 OR. heading/page title 매치가 본문(body)
     매치보다 훨씬 높은 점수를 받는다 — heading 제목이 검색어와 정확히 일치하면 가장 위로. */
  function scoreEntry(it, tokenGroups) {
    var hayH = it.h.toLowerCase();
    var hayT = (it.t || "").toLowerCase();
    var hayP = it.p.toLowerCase();
    var hayHLoose = looseForm(hayH);
    var hayTLoose = looseForm(hayT);
    var hayPLoose = looseForm(hayP);

    var score = 0;
    var matchedTerms = [];
    for (var i = 0; i < tokenGroups.length; i++) {
      var terms = tokenGroups[i];
      var inH = [], inP = [], inT = [];
      for (var j = 0; j < terms.length; j++) {
        var term = terms[j];
        var termLoose = looseForm(term);
        var hitH = hayH.indexOf(term) !== -1 || (termLoose.length > 1 && hayHLoose.indexOf(termLoose) !== -1);
        var hitP = hayP.indexOf(term) !== -1 || (termLoose.length > 1 && hayPLoose.indexOf(termLoose) !== -1);
        var hitT = hayT.indexOf(term) !== -1 || (termLoose.length > 1 && hayTLoose.indexOf(termLoose) !== -1);
        if (hitH) inH.push(term);
        if (hitP) inP.push(term);
        if (hitT) inT.push(term);
      }
      if (!inH.length && !inP.length && !inT.length) return null;
      if (inH.length) { score += 5; matchedTerms = matchedTerms.concat(inH); }
      if (inP.length) { score += 2; matchedTerms = matchedTerms.concat(inP); }
      if (inT.length) { score += 1; matchedTerms = matchedTerms.concat(inT); }
      if (hayH.indexOf(terms[0]) === 0) score += 2;
      if (hayH === terms[0]) score += 3;
    }
    var uniqueTerms = matchedTerms.filter(function (t, i) { return matchedTerms.indexOf(t) === i; });
    return { score: score, terms: uniqueTerms };
  }

  /* 검색어가 실제로 등장하는 위치 주변을 잘라 snippet으로 보여준다.
     예전에는 항상 본문 맨 앞 140자를 보여줘서 "왜 이 결과가 나왔지?"란 혼란이 있었다. */
  function buildSnippet(text, terms, windowSize) {
    text = text || "";
    windowSize = windowSize || 140;
    if (!text) return "";
    var lower = text.toLowerCase();
    var bestPos = -1;
    var sorted = (terms || []).filter(function (t) { return t.length > 1; })
      .sort(function (a, b) { return b.length - a.length; });
    for (var i = 0; i < sorted.length; i++) {
      var pos = lower.indexOf(sorted[i]);
      if (pos !== -1 && (bestPos === -1 || pos < bestPos)) bestPos = pos;
    }
    if (bestPos === -1) {
      return text.length > windowSize ? text.slice(0, windowSize) + "…" : text;
    }
    var before = Math.floor(windowSize * 0.35);
    var start = Math.max(0, bestPos - before);
    var end = Math.min(text.length, start + windowSize);
    var snippet = text.slice(start, end);
    if (start > 0) snippet = "…" + snippet;
    if (end < text.length) snippet = snippet + "…";
    return snippet;
  }

  return {
    SYNONYMS: SYNONYMS,
    TYPO_ALIASES: TYPO_ALIASES,
    PROBLEM_PHRASES: PROBLEM_PHRASES,
    expandTerm: expandTerm,
    fixTypo: fixTypo,
    looseForm: looseForm,
    tokenize: tokenize,
    scoreEntry: scoreEntry,
    buildSnippet: buildSnippet
  };
});
