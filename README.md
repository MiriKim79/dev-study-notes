# 🌱 개발 공부 가이드 (dev-study-notes)

> 개발을 처음 공부하는 사람부터 중급·고급 학습자까지, **잘못된 내용을 배우지 않고** 단계적으로 공부할 수 있는 개발 학습 가이드입니다.

[![GitHub Pages](https://img.shields.io/badge/site-live-4F7DF3?style=flat-square&logo=github)](https://mirikim79.github.io/dev-study-notes/)
[![문서 수](https://img.shields.io/badge/문서-40개+-4F7DF3?style=flat-square)](https://mirikim79.github.io/dev-study-notes/)
[![빌드](https://img.shields.io/badge/build-Python%20표준%20라이브러리만-4F7DF3?style=flat-square&logo=python)](build_site.py)
[![라이선스](https://img.shields.io/badge/license-학습%20자료-4F7DF3?style=flat-square)](#)

**👉 [지금 바로 보러 가기](https://mirikim79.github.io/dev-study-notes/)**

---

## 이게 뭔가요?

Git을 오늘 처음 들어본 사람도, 실무에서 캐싱·N+1·MSA 트레이드오프를 판단해야 하는 사람도 같은 사이트 안에서 자기 단계에 맞는 문서를 찾을 수 있게 만든 개발 학습 자료 모음입니다.

- 🔰 **초급** — 개발이 뭔지도 모르는 완전 초보자부터 팀 프로젝트를 처음 시작하는 사람까지
- 📈 **중급** — 기초는 뗐고, 실무에서 부딪히는 문제(캐시, N+1, 성능, 테스트, CI/CD)를 다루고 싶은 사람
- 🏔️ **고급** — 기술 이름을 아는 것보다 "언제, 왜 써야 하는가"라는 트레이드오프 판단이 필요한 사람
- 🏅 **자격증 대비** — SQLD, ADsP, 정보처리기사, 정보보안기사·산업기사, AWS 자격증, CSTS

## 이 사이트가 지키려는 원칙

- **"항상/반드시/무조건" 같은 단정은 예외가 있는지부터 검증한다.** 기술적 사실은 공식 문서를 우선 근거로 삼습니다.
- **초보자용 단순화 때문에 잘못된 mental model을 만들지 않는다.** 쉽게 설명하되 틀리게 설명하지 않습니다.
- **기술은 필요할 때 선택하는 도구다.** RAG, MSA, Kubernetes 같은 기술을 "고급이면 당연히 쓰는 것"처럼 다루지 않습니다.
- **버전에 따라 달라질 수 있는 내용(모델 ID, 자격증 시행기관, API 문법 등)은 주기적으로 재검증합니다.**

## 폴더 구조

```
develop_guide/
├── index.html                      # 학습 대시보드 (build_site.py가 생성)
├── build_site.py                   # .md → 학습용 HTML 변환 스크립트 (표준 라이브러리만 사용)
├── verify_site.py                  # 원본 .md ↔ 생성 HTML 정합성 검사
├── 개발 기초·실전 가이드/            # 🔰 초급 — Git, 프론트/백엔드 기초, 팀 개발 시작, 생성형 AI 기초
├── 개발 중급 가이드/                 # 📈 중급 — Git·프론트·백엔드·TS·DB·테스트·CI/CD·AI·협업
├── 개발 고급 가이드/                 # 🏔️ 고급 — 시스템 설계, 클라우드, 보안, 성능, 리더십, 생성형 AI
├── 자격증 대비/                      # 🏅 SQLD·ADsP·정보처리기사·정보보안기사·AWS·CSTS
├── GitHub 팀 협업 템플릿/            # CONTRIBUTING·AGENTS·CLAUDE·PLANNING·이슈/PR 템플릿 예시
└── assets/                          # 스타일시트·스크립트·검색 인덱스
```

각 폴더의 `.md` 파일이 원본입니다. **`.html`은 전부 `build_site.py`가 자동 생성**하므로 직접 수정하지 않습니다.

## 로컬에서 빌드하기

```bash
python build_site.py     # .md → .html 재생성 (외부 라이브러리 불필요)
python verify_site.py    # 원본과 생성 결과가 어긋나지 않았는지 확인
```

## 기여 / 오타 제보

사이트 하단 [방명록](https://mirikim79.github.io/dev-study-notes/방명록.html)에 GitHub 계정으로 남겨주시면 확인 후 반영합니다.

---

<sub>🐣 미리가 미리미리 만든 개발 공부 가이드. 계속 업데이트되고 있습니다.</sub>
