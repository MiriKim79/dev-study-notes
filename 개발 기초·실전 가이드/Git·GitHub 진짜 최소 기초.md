> **대상:** `git`이라는 단어를 오늘 처음 들어본 사람  
> **목적:** 팀 프로젝트에 바로 투입돼도 되는 딱 그만큼만 — branch, commit, push, PR, merge, pull이 각각 뭘 하는 건지 5분 안에 감 잡기  
> **사용법:** 이 문서는 끝까지 읽는 데 5분이면 충분합니다. 다 읽고 나서 "더 알고 싶다" 싶으면 아래 [Git·GitHub 기초 가이드](Git·GitHub%20기초%20가이드.html)로 넘어가세요. 지금은 용어와 명령어를 몰라도 됩니다 — 이 순서만 알면 됩니다.
---

# 0. 왜 이 문서부터 봐야 하나

Git을 처음 배울 때 가장 흔한 실수는 명령어부터 외우려고 하는 것입니다. 처음 보는 용어와 명령어가 한꺼번에 쏟아지면 머리만 아프고, 정작 알아야 할 큰 그림은 하나도 안 남습니다.

먼저 알아야 할 건 딱 하나, **"내 코드가 어떤 경로를 거쳐서 팀 코드가 되는가"** 뿐입니다. 이 경로 하나만 머릿속에 그려지면 충분합니다. 세세한 명령어와 옵션은 필요할 때 찾아보거나, AI 코딩 도구에게 시켜도 됩니다 — 이 문서는 그 경로 하나만 알려줍니다.

## Git과 GitHub는 다릅니다

이름이 비슷해서 헷갈리기 쉬운데, 완전히 다른 것입니다.

* **Git** = 내 컴퓨터에서 코드가 바뀐 기록을 관리해주는 도구(프로그램)
* **GitHub** = 그 Git 기록을 인터넷에 올려서 다른 사람과 공유·협업할 수 있게 해주는 서비스

Git은 인터넷이 없어도 내 컴퓨터 안에서만 혼자 쓸 수 있습니다. GitHub는 그 기록을 팀원들과 나눠 보기 위한 곳입니다. (GitLab, Bitbucket 같은 GitHub의 경쟁 서비스도 있는데, 전부 "Git 기록을 온라인에서 공유하는 서비스"라는 역할은 같습니다.)

# 1. branch란 무엇인가

**branch(브랜치)**는 같은 프로젝트 안에서, 기존 작업에 영향을 주지 않으면서 별도의 작업 흐름을 이어갈 수 있게 해주는 Git의 "분기"입니다. 코드를 통째로 복사하는 게 아니라, "지금 이 시점부터 나는 다른 갈래로 작업을 이어간다"는 표시에 가깝습니다.

아래 이름들은 실무에서 정말 자주 보이지만, **Git이라는 도구 자체가 강제하는 이름은 아닙니다.** 팀이나 프로젝트가 정한 관례(convention)일 뿐이라, 프로젝트마다 다를 수 있습니다.

| 이름 | 실무에서 흔히 쓰이는 뜻 | 주의할 점 |
| --- | --- | --- |
| `main` | 저장소의 기본/주요 branch로 쓰이는 경우가 많음 | 보통 배포와 연결되지만, 반드시 그런 것은 아닙니다 — 배포 branch는 팀 설정에 따라 다릅니다 |
| `develop` | Git Flow 같은 일부 협업 전략에서 쓰는 "팀 공동 작업용" 장기 branch | Git의 필수 요소가 아닙니다 — `main` + 짧은 `feature` branch만 쓰는 팀(GitHub Flow 방식)도 많습니다 |
| `feature/*` | 기능 하나를 작업할 때 쓰는 개인 작업 branch | `feature/`라는 접두사도 관례일 뿐, Git이 요구하는 문법이 아닙니다 |

