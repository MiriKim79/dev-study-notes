# -*- coding: utf-8 -*-
"""
build_site.py — 개발 학습·실전 노트의 Markdown 원본을 학습용 HTML로 변환한다.

- 원본 .md 파일은 절대 읽기만 하고 수정하지 않는다.
- 표준 라이브러리만 사용한다(외부 markdown 라이브러리·CDN 없음).
- 실행: python build_site.py
- Markdown을 수정한 뒤 다시 이 스크립트를 실행하면 HTML이 재생성된다.
"""
import hashlib
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

# Windows 콘솔은 기본 인코딩이 cp949라, 제목에 em dash(—) 같은 문자가 있으면
# print()가 그대로 죽는다. 콘솔 출력을 UTF-8로 강제해 빌드가 중간에 멈추지 않게 한다.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
SITE_BASE_URL = "https://mirikim79.github.io/dev-study-notes/"


def _compute_asset_version():
    """assets/style.css·main.js 내용이 바뀔 때만 값이 바뀌는 캐시 무효화용 버전 문자열.
    내용이 그대로면 값도 그대로라 불필요한 캐시 무효화가 없다."""
    h = hashlib.sha256()
    for name in ("assets/style.css", "assets/main.js", "assets/search-core.js"):
        p = ROOT / name
        if p.exists():
            h.update(p.read_bytes())
    return h.hexdigest()[:10]


ASSET_VERSION = _compute_asset_version()

# ==========================================================================
# 1. 사이트에 포함되는 문서 목록(메타데이터) — 실제 파일명을 기준으로 한다.
# ==========================================================================
PLAYBOOK_DIR = "개발 기초·실전 가이드"
TEMPLATE_DIR = "GitHub 팀 협업 템플릿"
MID_DIR = "개발 중급 가이드"
ADV_DIR = "개발 고급 가이드"
CERT_DIR = "자격증 대비"

