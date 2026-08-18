> **대상:** GitHub Actions로 테스트를 자동 실행해본 적은 있지만, 배포까지 자동화해본 적은 없는 사람
> **목적:** 빌드·테스트·배포를 잇는 파이프라인을 직접 구성하는 방법을 정리합니다

---

# 0. 시작 전에 — 자주 나오는 용어

기초 가이드에서 다룬 배포·환경변수 개념은 이미 안다고 가정합니다. 여기서는 이 문서에서 새로 나오는 용어만 정리합니다.

| 용어 | 쉬운 설명 |
| --- | --- |
| CI (Continuous Integration) | 커밋할 때마다 자동으로 빌드·테스트를 실행해 문제를 빨리 발견하는 방식 |
| CD (Continuous Delivery) | 테스트를 통과한 코드를 언제든 배포 가능한 상태로 자동 준비해두는 것. 실제 배포는 사람이 승인 |
| CD (Continuous Deployment) | 테스트를 통과하면 사람 개입 없이 자동으로 실서비스까지 배포하는 것 |
| 파이프라인(Pipeline) | 빌드 → 테스트 → 배포처럼, 코드가 거쳐 가는 자동화된 작업 순서 전체 |
| 워크플로우(Workflow) | GitHub Actions에서 파이프라인을 정의한 YAML 설정 파일 |
| Job / Step | 워크플로우 안의 큰 작업 단위(Job)와 그 안에서 순서대로 실행되는 세부 작업(Step) |
| Runner | 워크플로우의 Job이 실제로 실행되는 가상의 컴퓨터(서버) |
| GitHub Environments | 배포 대상 환경(dev/staging/production)마다 승인자·시크릿을 따로 설정할 수 있는 GitHub 기능 |
| 배포 전략(Rolling/Blue-Green/Canary) | 새 버전으로 바꿀 때 서비스 중단을 최소화하는 여러 방식들 |
| 시크릿(Secret) | 비밀번호·API 키처럼 코드에 직접 쓰면 안 되는 값을 안전하게 저장·주입하는 것 |
| 마스킹(Masking) | 로그에 시크릿 값이 그대로 노출되지 않도록 `***`처럼 가려서 출력하는 것 |
| 롤백(Rollback) | 새로 배포한 버전에 문제가 있을 때, 이전에 정상 동작하던 버전으로 되돌리는 것 |

---

# 1. CI, CD, Continuous Deployment 구분

세 단어가 섞여 쓰이지만 범위가 다릅니다.

```text
CI (Continuous Integration, 지속적 통합)
→ 커밋할 때마다 자동으로 빌드·테스트를 실행해 문제를 빨리 발견

CD (Continuous Delivery, 지속적 전달)
→ 테스트를 통과한 코드를 언제든 배포할 수 있는 상태로 자동 준비
   (실제 배포는 사람이 버튼을 눌러서 실행)

CD (Continuous Deployment, 지속적 배포)
→ 테스트를 통과하면 사람 개입 없이 자동으로 실서비스에 배포
```

**기본 상식**: 팀 초기에는 "테스트 통과 후 수동 배포 승인"(Continuous Delivery)부터 시작하는 것이 안전합니다. 배포 자동화에 대한 신뢰가 쌓인 뒤 완전 자동 배포(Continuous Deployment)로 넘어갑니다.

---

# 2. 빌드 → 테스트 → 배포 파이프라인

GitHub Actions로 `develop`에 머지되면 자동 배포하는 최소 예제입니다.

```yaml
name: deploy
on:
  push:
    branches: [develop]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm install
      - run: npm test
      - run: npm run build

  deploy:
    needs: build-and-test        # 위 job이 성공해야만 실행
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: 서버로 배포
        run: |
          echo "여기에 실제 배포 명령 (예: rsync, aws s3 sync 등)"
```

- `needs: build-and-test`: 테스트가 실패하면 배포 job 자체가 실행되지 않습니다 — 이것이 파이프라인의 핵심입니다.
- 두 job은 각각 독립된 가상 환경(runner)에서 실행되므로, 배포 job에서 다시 코드를 체크아웃해야 합니다.