이 문서에서는 이해를 돕기 위해 `main`(배포 기준) → `develop`(공동 작업본) → `feature`(개인 작업본)라는 **흔한 예시 하나**를 기준으로 설명합니다. 실제로 참여하는 팀·프로젝트는 branch를 다르게 쓸 수 있으니, 새 프로젝트에 들어가면 "이 팀은 branch를 어떻게 쓰나요?"부터 확인하는 습관을 들이는 게 Git 규칙을 외우는 것보다 훨씬 중요합니다.

팀 프로젝트에서는 보통 보호된 기본 branch(대개 `main`)에 직접 작업하기보다, 별도 작업 branch를 만들고 PR을 통해 합치는 방식을 많이 사용합니다. **정확한 방식은 팀 규칙에 따릅니다** — 새 프로젝트에 들어가면 CONTRIBUTING.md나 README, 또는 팀 규칙을 먼저 확인하세요.

# 2. 전체 흐름 한 장으로 보기

가장 기본적인 흐름은 다음 정도면 충분합니다.

1. Issue(내가 만들어야 할 기능)를 확인한다
2. 작업 branch를 만든다 (코드 작성 준비)
3. 코드를 수정한다
4. `add` → `commit` → `push`로 GitHub에 올린다
5. GitHub에 "이 코드 좀 봐주세요"라는 설명서를 올린다 — **PR(Pull Request)**
6. 팀원이 리뷰·검증한다
7. 팀이 정한 대상 branch에 **merge**된다
8. 팀원들도 최신 변경사항을 자기 컴퓨터로 동기화한다 — **pull**

이 여덟 줄이 이 문서의 전부입니다. 나머지는 전부 이 흐름을 실제 명령어로 옮기는 방법일 뿐입니다. **어떤 branch에 PR을 보내는지는 팀의 협업 전략에 따라 달라집니다** — 예를 들어 어떤 팀은 작업 branch를 `main`에 바로 합치고, 어떤 팀은 `develop`이라는 중간 branch를 먼저 거칩니다. 아래 다이어그램은 `develop`을 쓰는 팀의 예시입니다.

