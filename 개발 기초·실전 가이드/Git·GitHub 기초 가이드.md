> **대상:** Git과 GitHub를 처음 사용하는 사람  
> **목적:** 저장소, add/commit/push/pull, 브랜치, PR, 충돌, merge/rebase, 인증까지 어떤 언어·프레임워크에서도 공통으로 필요한 버전 관리와 협업 기초를 이해하는 가이드  
> **사용법:** 처음에는 개념과 안전한 기본 명령을 익히고, 마지막 실습에서 branch→commit→push→PR 흐름을 직접 반복합니다.
---

# 0. 시작 전에 — 자주 나오는 용어

| 용어 | 쉬운 설명 |
| --- | --- |
| 버전 관리(Version Control) | 파일이 바뀐 이력을 시간순으로 남겨서 언제든 특정 시점으로 돌아갈 수 있게 하는 것. |
| 저장소(Repository, repo) | 프로젝트 파일과 변경 이력이 저장되는 공간. 로컬 저장소(내 컴퓨터)와 원격 저장소(GitHub 등)로 나뉜다. |
| 워킹 디렉토리(Working Directory) | 지금 눈에 보이는, 실제로 수정 중인 파일들이 있는 공간. |
| 스테이징 영역(Staging Area) | 다음 커밋에 포함할 변경사항을 미리 담아두는 대기 공간. `git add`로 여기에 올린다. |
| 커밋(Commit) | 스테이징 영역의 내용을 저장소 이력에 하나의 버전으로 기록하는 것. 게임의 세이브 포인트에 비유할 수 있다. |
| origin | 원격 저장소를 가리키는 기본 별칭(이름). 대부분 GitHub 저장소 주소를 의미한다. |
| HEAD | 지금 체크아웃되어 있는(작업 중인) 브랜치의 최신 커밋을 가리키는 포인터. |
| 원격 추적 브랜치(remote-tracking branch) | `origin/main`처럼, 로컬 저장소 안에 있지만 원격 저장소의 상태를 기억해두는 브랜치. |
| Fast-forward | 브랜치를 병합할 때 별도의 병합 커밋 없이 포인터만 앞으로 이동시키는 가장 단순한 병합 방식. |
| HTTPS / SSH | GitHub 원격 저장소에 연결하는 대표 방식. HTTPS에서는 GitHub CLI·Git Credential Manager·PAT 등을 사용할 수 있고, SSH는 공개키/개인키를 사용합니다. |
| PAT (Personal Access Token) | HTTPS 인증 등에 사용할 수 있는 개인 액세스 토큰. 비밀번호처럼 비밀로 관리하고 필요한 권한만 부여합니다. |
| Fork | 남의 저장소를 내 계정으로 통째로 복사하는 것. 그 저장소에 직접 쓸 권한이 없을 때 기여하는 방법. |

---

# 1. Git과 GitHub의 차이

```
Git    = 로컬 컴퓨터에서 동작하는 분산 버전 관리 시스템(도구)
GitHub = Git 저장소를 온라인에서 관리·협업할 수 있게 해주는 플랫폼(웹사이트)
```

Git은 리누스 토르발즈가 만든 이후 오픈소스로 관리되고 있고, GitHub은 2018년 마이크로소프트가 인수했다. Git 없이 GitHub만 쓸 수 없고, 반대로 Git만 쓰고 GitHub 없이(또는 GitLab 등 다른 플랫폼으로) 협업할 수도 있다.

### 기본 상식

* Git의 핵심은 로컬·원격 두 저장소를 두고, 로컬에서 자유롭게 작업한 뒤 원하는 시점에만 원격과 동기화한다는 점이다.

* 주요 동작은 `commit`, `push`, `pull`, `merge`, `branch`, `checkout` 몇 가지로 요약된다. 나머지는 이 동작들의 변형이다.

---

# 2. 개발 환경 준비

* **Git 설치**: 공식 사이트에서 다운로드해 기본값으로 설치하면 된다.

* **에디터/IDE**: VS Code, IntelliJ 등 무엇이든 Git과 연동해 쓸 수 있다.

* **GitHub 계정**: 회원가입 후 저장소를 만들거나 초대받아 사용한다.

* **GUI 도구(선택)**: 소스트리(Sourcetree) 같은 도구는 브랜치 현황·변경 이력을 화면으로 보여줘 편리하다. 명령어에 익숙해지기 전까지 병행하면 도움이 된다.