**기본 상식**: "테스트를 통과해야만 배포한다"는 원칙은 예외 없이 지켜야 하는 규칙이 아니라 기본값입니다. 운영 장애를 급히 막아야 하는 hotfix 상황처럼 정말 예외가 필요할 때는, 파이프라인을 몰래 우회하는 대신 "누가 승인했는지, 왜 건너뛰었는지"가 남는 명시적인 절차(예: 승인자가 있는 별도 hotfix 워크플로, 배포 후 반드시 테스트를 재실행하는 후속 조치)를 미리 정해두는 것이 안전합니다.

---

# 3. 환경별 배포 전략

같은 코드를 개발(dev)·스테이징(staging)·운영(production) 환경에 다르게 배포합니다.

```text
develop 브랜치 push  → 자동으로 dev 환경에 배포 (팀 내부 테스트용)
main 브랜치 push     → 수동 승인 후 staging 배포 → 확인 후 production 배포
```

```yaml
deploy-production:
  needs: build-and-test
  runs-on: ubuntu-latest
  environment: production   # GitHub Environments 기능 — 승인자 지정, 시크릿 분리 가능
  steps:
    - run: echo "프로덕션 배포"
```

`environment`를 지정하면 GitHub에서 "이 환경에 배포하려면 특정 팀원의 승인이 필요"하도록 설정할 수 있고, 환경마다 다른 시크릿(운영 DB 주소 등)을 분리해 관리할 수 있습니다.

---

# 4. 배포 전략 — Blue-Green, Rolling, Canary

서버를 새 버전으로 바꿀 때 서비스 중단을 최소화하는 방법들입니다.

| 전략 | 방식 | 특징 |
| --- | --- | --- |
| Rolling | 서버를 한 대씩 순차적으로 새 버전으로 교체 | 구현이 간단하지만 잠시 신/구 버전이 섞여 동작함 |
| Blue-Green | 새 버전(Green)을 완전히 별도로 띄운 뒤, 트래픽을 한 번에 전환 | 문제 생기면 즉시 이전 버전(Blue)으로 되돌리기 쉬움. 서버가 2배 필요 |
| Canary | 새 버전에 트래픽의 일부(예: 5%)만 먼저 보내보고 점진적으로 확대 | 문제를 소수 사용자에게만 노출한 채 발견 가능. 구성이 복잡함 |

<svg viewBox="0 0 760 320" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Rolling Blue-Green Canary 배포 전략 3종 비교" style="max-width:100%;height:auto;font-family:inherit">
  <style>
    .dp-old{fill:var(--surface-soft-2);stroke:var(--border-strong);stroke-width:1.5}
    .dp-new{fill:var(--accent-weak);stroke:var(--accent);stroke-width:1.5}
    .dp-lb{fill:var(--callout-concept-bg);stroke:var(--accent);stroke-width:1.5}
    .dp-title{fill:var(--text-strong);font-size:13px;font-weight:700}
    .dp-text{fill:var(--text);font-size:11px;text-anchor:middle}
    .dp-sub{fill:var(--text-secondary);font-size:10px;text-anchor:middle}
  </style>

  <text x="16" y="20" class="dp-title">Rolling</text>
  <rect x="140" y="6" width="70" height="28" rx="5" class="dp-old"/><text x="175" y="24" class="dp-text">구버전</text>
  <rect x="220" y="6" width="70" height="28" rx="5" class="dp-new"/><text x="255" y="24" class="dp-text">신버전</text>
  <rect x="300" y="6" width="70" height="28" rx="5" class="dp-old"/><text x="335" y="24" class="dp-text">구버전</text>
  <rect x="380" y="6" width="70" height="28" rx="5" class="dp-new"/><text x="415" y="24" class="dp-text">신버전</text>
  <text x="580" y="24" class="dp-sub">한 대씩 순차 교체 — 신/구 혼재 구간 있음</text>

  <line x1="0" y1="50" x2="760" y2="50" stroke="var(--border)" stroke-width="1"/>

  <text x="16" y="80" class="dp-title">Blue-Green</text>
  <rect x="140" y="60" width="90" height="40" rx="6" class="dp-lb"/><text x="185" y="84" class="dp-text">로드밸런서</text>
  <rect x="260" y="60" width="90" height="18" rx="4" class="dp-old"/><text x="305" y="73" class="dp-text" style="font-size:10px">Blue(구)</text>
  <rect x="260" y="82" width="90" height="18" rx="4" class="dp-new"/><text x="305" y="95" class="dp-text" style="font-size:10px">Green(신)</text>
  <text x="450" y="70" class="dp-sub">트래픽을 한 번에 전환</text>
  <text x="450" y="90" class="dp-sub">문제 시 즉시 Blue로 롤백</text>

  <line x1="0" y1="120" x2="760" y2="120" stroke="var(--border)" stroke-width="1"/>

  <text x="16" y="150" class="dp-title">Canary</text>
  <rect x="140" y="130" width="90" height="40" rx="6" class="dp-lb"/><text x="185" y="154" class="dp-text">로드밸런서</text>
  <rect x="260" y="130" width="200" height="16" rx="4" class="dp-old"/><text x="360" y="142" class="dp-text" style="font-size:10px">구버전 95%</text>
  <rect x="260" y="152" width="30" height="16" rx="4" class="dp-new"/><text x="275" y="164" class="dp-text" style="font-size:9px" fill="var(--text)"></text>
  <text x="330" y="164" class="dp-sub" style="font-size:10px">↑ 신버전 5%부터 점진 확대</text>

  <text x="380" y="200" class="dp-sub" style="font-size:11px">공통: 세 전략 모두 "한 번에 전체 전환"의 위험을 줄이는 것이 목적</text>
