> **용도:** 새 저장소의 `.github/ISSUE_TEMPLATE/`와 `pull_request_template.md`를 만들 때 복사해서 쓰는 기본 예시입니다.

# 1. 기능 Issue 템플릿

파일 예: `.github/ISSUE_TEMPLATE/feature.md`

````markdown
---
name: 기능 구현
about: 새로운 기능 작업
title: "[Feat] "
labels: ""
assignees: ""
---

## 목적
이 기능이 왜 필요한지 적습니다.

## 구현 범위
- [ ]
- [ ]

## 완료 조건
- [ ]
- [ ]

## 관련 화면 / API
- 화면:
- API:

## 다른 파트와 합의할 내용
- [ ]

## 참고 자료
-
````

---

# 2. 버그 Issue 템플릿

파일 예: `.github/ISSUE_TEMPLATE/bug.md`

````markdown
---
name: 버그
about: 오류 수정
title: "[Bug] "
labels: "bug"
assignees: ""
---

## 발생 상황

## 재현 순서
1.
2.
3.

## 예상 결과

## 실제 결과

## 오류 메시지 / 로그
```text
붙여넣기
```

## 발생 환경
- 브랜치:
- OS:
- 브라우저/런타임:
- 관련 버전:

## 원인
확인 후 작성

## 해결
확인 후 작성
````

---

# 3. Pull Request 템플릿

파일 예: `.github/pull_request_template.md`

````markdown
## 관련 Issue
Closes #

## 변경 내용
-
-

## 변경 이유

## 확인 방법
1.
2.

## 테스트
- [ ] 로컬 실행 확인
- [ ] 관련 기능 정상 동작
- [ ] 오류/예외 케이스 확인
- [ ] build/lint/test 실행 (프로젝트에 있는 항목만)

## 공유가 필요한 변경
- [ ] API 변경
- [ ] DB/마이그레이션 변경
- [ ] 환경변수 추가
- [ ] 패키지 추가
- [ ] 없음

## 스크린샷
UI 변경 시 첨부

## 리뷰어가 특히 봐야 할 부분
-
````

---

# 4. 템플릿 사용 원칙

- 체크박스를 많이 만드는 것보다 **실제로 팀이 확인할 항목만** 둡니다.
- UI 변경은 스크린샷을 첨부하면 리뷰가 빨라집니다.
- API·DB·환경변수 변경은 PR에서 눈에 띄게 표시합니다.
- “테스트 완료”라고 체크했다면 실제로 어떤 명령/흐름을 확인했는지 적습니다.
- AI 코딩 에이전트가 작성한 PR도 같은 템플릿을 사용합니다.
