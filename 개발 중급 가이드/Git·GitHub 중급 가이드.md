> **대상:** `add`/`commit`/`push`/`pull`/`branch`/`merge`는 손에 익었고, 이제 커밋 이력을 다듬거나 자동화를 붙이고 싶은 사람
> **목적:** 기초 가이드에서 다루지 않은 이력 정리, 문제 추적, 자동화 도구를 실무 상황과 함께 정리합니다

---

# 0. 시작 전에 — 자주 나오는 용어

기초 가이드에서 다룬 `add`/`commit`/`push`/`pull`/`branch`/`merge`/충돌/PR 용어는 이미 안다고 가정합니다. 여기서는 이 문서에서 새로 나오는 용어만 정리합니다.

| 용어 | 쉬운 설명 |
| --- | --- |
| 커밋 이력(Commit History) | 지금까지 쌓인 커밋들의 순서와 내용. `git log`로 확인 |
| Rebase | 브랜치의 커밋들을 다른 지점 위로 다시 쌓아 이력을 정리하는 것. `merge`와 달리 이력이 직선으로 정리됨 |
| Cherry-pick | 다른 브랜치의 커밋 딱 하나만 골라서 지금 브랜치로 복사해오는 것 |
| Bisect | "언제부터 버그가 생겼는지"를 이진 탐색으로 찾는 Git 기능 |
| Reflog | 로컬 저장소에만 남는 모든 이동 기록. 실수로 커밋을 잃어버렸을 때 복구용 안전망 |
| Worktree | 같은 저장소를 여러 폴더에 동시에 펼쳐서, 브랜치를 전환하지 않고도 여러 작업을 동시에 하는 기능 |
| Git LFS (Large File Storage) | 이미지·영상 같은 큰 파일을 Git 저장소 용량을 늘리지 않고 관리하는 확장 기능 |
| CI (Continuous Integration) | 코드를 올릴 때마다 테스트를 자동으로 돌려서 문제를 빨리 발견하는 방식 |
| GitHub Actions | GitHub에서 제공하는 자동화 도구. push·PR 같은 이벤트가 생기면 정해둔 작업(테스트, 빌드 등)을 자동 실행 |
| 워크플로우(Workflow) | GitHub Actions에서 "언제, 무엇을 실행할지"를 정의한 설정 파일 전체 |
| CODEOWNERS | 저장소의 특정 폴더·파일은 특정 사람의 승인이 항상 필요하도록 지정하는 GitHub 설정 파일 |
| 커밋 서명(Commit Signing) | 이 커밋을 정말 그 사람이 작성했는지 암호학적으로 증명하는 기능. GitHub에서 "Verified" 배지로 표시됨 |

---

# 1. Interactive Rebase — 커밋 이력 정리하기

PR을 올리기 전에, 작업하면서 쌓인 지저분한 커밋(`fix typo`, `wip`, `다시 시도`)을 정리하는 데 씁니다.

```bash
git rebase -i HEAD~5   # 최근 5개 커밋을 대상으로
```

에디터가 열리면 각 커밋 앞에 명령을 바꿔 씁니다.

```text
pick   → 그대로 유지
reword → 메시지만 수정
squash → 바로 위 커밋에 합치기 (메시지도 합쳐서 편집)
fixup  → 바로 위 커밋에 합치기 (메시지는 버림)
drop   → 커밋 자체를 삭제
edit   → 이 커밋에서 멈춰서 내용을 수정
```

예를 들어 아래처럼 5개 커밋을 1개로 정리할 수 있습니다.

```text
pick a1b2c3 Feat: 로그인 폼 추가
fixup d4e5f6 fix typo
fixup g7h8i9 wip
fixup j1k2l3 다시 시도
reword m4n5o6 Feat: 에러 메시지 추가
```

**실무 팁**

