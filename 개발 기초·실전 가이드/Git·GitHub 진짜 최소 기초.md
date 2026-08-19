> **대상:** `git`이라는 단어를 오늘 처음 들어본 사람  
> **목적:** GitHub 팀 프로젝트를 오늘 바로 시작할 수 있는 최소한의 흐름 — clone부터 pull까지 8단계  
> **사용법:** 위에서 아래로 한 번 쭉 읽으면 끝입니다. 용어는 처음 나오는 곳에서 그 자리에서 설명합니다. 다시 위로 올라갈 필요 없습니다. 명령어와 옵션을 더 깊이 알고 싶으면 다 읽은 뒤 [Git·GitHub 기초 가이드](Git·GitHub%20기초%20가이드.html)로 넘어가세요.
---

# 0. Git과 GitHub는 다릅니다

* **Git** = 내 컴퓨터에서 코드가 바뀐 기록을 관리해주는 도구
* **GitHub** = 그 Git 기록을 인터넷에 올려서 다른 사람과 공유·협업할 수 있게 해주는 서비스

Git은 인터넷 없이 내 컴퓨터 안에서만 써도 됩니다. GitHub는 그 기록을 팀원과 나눠 보기 위한 곳입니다.

## 전체 흐름 한눈에 보기

아래 10단계가 이 문서의 전부입니다. 나머지는 전부 이 흐름을 실제 명령어로 옮기는 방법일 뿐입니다.

