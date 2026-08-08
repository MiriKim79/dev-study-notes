> **용도:** 새 팀 프로젝트를 시작할 때 저장소에 복사해서 쓰는 협업 문서 템플릿입니다.  
> **핵심:** 이 문서들은 “정답 규칙”이 아니라 **이번 프로젝트가 실제로 쓸 규칙을 명시하는 틀**입니다. 팀 상황이 다르면 **개발 협업 방식 선택 가이드**를 보고 브랜치·리뷰 방식을 바꿉니다.

---

# 사용 순서

1. **팀 협업 방식을 먼저 정합니다.**
   - `main + develop + 기능 브랜치`를 쓸지
   - `main + 기능 브랜치`만 쓸지
   - PR 승인 수, merge 방식, Issue 사용 여부를 정합니다.

2. 아래 문서의 `{{자리표시자}}`를 실제 프로젝트 값으로 바꿉니다.
   - **팀 GitHub 협업 규칙 (CONTRIBUTING.md)**
   - **AI 코딩 에이전트 작업 규칙 (AGENTS.md)**
   - **Claude Code 작업 규칙 (CLAUDE.md)** — Claude Code를 쓰는 경우
   - **기획·API·일정 템플릿 (PLANNING.md)**

3. 저장소에는 보통 다음처럼 둡니다.

```text
project-root/
├─ README.md
├─ AGENTS.md
├─ CLAUDE.md                  # Claude Code 사용 시
├─ CONTRIBUTING.md
├─ docs/
│  └─ PLANNING.md
└─ .github/
   ├─ pull_request_template.md
   └─ ISSUE_TEMPLATE/
      ├─ feature.md
      └─ bug.md
```

4. 팀원 모두가 문서를 한 번 읽고 **실제로 지킬 규칙만 남깁니다.**

5. GitHub 저장소 설정도 문서와 맞춥니다.
   - default branch
   - 허용 merge 방식
   - branch protection/ruleset 가능 여부
   - Collaborator/Team 권한

---

# 포함된 문서

| 문서 | 역할 | 주로 읽는 사람 |
| --- | --- | --- |
| **팀 GitHub 협업 규칙 (CONTRIBUTING.md)** | 브랜치, 커밋, Issue, PR, 리뷰, 코드 소유권 규칙 | 팀원 전원 |
| **AI 코딩 에이전트 작업 규칙 (AGENTS.md)** | AI 코딩 도구가 저장소에서 지켜야 할 압축 규칙 | 지원하는 AI 코딩 도구 + 사람 |
| **Claude Code 작업 규칙 (CLAUDE.md)** | Claude Code에만 필요한 추가 지침 | Claude Code |
| **기획·API·일정 템플릿 (PLANNING.md)** | 요구사항, 화면, API, ERD, 일정, 결정사항 | 팀원 전원 |
| **Issue·PR 템플릿 예시** | 작업 요청과 리뷰 내용을 일정한 형식으로 작성 | 팀원 전원 |

---

# AGENTS.md에 대한 주의

`AGENTS.md`를 자동으로 읽는지, 어느 범위까지 적용하는지는 **AI 코딩 도구마다 다릅니다.** 지원하는 도구에서는 자동 지침으로 활용할 수 있지만, 모든 도구가 같은 방식으로 읽는다고 가정하지 않습니다.

따라서:

- Claude Code는 `CLAUDE.md`에서 `AGENTS.md`를 참조하도록 구성
- 다른 AI 코딩 도구는 해당 도구의 공식 지침 파일 지원 여부 확인
- 중요한 규칙은 사람도 `CONTRIBUTING.md`에서 확인 가능하게 유지

AI 도구에만 규칙을 넣고 사람용 문서를 없애지 않습니다.

---

# 핵심 원칙

- **AI용 지침은 짧고 명확하게** 작성합니다.
- 규칙마다 가능하면 **올바른 예시**를 붙입니다.
- 금지사항은 추론에 맡기지 말고 명시합니다.
- FE/BE/AI의 **분업 경계와 API 계약**을 적습니다.
- 새 패키지·DB 구조·API 계약 변경은 팀 합의가 필요한지 적습니다.
- `.env`, 토큰, 비밀번호, 클라우드 키는 어떠한 템플릿에도 실제 값을 넣지 않습니다.
- AI가 만든 커밋·PR도 **사람이 만든 코드와 같은 리뷰 기준**을 적용합니다.

---

# GitHub Free 저장소에서 주의할 점

GitHub의 보호 브랜치 기능은 플랜과 저장소 공개 범위에 따라 사용 가능 범위가 달라질 수 있습니다. 현재 GitHub 문서 기준으로 **public repository는 GitHub Free에서도 보호 브랜치를 사용할 수 있고, private repository의 보호 브랜치는 Pro/Team/Enterprise 계열에서 제공**됩니다.

따라서 private Free 저장소에서 보호 규칙을 강제할 수 없다면:

1. `main`/`develop` 직접 push 금지
2. PR을 통해서만 머지
3. 팀원 1명 이상 확인
4. force push 금지

를 팀 규칙으로 명시합니다.

기능 제공 범위는 바뀔 수 있으므로 새 프로젝트를 시작할 때 GitHub 공식 문서를 다시 확인합니다.

---

# 새 프로젝트 세팅 체크리스트

- [ ] 저장소 생성
- [ ] 팀원 초대
- [ ] default branch 결정
- [ ] 브랜치 전략 결정
- [ ] `CONTRIBUTING.md` 작성
- [ ] `AGENTS.md` 작성
- [ ] 필요하면 `CLAUDE.md` 작성
- [ ] `docs/PLANNING.md` 작성
- [ ] `.gitignore` 확인
- [ ] `.env.example` 작성
- [ ] Issue 템플릿 추가
- [ ] PR 템플릿 추가
- [ ] 허용 merge 방식 설정
- [ ] branch protection/ruleset 가능 여부 확인
- [ ] 팀원 모두 로컬 실행 성공 확인