<svg viewBox="0 0 700 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="feature branch에서 develop을 거쳐 main으로 합쳐지는 Git 전체 작업 흐름도" style="max-width:100%;height:auto;font-family:inherit">
  <style>
    .gb-branch{fill:var(--surface-soft-2);stroke:var(--border-strong);stroke-width:1.5}
    .gb-main{fill:var(--callout-tip-bg);stroke:var(--callout-tip-border);stroke-width:1.5}
    .gb-step{fill:var(--callout-concept-bg);stroke:var(--accent);stroke-width:1.5}
    .gb-text{fill:var(--text);font-size:12px;text-anchor:middle}
    .gb-sub{fill:var(--text-secondary);font-size:10px;text-anchor:middle}
    .gb-arrow{stroke:var(--text-faint);stroke-width:1.5;fill:none;marker-end:url(#gbArrow)}
  </style>
  <defs>
    <marker id="gbArrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="var(--text-faint)"/>
    </marker>
  </defs>

  <rect x="30" y="20" width="140" height="40" rx="8" class="gb-step"/>
  <text x="100" y="45" class="gb-text">작업 브랜치 생성</text>

  <line x1="170" y1="40" x2="220" y2="40" class="gb-arrow"/>
  <rect x="220" y="20" width="120" height="40" rx="8" class="gb-step"/>
  <text x="280" y="45" class="gb-text">커밋</text>

  <line x1="340" y1="40" x2="390" y2="40" class="gb-arrow"/>
  <rect x="390" y="20" width="120" height="40" rx="8" class="gb-step"/>
  <text x="450" y="45" class="gb-text">푸시</text>

  <line x1="510" y1="40" x2="560" y2="40" class="gb-arrow"/>
  <rect x="560" y="20" width="110" height="40" rx="8" class="gb-step"/>
  <text x="615" y="45" class="gb-text">PR 생성</text>

  <line x1="615" y1="60" x2="615" y2="100" class="gb-arrow"/>

  <rect x="60" y="150" width="150" height="44" rx="8" class="gb-branch"/>
  <text x="135" y="172" class="gb-text" style="font-weight:700">feature 브랜치</text>
  <text x="135" y="187" class="gb-sub">작업 내용</text>

  <line x1="210" y1="172" x2="280" y2="150" class="gb-arrow"/>
  <rect x="280" y="130" width="150" height="44" rx="8" class="gb-branch"/>
  <text x="355" y="152" class="gb-text" style="font-weight:700">develop 브랜치</text>
  <text x="355" y="167" class="gb-sub">리뷰 후 머지</text>

  <line x1="430" y1="152" x2="500" y2="220" class="gb-arrow"/>
  <rect x="500" y="200" width="150" height="44" rx="8" class="gb-main"/>
  <text x="575" y="222" class="gb-text" style="font-weight:700">main 브랜치</text>
  <text x="575" y="237" class="gb-sub">배포 기준</text>

  <line x1="615" y1="100" x2="355" y2="130" class="gb-arrow"/>
</svg>

`develop` 없이 작업 branch를 바로 `main`(또는 팀이 정한 기본 branch)에 합치는 팀도 많습니다. 팀에 들어가면 어떤 흐름을 쓰는지부터 확인하세요.

# 3. 내 컴퓨터 코드를 GitHub에 올리기

`add` → `commit` → `push`, 이 세 단계가 "내 컴퓨터에 있는 코드를 GitHub로 옮기는 것"입니다. 이 과정에서 보통 새 branch도 함께 만들어집니다.

```bash
git add .
git commit -m "챗봇 UI 구현"
git push origin feature/chatbot
```

- `add .` — 지금까지 수정한 내용을 전부 담는다
- `commit -m "..."` — 무엇을 고쳤는지 한 줄로 남기고 저장한다 (중간 저장 포인트)
- `push origin feature/chatbot` — 그 저장 내용을 GitHub의 `feature/chatbot` branch로 올린다

# 4. 내 코드 + 팀 코드가 합쳐지는 과정

1. 코드를 올릴 때 보통 새 branch가 생긴다 (위 3번의 `feature/chatbot`처럼)
2. GitHub에서 **PR(Pull Request)**을 연다 — "제 코드를 팀이 정한 대상 branch에 합쳐주세요" 요청
3. 팀원이 오류 없는지 확인하고 **merge**한다 — 실제로 두 branch가 합쳐지는 순간
4. 다 합쳐진 branch는 삭제한다 (branch를 깔끔하게 유지하기 위해)
5. 이 코드와 관련 있는 팀원들은 GitHub에서 **pull**을 받는다 — 그래야 항상 최신 버전으로 작업할 수 있고 충돌도 줄어든다

# 5. 용어 한 줄 정리

| 용어 | 한 줄 정리 |
| --- | --- |
| `main` | 보통 프로젝트의 기본/주요 branch (배포와 항상 연결되는 것은 아님) |
| `develop` | 일부 팀에서 개발 내용을 모으기 위해 사용하는 branch (안 쓰는 팀도 많음) |
| 작업 branch (`feature/*` 등) | 특정 기능·수정을 다른 작업과 분리해서 진행하는 branch |
| commit | 중간 저장 |
| push | GitHub에 업로드 |
| PR (Pull Request) | "제 코드를 대상 branch에 합쳐주세요" 요청 |
| merge | 실제로 합치기 |
| pull | 다른 사람이 합친 최신 코드 받아오기 |

# 6. 직접 실습해보기 — 5분 미니 실습

읽기만 하고 넘어가면 다음에 또 헷갈립니다. 아무 폴더에서나 아래를 그대로 따라 쳐보세요. 딱 5분이면 됩니다.

## 실습 1. 로컬 저장소 만들고 첫 커밋 해보기

```bash
mkdir git-practice
cd git-practice
git init -b main
echo "hello git" > memo.txt
git add .
git commit -m "첫 커밋"
```

왜 이걸 하는지: `git init`은 이 폴더를 Git이 추적하는 저장소로 바꾸는 명령입니다. `-b main`은 시작 branch 이름을 `main`으로 명시적으로 지정하는 옵션입니다 — Git 버전이나 설정에 따라 초기 branch 이름이 `main`이 아니라 `master`로 만들어지는 경우가 있어서, 이 실습이 어떤 환경에서도 똑같이 동작하도록 명시했습니다. `add`와 `commit`을 직접 손으로 쳐봐야 "저장 = commit"이라는 감각이 생깁니다.

확인할 것: `git branch`를 쳤을 때 현재 branch 이름이 `main`인가? `git log --oneline`을 쳤을 때 방금 만든 "첫 커밋"이 보이는가?

## 실습 2. branch를 나눠서 작업해보기

```bash
git branch feature/practice
git switch feature/practice
echo "새 기능" >> memo.txt
git add .
git commit -m "기능 추가"
```

왜 이걸 하는지: `main`을 건드리지 않고 `feature/practice`라는 "내 개인 작업본"에서만 작업했다는 걸 눈으로 확인하기 위해서입니다.

## 실습 3. 다시 main으로 돌아와 merge 해보기

```bash
git switch main
git merge feature/practice
cat memo.txt
```

왜 이걸 하는지: PR에서 "merge" 버튼을 누르면 실제로는 이 명령이 실행되는 것과 같은 일이 일어납니다. 버튼 뒤에서 무슨 일이 벌어지는지 알면 팀 프로젝트에서 훨씬 덜 헷갈립니다.

<details class="quiz-answer">
<summary>정답 확인</summary>
<div class="quiz-answer-body">
<p>아래 항목을 스스로 체크해보세요. 전부 "예"라면 이 실습을 제대로 끝낸 것입니다.</p>
<ul>
<li>&#9744; <code>git branch</code>로 현재 branch 이름이 <code>main</code>인 것을 확인했다</li>
<li>&#9744; <code>git log --oneline</code>에서 "첫 커밋" 메시지가 보인다</li>
<li>&#9744; <code>git switch feature/practice</code> 이후 만든 커밋은 <code>main</code>이 아니라 <code>feature/practice</code> branch에만 있다는 것을 <code>git log --oneline --all --graph</code>로 확인했다</li>
<li>&#9744; <code>git switch main</code> 후 <code>cat memo.txt</code>를 쳤을 때는 아직 "새 기능" 줄이 없다 (merge 전이므로)</li>
<li>&#9744; <code>git merge feature/practice</code> 이후 <code>cat memo.txt</code>에 "새 기능" 줄이 추가된 것을 확인했다</li>
<li>&#9744; branch, commit, merge가 각각 무엇을 하는 명령인지 다른 사람에게 한 문장씩 설명할 수 있다</li>
</ul>
</div>
</details>

# 7. 여기까지 왔다면

branch 명령어를 외우거나, 충돌(conflict)을 손으로 푸는 방법은 아직 몰라도 됩니다. 실제로 팀에서 막힐 때는 대부분 AI 코딩 도구에게 "branch 만들어서 커밋하고 push하고 PR까지 올려줘"라고 시키면 처리해 줍니다 — 사람은 PR을 읽고 오류가 없으면 merge 버튼만 누르면 됩니다.

한 가지만 기억하세요 — **branch 이름과 협업 전략(main/develop을 쓰는지, feature를 어떻게 부르는지)은 팀마다 다를 수 있습니다.** 이 문서에서 본 `main`·`develop`·`feature`는 이해를 돕기 위한 흔한 예시일 뿐, Git 자체의 규칙이 아닙니다. 새 팀에 들어가면 branch 규칙부터 물어보는 습관을 들이세요.

지금 딱 이 정도만 알아도 팀 프로젝트에 투입될 수 있습니다. 실제 명령어를 손으로 치는 연습, 충돌 해결, 인증 설정까지 제대로 익히고 싶다면 → **[Git·GitHub 기초 가이드](Git·GitHub%20기초%20가이드.html)**로 이어서 보세요.