PAGES = [
    {
        "key": "playbook-hub",
        "src": f"{PLAYBOOK_DIR}.md",
        "title": "개발 기초·실전 가이드",
        "kicker": "가이드 모음",
        "cat": "start",
        "icon": "📚",
        "hub": None,
        "hub_children": ["first-steps", "git-min", "team-start", "frontend", "backend", "ai", "git", "profile-readme", "presentation", "vibe-coding", "agent-trends"],
    },
    {
        "key": "first-steps",
        "src": f"{PLAYBOOK_DIR}/개발 처음 시작하기.md",
        "title": "개발 처음 시작하기",
        "kicker": "개발 기초·실전 가이드",
        "cat": "start",
        "icon": "🗺️",
        "hub": "playbook-hub",
        "tagline": "프로그램이 뭔지도 감이 안 잡힌다? 5~10분이면 전체 지도가 보입니다.",
    },
    {
        "key": "git-min",
        "src": f"{PLAYBOOK_DIR}/Git·GitHub 진짜 최소 기초.md",
        "title": "Git·GitHub 진짜 최소 기초",
        "kicker": "개발 기초·실전 가이드",
        "cat": "git",
        "icon": "🔰",
        "hub": "playbook-hub",
        "tagline": "Git이 뭔지도 모른다? branch도 처음 들어봤다? 여기부터 시작하세요 — 5분이면 끝나요.",
    },
    {
        "key": "team-start",
        "src": f"{PLAYBOOK_DIR}/팀 개발 시작 가이드.md",
        "title": "팀 개발 시작 가이드",
        "kicker": "개발 기초·실전 가이드",
        "cat": "start",
        "icon": "🚀",
        "hub": "playbook-hub",
        "tagline": "뭐부터 해야 할지 감이 안 잡힌다? 전체 그림부터 여기서 잡고 가세요.",
    },
    {
        "key": "frontend",
        "src": f"{PLAYBOOK_DIR}/프론트엔드 기초 가이드.md",
        "title": "프론트엔드 기초 가이드",
        "kicker": "개발 기초·실전 가이드",
        "cat": "frontend",
        "icon": "🎨",
        "hub": "playbook-hub",
        "tagline": "HTML·CSS·JS가 뭔지도 헷갈린다? 화면 만들기, 여기서 시작하세요.",
    },
    {
        "key": "backend",
        "src": f"{PLAYBOOK_DIR}/백엔드 기초 가이드.md",
        "title": "백엔드 기초 가이드",
        "kicker": "개발 기초·실전 가이드",
        "cat": "backend",
        "icon": "🛠️",
        "hub": "playbook-hub",
        "tagline": "서버가 대체 뭘 하는 건지 감이 안 온다? 여기서부터 차근차근 풀립니다.",
    },
    {
        "key": "ai",
        "src": f"{PLAYBOOK_DIR}/생성형 AI 기능 개발 기초 가이드.md",
        "title": "생성형 AI 기능 개발 기초 가이드",
        "kicker": "개발 기초·실전 가이드",
        "cat": "ai",
        "icon": "🤖",
        "hub": "playbook-hub",
        "tagline": "AI 기능 넣고 싶은데 프롬프트가 뭔지도 모른다? 바로 이 문서입니다.",
    },
    {
        "key": "git",
        "src": f"{PLAYBOOK_DIR}/Git·GitHub 기초 가이드.md",
        "title": "Git·GitHub 기초 가이드",
        "kicker": "개발 기초·실전 가이드",
        "cat": "git",
        "icon": "🌿",
        "hub": "playbook-hub",
        "tagline": "add, commit, push를 외우기 전에 원리부터 — 충돌 해결까지 제대로 다룹니다.",
    },
    {
        "key": "profile-readme",
        "src": f"{PLAYBOOK_DIR}/GitHub 프로필 꾸미기 가이드.md",
        "title": "GitHub 프로필 꾸미기 가이드",
        "kicker": "개발 기초·실전 가이드",
        "cat": "misc",
        "icon": "✨",
        "hub": "playbook-hub",
        "tagline": "학습 필수는 아니지만 재미로 — shields.io 배지, 통계 카드로 프로필 꾸며보기.",
    },
    {
        "key": "presentation",
        "src": f"{PLAYBOOK_DIR}/개발자 발표·데모 잘하는 법.md",
        "title": "개발자 발표·데모 잘하는 법",
        "kicker": "개발 기초·실전 가이드",
        "cat": "misc",
        "icon": "🎤",
        "hub": "playbook-hub",
        "tagline": "데모데이 발표 앞두고 있다면 — 스톱워치로 리허설하는 법부터.",
    },
    {
        "key": "vibe-coding",
        "src": f"{PLAYBOOK_DIR}/바이브 코딩으로 개발하기.md",
        "title": "바이브 코딩으로 개발하기",
        "kicker": "개발 기초·실전 가이드",
        "cat": "misc",
        "icon": "🌀",
        "hub": "playbook-hub",
        "tagline": "AI에게 코드를 맡길 때, 언제는 괜찮고 언제는 위험한지 감 잡기.",
    },
    {
        "key": "agent-trends",
        "src": f"{PLAYBOOK_DIR}/AI 코딩 에이전트 최신 트렌드 — 하네스·루프·그래프 엔지니어링.md",
        "title": "AI 코딩 에이전트 최신 트렌드 — 하네스·루프·그래프 엔지니어링",
        "kicker": "개발 기초·실전 가이드",
        "cat": "misc",
        "icon": "🧩",
        "hub": "playbook-hub",
        "tagline": "요즘 자주 들리는 그 용어들, 정확히 뭘 가리키는지 정리했습니다.",
    },
    {
        "key": "collab-method",
        "src": "개발 협업 방식 선택 가이드.md",
        "title": "개발 협업 방식 선택 가이드",
        "kicker": "협업 방식",
        "cat": "collab",
        "icon": "🧭",
        "hub": None,
    },
    {
        "key": "github-hub",
        "src": f"{TEMPLATE_DIR}.md",
        "title": "GitHub 팀 협업 가이드",
        "kicker": "협업 템플릿",
        "cat": "github",
        "icon": "🤝",
        "hub": None,
        "hub_children": ["contributing", "agents", "claude", "planning", "issue-pr"],
    },
    {
        "key": "contributing",
        "src": f"{TEMPLATE_DIR}/팀 GitHub 협업 규칙 (CONTRIBUTING.md).md",
        "title": "팀 GitHub 협업 규칙 (CONTRIBUTING.md)",
        "kicker": "GitHub 팀 협업 가이드",
        "cat": "github",
        "icon": "📋",
        "hub": "github-hub",
    },
    {
        "key": "agents",
        "src": f"{TEMPLATE_DIR}/AI 코딩 에이전트 작업 규칙 (AGENTS.md).md",
        "title": "AI 코딩 에이전트 작업 규칙 (AGENTS.md)",
        "kicker": "GitHub 팀 협업 가이드",
        "cat": "github",
        "icon": "🧠",
        "hub": "github-hub",
    },
    {
        "key": "claude",
        "src": f"{TEMPLATE_DIR}/Claude Code 작업 규칙 (CLAUDE.md).md",
        "title": "Claude Code 작업 규칙 (CLAUDE.md)",
        "kicker": "GitHub 팀 협업 가이드",
        "cat": "github",
        "icon": "⚙️",
        "hub": "github-hub",
    },
    {
        "key": "planning",
        "src": f"{TEMPLATE_DIR}/기획·API·일정 템플릿 (PLANNING.md).md",
        "title": "기획·API·일정 템플릿 (PLANNING.md)",
        "kicker": "GitHub 팀 협업 가이드",
        "cat": "github",
        "icon": "🗂️",
        "hub": "github-hub",
    },
    {
        "key": "issue-pr",
        "src": f"{TEMPLATE_DIR}/GitHub Issue·PR 템플릿 예시.md",
        "title": "GitHub Issue·PR 템플릿 예시",
        "kicker": "GitHub 팀 협업 가이드",
        "cat": "github",
        "icon": "🏷️",
        "hub": "github-hub",
    },
    {
        "key": "mid-hub",
        "src": f"{MID_DIR}.md",
        "title": "개발 중급 가이드",
        "kicker": "가이드 모음",
        "cat": "start",
        "icon": "📈",
        "hub": None,
        "hub_children": [
            "git-mid", "frontend-mid", "backend-mid", "ai-mid", "team-mid",
            "test-mid", "cicd-mid", "db-mid", "ts-mid",
        ],
    },
    {
        "key": "git-mid",
        "src": f"{MID_DIR}/Git·GitHub 중급 가이드.md",
        "title": "Git·GitHub 중급 가이드",
        "kicker": "개발 중급 가이드",
        "cat": "git",
        "icon": "🌿",
        "hub": "mid-hub",
        "tagline": "add·commit·push는 손에 익었다? 이제 이력을 다듬고 자동화를 붙일 차례입니다.",
    },
    {
        "key": "frontend-mid",
        "src": f"{MID_DIR}/프론트엔드 중급 가이드.md",
        "title": "프론트엔드 중급 가이드",
        "kicker": "개발 중급 가이드",
        "cat": "frontend",
        "icon": "🎨",
        "hub": "mid-hub",
        "tagline": "화면은 일단 동작한다? 이제 성능·테스트·렌더링 전략까지 챙길 차례입니다.",
    },
    {
        "key": "backend-mid",
        "src": f"{MID_DIR}/백엔드 중급 가이드.md",
        "title": "백엔드 중급 가이드",
        "kicker": "개발 중급 가이드",
        "cat": "backend",
        "icon": "🛠️",
        "hub": "mid-hub",
        "tagline": "API 서버는 한 번 만들어봤다? 요청이 몰릴 때 무너지지 않는 법을 다룹니다.",
    },
    {
        "key": "ai-mid",
        "src": f"{MID_DIR}/생성형 AI 중급 가이드.md",
        "title": "생성형 AI 중급 가이드",
        "kicker": "개발 중급 가이드",
        "cat": "ai",
        "icon": "🤖",
        "hub": "mid-hub",
        "tagline": "RAG를 한 번 붙여봤다? 이제 비용·품질을 실무 수준으로 관리할 차례입니다.",
    },
    {
        "key": "team-mid",
        "src": f"{MID_DIR}/팀 협업 중급 가이드.md",
        "title": "팀 협업 중급 가이드",
        "kicker": "개발 중급 가이드",
        "cat": "start",
        "icon": "🚀",
        "hub": "mid-hub",
        "tagline": "팀이 커졌다? 코드가 아니라 '함께 오래 일하는 방식'이 문제가 되는 순간입니다.",
    },
    {
        "key": "test-mid",
        "src": f"{MID_DIR}/테스트 자동화 중급 가이드.md",
        "title": "테스트 자동화 중급 가이드",
        "kicker": "개발 중급 가이드",
        "cat": "common",
        "icon": "🧪",
        "hub": "mid-hub",
        "tagline": "매번 손으로 눌러보며 확인한다? 테스트 코드로 그 시간을 되찾는 방법입니다.",
    },
    {
        "key": "cicd-mid",
        "src": f"{MID_DIR}/CI·CD 중급 가이드.md",
        "title": "CI·CD 중급 가이드",
        "kicker": "개발 중급 가이드",
        "cat": "common",
        "icon": "⚙️",
        "hub": "mid-hub",
        "tagline": "배포를 손으로 한다? 테스트에서 배포까지 잇는 파이프라인을 직접 만들어봅니다.",
    },
    {
        "key": "db-mid",
        "src": f"{MID_DIR}/데이터베이스 중급 가이드.md",
        "title": "데이터베이스 중급 가이드",
        "kicker": "개발 중급 가이드",
        "cat": "common",
        "icon": "🗄️",
        "hub": "mid-hub",
        "tagline": "조회가 왜 느려지는지 감이 안 온다? 인덱스부터 백업까지 원인과 해법을 다룹니다.",
    },
    {
        "key": "ts-mid",
        "src": f"{MID_DIR}/TypeScript 중급 가이드.md",
        "title": "TypeScript 중급 가이드",
        "kicker": "개발 중급 가이드",
        "cat": "common",
        "icon": "🔷",
        "hub": "mid-hub",
        "tagline": "타입 표기가 귀찮은 잔소리처럼 느껴진다? 버그를 미리 잡아주는 도구로 바뀌는 순간을 다룹니다.",
    },
    {
        "key": "adv-hub",
        "src": f"{ADV_DIR}.md",
        "title": "개발 고급 가이드",
        "kicker": "가이드 모음",
        "cat": "start",
        "icon": "🏔️",
        "hub": None,
        "hub_children": [
            "system-design-adv", "cloud-adv", "db-adv", "security-adv",
            "perf-adv", "leadership-adv", "ai-adv",
        ],
    },
    {
        "key": "system-design-adv",
        "src": f"{ADV_DIR}/시스템 설계 고급 가이드.md",
        "title": "시스템 설계 고급 가이드",
        "kicker": "개발 고급 가이드",
        "cat": "system",
        "icon": "🏗️",
        "hub": "adv-hub",
        "tagline": "서버 한 대로는 더 이상 안 된다? MSA와 이벤트 기반 설계로 넘어갈 때 필요한 판단 기준입니다.",
    },
    {
        "key": "cloud-adv",
        "src": f"{ADV_DIR}/클라우드·IaC 고급 가이드.md",
        "title": "클라우드·IaC 고급 가이드",
        "kicker": "개발 고급 가이드",
        "cat": "cloud",
        "icon": "☁️",
        "hub": "adv-hub",
        "tagline": "서버 설정을 콘솔에서 손으로 클릭한다? Terraform·쿠버네티스로 코드화하는 법을 다룹니다.",
    },
    {
        "key": "db-adv",
        "src": f"{ADV_DIR}/데이터베이스 고급 가이드.md",
        "title": "데이터베이스 고급 가이드",
        "kicker": "개발 고급 가이드",
        "cat": "common",
        "icon": "🗄️",
        "hub": "adv-hub",
        "tagline": "복제·샤딩 기초는 안다? 분산 트랜잭션과 샤딩을 실전에 적용할 때의 함정을 다룹니다.",
    },
    {
        "key": "security-adv",
        "src": f"{ADV_DIR}/보안 심화 가이드.md",
        "title": "보안 심화 가이드",
        "kicker": "개발 고급 가이드",
        "cat": "security",
        "icon": "🔐",
        "hub": "adv-hub",
        "tagline": "로그인 기능만 있으면 안전하다고 생각했다? OWASP 기준으로 실제 공격 시나리오를 점검합니다.",
    },
    {
        "key": "perf-adv",
        "src": f"{ADV_DIR}/성능·스케일 고급 가이드.md",
        "title": "성능·스케일 고급 가이드",
        "kicker": "개발 고급 가이드",
        "cat": "perf",
        "icon": "⚡",
        "hub": "adv-hub",
        "tagline": "트래픽이 갑자기 몰리면 어떻게 될까 불안하다? 병목을 찾고 확장하는 실전 방법을 다룹니다.",
    },
    {
        "key": "leadership-adv",
        "src": f"{ADV_DIR}/기술 리더십·레거시 마이그레이션 가이드.md",
        "title": "기술 리더십·레거시 마이그레이션 가이드",
        "kicker": "개발 고급 가이드",
        "cat": "leadership",
        "icon": "🧭",
        "hub": "adv-hub",
        "tagline": "코드는 잘 짜는데 팀을 어떻게 이끌지 모르겠다? 기술 결정과 낡은 코드 전환의 기준을 다룹니다.",
    },
    {
        "key": "ai-adv",
        "src": f"{ADV_DIR}/생성형 AI 고급 가이드.md",
        "title": "생성형 AI 고급 가이드",
        "kicker": "개발 고급 가이드",
        "cat": "ai",
        "icon": "🤖",
        "hub": "adv-hub",
        "tagline": "AI 기능 하나는 붙여봤다? 여러 에이전트를 조율하고 직접 모델을 서빙하는 단계입니다.",
    },
    {
        "key": "cert-hub",
        "src": f"{CERT_DIR}.md",
        "title": "자격증 대비",
        "kicker": "가이드 모음",
        "cat": "start",
        "icon": "🏅",
        "hub": None,
        "hub_children": ["csts", "sqld", "adsp", "infoproc", "infosec", "aws-cert"],
    },
    {
        "key": "sqld",
        "src": f"{CERT_DIR}/SQLD 대비 가이드.md",
        "title": "SQLD 대비 가이드",
        "kicker": "자격증 대비",
        "cat": "cert",
        "icon": "🗄️",
        "hub": "cert-hub",
        "tagline": "SQL은 좀 짜는데 자격증은 처음? 시험에 나오는 딱 그 범위만 정리했습니다.",
    },
    {
        "key": "adsp",
        "src": f"{CERT_DIR}/ADSP 대비 가이드.md",
        "title": "ADSP 대비 가이드",
        "kicker": "자격증 대비",
        "cat": "cert",
        "icon": "📊",
        "hub": "cert-hub",
        "tagline": "통계·데이터 분석 용어가 낯설다? 시험에 나오는 개념만 추려서 정리했습니다.",
    },
    {
        "key": "infoproc",
        "src": f"{CERT_DIR}/정보처리기사 대비 가이드.md",
        "title": "정보처리기사 대비 가이드",
        "kicker": "자격증 대비",
        "cat": "cert",
        "icon": "💻",
        "hub": "cert-hub",
        "tagline": "국내 개발자 지망생이 가장 많이 따는 그 자격증, 범위부터 정리하고 시작하세요.",
    },
    {
        "key": "infosec",
        "src": f"{CERT_DIR}/정보보안기사·산업기사 대비 가이드.md",
        "title": "정보보안기사·산업기사 대비 가이드",
        "kicker": "자격증 대비",
        "cat": "cert",
        "icon": "🔐",
        "hub": "cert-hub",
        "tagline": "보안 심화 가이드로 개념은 잡았다? 이제 자격증 범위에 맞춰 정리할 차례입니다.",
    },
    {
        "key": "aws-cert",
        "src": f"{CERT_DIR}/AWS 클라우드 자격증 대비 가이드.md",
        "title": "AWS 클라우드 자격증 대비 가이드",
        "kicker": "자격증 대비",
        "cat": "cert",
        "icon": "☁️",
        "hub": "cert-hub",
        "tagline": "클라우드·IaC 고급 가이드는 봤다? 이제 AWS 자격증으로 검증해볼 차례입니다.",
    },
    {
        "key": "csts",
        "src": f"{CERT_DIR}/CSTS 대비 가이드.md",
        "title": "CSTS 대비 가이드",
        "kicker": "자격증 대비",
        "cat": "cert",
        "icon": "🧪",
        "hub": "cert-hub",
        "tagline": "테스트 코드는 짜봤다? 이제 테스트 설계 기법과 결함 관리 이론으로 검증해볼 차례입니다.",
    },
]
PAGES_BY_KEY = {p["key"]: p for p in PAGES}

