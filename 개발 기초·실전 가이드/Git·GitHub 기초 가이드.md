> **대상:** [Git·GitHub 진짜 최소 기초](Git·GitHub%20진짜%20최소%20기초.html)로 8단계 흐름을 감 잡은 사람  
> **목적:** 실제 팀 프로젝트를 하다 보면 곧 필요해지는 것 — 인증 설정, `.gitignore`, 자주 쓰는 명령어, 충돌 해결, 되돌리기  
> **사용법:** 위에서 아래로 한 번 읽으면 끝나게 구성했습니다. `HEAD`, `fetch`, `rebase`, `tag` 같은 더 깊은 내용은 여기서 다루지 않고 [Git·GitHub 중급 가이드](../개발%20중급%20가이드/Git·GitHub%20중급%20가이드.html)로 미룹니다.
---

# 0. 시작 전에 — 이 문서에서 쓰는 용어

| 용어 | 쉬운 설명 |
| --- | --- |
| 저장소(Repository) | 프로젝트 파일과 변경 기록이 저장되는 공간. 로컬(내 컴퓨터)과 원격(GitHub)으로 나뉜다. |
| 스테이징 영역 | 다음 commit에 포함할 변경사항을 미리 담아두는 대기 공간. `git add`로 여기에 올린다. |
| origin | 원격 저장소(대부분 GitHub 주소)를 가리키는 기본 별칭. |
| PAT (Personal Access Token) | HTTPS 인증에 쓰는 개인 토큰. 비밀번호처럼 비밀로 관리한다. |

---

# 1. 개발 환경 준비

* **Git 설치**: 공식 사이트에서 다운로드해 기본값으로 설치.
* **GitHub 계정**: 회원가입 후 저장소를 만들거나 초대받아 사용.
* **에디터**: VS Code 등 무엇이든 Git과 연동해 쓸 수 있습니다.

```bash
git config --global user.name "이름"
git config --global user.email "이메일"
```

이 설정이 앞으로 만드는 모든 commit에 "누가 만들었는지"로 기록됩니다.

---

# 2. GitHub 인증 — clone·push가 안 될 때

`clone`/`push`할 때 GitHub가 "너 정말 이 계정 맞아?"를 확인하는 절차입니다. 초보자에게는 **HTTPS + PAT** 조합이 가장 단순합니다.

```bash
gh auth login
```

GitHub CLI(`gh`)로 로그인하면 이후 `git push`할 때 별도 설정 없이 인증됩니다. `gh`를 안 쓴다면, GitHub 설정에서 **Personal Access Token(PAT)**을 발급받아 비밀번호 대신 입력합니다.

**PAT 주의점**: 비밀번호처럼 취급하고, 코드나 `.env`, 커밋 메시지에 남기지 않습니다. 노출되면 즉시 폐기하고 재발급합니다.

(SSH 키 방식도 있지만, 처음에는 HTTPS+PAT로 충분합니다. SSH는 [Git·GitHub 중급 가이드](../개발%20중급%20가이드/Git·GitHub%20중급%20가이드.html)에서 다룹니다.)

---

# 3. `.gitignore` — 이 파일들은 Git에 올리지 않기

`node_modules`, `.env`(비밀번호·API 키), 캐시 파일처럼 Git이 **추적하지 않을 파일**을 지정합니다. 프로젝트 시작할 때 바로 만드는 게 좋습니다.

```gitignore
node_modules/
.env
__pycache__/
*.log
dist/
```

**주의**: `.gitignore`는 *이미* Git이 추적 중인 파일을 자동으로 빼주지 않습니다. `.env`를 실수로 이미 commit했다면:

```bash
git rm --cached .env
```

로 추적만 해제하고, 그 뒤 `.gitignore`에 등록합니다. 만약 API 키·비밀번호가 이미 GitHub에 push까지 됐다면, `.gitignore`로는 부족합니다 — **그 키는 이미 노출된 것으로 보고 즉시 폐기하고 새로 발급**해야 합니다.

---

# 4. 자주 쓰는 명령어

| 명령어 | 언제 쓰나 |
| --- | --- |
| `git status` | 지금 뭐가 바뀌었는지, 뭐가 스테이징됐는지 확인할 때 |
| `git add <파일>` | 특정 파일만 다음 commit에 포함시킬 때 |
| `git add .` | 지금까지 바뀐 걸 전부 포함시킬 때 (commit 전에 `git status`로 뭐가 담겼는지 확인하는 습관을 들이세요) |
| `git commit -m "메시지"` | 스테이징된 변경을 하나의 기록으로 남길 때 |
| `git log --oneline` | 지금까지의 commit 기록을 간단히 볼 때 |
| `git switch <branch>` | 다른 branch로 옮겨갈 때 |
| `git switch -c <새branch>` | 새 branch를 만들면서 바로 옮겨갈 때 |
| `git restore <파일>` | commit 안 한 수정을 취소하고 원래대로 되돌릴 때 |
| `git push -u origin <branch>` | 새로 만든 branch를 GitHub에 처음 올릴 때 (`-u`를 한 번 붙여두면 다음부터는 `git push`만 써도 됨) |

---

# 5. 되돌리기

| 상황 | 명령어 |
| --- | --- |
| commit 안 한 파일 수정을 취소하고 싶다 | `git restore <파일>` |
| add까지만 했는데 취소하고 싶다 | `git restore --staged <파일>` |
| 방금 commit한 걸 취소하고 싶다 (아직 push 전) | `git reset HEAD~1` |
| 이미 push까지 한 commit을 취소하고 싶다 | `git revert <커밋ID>` |