### 기본 상식

* GUI 도구를 쓰더라도 명령어 기반 흐름(아래 8장)을 한 번은 손으로 익혀두는 것이 좋다. 오류가 났을 때 GUI만으로는 원인 파악이 어려운 경우가 많다.

---

# 3. 버전 관리 흐름

```
Working Directory (파일 수정/생성)
        ↓ git add
Staging Area (다음 커밋 후보 목록)
        ↓ git commit
Local Repository (이력 생성)
        ↓ git push
Remote Repository (GitHub 등)
```

* `git add`: 워킹 디렉토리의 변경사항 중 다음 커밋에 포함할 것을 스테이징 영역으로 올린다.

* `git commit -m "메시지"`: 스테이징 영역의 내용을 로컬 저장소에 하나의 버전(커밋)으로 기록한다. 커밋 후 스테이징 영역은 비워진다.

* `git push origin main`: 로컬 저장소의 커밋 이력을 원격 저장소에 반영한다.

---

# 4. GitHub 인증과 환경설정

GitHub에서 코드를 clone/pull/push할 때는 **어떤 원격 URL을 쓰는지(HTTPS 또는 SSH)**에 따라 인증 방식이 달라집니다.

## 4.1 명령줄에서 가장 많이 쓰는 두 연결 방식

| 방식 | 예시 원격 주소 | 인증 |
| --- | --- | --- |
| HTTPS | `https://github.com/owner/repo.git` | GitHub CLI 로그인, Git Credential Manager, 또는 PAT |
| SSH | `git@github.com:owner/repo.git` | SSH 공개키/개인키 |

### HTTPS

초보자에게는 HTTPS가 설정이 단순한 편입니다.

권장 흐름 중 하나:

```bash
gh auth login
```

GitHub CLI를 쓰지 않는 경우 HTTPS Git 작업에서 비밀번호 대신 **Personal Access Token(PAT)**을 사용할 수 있습니다. 매번 토큰을 직접 입력하기보다 Git Credential Manager 같은 자격 증명 도구를 사용하는 편이 안전하고 편리합니다.

### SSH

SSH는 키 쌍을 만들어 공개키를 GitHub 계정에 등록한 뒤 사용합니다.

```text
내 컴퓨터: 개인키 보관
GitHub: 공개키 등록
```

개인키는 절대 공유하거나 저장소에 올리지 않습니다.

### PAT 기본 상식

- PAT는 비밀번호처럼 취급
- 가능한 경우 필요한 저장소·권한만 주는 fine-grained token 우선 검토
- 코드·`.env`·커밋 메시지·스크린샷에 남기지 않기
- 노출되면 즉시 revoke 후 재발급

> “OAuth와 PAT 중 하나를 고른다”가 아니라, **Git 명령줄에서는 HTTPS/SSH 연결 방식을 먼저 구분하고 그 안에서 적절한 인증 수단을 선택**한다고 이해하면 됩니다.

## 4.2 커밋 사용자 정보 설정

```bash
git config --global user.name "이름"
git config --global user.email "이메일"
```

- `--global`: 이 컴퓨터의 모든 저장소에 기본 적용
- `--local`: 특정 저장소에만 적용. 보통 옵션을 생략하고 저장소 안에서 설정하면 로컬 설정이 됨
- 조회: `git config user.name`, `git config user.email`
- 전체 설정 확인: `git config --list --show-origin`

회사/학교/개인 계정을 섞어 쓰면 저장소별 이메일을 다르게 설정할 수 있습니다.

---

# 5. 프로젝트 시작하기

## 5.1 이미 있는 저장소를 받아올 때

```
git clone <repository 주소>
```

## 5.2 로컬에 이미 있는 프로젝트를 저장소로 만들 때

```bash
git init -b main                         # 새 Git 저장소 + main 브랜치 생성
git remote add origin <repository 주소>   # 원격 저장소 연결
```

`git init`만 실행했을 때 만들어지는 기본 브랜치 이름은 Git 설정(`init.defaultBranch`)에 따라 다를 수 있습니다. 팀 문서에서 `main`을 쓰기로 했다면 `git init -b main`처럼 명시하면 헷갈림이 줄어듭니다.

* `.git` 폴더에는 원격 저장소 정보, 사용자 정보, 커밋 이력 등 이 저장소의 모든 Git 정보가 들어 있다. 실수로 지우면 이력이 전부 사라지므로 삭제하지 않는다.