</svg>

**기본 상식**: 소규모 프로젝트에서는 단순 배포(서버 재시작)로 시작해도 충분합니다. 사용자 수가 늘고 "배포 중 잠깐의 오류도 허용 안 됨" 수준이 되면 위 전략들을 검토합니다.

---

# 5. 시크릿 관리

DB 비밀번호, API 키를 워크플로우 파일(YAML)에 직접 쓰지 않습니다.

```yaml
steps:
  - name: 배포
    env:
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
    run: ./deploy.sh
```

GitHub 저장소의 `Settings → Secrets and variables → Actions`에 값을 등록해두면, 워크플로우 실행 중에만 환경변수로 주입되고 로그에는 자동으로 마스킹되어 출력됩니다(`***`로 표시).

**기본 상식**: 시크릿은 fork된 저장소의 PR에서는 기본적으로 접근할 수 없도록 GitHub이 막아둡니다 — 외부 기여자가 PR을 통해 시크릿을 빼내는 것을 방지하기 위한 보안 장치이므로 임의로 우회하지 않습니다.

---

# 6. 실패했을 때 확인하는 순서

```text
1. Actions 탭에서 실패한 워크플로우 실행 열기
2. 실패한 job과 step을 정확히 확인 (어느 단계에서 멈췄는지)
3. 로그 전체를 읽기 (마지막 몇 줄만 보고 판단하지 않기)
4. 로컬에서 같은 명령을 그대로 재현해보기
5. 환경 차이(Node/Python 버전, 환경변수 누락)부터 의심하기
```

**실무 팁**: "로컬에서는 되는데 CI에서만 실패"하는 경우 대부분 환경 차이입니다. 로컬 버전과 워크플로우에 명시된 버전이 같은지, 로컬에만 있고 리포지토리에는 없는 환경변수·파일이 없는지부터 확인합니다.

---

# 7. 자주 하는 실수

- 테스트 실패를 무시하고 배포 job이 실행되도록 `needs` 없이 구성
- 시크릿을 워크플로우 파일에 평문으로 작성해 커밋
- 운영 환경 배포에 승인 절차 없이 바로 자동 배포
- 배포 실패 시 롤백 방법을 미리 정해두지 않음
- CI 로그를 안 읽고 "다시 실행" 버튼만 반복해서 누름

---

# 8. 실전 체크리스트

- [ ] 테스트를 통과해야만 배포 job이 실행되는가 (`needs` 연결)
- [ ] 운영 환경 배포에는 승인 절차가 있는가
- [ ] 시크릿을 GitHub Secrets로 관리하고 코드에 노출하지 않는가
- [ ] 배포가 실패했을 때 되돌리는(롤백) 방법이 정해져 있는가
- [ ] dev/staging/production 환경변수가 분리되어 있는가