# 학습 추천 순서(이전/다음 네비게이션에 사용) — index.html 포함
STUDY_ORDER = [
    "index",
    "playbook-hub",
    "first-steps",
    "git-min",
    "team-start",
    "git",
    "frontend",
    "backend",
    "ai",
    "profile-readme",
    "presentation",
    "vibe-coding",
    "agent-trends",
    "collab-method",
    "github-hub",
    "contributing",
    "agents",
    "claude",
    "planning",
    "issue-pr",
    "mid-hub",
    "team-mid",
    "git-mid",
    "frontend-mid",
    "backend-mid",
    "ai-mid",
    "test-mid",
    "cicd-mid",
    "db-mid",
    "ts-mid",
    "adv-hub",
    "system-design-adv",
    "cloud-adv",
    "db-adv",
    "security-adv",
    "perf-adv",
    "leadership-adv",
    "ai-adv",
    "cert-hub",
    "csts",
    "sqld",
    "adsp",
    "infoproc",
    "infosec",
    "aws-cert",
]

CAT_LABEL = {
    "start": "팀 개발 시작",
    "frontend": "프론트엔드",
    "backend": "백엔드",
    "ai": "생성형 AI",
    "git": "Git·GitHub",
    "collab": "협업 방식",
    "github": "GitHub 팀 협업",
    "common": "공통",
    "system": "시스템 설계",
    "cloud": "클라우드·IaC",
    "security": "보안",
    "perf": "성능·스케일",
    "leadership": "기술 리더십",
    "cert": "자격증 대비",
    "misc": "기타",
}


def url_of(key):
    if key == "index":
        return "index.html"
    return PAGES_BY_KEY[key]["src"][:-3] + ".html"


def prefix_of(key):
    """루트 기준 상대 경로 접두사('' 또는 '../')."""
    if key == "index" or key not in PAGES_BY_KEY:
        return ""   # PAGES에 등록되지 않은 루트 페이지(방명록 등)는 루트 기준으로 취급
    src = PAGES_BY_KEY[key]["src"]
    return "../" if "/" in src else ""


def rel_link(from_key, to_key):
    """from_key 페이지에서 to_key 페이지로 가는 상대 경로."""
    from_prefix = prefix_of(from_key)
    to_url = url_of(to_key)
    to_src = "" if to_key == "index" else PAGES_BY_KEY[to_key]["src"]
    to_in_sub = "/" in to_src if to_key != "index" else False
    from_in_sub = from_prefix == "../"

    if to_key == "index":
        return ("../" if from_in_sub else "") + "index.html"
    if from_in_sub and to_in_sub:
        # 둘 다 서브폴더에 있을 때: 같은 폴더인지 확인
        from_src = PAGES_BY_KEY[from_key]["src"]
        if from_src.split("/")[0] == to_src.split("/")[0]:
            return to_src.split("/")[-1][:-3] + ".html"
        return "../" + to_url
    if from_in_sub and not to_in_sub:
        return "../" + to_url
    if not from_in_sub and to_in_sub:
        return to_url
    return to_url


# ==========================================================================
# 2. 마크다운 파서 (표준 라이브러리만 사용, 이 저장소 문서에서 실제로
#    쓰인 구문만 지원한다: 헤딩 h1~h3, 문단, 굵게, 인라인 코드, 링크,
#    가로줄, blockquote, 펜스 코드블록(중첩 백틱 길이 포함),
#    순서/비순서 리스트(체크박스·중첩 포함), GFM 표)
# ==========================================================================
FENCE_OPEN_RE = re.compile(r"^(`{3,}|~{3,})\s*([^\s`]*)\s*$")
HEADING_RE = re.compile(r"^(#{1,3})\s+(.*)$")
HR_RE = re.compile(r"^-{3,}\s*$")
LIST_MARKER_RE = re.compile(r"^([-*]|\d+[.)])\s+(.*)$")
CHECKBOX_RE = re.compile(r"^\[( |x|X)\]\s?(.*)$")
SEP_CELL_RE = re.compile(r"^:?-{1,}:?$")
LABEL_RE = re.compile(r"^\*\*([^*]{1,14}):\*\*\s*(.*)$")


def is_ordered_marker(marker):
    return marker[0].isdigit()


def strip_table_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def is_table_start(lines, i, end):
    if i + 1 >= end:
        return False
    if "|" not in lines[i]:
        return False
    sep = lines[i + 1]
    if "|" not in sep and "-" not in sep:
        return False
    cells = strip_table_row(sep)
    return len(cells) > 0 and all(SEP_CELL_RE.match(c) for c in cells if c != "") and any(c for c in cells)


def parse_fence(lines, i, end):
    m = FENCE_OPEN_RE.match(lines[i])
    fence_char = m.group(1)[0]
    fence_len = len(m.group(1))
    lang = m.group(2) or ""
    i += 1
    close_re = re.compile(r"^" + re.escape(fence_char) + ("{%d,}" % fence_len) + r"\s*$")
    content = []
    while i < end:
        if close_re.match(lines[i]):
            i += 1
            break
        content.append(lines[i])
        i += 1
    else:
        pass
    return {"type": "code", "lang": lang, "code": "\n".join(content)}, i


DETAILS_OPEN_RE = re.compile(r"^<details[ >]", re.IGNORECASE)
DETAILS_OPEN_EXACT_RE = re.compile(r"^<details\b", re.IGNORECASE)
DETAILS_CLOSE_RE = re.compile(r"^</details\s*>$", re.IGNORECASE)

SVG_OPEN_RE = re.compile(r"^<svg[ >]", re.IGNORECASE)
SVG_OPEN_EXACT_RE = re.compile(r"^<svg\b", re.IGNORECASE)
SVG_CLOSE_RE = re.compile(r"^</svg\s*>$", re.IGNORECASE)

# 단일 라인 <img ...> 원문 HTML 패스스루(자체 닫힘 태그이므로 open/close 쌍이 아니라 한 줄 자체로 완결)
IMG_LINE_RE = re.compile(r"^<img[ >].*>$", re.IGNORECASE)


def parse_raw_html_block(lines, i, end, open_exact_re=DETAILS_OPEN_EXACT_RE, close_re=DETAILS_CLOSE_RE):
    """<details>...</details> 또는 <svg>...</svg> 원문 HTML을 그대로 통과시킨다(중첩 지원).
    안쪽 내용은 마크다운으로 해석하지 않고 작성자가 직접 HTML로 쓴다."""
    depth = 0
    content = []
    while i < end:
        line = lines[i]
        s = line.strip()
        if open_exact_re.match(s):
            depth += 1
        if close_re.match(s):
            depth -= 1
            content.append(line)
            i += 1
            if depth <= 0:
                break
            continue
        content.append(line)
        i += 1
    return {"type": "raw_html", "html": "\n".join(content)}, i


def parse_blockquote(lines, i, end):
    content = []
    while i < end and lines[i].lstrip().startswith(">"):
        l = lines[i].lstrip()[1:]
        if l.startswith(" "):
            l = l[1:]
        content.append(l)
        i += 1
    sub_blocks = parse_blocks(content, 0, len(content))
    return {"type": "blockquote", "blocks": sub_blocks}, i


def parse_table(lines, i, end):
    header = strip_table_row(lines[i])
    i += 2  # 헤더 + 구분행
    rows = []
    while i < end and lines[i].strip() != "" and "|" in lines[i] and not FENCE_OPEN_RE.match(lines[i]):
        rows.append(strip_table_row(lines[i]))
        i += 1
    return {"type": "table", "header": header, "rows": rows}, i


def parse_paragraph(lines, i, end):
    content = []
    while i < end:
        line = lines[i]
        if line.strip() == "":
            break
        if FENCE_OPEN_RE.match(line):
            break
        if HEADING_RE.match(line):
            break
        if HR_RE.match(line):
            break
        if line.lstrip().startswith(">"):
            break
        if DETAILS_OPEN_RE.match(line.strip()) or DETAILS_OPEN_EXACT_RE.match(line.strip()):
            break
        if SVG_OPEN_RE.match(line.strip()) or SVG_OPEN_EXACT_RE.match(line.strip()):
            break
        if IMG_LINE_RE.match(line.strip()):
            break
        if is_table_start(lines, i, end):
            break
        content.append(line.rstrip())
        i += 1
    return {"type": "para", "lines": content}, i


def parse_list(lines, i, end):
    first = lines[i]
    indent = len(first) - len(first.lstrip(" "))
    m0 = LIST_MARKER_RE.match(first.strip())
    ordered = is_ordered_marker(m0.group(1))
    items = []
    while i < end:
        line = lines[i]
        if line.strip() == "":
            j = i
            while j < end and lines[j].strip() == "":
                j += 1
            if j >= end:
                i = j
                break
            nxt = lines[j]
            nxt_indent = len(nxt) - len(nxt.lstrip(" "))
            nxt_is_item = bool(LIST_MARKER_RE.match(nxt.strip())) and nxt_indent == indent
            if nxt_is_item or nxt_indent > indent:
                i = j
                continue
            break
        cur_indent = len(line) - len(line.lstrip(" "))
        if cur_indent != indent:
            break
        m = LIST_MARKER_RE.match(line.strip())
        if not m:
            break
        marker_text = line.strip()[: m.start(2)]
        content_col = indent + len(marker_text)
        first_content = m.group(2)
        item_lines = [first_content]
        i += 1
        while i < end:
            l2 = lines[i]
            if l2.strip() == "":
                j = i
                while j < end and lines[j].strip() == "":
                    j += 1
                if j < end:
                    l2i = len(lines[j]) - len(lines[j].lstrip(" "))
                    if l2i >= content_col:
                        item_lines.append("")
                        i = j
                        continue
                break
            l2_indent = len(l2) - len(l2.lstrip(" "))
            if l2_indent >= content_col:
                if len(l2) >= content_col and l2[:content_col].strip() == "":
                    item_lines.append(l2[content_col:])
                else:
                    item_lines.append(l2.strip())
                i += 1
                continue
            break
        checked = None
        cb = CHECKBOX_RE.match(item_lines[0])
        if cb:
            checked = cb.group(1).lower() == "x"
            item_lines[0] = cb.group(2)
        sub_blocks = parse_blocks(item_lines, 0, len(item_lines))
        items.append({"blocks": sub_blocks, "checked": checked})
    return {"type": "list", "ordered": ordered, "items": items}, i