* `origin`은 원격 저장소 주소를 가리키는 기본 별칭이다.

## 5.3 원격 주소 변경·삭제

```
git remote set-url origin <새 주소>   # 저장소 주소 변경 (기존 커밋 이력은 유지된 채 새 주소로 push됨)
git remote remove origin              # 원격 연결 정보 삭제
```

---

# 6. `.gitignore`

Git이 **새로 추적하지 않을 파일·폴더**를 지정하는 파일입니다.

```gitignore
node_modules/
.env
.venv/
__pycache__/
*.log
dist/
```

프로젝트 초기에 만드는 것이 가장 좋습니다.

## 이미 추적 중인 파일은 별도 처리

`.gitignore`는 이미 Git이 추적하고 있는 파일을 자동으로 추적 해제하지 않습니다.

예를 들어 `.env`가 이미 추적 중인지 확인:

```bash
git ls-files .env
```

결과에 `.env`가 나오면 Git 추적만 해제:

```bash
git rm --cached .env
```

그 뒤 `.gitignore`에 `.env`가 있는지 확인하고 커밋합니다.

### `git rm -r --cached .`는 언제 쓰나?

이 명령은 **저장소의 모든 추적 파일을 인덱스에서 한 번 빼고 `.gitignore` 기준으로 다시 등록**할 때 쓰는 큰 범위의 명령입니다.

초보자가 특정 파일 하나 때문에 기본 해결책처럼 실행하지 않습니다. 대부분은 아래처럼 대상 파일만 지정하는 것이 안전합니다.

```bash
git rm --cached .env
git rm -r --cached node_modules
```

### 시크릿을 이미 push했다면

`.env`를 삭제하는 것만으로는 충분하지 않습니다.

```text
1. 노출된 API Key / Token / 비밀번호 폐기
2. 새 값 발급
3. 코드·환경변수 교체
4. 필요하면 Git 이력의 민감정보 제거
5. 팀원에게 영향 범위 공유
```

---

# 7. 기본 명령어

| 명령어 | 설명 |
| --- | --- |
| `git status` | 워킹 디렉토리·스테이징 영역 상태 확인 |
| `git add <파일>` | 특정 변경을 다음 커밋 후보로 올림 |
| `git add .` | 현재 경로 아래 변경을 한꺼번에 스테이징. 커밋 전에 `git status`로 포함 범위 확인 |
| `git commit -m "메시지"` | 스테이징된 변경으로 커밋 생성 |
| `git log --oneline --graph --all` | 브랜치 전체 이력을 간단한 그래프로 확인 |
| `git fetch origin` | 원격의 최신 이력만 받아옴. 내 작업 파일을 자동 병합하지 않음 |
| `git pull` | `fetch` 후 현재 설정/옵션에 따라 원격 이력을 현재 브랜치에 통합 |
| `git push -u origin <브랜치>` | 처음 브랜치를 원격에 올리고 upstream 연결 |
| `git switch <브랜치>` | 브랜치 전환 |
| `git switch -c <새브랜치>` | 새 브랜치 생성 + 전환 |
| `git restore <파일>` | 커밋하지 않은 파일 변경을 되돌릴 때 사용 |
| `git restore --staged <파일>` | add한 파일을 스테이징에서 내림 |
| `git diff` | 아직 스테이징하지 않은 변경 비교 |
| `git diff --staged` | 다음 커밋에 들어갈 변경 비교 |
| `git remote -v` | 연결된 원격 주소 확인 |

## `git commit -am` 주의

```bash
git commit -am "Fix: 오류 수정"
```

`-a`는 **Git이 이미 추적 중인 파일의 수정·삭제**를 자동 스테이징합니다. 새로 만든 untracked 파일은 포함하지 않습니다.

따라서 초보자에게는 다음 흐름이 더 명확합니다.

```bash
git status
git add <필요한 파일>
git diff --staged
git commit -m "메시지"
```

## `git pull`은 항상 merge만 하는 명령이 아니다

`git pull`은 먼저 `fetch`한 뒤 원격 브랜치를 현재 브랜치에 통합합니다. 통합 방식은 옵션·설정에 따라 달라질 수 있습니다.

대표 옵션:

```bash
git pull --ff-only     # fast-forward만 허용
git pull --rebase      # rebase 방식
git pull --no-rebase   # merge 방식
git pull --squash      # squash 방식
```