**핵심만 기억하세요**: 아직 나만 보는 commit(push 전)은 `reset`으로 지워도 괜찮지만, **이미 push해서 팀원도 보고 있는 commit은 `reset`으로 지우지 말고 `revert`를 씁니다.** `revert`는 이력을 지우는 대신 "이걸 취소한다"는 새 commit을 추가하는 방식이라, 팀원의 기록과 어긋나지 않습니다.

---

# 6. 충돌(conflict) 제대로 해결하기

[최소 기초 문서](Git·GitHub%20진짜%20최소%20기초.html)에서 충돌이 뭔지 감을 잡았다면, 실제로 겪었을 때 확인할 순서입니다.

### pull이 "local changes가 덮어써진다"며 막힐 때

commit하지 않은 내 수정이 남아있어서입니다. 셋 중 하나를 고르세요.

```text
A. 지금까지 작업이 의미 있으면 → 먼저 commit
B. 잠깐 치워두고 싶으면 → git stash (임시 보관함에 넣어두기)
C. 필요 없는 수정이면 → git restore <파일>로 되돌리기
```

### 충돌 표시가 나타났을 때

```text
<<<<<<< HEAD
내 코드
=======
팀원의 코드
>>>>>>> 팀원의 브랜치
```

1. 두 코드를 읽고 어떤 걸 남길지(또는 합칠지) 정합니다.
2. `<<<<<<<`/`=======`/`>>>>>>>` 표시를 전부 지우고, 최종 코드만 남깁니다.
3. 실행해서 제대로 동작하는지 확인합니다.
4. `git add <파일>` → `git commit`으로 마무리합니다.

**시작을 잘못했다면** `git merge --abort`로 충돌 이전 상태로 되돌아갈 수 있습니다.

같은 파일이라도 서로 다른 줄을 고쳤다면 Git이 자동으로 합쳐주기도 합니다 — 충돌은 "같은 파일"이 아니라 "같은 부분"을 다르게 고쳤을 때만 일어납니다.

---

# 7. branch 이름 규칙과 팀 저장소 운영

branch 이름(`feature/*`, `bugfix/*` 등)과 팀 저장소를 어떻게 꾸릴지(개인 저장소+Collaborator, Organization, Fork 등)는 **Git 자체 규칙이 아니라 팀마다 정하는 것**입니다. 이 사이트에서는 두 가지로 따로 다룹니다.

```
개발 협업 방식 선택 가이드 → 어떤 브랜치 전략을 쓸지 비교·선택
팀 GitHub 협업 규칙 (CONTRIBUTING.md) → 우리 팀이 채택한 규칙을 확정해서 적어두는 문서
```

새 프로젝트에 들어가면 이 두 문서(또는 팀의 실제 CONTRIBUTING.md)부터 확인하세요.

---

# 8. 자주 하는 실수

* `.env`·토큰·키 파일을 `.gitignore` 설정 전에 먼저 commit해버림
* 팀 공용 branch(`main`)에서 바로 작업하고 commit함
* `git reset`으로 이미 push된 commit을 지워버림 (→ `revert`를 썼어야 함)
* PAT를 코드나 커밋 메시지에 그대로 남김
* 의미 없는 커밋 메시지("수정", "ㅇㅇ")로 commit

---

# 9. 직접 실습해보기

연습용 저장소나 새로 만든 빈 저장소에서 아래를 순서대로 해봅니다.

```bash
git clone <저장소주소>
cd <폴더>
git status

git switch -c feat/practice
echo "test" >> practice.txt
git add practice.txt
git status
git commit -m "연습: 파일 추가"
git push -u origin feat/practice
```

이후 GitHub 웹사이트에서 PR을 직접 만들어봅니다.

```bash
git add practice.txt
git restore --staged practice.txt
```

파일 내용은 그대로 남고 staging만 풀리는지 확인해보세요.

```bash
git stash
git status
git stash pop
```

작업을 잠깐 치웠다가(`stash`) 다시 꺼내는(`pop`) 흐름도 한 번 해보세요.

<details class="quiz-answer">
<summary>정답 확인</summary>
<div class="quiz-answer-body">
<p>아래 항목을 스스로 체크해보세요. 전부 "예"라면 이 문서를 제대로 끝낸 것입니다.</p>
<ul>
<li>&#9744; <code>git add</code>는 로컬 스테이징에만 올리는 것이고, GitHub에 올라가는 건 <code>git push</code>뿐이라고 설명할 수 있다</li>
<li>&#9744; <code>git restore --staged</code> 실행 후 파일 내용은 그대로 남고 staging만 풀리는 걸 확인했다</li>
<li>&#9744; <code>.gitignore</code>가 이미 추적 중인 파일은 자동으로 빼주지 않는다는 걸 안다</li>
<li>&#9744; 아직 push 안 한 commit은 <code>reset</code>, 이미 push한 commit은 <code>revert</code>를 쓴다는 기준을 설명할 수 있다</li>
<li>&#9744; 충돌 표시(<code>&lt;&lt;&lt;&lt;&lt;&lt;&lt;</code>/<code>=======</code>/<code>&gt;&gt;&gt;&gt;&gt;&gt;&gt;</code>)를 보면 무엇부터 해야 하는지 안다</li>
</ul>
</div>
</details>

여기까지 익혔다면 팀 프로젝트에서 Git 때문에 막히는 일은 거의 없습니다. `rebase`, `fetch`, 태그, 브랜치 보호 규칙처럼 더 깊은 내용이 필요해지면 → **[Git·GitHub 중급 가이드](../개발%20중급%20가이드/Git·GitHub%20중급%20가이드.html)**로 이어서 보세요.