def parse_blocks(lines, i, end):
    blocks = []
    while i < end:
        line = lines[i]
        if line.strip() == "":
            i += 1
            continue
        if FENCE_OPEN_RE.match(line):
            b, i = parse_fence(lines, i, end)
            blocks.append(b)
            continue
        m = HEADING_RE.match(line)
        if m:
            blocks.append({"type": "heading", "level": len(m.group(1)), "text": m.group(2).strip()})
            i += 1
            continue
        if HR_RE.match(line):
            blocks.append({"type": "hr"})
            i += 1
            continue
        if line.lstrip().startswith(">"):
            b, i = parse_blockquote(lines, i, end)
            blocks.append(b)
            continue
        if DETAILS_OPEN_EXACT_RE.match(line.strip()):
            b, i = parse_raw_html_block(lines, i, end)
            blocks.append(b)
            continue
        if SVG_OPEN_EXACT_RE.match(line.strip()):
            b, i = parse_raw_html_block(lines, i, end, open_exact_re=SVG_OPEN_EXACT_RE, close_re=SVG_CLOSE_RE)
            blocks.append(b)
            continue
        if IMG_LINE_RE.match(line.strip()):
            blocks.append({"type": "raw_html", "html": '<div class="doc-img-wrap">%s</div>' % line.strip()})
            i += 1
            continue
        if is_table_start(lines, i, end):
            b, i = parse_table(lines, i, end)
            blocks.append(b)
            continue
        if LIST_MARKER_RE.match(line.strip()):
            b, i = parse_list(lines, i, end)
            blocks.append(b)
            continue
        b, i = parse_paragraph(lines, i, end)
        blocks.append(b)
    return blocks


def extract_intro(lines):
    if not lines or not lines[0].lstrip().startswith(">"):
        return None, 0
    i = 0
    rows = []
    while i < len(lines) and lines[i].lstrip().startswith(">"):
        raw = lines[i].lstrip()[1:]
        if raw.startswith(" "):
            raw = raw[1:]
        rows.append(raw.rstrip())
        i += 1
    return rows, i


def og_description_for(page, intro_rows):
    """공유 미리보기(OG/Twitter 카드)에 쓸 한 줄 설명. 문서 소개 박스의 '목적' 줄을 우선 사용한다."""
    if intro_rows:
        for row in intro_rows:
            m = LABEL_RE.match(row.strip())
            if m and m.group(1) == "목적":
                return m.group(2).strip()
        first = LABEL_RE.match(intro_rows[0].strip())
        if first:
            return first.group(2).strip()
        if intro_rows[0].strip():
            return intro_rows[0].strip()
    fallback = next((learn for k, _, learn, _ in OVERVIEW_ROWS if k == page["key"]), None)
    if fallback:
        return fallback
    return "개발 공부 가이드 — 개발 분야별 기초를 실전 흐름 속에서 이해하는 학습 자료입니다."


# ==========================================================================
# 3. 인라인 렌더링 (인라인 코드 보호 → 링크 → 굵게 → 이스케이프 복원 순서)
# ==========================================================================
INLINE_CODE_RE = re.compile(r"`([^`]+)`")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")


def render_inline(text):
    codes = []

    def stash_code(m):
        codes.append(m.group(1))
        return "\x00C%d\x00" % (len(codes) - 1)

    text = INLINE_CODE_RE.sub(stash_code, text)

    links = []

    def stash_link(m):
        links.append((m.group(1), m.group(2)))
        return "\x00L%d\x00" % (len(links) - 1)

    text = LINK_RE.sub(stash_link, text)

    text = html.escape(text, quote=False)
    text = BOLD_RE.sub(r"<strong>\1</strong>", text)

    def restore_link(m):
        idx = int(m.group(1))
        label, url = links[idx]
        label_html = html.escape(label, quote=False)
        label_html = BOLD_RE.sub(r"<strong>\1</strong>", label_html)
        target = ' target="_blank" rel="noopener"' if url.startswith("http") else ""
        return '<a href="%s"%s>%s</a>' % (html.escape(url, quote=True), target, label_html)

    text = re.sub(r"\x00L(\d+)\x00", restore_link, text)

    def restore_code(m):
        idx = int(m.group(1))
        return '<code class="inline-code">%s</code>' % html.escape(codes[idx], quote=False)

    text = re.sub(r"\x00C(\d+)\x00", restore_code, text)
    return text


def join_para_lines(lines):
    parts = []
    n = len(lines)
    for idx, raw in enumerate(lines):
        hard_break = raw.endswith("  ") and idx < n - 1
        parts.append(render_inline(raw.strip()))
        if hard_break:
            parts.append("<br>")
        elif idx < n - 1:
            parts.append(" ")
    return "".join(parts)


# ==========================================================================
# 4. 최소 syntax highlight (언어가 명시된 코드블록에만 적용, 나머지는 평문)
# ==========================================================================
HIGHLIGHT_RULES = {
    "bash": [
        (r"#.*$", "tok-comment"),
        (r'"[^"]*"', "tok-string"),
        (r"'[^']*'", "tok-string"),
        (r"\b(git|npm|pip|python|node|cd|ls|export|source|sudo|curl|gh)\b", "tok-keyword"),
    ],
    "python": [
        (r"#.*$", "tok-comment"),
        (r'"[^"]*"|\'[^\']*\'', "tok-string"),
        (r"\b(def|class|import|from|return|if|else|elif|for|while|as|with|try|except|in|is|not|and|or|None|True|False)\b", "tok-keyword"),
        (r"\b\d+\b", "tok-number"),
    ],
    "js": [
        (r"//.*$", "tok-comment"),
        (r'"[^"]*"|\'[^\']*\'|`[^`]*`', "tok-string"),
        (r"\b(const|let|var|function|return|if|else|for|while|import|from|export|default|async|await|class|new|extends|try|catch|null|undefined|true|false)\b", "tok-keyword"),
        (r"\b\d+\b", "tok-number"),
    ],
    "ts": [],  # js 규칙 재사용(아래에서 매핑)
    "jsx": [],
    "json": [
        (r'"[^"]*"\s*:', "tok-func"),
        (r'"[^"]*"', "tok-string"),
        (r"\b\d+\b", "tok-number"),
    ],
    "css": [
        (r"/\*.*?\*/", "tok-comment"),
        (r"[.#][\w-]+", "tok-func"),
        (r"\b\d+(px|em|rem|%)?\b", "tok-number"),
    ],
    "http": [
        (r"^(GET|POST|PUT|PATCH|DELETE)\b", "tok-keyword"),
    ],
}
HIGHLIGHT_RULES["ts"] = HIGHLIGHT_RULES["js"]
HIGHLIGHT_RULES["jsx"] = HIGHLIGHT_RULES["js"]
HIGHLIGHT_RULES["tsx"] = HIGHLIGHT_RULES["js"]


def highlight_code(code, lang):
    rules = HIGHLIGHT_RULES.get(lang.lower())
    escaped = html.escape(code)
    if not rules:
        return escaped

    # 이스케이프된 텍스트 위에서 토큰을 감싼다(겹치지 않게 순차 처리 + 플레이스홀더)
    placeholders = []

    def wrap(pattern, cls, text):
        def sub(m):
            placeholders.append('<span class="%s">%s</span>' % (cls, m.group(0)))
            return "\x00T%d\x00" % (len(placeholders) - 1)
        return re.sub(pattern, sub, text, flags=re.MULTILINE)

    text = escaped
    for pattern, cls in rules:
        text = wrap(pattern, cls, text)
    text = re.sub(r"\x00T(\d+)\x00", lambda m: placeholders[int(m.group(1))], text)
    return text


# ==========================================================================
# 5. 헤딩 메타데이터 부여 / 목차 / '기본 상식' 콜아웃 래핑
# ==========================================================================
def slugify(text, used):
    s = re.sub(r"[`*]", "", text)
    s = re.sub(r"[^0-9A-Za-z가-힣]+", "-", s)
    s = s.strip("-") or "section"
    base, n = s, 2
    while s in used:
        s = f"{base}-{n}"
        n += 1
    used.add(s)
    return s


TAG_BY_OFFSET = {0: "h2", 1: "h3", 2: "h4"}
CLS_BY_OFFSET = {0: "section-h1", 1: "section-h2", 2: "section-h3"}


def assign_heading_meta(blocks):
    levels = [b["level"] for b in blocks if b["type"] == "heading"]
    min_level = min(levels) if levels else 1
    used = set()
    for b in blocks:
        if b["type"] != "heading":
            continue
        offset = max(0, min(2, b["level"] - min_level))
        b["tag"] = TAG_BY_OFFSET[offset]
        b["cls"] = CLS_BY_OFFSET[offset]
        b["mapped"] = offset
        b["id"] = slugify(b["text"], used)


def build_toc(blocks):
    toc = []
    current = None
    for b in blocks:
        if b["type"] != "heading":
            continue
        if b["mapped"] == 0:
            current = {"id": b["id"], "text": b["text"], "children": []}
            toc.append(current)
        elif b["mapped"] == 1:
            entry = {"id": b["id"], "text": b["text"]}
            if current is not None:
                current["children"].append(entry)
            else:
                toc.append({"id": b["id"], "text": b["text"], "children": []})
    return toc


def normalize_heading_text(t):
    return t.replace(" ", "")


def wrap_concept_boxes(blocks):
    out = []
    i, n = 0, len(blocks)
    while i < n:
        b = blocks[i]
        if b["type"] == "heading" and b["mapped"] == 2 and normalize_heading_text(b["text"]) == "기본상식":
            j = i + 1
            while j < n and blocks[j]["type"] != "heading":
                j += 1
            out.append({"type": "concept_box", "inner": blocks[i:j]})
            i = j
        else:
            out.append(b)
            i += 1
    return out


# ==========================================================================
# 6. 블록 렌더링
# ==========================================================================
def render_item_inner(item_blocks):
    if len(item_blocks) == 1 and item_blocks[0]["type"] == "para":
        return join_para_lines(item_blocks[0]["lines"])
    return render_blocks(item_blocks)


def render_list(b):
    is_checklist = any(it.get("checked") is not None for it in b["items"])
    tag = "ul" if is_checklist else ("ol" if b["ordered"] else "ul")
    cls = ' class="checklist"' if is_checklist else ""
    parts = []
    for it in b["items"]:
        inner = render_item_inner(it["blocks"])
        if it.get("checked") is not None:
            checked_attr = " checked" if it["checked"] else ""
            li_cls = ' class="checked"' if it["checked"] else ""
            parts.append('<li%s><input type="checkbox" disabled%s><span>%s</span></li>' % (li_cls, checked_attr, inner))
        else:
            parts.append("<li>%s</li>" % inner)
    return "<%s%s>%s</%s>" % (tag, cls, "".join(parts), tag)