<svg viewBox="0 0 700 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="clone부터 작업 브랜치 생성, 코드 수정, add, commit, push, PR, review, merge, pull까지 이어지는 Git 팀 작업 전체 흐름도" style="max-width:100%;height:auto;font-family:inherit">
  <style>
    .gb-branch{fill:var(--surface-soft-2);stroke:var(--border-strong);stroke-width:1.5}
    .gb-main{fill:var(--callout-tip-bg);stroke:var(--callout-tip-border);stroke-width:1.5}
    .gb-step{fill:var(--callout-concept-bg);stroke:var(--accent);stroke-width:1.5}
    .gb-text{fill:var(--text);font-size:12px;text-anchor:middle}
    .gb-sub{fill:var(--text-secondary);font-size:10px;text-anchor:middle}
    .gb-note{fill:var(--text-faint);font-size:10.5px;text-anchor:middle}
    .gb-arrow{stroke:var(--text-faint);stroke-width:1.5;fill:none;marker-end:url(#gbArrow2)}
  </style>
  <defs>
    <marker id="gbArrow2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="var(--text-faint)"/>
    </marker>
  </defs>

  <!-- 1행: clone → branch 생성 → 수정·add·commit → push → PR -->
  <rect x="10" y="20" width="90" height="42" rx="8" class="gb-step"/>
  <text x="55" y="46" class="gb-text">clone</text>

  <line x1="100" y1="41" x2="130" y2="41" class="gb-arrow"/>
  <rect x="130" y="20" width="110" height="42" rx="8" class="gb-step"/>
  <text x="185" y="46" class="gb-text">작업 브랜치 생성</text>

  <line x1="240" y1="41" x2="270" y2="41" class="gb-arrow"/>
  <rect x="270" y="20" width="140" height="42" rx="8" class="gb-step"/>
  <text x="340" y="41" class="gb-text">코드 수정</text>
  <text x="340" y="55" class="gb-sub">add → commit</text>

  <line x1="410" y1="41" x2="440" y2="41" class="gb-arrow"/>
  <rect x="440" y="20" width="90" height="42" rx="8" class="gb-step"/>
  <text x="485" y="46" class="gb-text">push</text>

  <line x1="530" y1="41" x2="560" y2="41" class="gb-arrow"/>
  <rect x="560" y="20" width="90" height="42" rx="8" class="gb-step"/>
  <text x="605" y="46" class="gb-text">PR</text>

  <line x1="605" y1="62" x2="605" y2="100" class="gb-arrow"/>

  <!-- 2행: 작업 브랜치 → review → main(또는 팀이 정한 브랜치) -->
  <rect x="30" y="150" width="150" height="46" rx="8" class="gb-branch"/>
  <text x="105" y="172" class="gb-text" style="font-weight:700">작업 브랜치</text>
  <text x="105" y="187" class="gb-sub">내 작업 내용</text>

  <line x1="180" y1="173" x2="250" y2="173" class="gb-arrow"/>
  <text x="215" y="165" class="gb-sub">review</text>

  <rect x="250" y="150" width="120" height="46" rx="8" class="gb-step"/>
  <text x="310" y="177" class="gb-text">merge</text>

  <line x1="370" y1="173" x2="440" y2="173" class="gb-arrow"/>
  <rect x="440" y="150" width="220" height="46" rx="8" class="gb-main"/>
  <text x="550" y="170" class="gb-text" style="font-weight:700">main (또는 팀이 정한 브랜치)</text>
  <text x="550" y="185" class="gb-sub">배포·기준 코드</text>

  <line x1="605" y1="100" x2="310" y2="150" class="gb-arrow"/>

  <!-- pull: main → 내 컴퓨터로 되돌아오는 화살표 -->
  <line x1="550" y1="196" x2="550" y2="225" class="gb-arrow"/>
  <line x1="550" y1="225" x2="105" y2="225" class="gb-arrow"/>
  <line x1="105" y1="225" x2="105" y2="196" class="gb-arrow"/>
  <text x="327" y="218" class="gb-sub">pull — 팀원이 합친 최신 코드 받아오기</text>

  <text x="350" y="270" class="gb-note">기본 흐름은 작업 브랜치 → PR → main(또는 팀이 정한 대상 브랜치)입니다.</text>
  <text x="350" y="286" class="gb-note">중간에 develop 브랜치를 두고 거치는 팀도 있지만, 필수 단계는 아닙니다.</text>
</svg>

# 1. clone — 팀 저장소를 내 컴퓨터로 가져오기

**저장소(repository, repo)**는 프로젝트 파일과 그 변경 기록이 저장되는 공간입니다. 팀 프로젝트에서 가장 먼저 할 일은, GitHub에 이미 있는 팀 저장소를 내 컴퓨터로 통째로 복사해오는 것입니다. 이걸 **clone**이라고 합니다.

```bash
git clone https://github.com/팀이름/프로젝트이름.git
```

이 한 줄이면 그 프로젝트의 모든 코드와 지금까지의 변경 기록이 내 컴퓨터에 그대로 생깁니다. 이제 이 폴더 안에서 작업합니다.

# 2. branch — 내 작업 공간 만들기

**branch(브랜치)**는 팀의 기준 코드에 영향을 주지 않으면서, 나만 따로 작업할 수 있게 갈라져 나온 작업 공간입니다. 팀 프로젝트에서는 보통 팀의 기준 branch(대개 `main`)에 바로 코드를 올리지 않고, 새 branch를 만들어 그 안에서 작업한 뒤 나중에 합칩니다.

```bash
git switch -c my-feature
```

`my-feature`는 지금 만드는 작업 branch 이름입니다. 팀마다 이름 짓는 방식(`feature/로그인`처럼)이 다를 수 있으니, 새 팀에 들어가면 어떤 이름 규칙을 쓰는지 먼저 확인하세요.

# 3. 코드 수정 → add → commit — 변경사항 저장하기

이제 에디터로 코드를 자유롭게 수정합니다. 수정이 끝나면 그 변경 내용을 Git에게 "저장해줘"라고 알려줘야 하는데, 이 과정이 두 단계로 나뉩니다.

```bash
git add .
git commit -m "로그인 버튼 추가"
```

* `add .` — 지금까지 수정한 파일을 전부 "다음 저장에 포함할 목록"에 담습니다.
* `commit -m "..."` — 담아둔 변경사항을 **하나의 저장 기록(commit)**으로 실제로 남깁니다. 게임의 세이브 포인트라고 생각하면 됩니다. `-m` 뒤에는 "무엇을 고쳤는지" 한 줄로 씁니다.

commit은 아직 내 컴퓨터 안에만 있습니다. 팀원은 아직 이 변경사항을 볼 수 없습니다.

# 4. push — GitHub에 올리기

```bash
git push origin my-feature
```

`push`는 내 컴퓨터에 쌓인 commit을 GitHub로 올리는 명령입니다. `origin`은 우리 팀 GitHub 저장소를 가리키는 이름(1장에서 clone한 그 주소)이고, `my-feature`는 몇 단계 전에 만든 내 작업 branch입니다. 이 명령을 처음 실행하면 GitHub에도 `my-feature`라는 이름의 branch가 새로 생깁니다.

# 5. PR — "이 코드 봐주세요" 요청하기

push까지 했다고 바로 팀 코드에 합쳐지는 건 아닙니다. GitHub 웹사이트에서 **PR(Pull Request)**을 만들어야 합니다. PR은 "제가 `my-feature`에서 작업한 걸 팀 기준 branch에 합쳐주세요"라는 요청서입니다. 여기서 팀원이 코드를 보고 의견을 남기거나 승인합니다.

# 6. merge — 실제로 합쳐지기

팀원이 PR을 확인하고 문제없으면 GitHub의 **Merge** 버튼을 눌러 두 branch를 합칩니다. 이 순간부터 내가 작업한 코드가 팀의 공식 코드가 됩니다.

# 7. pull — 팀원의 변경사항 받아오기

나만 코드를 올리는 게 아니라 팀원도 각자 작업해서 merge합니다. 그 변경사항을 내 컴퓨터로 가져오려면:

```bash
git switch main
git pull
```

`pull`은 GitHub에 쌓인 최신 변경사항을 내 컴퓨터로 받아오는 명령입니다. 새로 작업을 시작할 때마다 먼저 `pull`부터 하는 습관을 들이면, 오래된 코드 위에서 작업하다 생기는 문제를 줄일 수 있습니다.

# 8. conflict — 충돌이 나면 당황하지 않기

같은 파일의 같은 부분을 나와 팀원이 각자 다르게 고쳤다면, `pull`이나 merge 도중 Git이 "어느 쪽 코드를 남길지 모르겠다"며 멈춥니다. 이걸 **conflict(충돌)**이라고 합니다. 파일을 열어보면 이렇게 표시됩니다.

```text
<<<<<<< HEAD
내 코드
=======
팀원의 코드
>>>>>>> 팀원의 브랜치
```

충돌이 나면 에러가 아니라 "둘 중 뭘 남길지 네가 정해라"는 뜻입니다. 두 코드를 읽고, 최종적으로 남길 코드로 직접 고친 뒤, `<<<<<<<`/`=======`/`>>>>>>>` 표시를 전부 지우고, 다시 `add`·`commit`하면 끝납니다. 자세한 해결 절차는 [Git·GitHub 기초 가이드](Git·GitHub%20기초%20가이드.html)에서 다룹니다.

---

# 9. 용어 한 줄 정리

| 용어 | 한 줄 정리 |
| --- | --- |
| clone | 팀 저장소를 내 컴퓨터로 복사해오기 |
| branch | 팀 코드에 영향 없이 따로 작업하는 공간 |
| commit | 변경사항을 하나의 저장 기록으로 남기기 |
| push | 내 저장 기록을 GitHub에 올리기 |
| PR (Pull Request) | "제 코드를 합쳐주세요" 요청 |
| merge | 실제로 합치기 |
| pull | 팀원이 합친 최신 코드 받아오기 |
| conflict | 같은 부분을 서로 다르게 고쳐서 자동으로 못 합치는 상태 |

# 10. 직접 실습해보기 — 5분 미니 실습

```bash
mkdir git-practice
cd git-practice
git init -b main
echo "hello git" > memo.txt
git add .
git commit -m "첫 커밋"

git switch -c my-feature
echo "새 기능" >> memo.txt
git add .
git commit -m "기능 추가"

git switch main
git merge my-feature
cat memo.txt
```

`git init -b main`은 지금 폴더를 Git 저장소로 만들면서 시작 branch 이름을 `main`으로 지정합니다(환경에 따라 `main`이 아닌 이름으로 만들어지는 걸 막기 위한 옵션입니다). 나머지는 위에서 배운 순서 그대로입니다 — 실제로는 `push`·`PR`·`merge` 버튼 클릭이 GitHub 웹사이트에서 일어나지만, 여기서는 `git merge`로 그 마지막 단계만 내 컴퓨터에서 흉내 냅니다.

<details class="quiz-answer">
<summary>정답 확인</summary>
<div class="quiz-answer-body">
<p>아래 항목을 스스로 체크해보세요. 전부 "예"라면 이 실습을 제대로 끝낸 것입니다.</p>
<ul>
<li>&#9744; <code>git log --oneline</code>에서 "첫 커밋"과 "기능 추가" 두 커밋이 보인다</li>
<li>&#9744; <code>git switch main</code> 직후 <code>cat memo.txt</code>에는 아직 "새 기능" 줄이 없다 (merge 전이므로)</li>
<li>&#9744; <code>git merge my-feature</code> 이후 <code>cat memo.txt</code>에 "새 기능" 줄이 추가됐다</li>
<li>&#9744; clone·branch·commit·push·PR·merge·pull·conflict를 각각 한 문장씩 설명할 수 있다</li>
</ul>
</div>
</details>

# 11. 여기까지 왔다면

이 8단계(clone → branch → 수정 → add·commit → push → PR → merge → pull, 그리고 conflict 대처)만 알면 팀 프로젝트에 바로 투입될 수 있습니다. branch 이름 규칙, 인증 설정, `.gitignore`, 되돌리기처럼 팀 프로젝트를 하다 보면 곧 필요해지는 내용은 → **[Git·GitHub 기초 가이드](Git·GitHub%20기초%20가이드.html)**에서 이어서 보세요.