- 이미 `push`해서 다른 사람이 받아간 브랜치는 rebase하지 않습니다. 커밋ID가 전부 바뀌어서 팀원과 이력이 어긋납니다. **내 로컬에만 있는 브랜치**에서만 씁니다.
- rebase 도중 충돌이 나면 `git rebase --abort`로 언제든 원래 상태로 되돌릴 수 있습니다.
- PR을 이미 올린 브랜치를 rebase해야 한다면 `git push --force-with-lease` (그냥 `--force`보다 안전 — 내가 마지막으로 받은 이후 원격에 다른 커밋이 추가됐으면 실패해서 덮어쓰기 사고를 막아줍니다).

---

# 2. Cherry-pick — 특정 커밋만 가져오기

다른 브랜치의 커밋 하나만 지금 브랜치로 가져오고 싶을 때 씁니다. 예: `hotfix` 브랜치에서 만든 버그 수정을 `develop`에도 반영해야 할 때.

```bash
git log other-branch --oneline     # 가져올 커밋ID 확인
git cherry-pick a1b2c3d
```

충돌이 나면 일반 병합 충돌처럼 해결한 뒤 `git cherry-pick --continue`, 그만두려면 `git cherry-pick --abort`.

---

# 3. Bisect — 버그가 생긴 커밋 찾기

"예전엔 됐는데 언제부터인가 안 된다"를 이진 탐색으로 찾습니다. 커밋이 수백 개라도 로그 대신 사람은 최대 10번 안팎만 확인하면 됩니다.

```bash
git bisect start
git bisect bad                # 지금 커밋은 버그가 있음
git bisect good v1.2.0        # 이 태그(또는 커밋)는 정상이었음
# Git이 중간 지점으로 자동 checkout
# 그 지점에서 직접 테스트한 뒤:
git bisect good   # 또는 git bisect bad
# 위 과정을 반복하면 Git이 "이 커밋이 원인"이라고 알려줌
git bisect reset  # 탐색 종료, 원래 브랜치로 복귀
```

테스트 스크립트가 있다면 `git bisect run ./test.sh`로 전체를 자동화할 수도 있습니다.

---

# 4. Reflog — 잃어버린 커밋 복구

`reset --hard`를 잘못 쓰거나 브랜치를 실수로 삭제해도, Git은 한동안(기본 90일) 이력을 `reflog`에 남겨둡니다.

```bash
git reflog
# a1b2c3d HEAD@{0}: reset: moving to HEAD~3
# d4e5f6g HEAD@{1}: commit: Feat: 결제 기능 추가   ← 이게 사라진 것처럼 보였던 커밋

git checkout d4e5f6g          # 확인
git branch recovered d4e5f6g  # 이 지점에서 새 브랜치 생성
```

**기본 상식**: `reflog`는 로컬 저장소에만 있는 안전망입니다. 원격(GitHub)에는 없으므로, 심각한 실수를 했을 때는 먼저 `git reflog`부터 확인하는 습관을 들입니다.

---

# 5. Worktree — 브랜치 여러 개 동시에 작업

브랜치를 전환할 때마다 `stash`하기 귀찮다면, 같은 저장소를 여러 폴더에 동시에 펼쳐둘 수 있습니다.

```bash
git worktree add ../my-app-hotfix hotfix/urgent-bug
# ../my-app-hotfix 폴더가 새로 생기고, 그 브랜치가 체크아웃된 채로 열림
# 원래 폴더에서 하던 작업은 그대로 유지됨

git worktree list             # 현재 연결된 worktree 목록
git worktree remove ../my-app-hotfix   # 다 쓰면 정리
```

급한 hotfix가 생겼는데 지금 작업 중인 내용을 커밋하기도 stash하기도 애매할 때 유용합니다.

---

# 6. 대용량 파일 관리 — Git LFS

이미지·모델 가중치처럼 큰 바이너리 파일을 그냥 커밋하면 저장소 용량이 급격히 커지고 clone이 느려집니다. Git LFS(Large File Storage)는 실제 파일은 별도 저장소에 두고, Git에는 포인터만 남깁니다.