def render_table(b):
    thead = "<tr>" + "".join("<th>%s</th>" % render_inline(c) for c in b["header"]) + "</tr>"
    body_rows = []
    for r in b["rows"]:
        cells = "".join("<td>%s</td>" % render_inline(c) for c in r)
        body_rows.append("<tr>%s</tr>" % cells)
    return '<div class="table-scroll"><table><thead>%s</thead><tbody>%s</tbody></table></div>' % (thead, "".join(body_rows))


def render_code(b):
    lang = (b["lang"] or "").strip()
    label = lang if lang else "text"
    code_html = highlight_code(b["code"], lang) if lang else html.escape(b["code"])
    return (
        '<div class="code-block"><div class="code-block-header">'
        '<span class="code-lang">%s</span>'
        '<button class="copy-btn" type="button">복사</button></div>'
        "<pre><code>%s</code></pre></div>" % (html.escape(label), code_html)
    )


def render_heading(b):
    return '<%s class="%s" id="%s">%s<a class="heading-anchor" href="#%s" aria-label="이 섹션 링크">#</a></%s>' % (
        b["tag"], b["cls"], b["id"], render_inline(b["text"]), b["id"], b["tag"]
    )


def render_blocks(blocks):
    out = []
    for b in blocks:
        t = b["type"]
        if t == "heading":
            out.append(render_heading(b))
        elif t == "code":
            out.append(render_code(b))
        elif t == "table":
            out.append(render_table(b))
        elif t == "list":
            out.append(render_list(b))
        elif t == "blockquote":
            out.append("<blockquote>" + render_blocks(b["blocks"]) + "</blockquote>")
        elif t == "hr":
            out.append("<hr>")
        elif t == "raw_html":
            out.append(b["html"])
        elif t == "para":
            if b["lines"]:
                out.append("<p>" + join_para_lines(b["lines"]) + "</p>")
        elif t == "concept_box":
            out.append(
                '<div class="callout callout-concept"><div class="callout-label">💡 핵심 개념</div>'
                + render_blocks(b["inner"])
                + "</div>"
            )
    return "\n".join(out)


def render_intro_box(rows):
    parts = []
    for row in rows:
        m = LABEL_RE.match(row)
        if m:
            parts.append(
                '<div class="intro-row"><strong>%s:</strong> %s</div>'
                % (html.escape(m.group(1)), render_inline(m.group(2)))
            )
        else:
            parts.append('<div class="intro-row">%s</div>' % render_inline(row))
    return '<div class="callout callout-intro"><div class="callout-label">📘 문서 소개</div>%s</div>' % "".join(parts)


def render_outline_box(toc):
    if not toc:
        return ""
    items = "".join("<li>%s</li>" % html.escape(t["text"]) for t in toc)
    return (
        '<div class="callout callout-outline"><div class="callout-label">🗂️ 이 문서의 구성</div>'
        "<ol>%s</ol></div>" % items
    )


# ==========================================================================
# 7. 페이지 조립 (공통 셸)
# ==========================================================================
def render_sidebar_toc(toc):
    items = []
    for t in toc:
        children = ""
        if t["children"]:
            children = '<ul class="toc-h2-list">' + "".join(
                '<li><a href="#%s">%s</a></li>' % (c["id"], html.escape(c["text"])) for c in t["children"]
            ) + "</ul>"
        items.append('<li class="toc-h1"><a href="#%s">%s</a>%s</li>' % (t["id"], html.escape(t["text"]), children))
    return '<ul class="toc">' + "".join(items) + "</ul>"


TIER_HUBS = [
    ("playbook-hub", "🔰", "초급"),
    ("mid-hub", "📈", "중급"),
    ("adv-hub", "🏔️", "고급"),
    ("cert-hub", "🏅", "자격증"),
]


def top_hub_of(key):
    """페이지가 속한 최상위 허브 key를 반환. 허브 소속이 아니면 None."""
    seen = set()
    cur = key
    while cur and cur not in seen:
        seen.add(cur)
        page = PAGES_BY_KEY.get(cur)
        if not page:
            return None
        hub = page.get("hub")
        if hub is None:
            return cur
        cur = hub
    return None


def render_tier_nav(current_key):
    active_hub = top_hub_of(current_key) if current_key != "index" else None
    items = []
    for hub_key, icon, label in TIER_HUBS:
        cls = "tier-nav-link active" if hub_key == active_hub else "tier-nav-link"
        href = rel_link(current_key, hub_key)
        items.append('<a class="%s" href="%s">%s %s</a>' % (cls, href, icon, html.escape(label)))
    return '<nav class="tier-nav"><div class="tier-nav-inner">%s</div></nav>' % "".join(items)


def render_breadcrumb(page):
    parts = ['<a href="%s">대시보드</a>' % rel_link(page["key"], "index")]
    if page.get("hub"):
        hub = PAGES_BY_KEY[page["hub"]]
        parts.append('<span>›</span><a href="%s">%s</a>' % (rel_link(page["key"], page["hub"]), html.escape(hub["title"])))
    parts.append('<span>›</span><span class="current">%s</span>' % html.escape(page["title"]))
    return " ".join(parts)


def render_prev_next(page_key):
    idx = STUDY_ORDER.index(page_key)
    prev_key = STUDY_ORDER[idx - 1] if idx > 0 else None
    next_key = STUDY_ORDER[idx + 1] if idx < len(STUDY_ORDER) - 1 else None

    def label(k):
        # "이전 학습"/"다음 학습" 방향 텍스트 뒤에 "학습 대시보드"가 붙으면
        # "이전 학습학습 대시보드"처럼 "학습"이 겹쳐 보여서, 대시보드로 갈 때만 짧게 표기한다.
        return "대시보드" if k == "index" else PAGES_BY_KEY[k]["title"]

    # 방향 라벨과 문서 제목이 한 줄에 붙어 보이지 않도록, 둘 사이에 항상 구분자를 명시적으로 넣는다.
    left = ""
    right = ""
    if prev_key:
        left = '<a class="doc-nav-link prev" href="%s"><span class="doc-nav-dir">← 이전 학습</span><span class="doc-nav-sep"> · </span><span class="doc-nav-title">%s</span></a>' % (
            rel_link(page_key, prev_key), html.escape(label(prev_key))
        )
    else:
        left = '<span class="doc-nav-spacer"></span>'
    if next_key:
        right = '<a class="doc-nav-link next" href="%s"><span class="doc-nav-dir">다음 학습 →</span><span class="doc-nav-sep"> </span><span class="doc-nav-title">%s</span></a>' % (
            rel_link(page_key, next_key), html.escape(label(next_key))
        )
    if not (prev_key or next_key):
        return ""
    return '<nav class="doc-nav">%s%s</nav>' % (left, right)


def render_hub_quicklinks(page):
    children = page.get("hub_children")
    if not children:
        return ""
    items = []
    for ck in children:
        c = PAGES_BY_KEY[ck]
        items.append(
            '<a class="hub-item" href="%s"><div><div class="hub-item-title">%s %s</div>'
            '<div class="hub-item-desc">%s</div></div><span class="hub-item-arrow">→</span></a>'
            % (rel_link(page["key"], ck), c["icon"], html.escape(c["title"]), html.escape(CAT_LABEL.get(c["cat"], "")))
        )
    return (
        '<div class="section-heading" style="margin-top:32px;">바로가기</div>'
        '<div class="hub-list">%s</div>' % "".join(items)
    )


PAGE_HTML_TMPL = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · 개발 학습·실전 노트</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%F0%9F%8C%B1%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="{prefix}assets/style.css?v={asset_v}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="개발 공부 가이드">
<meta property="og:title" content="{title} · 개발 학습·실전 노트">
<meta property="og:description" content="{og_description}">
<meta property="og:url" content="{og_url}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{title} · 개발 학습·실전 노트">
<meta name="twitter:description" content="{og_description}">
<script src="{prefix}assets/search-index.js?v={asset_v}" defer></script>
</head>
<body data-root-prefix="{prefix}">
<div id="reading-progress"></div>
<header class="site-header">
  <div class="header-inner">
    <button class="menu-btn" type="button" aria-label="목차 열기">☰</button>
    <a class="brand" href="{prefix}index.html">개발 공부 가이드</a>
    <nav class="breadcrumb">{breadcrumb}</nav>
    <div class="header-actions">
      <div class="search-box-desktop"><span>🔍</span><input type="text" placeholder="검색 (Ctrl+K)" readonly></div>
      <a class="guestbook-btn" href="{prefix}방명록.html">💬 <span class="guestbook-btn-label">방명록</span></a>
      <button class="search-btn" type="button" aria-label="검색">🔍</button>
      <button class="theme-btn" type="button" aria-label="다크모드 전환">🌙</button>
    </div>
  </div>
</header>
{tier_nav}
<div class="sidebar-overlay"></div>
<button class="sidebar-reopen-btn" type="button" aria-label="사이드바 펼치기" title="목차 펼치기">»</button>
<div class="page-shell">
  <div class="layout">
    <aside class="sidebar">
      <div class="sidebar-title-row">
        <div class="sidebar-title">목차</div>
        <button class="sidebar-collapse-btn" type="button" aria-label="사이드바 접기" title="목차 접기">«</button>
      </div>
      {sidebar}
      <a class="sidebar-footer-link" href="{prefix}index.html">← 학습 대시보드로</a>
    </aside>
    <main class="main-content">
      <div class="doc-inner" style="--card-accent: var(--cat-{cat});">
        <span class="page-kicker">{icon} {kicker}</span>
        <h1 class="page-title">{title}</h1>
        {tagline}
        {intro}
        {outline}
        {hub_links}
        {body}
        {nav}
      </div>
    </main>
  </div>
</div>
<div class="search-overlay" id="search-overlay">
  <div class="search-panel">
    <input type="text" id="search-input" placeholder="키워드로 검색 — 유사어도 함께 찾아요 (예: 로그인, 머지, 상태)">
    <div class="search-results" id="search-results"></div>
  </div>
