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