팀에서는 한 가지 정책을 정해두는 것이 좋습니다. 아직 Git이 익숙하지 않다면 문제가 생겼을 때 `git pull`을 반복하기보다 다음처럼 단계적으로 확인하면 이해하기 쉽습니다.

```bash
git fetch origin
git status
git log --oneline --graph --all
git diff HEAD origin/main
```

그다음 팀 정책에 맞게 merge/rebase 등을 진행합니다.

## 강제 push 주의

공용 브랜치(`main`, `develop`)에는 원칙적으로 force push하지 않습니다.

내 개인 기능 브랜치에서 rebase 후 강제 push가 꼭 필요한 경우에도 일반 `--force`보다 **원격이 예상 상태일 때만 덮어쓰는 `--force-with-lease`**를 우선 검토합니다.

```bash
git push --force-with-lease
```

그래도 다른 사람이 같은 브랜치를 쓰고 있다면 먼저 합의합니다.

---

# 8. 되돌리기 (단계별 취소)

작업 취소는 **어느 단계까지 진행됐는지**에 따라 방법이 다르다.

```
1. 워킹 디렉토리 수정 (add 전)      → 에디터/IDE에서 되돌리기
2. 스테이징 반영 (add 이후)         → git reset 또는 git restore --staged .
3. 로컬 저장소 반영 (commit 이후)    → git reset HEAD~1 (또는 --soft)
4. 원격까지 배포 (push 이후)        → git revert <커밋ID>
```

| 상황 | 명령어 | 결과 |
| --- | --- | --- |
| add 취소 | `git restore --staged .` | 스테이징 해제, 파일 수정 내용은 유지 |
| 마지막 커밋 취소 (unstaged로) | `git reset HEAD~1` (`HEAD^`도 동일) | 커밋이 취소되고 변경사항은 워킹 디렉토리로 되돌아감 |
| 마지막 커밋 취소 (staged 유지) | `git reset --soft HEAD~1` | 커밋만 취소, 변경사항은 스테이징 상태로 유지 |
| 이미 push된 커밋 취소 | `git revert <커밋ID>` | 해당 커밋을 취소하는 **새 커밋**을 만들어 다시 push. vi 편집창이 뜨면 `:wq`로 저장 |

### 기본 상식

* `git reset`은 이력 자체를 바꾸므로 **이미 push한 커밋에는 쓰지 않는다.** 다른 사람이 이미 받아간 이력이 꼬일 수 있다.

* 이미 공유된(push된) 커밋을 취소해야 한다면 `reset`이 아니라 `revert`를 쓴다 — 이력을 지우지 않고 “취소하는 커밋”을 추가하는 방식이라 안전하다.

---

# 9. `git pull`과 충돌을 이해하기

충돌은 “같은 파일을 수정했기 때문”이 아니라 **Git이 두 변경을 자동으로 합칠 수 없는 같은 부분(hunk)을 서로 다르게 수정했기 때문**에 발생합니다.

같은 파일의 서로 다른 줄을 수정했다면 자동 병합될 수도 있습니다.

## 가장 안전한 확인 흐름

```bash
git fetch origin
git status
git log --oneline --graph --all
```

현재 브랜치와 원격 브랜치가 갈라졌는지 확인한 뒤 팀 정책에 따라 통합합니다.

### 상황 1. 원격에만 새 커밋이 있음

내 로컬에 별도 커밋이 없다면 fast-forward로 이동할 수 있습니다.

```bash
git pull --ff-only
```

### 상황 2. 로컬과 원격 모두 새 커밋이 있음

브랜치가 diverged 상태입니다.

선택지는 팀 정책에 따라:

```bash
git pull --no-rebase   # merge
git pull --rebase      # rebase
```

공용 브랜치에서 임의로 정책을 바꾸지 않습니다.

### 상황 3. 충돌 발생

예:

```text
<<<<<<< HEAD
내 코드
=======
원격 코드
>>>>>>> origin/main
```

해야 할 일:

```text
1. 두 코드의 의도를 읽는다.
2. 최종적으로 남길 코드로 직접 수정한다.
3. 충돌 표시 문자를 모두 제거한다.
4. 테스트한다.
5. git add로 해결 완료 표시
6. merge/rebase 절차를 마친다.
```

Merge 중이었다면 보통:

```bash
git add <충돌해결파일>
git commit
```