---

# 9. 캐싱으로 파이프라인 속도 높이기

```yaml
- uses: actions/setup-node@v4
  with:
    node-version: 20
    cache: 'npm'          # package-lock.json 기준으로 node_modules 캐시

- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: pip-${{ hashFiles('requirements.txt') }}
```

매번 처음부터 의존성을 설치하면 파이프라인이 느려집니다. 의존성 파일(lock 파일)의 해시를 캐시 키로 써서, 의존성이 바뀌지 않았다면 이전에 설치한 결과를 재사용합니다.

**실무 팁**: Job을 병렬로 나눌 수도 있습니다(`lint`, `test`, `build`를 각각 별도 job으로 동시에 실행). 순서대로 실행할 필요가 없는 검사들을 병렬화하면 전체 파이프라인 시간이 줄어듭니다.

---

# 10. 배포 후 검증(Smoke Test)과 자동 롤백

```yaml
deploy:
  needs: [test]
  steps:
    - run: ./deploy.sh
    - name: 헬스체크로 배포 검증
      run: |
        for i in {1..5}; do
          curl -f https://api.example.com/health && exit 0
          sleep 10
        done
        exit 1   # 5번 시도해도 실패하면 파이프라인 실패 처리
  # 이 job이 실패하면 이전 버전으로 자동 롤백하는 후속 job 연결 가능
```

배포가 "실행됐다"와 "정상 동작한다"는 다릅니다. 배포 직후 헬스체크 엔드포인트를 호출해 실제로 응답하는지 확인하는 스모크 테스트를 파이프라인에 포함시키면, 문제가 있는 배포를 사람이 알아채기 전에 자동으로 감지할 수 있습니다.

---

# 11. 인프라 배포 파이프라인 기초

애플리케이션 코드뿐 아니라 인프라 변경(서버 설정, DB 스키마)도 파이프라인으로 관리할 수 있습니다.

```yaml
- name: DB 마이그레이션 적용
  run: flask db upgrade
  # 애플리케이션 배포보다 먼저 실행되어야, 새 코드가 기대하는 스키마가 준비됨
```

**기본 상식**: 마이그레이션 순서는 신중해야 합니다. 컬럼을 삭제하는 마이그레이션을 애플리케이션 코드 배포보다 먼저 실행하면, 아직 그 컬럼을 쓰는 이전 버전 코드가 오류를 낼 수 있습니다. "하위 호환되는 순서"(컬럼 추가 → 코드 배포 → 이후 스프린트에 옛 컬럼 제거)로 나누는 것이 안전합니다.

---

# 12. 모노레포 CI 최적화 — 변경된 부분만 빌드

프론트엔드·백엔드가 한 저장소에 있으면, 백엔드만 고쳤는데도 프론트엔드까지 매번 빌드·테스트하면 파이프라인이 느려집니다.

```yaml
name: ci
on:
  push:
    branches: [develop]

jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      frontend: ${{ steps.filter.outputs.frontend }}
      backend: ${{ steps.filter.outputs.backend }}
    steps:
      - uses: actions/checkout@v4
      - uses: dorny/paths-filter@v4
        id: filter
        with:
          filters: |
            frontend:
              - 'frontend/**'
            backend:
              - 'backend/**'

  test-frontend:
    needs: changes
    if: needs.changes.outputs.frontend == 'true'
    runs-on: ubuntu-latest
    steps:
      - run: echo "frontend/ 디렉터리에서만 테스트 실행"

  test-backend:
    needs: changes
    if: needs.changes.outputs.backend == 'true'
    runs-on: ubuntu-latest
    steps:
      - run: echo "backend/ 디렉터리에서만 테스트 실행"
```

`changes` job이 어떤 디렉터리가 바뀌었는지 먼저 판단하고, 이후 job들은 `if` 조건으로 해당 파트가 바뀌었을 때만 실행됩니다.

**실무 팁**: 저장소가 커질수록 이 최적화의 효과가 커집니다. 팀 초기(파일 수가 적을 때)는 그냥 전체를 매번 빌드해도 되고, 파이프라인 시간이 눈에 띄게 길어질 때(체감상 3~5분 이상) 도입을 검토해도 늦지 않습니다.