</div>
<script src="{prefix}assets/search-core.js?v={asset_v}" defer></script>
<script src="{prefix}assets/main.js?v={asset_v}" defer></script>
</body>
</html>
"""


def build_content_page(page):
    md_path = ROOT / page["src"]
    raw = md_path.read_text(encoding="utf-8")
    lines = raw.replace("\r\n", "\n").replace("\r", "\n").split("\n")

    intro_rows, start_idx = extract_intro(lines)
    blocks = parse_blocks(lines, start_idx, len(lines))
    assign_heading_meta(blocks)
    toc = build_toc(blocks)
    blocks = wrap_concept_boxes(blocks)
    body_html = render_blocks(blocks)

    tagline_html = (
        '<p class="page-tagline">%s</p>' % html.escape(page["tagline"]) if page.get("tagline") else ""
    )
    intro_html = render_intro_box(intro_rows) if intro_rows else ""
    outline_html = render_outline_box(toc)
    hub_links_html = render_hub_quicklinks(page)
    sidebar_html = render_sidebar_toc(toc)
    nav_html = render_prev_next(page["key"])
    breadcrumb_html = render_breadcrumb(page)
    prefix = prefix_of(page["key"])
    og_description = html.escape(og_description_for(page, intro_rows))
    og_url = SITE_BASE_URL + quote(page["src"][:-3] + ".html")

    html_out = PAGE_HTML_TMPL.format(
        title=html.escape(page["title"]),
        prefix=prefix,
        asset_v=ASSET_VERSION,
        breadcrumb=breadcrumb_html,
        tier_nav=render_tier_nav(page["key"]),
        sidebar=sidebar_html,
        cat=page["cat"],
        icon=page["icon"],
        kicker=html.escape(page["kicker"]),
        tagline=tagline_html,
        intro=intro_html,
        outline=outline_html,
        hub_links=hub_links_html,
        body=body_html,
        nav=nav_html,
        og_description=og_description,
        og_url=og_url,
    )

    out_path = ROOT / (page["src"][:-3] + ".html")
    out_path.write_text(html_out, encoding="utf-8")

    # 검색 인덱스용 항목 수집
    search_entries = []
    for b in blocks_flatten_for_search(blocks):
        pass
    search_entries = collect_search_entries(page, blocks)
    return search_entries, toc


def blocks_flatten_for_search(blocks):
    return blocks


def block_text(b):
    """검색 스니펫용: 블록에서 순수 텍스트만 뽑는다."""
    t = b["type"]
    if t == "para":
        return " ".join(l.strip() for l in b["lines"])
    if t == "list":
        parts = []
        for it in b["items"]:
            for sub in it["blocks"]:
                parts.append(block_text(sub))
        return " ".join(parts)
    if t == "blockquote":
        return " ".join(block_text(sb) for sb in b["blocks"])
    if t == "table":
        return " ".join(" ".join(r) for r in b["rows"])
    if t == "concept_box":
        return " ".join(block_text(sb) for sb in b["inner"])
    if t == "raw_html":
        return re.sub(r"<[^>]+>", " ", b["html"])
    return ""


# 검색 대상 텍스트(t)의 최대 길이. 화면에 보여줄 snippet과는 별개로, 검색 매칭에만
# 쓰이는 필드라서 heading 하나의 본문 전체(중앙값 약 150자, p90 약 530자)를 충분히
# 담으면서도 인덱스 파일이 지나치게 커지지 않도록 상한을 둔다.
SEARCH_TEXT_MAX_LEN = 1000


def collect_search_entries(page, blocks):
    entries = []
    url = page["src"][:-3] + ".html"
    current_heading = None
    buffer_text = []

    def flush():
        if current_heading is not None:
            full_text = " ".join(buffer_text).strip()
            full_text = re.sub(r"\s+", " ", full_text)[:SEARCH_TEXT_MAX_LEN]
            entries.append({
                "p": page["title"],
                "h": current_heading["text"],
                "u": url + "#" + current_heading["id"],
                "t": full_text,
            })

    def walk(blist):
        nonlocal current_heading, buffer_text
        for b in blist:
            if b["type"] == "heading":
                flush()
                current_heading = b
                buffer_text = []
            elif b["type"] == "concept_box":
                walk(b["inner"])
            else:
                txt = block_text(b)
                if txt:
                    buffer_text.append(txt)

    walk(blocks)
    flush()
    if not entries:
        entries.append({"p": page["title"], "h": page["title"], "u": url, "t": page["kicker"]})
    return entries


# ==========================================================================
# 8. 대시보드(index.html)
# ==========================================================================
DASHBOARD_INTRO = (
    "프론트엔드·백엔드·생성형 AI·Git, 실제 팀 프로젝트를 만드는 순서 그대로 배우는 학습 자료입니다. "
    "초급부터 고급까지 단계별로 정리돼 있으니, 지금 나에게 필요한 단계부터 골라서 보면 됩니다."
)

OVERVIEW_ROWS = [
    ("first-steps", "개발 처음 시작하기", "프로그램·에디터·터미널·프론트/백엔드·서버·DB가 뭔지 5~10분 만에 전체 지도 잡기", "프로그래밍이라는 단어를 오늘 처음 들어봤을 때"),
    ("git-min", "Git·GitHub 진짜 최소 기초", "branch·commit·push·PR·merge·pull이 뭔지 5분 만에 감 잡기", "Git이라는 단어를 오늘 처음 들어봤을 때"),
    ("team-start", "팀 개발 시작 가이드", "요구사항 확인, MVP 범위, 사용자 흐름, 기술·구조 결정, 구현, 테스트, 배포, 회고까지 전체 순서", "처음 팀 프로젝트를 시작할 때"),
    ("frontend", "프론트엔드 기초 가이드", "HTML·CSS·JavaScript부터 React, API 통신, 상태 관리, 인증, 배포까지 공통 기초", "프론트엔드를 처음 공부할 때"),
    ("backend", "백엔드 기초 가이드", "서버, HTTP/REST, DB, 인증·인가, 보안, 테스트, 운영·배포의 기본 원리", "백엔드를 처음 공부할 때"),
    ("ai", "생성형 AI 기능 개발 기초 가이드", "프롬프트, 구조화 출력, 평가, RAG, Tool Calling, Agent, 보안, 비용·지연시간", "AI 기능을 서비스에 붙이고 싶을 때"),
    ("git", "Git·GitHub 기초 가이드", "저장소, add/commit/push/pull, 브랜치, PR, 충돌, merge/rebase, 인증", "Git을 처음 사용할 때"),
    ("collab-method", "개발 협업 방식 선택 가이드", "브랜치 전략, 리뷰·머지 방식, 실시간 협업, 저장소 구조 비교", "팀 Git 협업 방식을 정할 때"),
    ("github-hub", "GitHub 팀 협업 가이드", "CONTRIBUTING, AGENTS, CLAUDE, PLANNING, Issue·PR 템플릿", "실제 팀 프로젝트를 진행할 때"),
]

DASHBOARD_CARDS = [
    "first-steps", "git-min", "team-start", "frontend", "backend", "ai", "git",
    "collab-method", "github-hub",
]

# "기타" — 학습 필수는 아니지만 재미·최신 트렌드로 가볍게 보는 문서들.
# 핵심 학습 흐름(초급~자격증)과는 구분해서 대시보드에 별도 섹션으로 보여준다.
OVERVIEW_ROWS_MISC = [
    ("profile-readme", "GitHub 프로필 꾸미기 가이드", "프로필 README 저장소, shields.io 배지, 통계 카드, 주의점", "학습은 다 했고 재미로 프로필을 꾸며보고 싶을 때"),
    ("presentation", "개발자 발표·데모 잘하는 법", "시간 배분, 스톱워치 리허설, 데모데이 구조, 라이브 데모 리스크 관리", "팀 프로젝트 데모데이나 발표를 앞두고 있을 때"),
    ("vibe-coding", "바이브 코딩으로 개발하기", "바이브 코딩의 정의, 언제 적합한지, 안전하게 쓰는 법", "AI에게 코드를 맡겨 빠르게 뭔가 만들어보고 싶을 때"),
    ("agent-trends", "AI 코딩 에이전트 최신 트렌드", "하네스 엔지니어링, 루프 엔지니어링, 그래프/멀티 에이전트 오케스트레이션", "요즘 자주 들리는 AI 에이전트 용어가 궁금할 때"),
]

DASHBOARD_CARDS_MISC = ["profile-readme", "presentation", "vibe-coding", "agent-trends"]

OVERVIEW_ROWS_MID = [
    ("git-mid", "Git·GitHub 중급 가이드", "interactive rebase, cherry-pick, bisect, worktree, GitHub Actions, 브랜치 보호 심화", "Git 기본 명령이 손에 익은 뒤"),
    ("frontend-mid", "프론트엔드 중급 가이드", "성능 최적화, 상태관리 라이브러리 비교, 렌더링 전략(SSR/SSG), 테스트, Core Web Vitals", "화면 하나를 끝까지 만들어본 뒤"),
    ("backend-mid", "백엔드 중급 가이드", "캐싱, 메시지 큐, N+1 쿼리, API 버저닝, Rate Limiting, 구조화 로깅", "API 서버 하나를 끝까지 만들어본 뒤"),
    ("ai-mid", "생성형 AI 중급 가이드", "파인튜닝, 벡터 DB 심화, 프롬프트 체이닝, 비용 최적화, 평가 자동화", "기초 RAG·Tool Calling을 붙여본 뒤"),
    ("team-mid", "팀 협업 중급 가이드", "코드 리뷰 문화, ADR, 기술 부채 관리, 온보딩 문서화, 회고", "여러 명이 함께 개발을 시작한 뒤"),
    ("test-mid", "테스트 자동화 중급 가이드", "테스트 피라미드, TDD, Mock/Stub, 커버리지의 함정, 플레이키 테스트", "테스트 코드를 체계적으로 짜고 싶을 때"),
    ("cicd-mid", "CI·CD 중급 가이드", "CI/CD 개념, GitHub Actions 배포 파이프라인, 배포 전략, 시크릿 관리", "배포까지 자동화하고 싶을 때"),
    ("db-mid", "데이터베이스 중급 가이드", "인덱스 튜닝, 정규화·역정규화, 복제, 샤딩 기초, 백업과 복구", "데이터가 많아져 조회가 느려질 때"),
    ("ts-mid", "TypeScript 중급 가이드", "Union/Generic, interface vs type, 유틸리티 타입, 런타임 검증, any 피하기", "TypeScript를 실전에 활용하고 싶을 때"),
]

DASHBOARD_CARDS_MID = [
    "git-mid", "frontend-mid", "backend-mid", "ai-mid", "team-mid",
    "test-mid", "cicd-mid", "db-mid", "ts-mid",
]

OVERVIEW_ROWS_ADV = [
    ("system-design-adv", "시스템 설계 고급 가이드", "MSA 분리 기준, 이벤트 기반 아키텍처, 서비스 간 통신, 장애 격리", "서버 하나로 감당이 안 되기 시작할 때"),
    ("cloud-adv", "클라우드·IaC 고급 가이드", "Terraform으로 인프라 코드화, 쿠버네티스 기본 개념, 배포 전략", "인프라를 손으로 관리하는 게 한계에 부딪혔을 때"),
    ("db-adv", "데이터베이스 고급 가이드", "분산 트랜잭션, 샤딩 실전, 정합성 모델, 대규모 마이그레이션", "복제·샤딩 기초로도 부족해졌을 때"),
    ("security-adv", "보안 심화 가이드", "OWASP Top 10, 인증·인가 심화, 시크릿 관리, 보안 점검 루틴", "서비스가 실제 사용자를 받기 시작할 때"),
    ("perf-adv", "성능·스케일 고급 가이드", "병목 진단, 캐싱 전략, 부하 테스트, 수평·수직 확장", "트래픽이 늘어나는 게 눈에 보일 때"),
    ("leadership-adv", "기술 리더십·레거시 마이그레이션 가이드", "기술 의사결정, ADR, 팀 성장, 레거시 코드 단계적 전환", "기술 결정을 직접 내려야 하는 위치가 됐을 때"),
    ("ai-adv", "생성형 AI 고급 가이드", "멀티 에이전트 오케스트레이션, 자체 모델 서빙, 대규모 평가·모니터링", "AI 기능 하나로는 부족해졌을 때"),
]

DASHBOARD_CARDS_ADV = [
    "system-design-adv", "cloud-adv", "db-adv", "security-adv",
    "perf-adv", "leadership-adv", "ai-adv",
]

OVERVIEW_ROWS_CERT = [
    ("csts", "CSTS 대비 가이드", "테스트 원칙, V-모델, 테스트 설계 기법, 결함 관리 프로세스", "테스트 코드는 짜봤지만 이론으로도 검증받고 싶을 때"),
    ("sqld", "SQLD 대비 가이드", "데이터 모델링, SQL 기본·활용, 자주 나오는 함정 포인트", "SQL은 짤 줄 아는데 SQLD를 준비할 때"),
    ("adsp", "ADSP 대비 가이드", "데이터 이해, 분석 기획, 통계·분석 기법 개요", "데이터 분석 기초를 자격증으로 검증하고 싶을 때"),
    ("infoproc", "정보처리기사 대비 가이드", "소프트웨어 설계·개발, DB 구축, 프로그래밍 언어 활용, 정보시스템 구축관리", "국내에서 널리 알려진 국가기술자격을 준비할 때"),
    ("infosec", "정보보안기사·산업기사 대비 가이드", "시스템·네트워크·애플리케이션 보안, 정보보안 관리", "보안 심화 가이드로 개념을 잡은 뒤 자격증까지 노릴 때"),
    ("aws-cert", "AWS 클라우드 자격증 대비 가이드", "EC2·S3·IAM·VPC 핵심 개념, Well-Architected Framework 개요", "클라우드·IaC 가이드를 실제 자격증으로 검증하고 싶을 때"),
]

DASHBOARD_CARDS_CERT = [
    "csts", "sqld", "adsp", "infoproc", "infosec", "aws-cert",
]

def render_card_grid(keys=None, data=None):
    keys = DASHBOARD_CARDS if keys is None else keys
    data = OVERVIEW_ROWS if data is None else data
    cards = []
    for key in keys:
        p = PAGES_BY_KEY[key]
        desc = next((learn for k, _, learn, _ in data if k == key), "")
        who = next((who for k, _, _, who in data if k == key), "")
        who_html = '<div class="study-card-who">💡 %s</div>' % html.escape(who) if who else ""
        cards.append(
            '<a class="study-card" href="%s" style="--card-accent: var(--cat-%s);">'
            '<span class="study-card-icon">%s</span>'
            '<div class="study-card-title">%s</div>'
            '<div class="study-card-desc">%s</div>'
            "%s"
            '<span class="study-card-tag">%s →</span></a>'
            % (url_of(key), p["cat"], p["icon"], html.escape(p["title"]), html.escape(desc), who_html, html.escape(CAT_LABEL.get(p["cat"], "")))
        )
    return '<div class="card-grid">%s</div>' % "".join(cards)


DASHBOARD_TMPL = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>개발 공부 가이드 · 개발 학습·실전 노트</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%F0%9F%8C%B1%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="assets/style.css?v={asset_v}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="개발 공부 가이드">
<meta property="og:title" content="개발 공부 가이드 · 개발 학습·실전 노트">
<meta property="og:description" content="{intro}">
<meta property="og:url" content="{og_url}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="개발 공부 가이드 · 개발 학습·실전 노트">
<meta name="twitter:description" content="{intro}">
<script src="assets/search-index.js?v={asset_v}" defer></script>
</head>
<body data-root-prefix="">
<div id="reading-progress"></div>
<header class="site-header">
  <div class="header-inner">
    <button class="menu-btn" type="button" aria-label="메뉴" style="visibility:hidden;">☰</button>
    <a class="brand" href="index.html">개발 공부 가이드</a>
    <nav class="breadcrumb"><span class="current">학습 대시보드</span></nav>
    <div class="header-actions">
      <div class="search-box-desktop"><span>🔍</span><input type="text" placeholder="검색 (Ctrl+K)" readonly></div>
      <a class="guestbook-btn" href="방명록.html">💬 <span class="guestbook-btn-label">방명록</span></a>
      <button class="search-btn" type="button" aria-label="검색">🔍</button>
      <button class="theme-btn" type="button" aria-label="다크모드 전환">🌙</button>
    </div>
  </div>
</header>
{tier_nav}
<div class="page-shell">
  <div class="dashboard-shell">
    <div class="dashboard-intro">
      <h1 class="dashboard-title">개발 공부 가이드</h1>
      <p class="dashboard-desc">{intro}</p>
    </div>

    <div class="stat-strip">
      <a class="stat-item" href="#tier-beginner"><div class="stat-num">{n_beginner}</div><div class="stat-label">🔰 초급</div></a>
      <a class="stat-item" href="#tier-mid"><div class="stat-num">{n_mid}</div><div class="stat-label">📈 중급</div></a>
      <a class="stat-item" href="#tier-adv"><div class="stat-num">{n_adv}</div><div class="stat-label">🏔️ 고급</div></a>
      <a class="stat-item" href="#tier-cert"><div class="stat-num">{n_cert}</div><div class="stat-label">🏅 자격증</div></a>
      <a class="stat-item" href="#tier-misc"><div class="stat-num">{n_misc}</div><div class="stat-label">🎈 기타</div></a>
      <div class="stat-item stat-item-total"><div class="stat-num">{n_total}</div><div class="stat-label">전체 학습 자료</div></div>
    </div>

    <div class="section-heading" style="margin-top:28px;">📰 오늘의 개발 소식</div>
    <p class="dashboard-desc" style="margin-bottom:12px;">GeekNews 최신 글을 매일 자동으로 가져옵니다(자소설닷컴은 공식 피드가 없어 자동 갱신 대신 바로가기만 제공합니다).</p>
    <div id="news-feed" class="news-feed" data-src="assets/news-feed.json">
      <div class="news-feed-loading">불러오는 중…</div>
    </div>
    <a class="news-static-link" href="https://www.jasoseol.com" target="_blank" rel="noopener">🔗 자소설닷컴 바로가기 — 채용공고·자소서·면접 후기 커뮤니티</a>

    <a class="hero-cta" href="{first_steps_url}">
      <span class="hero-cta-text">프로그래밍이 뭔지, 프론트/백엔드가 뭔지도 잘 모르겠어요 🌱 — <strong>웹 서비스 하나가 어떻게 구성되는지</strong>부터 5~10분 만에 큰 그림 잡고 싶다면?</span>
      <span class="hero-cta-btn">🗺️ 개발 전체 지도부터 보기 →</span>
    </a>

    <a class="hero-cta" href="{git_min_url}">
      <span class="hero-cta-text">개발 흐름은 대충 아는데 Git만 몰라요 😭 — <strong>branch가 뭔지, commit이 뭔지</strong>부터 5분 만에 정리하고 싶다면?</span>
      <span class="hero-cta-btn">🔰 Git 최소 기초부터 시작하기 →</span>
    </a>

    <a class="hero-cta" href="{level_guide_url}">
      <span class="hero-cta-text">나는 초급·중급·고급 중 <strong>어디부터 봐야 할지</strong> 잘 모르겠다면?</span>
      <span class="hero-cta-btn">🧭 등급별 시작 기준 확인하기 →</span>
    </a>

    <div class="section-heading" id="tier-beginner">🔰 초급 학습 자료</div>
    {card_grid}

    <div class="section-heading" id="tier-mid" style="margin-top:40px;">📈 중급 학습 자료</div>
    <p class="dashboard-desc" style="margin-bottom:20px;">기초 가이드로 혼자 힘으로 동작하는 앱을 만들 수 있게 됐다면, 다음은 실무에서 부딪히는 문제를 다루는 <a href="{mid_hub_url}">중급 가이드</a>로 이어집니다.</p>
    {mid_card_grid}

    <div class="section-heading" id="tier-adv" style="margin-top:40px;">🏔️ 고급 학습 자료</div>
    <p class="dashboard-desc" style="margin-bottom:20px;">중급 가이드로 실무 문제를 다룰 수 있게 됐다면, 다음은 설계 판단과 팀 전체 관점을 다루는 <a href="{adv_hub_url}">고급 가이드</a>로 이어집니다.</p>
    {adv_card_grid}

    <div class="section-heading" id="tier-cert" style="margin-top:40px;">🏅 자격증 대비</div>
    <p class="dashboard-desc" style="margin-bottom:20px;">개발 실력과는 별개로, 공식적으로 검증받고 싶을 때 참고하는 <a href="{cert_hub_url}">자격증 대비 가이드</a>입니다. 연습문제는 직접 만든 것으로 실제 기출문제가 아니며, 진짜 기출은 각 문서 끝의 공식 링크를 이용하세요.</p>
    {cert_card_grid}

    <div class="section-heading" id="tier-misc" style="margin-top:40px;">🎈 기타 — 가볍게 보기</div>
    <p class="dashboard-desc" style="margin-bottom:20px;">학습 필수는 아니지만 재미로, 또는 요즘 트렌드가 궁금해서 보면 좋은 문서들입니다.</p>
    {misc_card_grid}

    <div class="dashboard-footer">🐣 미리가 미리미리 만든 개발 공부 가이드 · 연호·이현이의 프롬프트 한 스푼 — 계속 업데이트되고 있습니다.</div>
  </div>
</div>
<div class="search-overlay" id="search-overlay">
  <div class="search-panel">
    <input type="text" id="search-input" placeholder="키워드로 검색 — 유사어도 함께 찾아요 (예: 로그인, 머지, 상태)">
    <div class="search-results" id="search-results"></div>
  </div>
</div>
<script src="assets/search-core.js?v={asset_v}" defer></script>
<script src="assets/main.js?v={asset_v}" defer></script>
</body>
</html>
"""