Rebase 중이었다면:

```bash
git add <충돌해결파일>
git rebase --continue
```

잘못 시작했다면:

```bash
git merge --abort
git rebase --abort
```

### 상황 4. 커밋하지 않은 로컬 수정 때문에 pull이 막힘

오류 예:

```text
Your local changes ... would be overwritten
```

선택:

```text
A. 작업이 의미 있는 단위면 먼저 커밋
B. 잠시 치울 거면 git stash
C. 필요 없는 수정이면 안전하게 되돌림
```

무조건 `reset --hard`부터 실행하지 않습니다.

---

# 10. `git stash` — 작업 임시 저장

브랜치를 전환해야 하는데 지금 작업이 끝나지 않았을 때, 커밋하지 않고 임시로 치워두는 명령이다.

```
git stash                    # 워킹 디렉토리 변경사항을 임시 저장
git stash list               # 저장된 작업 목록 확인 (스택 구조, 최근 것이 0번)
git stash show -p 0          # 특정 인덱스의 상세 내용 확인
git stash pop                # 가장 최근 저장분을 적용하면서 목록에서 제거
git stash apply stash@{0}    # 목록에는 남긴 채 적용만
git stash clear              # 전체 목록 삭제
```

---

# 11. `git tag` — 버전 표시

특정 커밋에 버전 이름을 붙여 릴리즈 시점을 표시한다.

```
git tag v1.0                       # 마지막 커밋에 태그
git tag -a v1.0 -m "메시지"         # 메시지를 남기는 태그(annotated tag)
git push origin v1.0               # 태그 push (소스코드 push와는 별개)
git tag                            # 태그 목록 조회
```

GitHub에서 태그를 기준으로 Release를 만들면 해당 시점의 소스코드가 압축파일로 제공된다.

---

# 12. 브랜치

## 12.1 브랜치란

브랜치는 저장소의 특정 시점에서 작업을 분리해 독립적으로 개발할 수 있게 해주는 가상의 포인터다. 실무에서는 보통 `main`(배포용), `dev`/`develop`(개발 기준), 그리고 작업별 개별 브랜치를 함께 운영한다.

## 12.2 브랜치 네이밍 (팀마다 다름 — 자주 쓰이는 예시)

| 접두어 | 용도 |
| --- | --- |
| `feature/*` | 새 기능 추가. 가장 많이 사용 |
| `bugfix/*` | 버그 수정 |
| `hotfix/*` | 긴급한 버그 수정 |

> 이 바인더의 `CONTRIBUTING`는 `feat/fix/refactor/hotfix` 네이밍을 팀 규칙으로 이미 확정해두었다. 새 프로젝트에서는 그 규칙을 따르고, 이 절은 “왜 이런 접두어를 쓰는지”를 이해하는 배경 지식으로 참고한다.

## 12.3 현업에서 흔한 브랜치 작업 순서

```
1. 최신 main(또는 dev) 기준으로 로컬에서 feature 브랜치 생성
2. 작업 후 git push origin feature/브랜치명
3. Pull Request로 dev까지 merge
4. dev에서 main으로 최종 merge
5. 작업 완료된 브랜치 삭제
```

## 12.4 브랜치 관련 명령어

| 명령어 | 설명 |
| --- | --- |
| `git branch` | 로컬 브랜치 목록. `-a` 옵션으로 원격 브랜치까지 조회 |
| `git branch <이름>` | 현재 체크아웃된 브랜치를 기준으로 새 브랜치 생성 |
| `git switch <브랜치>` | 브랜치 전환 |
| `git switch -c <브랜치>` | 새 브랜치 생성과 전환을 동시에 |
| `git branch -d <브랜치>` | 병합된 로컬 브랜치를 안전하게 삭제 |
| `git branch -D <브랜치>` | **강제 삭제**. 병합되지 않은 커밋도 버릴 수 있으므로 필요성을 확인한 뒤 사용 |
| `git push origin --delete <브랜치>` | 원격 브랜치 삭제 (GitHub 화면에서 직접 삭제도 가능) |
| `git fetch --all --prune` | 모든 브랜치 정보를 가져오면서, 원격에서 삭제된 브랜치 정보도 함께 정리 |

### 기본 상식

* 항상 최신화된 `main`(또는 `develop`) 기준으로 새 브랜치를 만든다. 오래된 브랜치에서 새로 갈라치면 나중에 병합 시 충돌이 커진다.