---

# 13. 매트릭스 빌드 — 여러 버전을 동시에 테스트

라이브러리를 여러 Node/Python 버전에서 지원해야 하거나, 여러 OS에서 동작을 검증해야 할 때 씁니다.

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20, 22]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm install
      - run: npm test
```

이 워크플로우는 `node-version` 3개에 대해 동일한 step들을 병렬로 3번 실행합니다. 하나라도 실패하면 매트릭스 전체 job이 실패로 표시됩니다.

**기본 상식**: 매트릭스는 "여러 조합을 동시에 검증"하는 데 유용하지만, 조합이 늘어날수록(Node 버전 × OS × DB 버전 등) 실행 시간과 비용도 곱으로 늘어납니다. 실제로 지원해야 하는 조합만 최소한으로 유지합니다.

---

# 14. Docker 이미지 빌드·배포 파이프라인

컨테이너로 배포하는 경우, 이미지를 빌드해서 레지스트리에 올리고 서버가 그 이미지를 받아 실행하는 흐름입니다.

```yaml
jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write   # 저장소/조직 설정에 따라 GITHUB_TOKEN의 packages 기본 권한이 read일 수 있어, ghcr.io에 push하려면 write를 명시해두는 것이 안전함
    steps:
      - uses: actions/checkout@v4

      - name: 레지스트리 로그인
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: 이미지 빌드·푸시
        uses: docker/build-push-action@v7
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

- 태그를 `latest`가 아니라 커밋 SHA(`github.sha`)로 붙이면, 배포된 이미지가 어느 커밋에서 만들어졌는지 추적할 수 있고 문제 발생 시 이전 SHA로 즉시 롤백할 수 있습니다.
- `cache-from`/`cache-to`로 Docker 레이어 캐시를 GitHub Actions 캐시에 저장해두면, 변경 없는 레이어(예: 의존성 설치 단계)는 다시 빌드하지 않아 속도가 크게 빨라집니다.
- `GITHUB_TOKEN`으로 ghcr.io에 push하려면 `packages: write` 권한이 필요합니다. 저장소·조직 설정에 따라 `GITHUB_TOKEN`의 기본 권한이 packages read로 제한되어 있을 수 있으므로(15장 참고), `permissions`에 명시하지 않으면 환경에 따라 push 단계에서 403 오류가 날 수 있습니다.

**기본 상식**: 이미지에 소스코드의 `.env` 파일이나 시크릿을 그대로 복사해 넣지 않습니다. `.dockerignore`에 `.env`, `node_modules`, `.git` 등을 반드시 등록해 이미지 크기와 노출 위험을 함께 줄입니다.

---

# 15. 파이프라인 보안 — 최소 권한과 OIDC

## GitHub Actions 토큰의 권한 최소화

```yaml
permissions:
  contents: read
  deployments: write
```

워크플로우가 실제로 필요로 하는 권한만 명시하면, 워크플로우 코드에 취약점이 있더라도 피해 범위가 제한됩니다.

**기본 상식**: `GITHUB_TOKEN`의 기본 권한은 항상 넓은 것이 아니라 저장소·조직 설정에 따라 다릅니다. 2023년 2월 이후 만들어진 저장소는 기본적으로 read 전용으로 시작하는 경우가 많지만, 조직 설정이나 저장소 생성 시점에 따라 더 넓은 권한(write 포함)이 기본값일 수도 있습니다. `permissions`를 워크플로우 파일에 명시하면 이 기본값이 무엇이든 상관없이 의도한 권한만 갖도록 고정할 수 있으므로, 기본값을 추측하기보다 항상 명시하는 습관을 들이는 것이 안전합니다.

## 장기 자격 증명 대신 OIDC

AWS/GCP 등 클라우드에 배포할 때, 액세스 키를 GitHub Secrets에 영구 저장하는 대신 OIDC(OpenID Connect)로 워크플로우 실행마다 단기 자격 증명을 발급받는 방식이 권장됩니다.

```yaml
permissions:
  id-token: write   # OIDC 토큰 발급에 필요
  contents: read

steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789012:role/github-actions-deploy
      aws-region: ap-northeast-2
      # 액세스 키/시크릿 키를 저장할 필요 없이, 이 워크플로우 실행에 한해서만 유효한
      # 임시 자격 증명을 발급받음
```