```bash
git lfs install
git lfs track "*.psd" "*.mp4"
git add .gitattributes
git add design.psd
git commit -m "Chore: 디자인 원본 추가 (LFS)"
```

**기본 상식**: 이미 일반 커밋으로 올라간 대용량 파일은 LFS로 바꿔도 과거 이력에 그대로 남아 저장소가 무거워집니다. 처음부터 `.gitattributes`로 추적 대상을 정해두는 것이 좋습니다.

---

# 7. GitHub Actions 기초 — 첫 자동화 워크플로우

`push`할 때마다 테스트를 자동으로 돌리는 최소 예제입니다. `.github/workflows/test.yml`에 저장합니다.

```yaml
name: test
on:
  push:
    branches: [develop, main]
  pull_request:
    branches: [develop]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm install
      - run: npm test
```

- `on`: 언제 실행할지 (push, pull_request 등 이벤트)
- `jobs.test.steps`: 위에서 아래로 순서대로 실행되는 작업 목록
- `uses`: 다른 사람이 만들어둔 재사용 가능한 작업(action)을 가져다 씀
- `run`: 셸 명령어를 직접 실행

PR을 만들면 GitHub이 이 워크플로우를 자동 실행하고, 성공/실패를 PR 화면에 체크 표시로 보여줍니다.

---

# 8. 브랜치 보호 규칙 심화

기초 가이드에서 다룬 "리뷰 승인 필수" 규칙에 실무에서는 보통 이런 조건을 더합니다.

- **Require status checks to pass**: 위 GitHub Actions 같은 자동 테스트가 통과해야만 머지 버튼이 활성화됨
- **CODEOWNERS 연동**: `.github/CODEOWNERS` 파일로 특정 폴더는 특정 팀원의 승인이 항상 필요하도록 지정

```text
# .github/CODEOWNERS
/backend/          @backend-team-lead
/frontend/          @frontend-team-lead
*.md                 @docs-owner
```

- **Require branches to be up to date**: 머지 전에 기준 브랜치의 최신 커밋을 반영하도록 강제 — 오래된 브랜치가 몰래 머지되는 것을 막습니다.

---

# 9. 커밋 서명 (GPG/SSH Signing)

GitHub에서 "Verified" 배지가 붙은 커밋을 본 적이 있을 겁니다. 커밋 작성자를 암호학적으로 증명하는 기능으로, 오픈소스나 보안이 중요한 조직에서 요구합니다.

```bash
git config --global commit.gpgsign true
git config --global user.signingkey <키ID>
```

개인·소규모 팀 프로젝트에서는 필수는 아니지만, "이 커밋이 정말 그 사람이 작성한 게 맞는지"가 중요한 프로젝트에서는 표준 관행입니다.

---

# 10. 자주 하는 실수

- 이미 push한 공유 브랜치를 rebase해서 팀원과 이력이 어긋남
- `--force`로 강제 push해서 동료의 커밋을 날림 (`--force-with-lease`를 대신 씁니다)
- bisect 도중 `good`/`bad` 판단을 서두르다 잘못 표시해 탐색이 꼬임
- 이미 일반 커밋으로 올라간 대용량 파일을 뒤늦게 LFS로 옮기려다 이력 정리가 더 복잡해짐
- CI가 실패했는데 "로컬에서는 됐다"며 그냥 머지

---

# 11. 실전 체크리스트

- [ ] PR 올리기 전 지저분한 커밋을 rebase -i로 정리했는가
- [ ] 공유 브랜치를 rebase하지 않았는가
- [ ] 강제 push가 필요하다면 `--force-with-lease`를 썼는가
- [ ] CI(GitHub Actions)가 통과한 뒤에만 머지했는가
- [ ] 저장소에 대용량 바이너리가 있다면 LFS 적용을 검토했는가