* 기능 브랜치는 작은 단위·짧은 기간으로 유지한다. 오래 살아있는 브랜치일수록 병합이 어려워진다.

* 같은 파일의 같은 영역을 여러 명이 동시에 수정하면 충돌 가능성이 커집니다. 공통 설정·라우터·패키지 파일처럼 모두가 건드리는 파일은 미리 공유합니다.

---

# 13. 팀 저장소 운영 방식

| 방식 | 설명 | 적합한 경우 |
| --- | --- | --- |
| 개인 저장소 + Collaborator 초대 | 한 사람 계정에 저장소를 만들고 팀원을 Collaborator로 초대 | 소규모·단기 팀 프로젝트 |
| Organization + 저장소 | 조직을 만들고 그 아래 저장소 생성, 팀원 초대 | 권한·팀 단위 관리가 필요한 경우, 회사에서 흔히 쓰는 방식 |
| Fork | 저장소에 대한 쓰기 권한이 없는 외부 기여자가 저장소를 통째로 복사해 PR로 기여 | 오픈소스 기여 등 |

## 13.1 브랜치 보호 규칙 (권장)

* *Require pull request reviews before merging* 같은 규칙을 `main`/`develop`에 적용하면 리뷰 없는 머지를 막을 수 있다.

* 규칙 적용 대상 브랜치는 저장소 설정의 *targets*(또는 Branch protection rules)에서 지정한다.

### 기본 상식

* 이슈 관리 기능(GitHub Issues)만으로도 소규모 팀에서는 Jira 같은 별도 협업 툴 없이 작업을 추적할 수 있다.

---

# 14. Merge 전략 — merge / rebase / squash

| 전략 | 방식 | 장점 | 주의점 |
| --- | --- | --- | --- |
| **Merge** | 두 브랜치의 이력을 유지하면서 합침 | 분기·병합 기록이 명확 | 브랜치가 많으면 로그가 복잡해질 수 있음 |
| **Rebase** | 내 커밋을 다른 기준 커밋 위에 다시 적용 | 선형 이력을 만들기 좋음 | 커밋 ID가 바뀌므로 공유 이력에서 조심해야 함 |
| **Squash merge** | PR의 여러 커밋을 기준 브랜치에 하나의 커밋으로 합침 | 기준 브랜치 이력이 단순 | 세부 작업 커밋은 기준 브랜치에 그대로 남지 않음 |

## Rebase의 안전 기준

“push한 브랜치는 절대 rebase 금지”라고 외우기보다 다음처럼 이해합니다.

- **나 혼자 쓰는 기능 브랜치**: 팀 규칙이 허용하면 rebase 가능. 이미 push했다면 이후 `--force-with-lease`가 필요할 수 있음
- **여러 사람이 함께 쓰는 브랜치**: rebase로 기존 커밋 ID를 바꾸면 다른 사람 이력과 어긋날 수 있으므로 임의로 하지 않음
- **main/develop 같은 공용 기준 브랜치**: 이력을 다시 쓰는 작업을 임의로 하지 않음

## Squash merge 후 브랜치

GitHub에서 Squash merge하면 기준 브랜치에는 새로운 하나의 커밋이 생깁니다. 작업 브랜치는 보통 삭제하고 다음 작업은 최신 기준 브랜치에서 새 브랜치를 만드는 편이 단순합니다.

**어떤 전략이 더 “좋다”기보다 팀의 리뷰·배포 방식에 맞춰 하나의 규칙으로 통일하는 것이 중요**합니다.

---

# 15. 자주 하는 실수

* `.env`, 토큰, 키 파일을 `.gitignore` 설정 전에 먼저 커밋해버림 (커밋 이후엔 캐시 삭제까지 필요)

* 팀 공용 브랜치(`main`, `develop`)에 `-force` push

* 이미 push된 브랜치를 rebase해서 팀원과 커밋ID가 어긋남

* 오래된 브랜치에서 새 기능 브랜치를 생성해 나중에 충돌이 커짐

* `git reset`으로 이미 공유된 커밋을 지워버림 (→ `revert`를 썼어야 함)

* PAT를 코드나 커밋 메시지에 그대로 남김

* 커밋 메시지 없이 또는 의미 없는 메시지로 커밋

---

# 16. 이 문서 사용법