**기본 상식**: 장기 액세스 키는 유출되면 만료 전까지 계속 악용될 수 있습니다. OIDC 기반 단기 자격 증명은 워크플로우 실행이 끝나면 자동으로 만료되므로, 유출 시 피해 범위와 시간이 훨씬 제한적입니다.

---

# 16. 배포 결과 알림 연동

배포 성공·실패를 팀 채널에 자동으로 공유하면, Actions 탭을 매번 열어보지 않아도 됩니다.

```yaml
- name: Slack 알림
  if: always()          # 성공/실패 관계없이 항상 실행
  uses: slackapi/slack-github-action@v2
  with:
    webhook: ${{ secrets.SLACK_WEBHOOK_URL }}
    webhook-type: incoming-webhook
    payload: |
      {
        "text": "배포 ${{ job.status }}: ${{ github.repository }} (${{ github.sha }})"
      }
```

`if: always()`를 쓰면 이전 step이 실패해도 알림 step은 실행되어, 실패 사실 자체를 놓치지 않습니다. 성공만 알리면 "조용히 실패한" 배포를 아무도 눈치채지 못할 수 있습니다.

---

# 17. 다른 CI 도구와의 비교

GitHub Actions 외에도 여러 CI/CD 도구가 있습니다. 개념은 거의 동일하고 문법만 다릅니다.

| 도구 | 특징 |
| --- | --- |
| GitHub Actions | GitHub 저장소에 내장, 설정이 가장 간단, 이 문서에서 다룬 도구 |
| GitLab CI/CD | GitLab에 내장, `.gitlab-ci.yml` 하나로 전체 파이프라인 정의 |
| Jenkins | 자체 서버에 설치해 운영, 플러그인이 매우 풍부하지만 직접 관리 부담이 큼 |
| CircleCI | GitHub Actions와 유사한 클라우드 기반 SaaS, 대기업에서도 널리 사용 |

**기본 상식**: 어떤 도구를 쓰든 "커밋 → 빌드 → 테스트 → 배포"라는 핵심 흐름과 "환경 분리, 시크릿 관리, 승인 절차"라는 원칙은 동일합니다. 도구별 YAML 문법 차이는 공식 문서를 찾아보면 되므로, 개념을 먼저 확실히 익히는 것이 더 중요합니다.

---

# 18. 무중단 배포를 위한 헬스체크와 그레이스풀 셧다운

## 헬스체크(Health Check)

로드밸런서나 오케스트레이터가 "이 서버(컨테이너)가 요청을 받을 준비가 됐는지"를 판단하는 기준입니다.

```python
# Flask 예시
@app.route("/health")
def health():
    # DB 연결 등 핵심 의존성이 정상인지 확인 후 응답
    return {"status": "ok"}, 200
```

새 버전 컨테이너가 떠도 `/health`가 200을 반환하기 전까지는 로드밸런서가 트래픽을 보내지 않으므로, 아직 준비 안 된 서버로 요청이 가서 에러가 나는 상황을 막습니다.

## 그레이스풀 셧다운(Graceful Shutdown)

배포 중 이전 버전 서버를 바로 죽이면, 그 순간 처리 중이던 요청이 끊깁니다.

```text
1. 로드밸런서가 이 서버로 새 요청을 그만 보냄 (기존 연결은 유지)
2. 서버는 이미 받은 요청을 마저 처리
3. 처리 중인 요청이 다 끝나면(또는 타임아웃) 그때 프로세스 종료
```

**기본 상식**: 배포할 때마다 사용자 요청이 순간적으로 끊기는 것 같다면, 헬스체크와 그레이스풀 셧다운이 제대로 설정되어 있는지부터 확인합니다. 대부분의 "배포 중 에러 급증"은 이 두 가지 중 하나가 빠져서 발생합니다.

---

# 19. 실전 트러블슈팅 시나리오