def build_dashboard():
    n_beginner = len(DASHBOARD_CARDS)
    n_mid = len(DASHBOARD_CARDS_MID)
    n_adv = len(DASHBOARD_CARDS_ADV)
    n_cert = len(DASHBOARD_CARDS_CERT)
    n_misc = len(DASHBOARD_CARDS_MISC)
    html_out = DASHBOARD_TMPL.format(
        intro=html.escape(DASHBOARD_INTRO),
        n_beginner=n_beginner,
        n_mid=n_mid,
        n_adv=n_adv,
        n_cert=n_cert,
        n_misc=n_misc,
        n_total=n_beginner + n_mid + n_adv + n_cert + n_misc,
        asset_v=ASSET_VERSION,
        tier_nav=render_tier_nav("index"),
        first_steps_url=url_of("first-steps"),
        git_min_url=url_of("git-min"),
        level_guide_url=url_of("playbook-hub") + "#나는-어디부터-봐야-하나-등급별-시작-기준",
        card_grid=render_card_grid(),
        mid_card_grid=render_card_grid(DASHBOARD_CARDS_MID, OVERVIEW_ROWS_MID),
        mid_hub_url=url_of("mid-hub"),
        adv_card_grid=render_card_grid(DASHBOARD_CARDS_ADV, OVERVIEW_ROWS_ADV),
        adv_hub_url=url_of("adv-hub"),
        cert_card_grid=render_card_grid(DASHBOARD_CARDS_CERT, OVERVIEW_ROWS_CERT),
        cert_hub_url=url_of("cert-hub"),
        misc_card_grid=render_card_grid(DASHBOARD_CARDS_MISC, OVERVIEW_ROWS_MISC),
        og_url=SITE_BASE_URL,
    )
    (ROOT / "index.html").write_text(html_out, encoding="utf-8")