이 문서는 특정 프로젝트의 브랜치 전략이 아니라 **Git이라는 도구 자체**를 다루는 공통 기초 문서다.

```
개발 협업 방식 선택 가이드
→ 어떤 브랜치 전략·리뷰 방식을 쓸지 "비교·선택"하는 문서

팀 GitHub 협업 규칙 (CONTRIBUTING.md)
→ 이번 프로젝트가 채택한 규칙을 "확정"해서 적어두는 문서

팀 개발 시작 가이드
→ Git을 포함해 개발 전체 흐름에서 "언제 무엇을 하는지" 행동 순서를 정리한 문서

Git·GitHub 기초 가이드 (이 문서)
→ 브랜치 전략과 무관하게, Git 명령어·인증·충돌 해결을 다루는 "도구 사용법" 문서
```

프로젝트마다 달라지는 것은 위 세 문서에 적고, Git 자체에 대한 지식은 이 문서를 반복해서 참고한다.

---

# 17. 직접 실습해보기 — Git 최소 실습

연습용 저장소에서 다음 흐름을 직접 한 번 해봅니다.

## 1단계. 저장소 받기

```bash
git clone <저장소주소>
cd <폴더>
git status
git remote -v
```

## 2단계. 기능 브랜치

```bash
git switch main
git pull --ff-only
git switch -c feat/practice
```

## 3단계. 파일 수정 후 커밋

```bash
git status
git add <파일>
git diff --staged
git commit -m "Feat: 연습 기능 추가"
```

## 4단계. 원격에 처음 올리기

```bash
git push -u origin feat/practice
```

이후 GitHub에서 PR을 생성합니다.

## 5단계. add 취소도 해보기

```bash
git add practice.txt
git restore --staged practice.txt
```

파일 내용은 남아 있고 staging만 풀리는지 확인합니다.

## 6단계. stash 해보기

```bash
git stash
git status
git stash pop
```

## 7단계. 일부러 충돌 경험하기

연습 저장소에서 같은 줄을 두 브랜치에서 다르게 수정한 뒤 merge해봅니다.

```bash
git merge <다른브랜치>
```

`<<<<<<<`, `=======`, `>>>>>>>` 표시를 직접 해결하고 `git add` → `git commit`까지 해봅니다.

### 이 실습 후 설명할 수 있어야 하는 것

```text
Working Directory / Staging / Commit의 차이는?
fetch와 pull은 무엇이 다른가?
git add는 GitHub에 올리는 명령인가?
commit과 push는 무엇이 다른가?
같은 파일을 수정하면 항상 충돌하는가?
reset과 revert는 언제 다르게 쓰는가?
-d와 -D는 무엇이 다른가?
force push가 왜 위험한가?
```

<details class="quiz-answer">
<summary>정답 확인</summary>
<div class="quiz-answer-body">
<p>아래 항목을 스스로 체크해보세요. 전부 "예"라면 이 실습을 제대로 끝낸 것입니다.</p>
<ul>
<li>&#9744; <code>git clone</code> 후 <code>git status</code>로 브랜치 상태를, <code>git remote -v</code>로 원격 주소를 확인했다</li>
<li>&#9744; <code>feat/practice</code> 브랜치를 만들고 그 위에서만 작업했다 (main에서 직접 커밋하지 않았다)</li>
<li>&#9744; <code>git add</code>는 로컬 staging 영역에만 올리는 명령이고, GitHub에 올라가는 건 <code>git push</code>뿐이라고 설명할 수 있다</li>
<li>&#9744; <code>git restore --staged</code> 실행 후 파일 내용은 그대로 남고 staging만 풀리는 것을 확인했다</li>
<li>&#9744; <code>git stash</code>로 작업을 잠시 치운 뒤 <code>git stash pop</code>으로 다시 꺼냈다</li>
<li>&#9744; 일부러 충돌을 낸 뒤 <code>&lt;&lt;&lt;&lt;&lt;&lt;&lt;</code> / <code>=======</code> / <code>&gt;&gt;&gt;&gt;&gt;&gt;&gt;</code> 표시를 직접 지우고 원하는 내용으로 정리했다</li>
<li>&#9744; 충돌 해결 후 <code>git add</code> → <code>git commit</code>까지 마쳤다</li>
<li>&#9744; fetch(원격 정보만 받아옴)와 pull(받아온 뒤 merge까지)의 차이를 한 문장으로 설명할 수 있다</li>
</ul>
</div>
</details>