```text
증상: "develop에 머지했는데 배포 job이 아예 안 보임"
원인 후보: 워크플로우 파일의 on.push.branches에 develop이 빠져 있음, YAML 문법 오류로
          워크플로우 자체가 파싱 실패(Actions 탭에 "invalid workflow file" 표시)

증상: "CI에서만 테스트가 실패, 로컬은 통과"
원인 후보: 타임존 차이(CI는 보통 UTC), 환경변수 누락, 테스트 실행 순서에 의존하는 코드
          (로컬은 항상 같은 순서로 실행되지만 CI는 병렬/다른 순서일 수 있음)

증상: "배포는 성공했다는데 실제로는 이전 버전이 떠 있음"
원인 후보: 이미지 태그를 latest로 고정해 캐시된 이전 이미지를 재사용,
          배포 스크립트가 새 프로세스를 안 띄우고 기존 프로세스에 재시작 신호만 보냄

증상: "시크릿 값이 로그에 그대로 노출됨"
원인 후보: 시크릿을 echo로 직접 출력, 혹은 시크릿 값을 조합한 문자열(URL 등)을 출력해
          GitHub의 자동 마스킹이 전체 문자열을 못 알아챔 — 값 자체를 출력하지 않는 것이 원칙
```

**실무 팁**: 파이프라인 문제는 "재현 가능한 최소 단위"로 좁혀가며 디버깅합니다. 워크플로우 전체를 의심하기보다, 실패한 step의 로그를 처음부터 끝까지 읽고 그 step만 로컬(또는 `act` 같은 로컬 실행 도구)로 재현해보는 것이 가장 빠릅니다.

---

# 20. 릴리스 태깅과 버전 자동화

배포할 때마다 버전 번호를 수동으로 정하면 실수가 생기기 쉽습니다. 커밋 메시지 규칙을 지키면 버전을 자동으로 계산할 수 있습니다.

```text
커밋 메시지 규칙 예 (Semantic Versioning과 연결)
Fix: ...      → 패치 버전 증가 (1.2.0 → 1.2.1)
Feat: ...     → 마이너 버전 증가 (1.2.1 → 1.3.0)
BREAKING CHANGE: ... → 메이저 버전 증가 (1.3.0 → 2.0.0)
```

```yaml
- name: 태그 생성 및 릴리스 노트 자동 작성
  uses: some-release-action@v1
  with:
    tag: v${{ steps.version.outputs.next }}
    generate_release_notes: true
```

이 저장소의 커밋 컨벤션(`Feat:`, `Fix:` 등 머릿말)은 이런 자동화와도 잘 맞습니다. 머릿말만 일관되게 지켜도, 버전 계산이나 릴리스 노트 생성을 도구가 대신할 수 있습니다.

**기본 상식**: 버전을 자동으로 올리더라도, 실제로 "이 버전을 배포해도 되는가"는 여전히 테스트 통과와 (필요하다면) 사람의 승인을 거쳐야 합니다. 버전 자동화는 번호를 매기는 반복 작업을 줄여줄 뿐, 배포 안전장치를 대체하지 않습니다.

---

# 21. 배포 빈도와 DORA 지표

팀의 배포 프로세스가 건강한지 판단하는 데 자주 쓰이는 4가지 지표(DORA metrics)입니다.

| 지표 | 의미 | 좋은 팀의 예시 |
| --- | --- | --- |
| 배포 빈도(Deployment Frequency) | 얼마나 자주 배포하는가 | 하루에도 여러 번 |
| 변경 리드 타임(Lead Time for Changes) | 커밋부터 배포까지 걸리는 시간 | 몇 시간 이내 |
| 변경 실패율(Change Failure Rate) | 배포 중 문제가 생기는 비율 | 15% 이하 |
| 복구 시간(Time to Restore Service) | 장애 발생 후 정상화까지 걸리는 시간 | 1시간 이내 |

**기본 상식**: 이 지표들은 "배포를 무조건 자주 하라"는 뜻이 아닙니다. 배포를 작고 자주 하면 한 번의 배포에 담기는 변경량이 줄어들어, 문제가 생겨도 원인을 좁히기 쉽고 롤백 범위도 작아진다는 것이 핵심입니다. 지표 자체를 목표로 삼기보다, 지표가 나빠지는 원인(파이프라인이 느리다, 테스트가 불안정하다 등)을 찾는 데 활용합니다.