# ==========================================================================
# 8-1. 방명록 (giscus — GitHub Discussions 기반)
# ==========================================================================
GISCUS_REPO = "MiriKim79/dev-study-notes"
GISCUS_REPO_ID = "R_kgDOTx7W7g"
GISCUS_CATEGORY = "General"
GISCUS_CATEGORY_ID = "DIC_kwDOTx7W7s4DDgCF"
GISCUS_TERM = "방명록"

GUESTBOOK_TMPL = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>방명록 · 개발 학습·실전 노트</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%F0%9F%8C%B1%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="assets/style.css?v={asset_v}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="개발 공부 가이드">
<meta property="og:title" content="방명록 · 개발 학습·실전 노트">
<meta property="og:description" content="공부하다 막힌 부분, 하고 싶은 말, 응원 한마디 — 자유롭게 남겨주세요.">
<meta property="og:url" content="{og_url}">
<script src="assets/search-index.js?v={asset_v}" defer></script>
</head>
<body data-root-prefix="">
<div id="reading-progress"></div>
<header class="site-header">
  <div class="header-inner">
    <button class="menu-btn" type="button" aria-label="메뉴" style="visibility:hidden;">☰</button>
    <a class="brand" href="index.html">개발 공부 가이드</a>
    <nav class="breadcrumb"><a href="index.html">대시보드</a> <span>›</span><span class="current">방명록</span></nav>
    <div class="header-actions">
      <div class="search-box-desktop"><span>🔍</span><input type="text" placeholder="검색 (Ctrl+K)" readonly></div>
      <a class="guestbook-btn" href="방명록.html">💬 <span class="guestbook-btn-label">방명록</span></a>
      <button class="search-btn" type="button" aria-label="검색">🔍</button>
      <button class="theme-btn" type="button" aria-label="다크모드 전환">🌙</button>
    </div>
  </div>
</header>
{tier_nav}
<div class="page-shell">
  <div class="layout no-sidebar">
    <main class="main-content">
      <div class="doc-inner" style="--card-accent: var(--cat-start);">
        <span class="page-kicker">💬 방명록</span>
        <h1 class="page-title">방명록 & 피드백</h1>
        <p class="page-tagline">오타 제보, 이해 안 되는 설명, 응원 한마디까지 뭐든 좋아요. GitHub 계정으로 로그인하면 남길 수 있어요 (스팸 방지용) — 댓글에는 미리가 직접 답장합니다.</p>
        <div id="giscus-comments"></div>
      </div>
    </main>
  </div>
</div>
<div class="search-overlay" id="search-overlay">
  <div class="search-panel">
    <input type="text" id="search-input" placeholder="키워드로 검색 — 유사어도 함께 찾아요 (예: 로그인, 머지, 상태)">
    <div class="search-results" id="search-results"></div>
  </div>
</div>
<script src="assets/search-core.js?v={asset_v}" defer></script>
<script src="assets/main.js?v={asset_v}" defer></script>
<script>
  (function () {{
    var script = document.createElement("script");
    script.src = "https://giscus.app/client.js";
    script.setAttribute("data-repo", "{giscus_repo}");
    script.setAttribute("data-repo-id", "{giscus_repo_id}");
    script.setAttribute("data-category", "{giscus_category}");
    script.setAttribute("data-category-id", "{giscus_category_id}");
    script.setAttribute("data-mapping", "specific");
    script.setAttribute("data-term", "{giscus_term}");
    script.setAttribute("data-strict", "0");
    script.setAttribute("data-reactions-enabled", "1");
    script.setAttribute("data-emit-metadata", "0");
    script.setAttribute("data-input-position", "top");
    script.setAttribute("data-lang", "ko");
    var savedTheme = localStorage.getItem("dev-notes-theme");
    var isDark = savedTheme === "dark" || (!savedTheme && window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches);
    script.setAttribute("data-theme", isDark ? "dark_dimmed" : "light");
    script.crossOrigin = "anonymous";
    script.async = true;
    document.getElementById("giscus-comments").appendChild(script);

    // 사이트 다크모드 버튼과 giscus 테마를 함께 전환
    var themeBtn = document.querySelector(".theme-btn");
    if (themeBtn) {{
      themeBtn.addEventListener("click", function () {{
        setTimeout(function () {{
          var nowDark = document.documentElement.getAttribute("data-theme") === "dark" ||
            (!document.documentElement.getAttribute("data-theme") && window.matchMedia("(prefers-color-scheme: dark)").matches);
          var frame = document.querySelector("iframe.giscus-frame");
          if (frame) {{
            frame.contentWindow.postMessage(
              {{ giscus: {{ setConfig: {{ theme: nowDark ? "dark_dimmed" : "light" }} }} }},
              "https://giscus.app"
            );
          }}
        }}, 50);
      }});
    }}
  }})();
</script>
</body>
</html>
"""


def build_guestbook():
    html_out = GUESTBOOK_TMPL.format(
        asset_v=ASSET_VERSION,
        tier_nav=render_tier_nav("guestbook"),
        og_url=SITE_BASE_URL + "방명록.html",
        giscus_repo=GISCUS_REPO,
        giscus_repo_id=GISCUS_REPO_ID,
        giscus_category=GISCUS_CATEGORY,
        giscus_category_id=GISCUS_CATEGORY_ID,
        giscus_term=GISCUS_TERM,
    )
    (ROOT / "방명록.html").write_text(html_out, encoding="utf-8")


NOT_FOUND_TMPL = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>404 · 이 문서는 아직 안 배웠습니다 · 개발 학습·실전 노트</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%F0%9F%8C%B1%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="assets/style.css?v={asset_v}">
</head>
<body data-root-prefix="">
<header class="site-header">
  <div class="header-inner">
    <button class="menu-btn" type="button" aria-label="메뉴" style="visibility:hidden;">☰</button>
    <a class="brand" href="index.html">개발 공부 가이드</a>
    <nav class="breadcrumb"><span class="current">404</span></nav>
  </div>
</header>
<div class="page-shell">
  <div class="layout no-sidebar">
    <main class="main-content">
      <div class="doc-inner" style="text-align:center; padding-top:60px; padding-bottom:60px;">
        <div style="font-size:52px; margin-bottom:8px;">🤔</div>
        <h1 class="page-title">404 — 이 문서는 아직 안 배웠습니다</h1>
        <p class="page-tagline" style="max-width:520px; margin:12px auto 28px;">
          찾으시는 페이지가 없거나 주소가 바뀌었어요. 링크가 오래됐을 수도 있고, 아니면 그냥 존재하지 않는 URL일 수도 있습니다 — 404도 결국 서버가 "그런 리소스 없음"이라고 정확하게 응답한 것뿐이에요.
        </p>
        <a class="hero-cta-btn" href="index.html" style="display:inline-block; text-decoration:none;">🏠 학습 대시보드로 돌아가기</a>
      </div>
    </main>
  </div>
</div>
<script src="assets/search-core.js?v={asset_v}" defer></script>
<script src="assets/main.js?v={asset_v}" defer></script>
</body>
</html>
"""


def build_404():
    html_out = NOT_FOUND_TMPL.format(asset_v=ASSET_VERSION)
    (ROOT / "404.html").write_text(html_out, encoding="utf-8")


# ==========================================================================
# 9. 실행 진입점
# ==========================================================================
def main():
    all_search_entries = []
    for page in PAGES:
        entries, _toc = build_content_page(page)
        all_search_entries.extend(entries)
        print("생성:", page["src"][:-3] + ".html")

    build_dashboard()
    print("생성: index.html")

    build_guestbook()
    print("생성: 방명록.html")

    build_404()
    print("생성: 404.html")

    assets_dir = ROOT / "assets"
    assets_dir.mkdir(exist_ok=True)
    search_js = "window.SEARCH_INDEX = " + json.dumps(all_search_entries, ensure_ascii=False) + ";\n"
    (assets_dir / "search-index.js").write_text(search_js, encoding="utf-8")
    print("생성: assets/search-index.js (%d개 항목)" % len(all_search_entries))

    print("\n총 %d개 HTML 생성 완료." % (len(PAGES) + 3))


if __name__ == "__main__":
    main()
