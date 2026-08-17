> **대상:** SELECT/JOIN 정도는 짤 줄 알고, SQLD 자격증을 처음 준비하는 사람
> **목적:** 한국데이터산업진흥원이 주관하는 SQLD(SQL 개발자) 시험 범위를 정리하고, 실무 SQL 지식을 시험에 나오는 형태로 다시 정리합니다
> **사용법:** 시험 정보(문항 수, 합격 기준, 접수 일정)는 회차마다 바뀔 수 있으니 이 문서로 개념을 잡은 뒤 반드시 공식 사이트(데이터자격검정 dataq.or.kr)에서 최신 공고를 확인하세요.
> **📝 이 문서는 핵심 요약노트입니다.** 정식 교재를 대체하지 않습니다 — 감을 잡고 복습하는 용도로 쓰고, 실전 대비는 공식 교재와 기출문제로 함께 준비하세요.

## 🎯 이 문서로 얼마나 커버되나

이 문서 내용을 완전히 이해하면 SQLD 시험 범위의 핵심 개념 대부분을 다루게 되어, 합격선(과목별 최소 점수 + 전체 평균 최소 점수 기준)을 무난히 넘길 수 있는 수준입니다. 다만 실제 시험은 세부 함정 보기·응용 계산 문제·최신 출제 경향이 반영될 수 있으므로 공식 기출문제(9번 섹션 링크)를 꼭 함께 풀어보세요. 정확한 합격 기준(과목별 커트라인, 전체 평균 기준 점수)은 회차 공고에 따라 다를 수 있으니 [데이터자격검정 공식 사이트](https://www.dataq.or.kr) 공고를 확인하세요.

**영역별 커버리지** (● = 이 문서가 다루는 상대적 비중, 절대 점수가 아닙니다)

| 영역 | 커버리지 |
| --- | --- |
| 데이터 모델링(엔터티·정규화·ERD) | ●●●●● |
| SQL 기본(SELECT·조인·서브쿼리) | ●●●●● |
| SQL 활용(윈도우 함수·집합 연산·계층형 질의) | ●●●●○ |
| 트랜잭션·DCL·관리 구문 | ●●●○○ |

---

# 0. 시작 전에 — 자주 나오는 용어

데이터베이스 기초 가이드에서 다룬 테이블·SQL 기본 문법(SELECT/WHERE/JOIN)은 이미 안다고 가정합니다. 여기서는 시험에서 새로 나오는 용어만 정리합니다.

| 용어 | 쉬운 설명 |
| --- | --- |
| 엔터티(Entity) | 데이터로 관리해야 하는 대상. 테이블로 구현되는 경우가 많음(예: 회원, 주문) |
| 속성(Attribute) | 엔터티가 가지는 세부 정보 하나(예: 회원의 이름, 이메일) |
| 관계(Relationship) | 엔터티와 엔터티 사이의 연관성(예: 회원이 주문을 여러 건 가질 수 있음) |
| 식별자(Identifier) | 엔터티 안의 각 행을 구분하는 값. 기본키(PK)가 대표적 |
| 정규화(Normalization) | 데이터 중복을 없애도록 테이블을 단계적으로 분리하는 설계 원칙 |
| 반정규화(De-normalization) | 조회 성능을 위해 일부러 정규화 원칙을 깨는 것 |
| 윈도우 함수(Window Function) | 행을 그룹으로 묶지 않으면서, 그룹별 순위·누계 같은 계산을 할 수 있게 해주는 SQL 함수 |
| 계층형 질의(Hierarchical Query) | 조직도처럼 "상위-하위" 관계로 이어진 데이터를 조회하는 SQL 문법 |
| DDL(데이터 정의어) | `CREATE`/`ALTER`/`DROP`처럼 테이블 등 객체 자체를 만들고 바꾸고 지우는 구문 |
| DCL(데이터 제어어) | `GRANT`/`REVOKE`처럼 다른 사용자에게 권한을 주거나 뺏는 구문 |
| TCL(트랜잭션 제어어) | `COMMIT`/`ROLLBACK`처럼 트랜잭션을 확정하거나 되돌리는 구문 |
| 식별자 관계 | 부모 엔터티의 기본키가 자식 엔터티의 기본키에도 포함되는 강한 종속 관계 |
| 슈퍼타입/서브타입 | 여러 엔터티가 공통 속성은 슈퍼타입으로 묶고, 다른 속성만 서브타입으로 나누는 모델링 방식 |
| 상관 서브쿼리(Correlated Subquery) | 바깥 쿼리의 각 행마다 안쪽 서브쿼리가 그 행 값을 참조해서 다시 실행되는 서브쿼리 |
| ROLLUP | `GROUP BY` 결과에 더해, 더 상위 단계의 소계·전체 합계까지 함께 계산해주는 확장 문법 |

---

# 1. 시험 구성

SQLD는 2과목으로 나뉩니다.

| 과목 | 다루는 내용 |
| --- | --- |
| 1과목: 데이터 모델링의 이해 | 엔터티·속성·관계, 정규화, ERD(개체관계도) 읽고 해석하기 |
| 2과목: SQL 기본 및 활용 | SELECT 기본 문법부터 서브쿼리, 조인, 윈도우 함수, 그룹 함수까지 |

시험은 객관식이며, **과목별 최소 점수**와 **전체 평균 최소 점수**를 모두 넘겨야 합격입니다(정확한 문항 수·배점·시간은 공식 사이트 공고 기준으로 확인).

---

# 2. 1과목 핵심 — 데이터 모델링

## ERD 읽는 법

ERD(Entity Relationship Diagram)는 엔터티 사이의 관계를 그림으로 표현한 것입니다. 시험에서는 ERD를 보고 "이 관계가 1:1인지 1:N인지, 그리고 그게 실제 SQL 테이블 구조로 어떻게 구현되는지"를 묻습니다.

```text
회원(1) --- (N)주문
→ 회원 한 명이 여러 주문을 가질 수 있음(1:N)
→ 실제 구현: 주문 테이블에 회원을 가리키는 외래키(FK)를 둠
```

## 정규화 단계 — 시험에서 정확한 정의로 자주 물어봄

| 단계 | 조건 |
| --- | --- |
| 제1정규형(1NF) | 한 칸에 값이 하나만 들어있어야 함(반복 그룹 제거) |
| 제2정규형(2NF) | 기본키의 일부에만 종속된 컬럼을 분리(부분 함수 종속 제거) |
| 제3정규형(3NF) | 기본키가 아닌 컬럼끼리 서로 종속된 관계를 분리(이행 함수 종속 제거) |

**기본 상식**: 실무에서는 "정규화가 왜 필요한가"라는 개념 이해가 중요하지만, SQLD 시험에서는 "이 예시 테이블은 몇 정규형을 위반했는가"처럼 정의를 정확히 적용하는 문제가 나옵니다. 각 단계의 조건을 예시와 함께 정확히 외워두는 것이 필요합니다.

## 정규화 단계별 실습 — 실제로 테이블을 쪼개보기

시험에서 가장 많이 틀리는 유형은 "이 테이블을 1NF→2NF→3NF로 순서대로 분해하라"는 계산형 문제입니다. 예시로 직접 따라가 봅니다.

```text
[분해 전] 수강신청(학번, 과목번호, 학생이름, 과목명, 교수번호, 교수이름, 성적)
```

**1단계 — 제1정규형(1NF): 반복 그룹/다중값 제거**

한 학생이 여러 과목을 신청하면 (학번, 과목번호, 성적)이 반복되는 구조를 만들 수 있으므로, "학번+과목번호"를 복합키로 하는 하나의 행 단위로 원자값만 남깁니다. 이미 위 테이블은 한 행에 값이 하나씩만 있어 1NF는 만족한 상태로 봅니다.

**2단계 — 제2정규형(2NF): 부분 함수 종속 제거**

기본키는 (학번, 과목번호) 복합키입니다. 이때 종속 관계를 하나씩 따져봅니다.

| 속성 | 무엇에 종속되는가 | 판정 |
| --- | --- | --- |
| 학생이름 | 학번에만 종속(과목번호와 무관) | 부분 함수 종속 → 분리 대상 |
| 과목명, 교수번호, 교수이름 | 과목번호에만 종속 | 부분 함수 종속 → 분리 대상 |
| 성적 | (학번, 과목번호) 전체에 종속 | 완전 함수 종속 → 그대로 유지 |

```text
[2NF 분해 후]
학생(학번, 학생이름)
과목(과목번호, 과목명, 교수번호, 교수이름)
수강(학번, 과목번호, 성적)
```

**3단계 — 제3정규형(3NF): 이행적 함수 종속 제거**

과목 테이블을 보면 "과목번호 → 교수번호 → 교수이름"처럼 기본키가 아닌 속성(교수번호)을 거쳐 다른 비키 속성(교수이름)이 결정되는 이행적 함수 종속이 남아 있습니다. 이를 다시 분리합니다.

```text
[3NF 분해 후]
학생(학번, 학생이름)
과목(과목번호, 과목명, 교수번호)
교수(교수번호, 교수이름)
수강(학번, 과목번호, 성적)
```

**기본 상식**: "부분 함수 종속"은 복합키의 일부만으로 결정되는 속성을 찾는 문제이고, "이행적 함수 종속"은 비키 속성이 다른 비키 속성을 거쳐 간접적으로 결정되는 속성을 찾는 문제입니다. 시험에서는 이 둘을 헷갈리게 섞은 보기가 자주 나오므로, "기본키 일부 → 속성"이면 2NF 위반, "비키 속성 → 비키 속성"이면 3NF 위반이라고 기계적으로 구분하는 연습이 필요합니다.

## 정규화 vs 반정규화 — 언제 일부러 규칙을 깨는가

| 구분 | 정규화 | 반정규화 |
| --- | --- | --- |
| 목적 | 데이터 중복 최소화, 무결성 확보 | 조회 성능 향상(조인 횟수 감소) |
| 부작용 | 조회 시 조인이 많아짐 | 데이터 중복으로 갱신 이상 위험 증가 |
| 적용 예 | 회원-주문-주문상세를 각각 테이블로 분리 | 주문 테이블에 회원이름 컬럼을 미리 복사해둬서 조인 없이 조회 |
| 대표 기법 | 1NF~3NF, BCNF 단계적 분해 | 테이블 병합, 중복 컬럼 추가, 요약 테이블(집계 테이블) 추가 |

**기본 상식**: 반정규화는 "정규화를 몰라서 안 한 것"이 아니라 "정규화된 상태에서 조회 성능 문제가 확인된 뒤, 트레이드오프를 감수하고 의도적으로 중복을 허용하는 것"입니다. 시험에서는 반정규화의 대표 기법(테이블 통합, 중복 컬럼, 집계 테이블)을 묻는 문제가 나옵니다.

## 데이터 모델과 SQL — ERD를 실제 테이블로 옮기기

1과목의 마지막 관문은 "그려놓은 ERD를 실제로 어떻게 SQL로 구현하는가"입니다.

```sql
-- 회원(1) --- (N)주문 관계를 실제 테이블로 구현
CREATE TABLE member (
  member_id   INT PRIMARY KEY,
  name        VARCHAR(50) NOT NULL
);

CREATE TABLE orders (
  order_id    INT PRIMARY KEY,
  member_id   INT NOT NULL,
  FOREIGN KEY (member_id) REFERENCES member(member_id)   -- 관계를 외래키로 구현
);
```

**기본 상식**: 엔터티는 테이블로, 속성은 컬럼으로, 식별자는 기본키(PK)로, 관계는 외래키(FK)로 옮겨집니다. 시험에서는 ERD 그림을 주고 "이걸 구현한 SQL로 맞는 것은?"이라거나, 반대로 테이블 정의(SQL)를 주고 "이 관계를 ERD로 그리면?"을 묻는 식으로 양방향으로 나옵니다.

## 식별자 관계 vs 비식별자 관계

부모 엔터티의 기본키가 자식 엔터티의 기본키에도 포함되는지에 따라 나뉩니다.

```sql
-- 식별자 관계: 부모(order)의 PK가 자식(order_item)의 PK 일부로도 쓰임
CREATE TABLE order_item (
  order_id    INT,
  item_seq    INT,
  PRIMARY KEY (order_id, item_seq),              -- 부모 PK가 자식 PK에 포함됨
  FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- 비식별자 관계: 부모의 PK가 자식의 일반 컬럼(FK)으로만 쓰임
CREATE TABLE review (
  review_id   INT PRIMARY KEY,                    -- 자기만의 독립적인 PK를 가짐
  order_id    INT,
  FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
```

**기본 상식**: 자식 엔터티가 부모 없이는 존재할 의미가 없을 만큼 강하게 종속되면 식별자 관계(예: 주문-주문상세), 부모와 독립적으로도 의미가 있으면 비식별자 관계(예: 주문-리뷰)를 씁니다. 시험에서는 "이 관계는 부모 PK가 자식 PK에 포함되는가"로 둘을 구분하는 문제가 나옵니다.

## 슈퍼타입/서브타입

여러 엔터티가 공통 속성은 공유하고, 일부만 다른 속성을 가질 때 쓰는 모델링 방식입니다.

```text
슈퍼타입: 회원(공통 속성 — 이름, 이메일, 가입일)
서브타입: 학생회원(학교명), 기업회원(사업자번호) — 각자만의 속성
```

| 구현 방식 | 설명 |
| --- | --- |
| 1:1 (개별 테이블) | 슈퍼타입과 서브타입을 각각 테이블로 분리, 서브타입 테이블은 PK가 곧 FK |
| 전체 통합 (단일 테이블) | 슈퍼타입+모든 서브타입 속성을 테이블 하나에 다 넣고, 구분 컬럼으로 서브타입을 구분 |
| 서브타입 통합 | 슈퍼타입은 없애고 서브타입마다 공통 속성을 중복해서 각자 테이블로 만듦 |

**기본 상식**: 조회가 잦고 서브타입 간 차이가 크면 개별 테이블로, 구조를 단순하게 유지하고 싶으면 단일 테이블로 구현하는 것이 일반적인 선택 기준입니다.

---

# 3. 2과목 핵심 — SQL 기본 및 활용

## 실행 순서 — 작성 순서와 다릅니다

```sql
SELECT department, COUNT(*)
FROM employees
WHERE salary > 3000
GROUP BY department
HAVING COUNT(*) > 5
ORDER BY department;
```

```text
실제 실행 순서: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY
```

`WHERE`는 그룹으로 묶기 *전* 개별 행을 거르고, `HAVING`은 그룹으로 묶은 *후* 그룹을 거릅니다. 이 실행 순서를 모르면 "왜 SELECT의 별칭을 WHERE에서 못 쓰는지" 같은 문제를 틀리게 됩니다.

## 조인(JOIN) 종류

| 종류 | 결과 |
| --- | --- |
| INNER JOIN | 양쪽 테이블에 모두 값이 있는 행만 |
| LEFT OUTER JOIN | 왼쪽 테이블은 전부, 오른쪽은 매칭되는 값만(없으면 NULL) |
| RIGHT OUTER JOIN | 오른쪽 테이블은 전부, 왼쪽은 매칭되는 값만 |
| FULL OUTER JOIN | 양쪽 테이블의 모든 행(매칭 안 되면 NULL) |

## 서브쿼리 — 쿼리 안의 쿼리

| 종류 | 반환하는 값 | 어디서 씀 |
| --- | --- | --- |
| 단일 행 서브쿼리 | 값 하나 | `WHERE salary > (SELECT AVG(salary) FROM employees)` |
| 다중 행 서브쿼리 | 여러 값 | `WHERE department IN (SELECT department FROM ...)` |
| 다중 컬럼 서브쿼리 | 여러 컬럼 조합 | `WHERE (dept, level) IN (SELECT dept, level FROM ...)` |
| 상관 서브쿼리(Correlated) | 바깥 쿼리의 각 행마다 다시 실행됨 | `WHERE EXISTS (SELECT 1 FROM orders o WHERE o.member_id = m.id)` |

```sql
-- 상관 서브쿼리: 바깥 쿼리(m)의 한 행씩 안쪽 서브쿼리에 대입해서 반복 실행
SELECT m.name
FROM member m
WHERE EXISTS (
  SELECT 1 FROM orders o WHERE o.member_id = m.member_id
);
```

**기본 상식**: 단일 행 서브쿼리 자리에 `=` 대신 다중 행이 나오는 서브쿼리를 넣으면 오류가 납니다(`단일-행 하위 질의에 2개 이상의 행이 리턴됩니다` 같은 에러). 서브쿼리가 몇 개의 값을 반환하는지 먼저 파악하는 것이 첫 단계입니다.

## 집합 연산자 — 여러 SELECT 결과를 합치기

| 연산자 | 결과 |
| --- | --- |
| `UNION` | 두 결과를 합치고 중복을 제거 |
| `UNION ALL` | 두 결과를 합치되 중복도 그대로 유지(더 빠름 — 중복 제거 연산이 없어서) |
| `INTERSECT` | 두 결과의 교집합(둘 다에 있는 행) |
| `MINUS` (또는 `EXCEPT`) | 첫 번째 결과에서 두 번째 결과에 있는 행을 뺌 |

**기본 상식**: 집합 연산자로 합치는 두 SELECT는 컬럼 개수와 데이터 타입이 서로 맞아야 합니다. 중복 제거가 필요 없다면 `UNION`보다 `UNION ALL`이 성능상 유리하다는 점이 자주 출제됩니다.

## GROUP BY 확장 — ROLLUP

```sql
SELECT department, position, SUM(salary)
FROM employees
GROUP BY ROLLUP(department, position);
```

일반 `GROUP BY`는 각 그룹의 소계만 보여주지만, `ROLLUP`은 그룹별 소계에 더해 **더 상위 단계의 중간 합계와 전체 합계까지** 한 번에 만들어줍니다(부서+직급별 합계, 부서별 합계, 전체 합계).

## 계층형 질의 — 조직도 같은 상하 구조 조회

```sql
-- Oracle 문법 예시
SELECT employee_id, manager_id, name, LEVEL
FROM employees
START WITH manager_id IS NULL     -- 최상위(루트)부터 시작
CONNECT BY PRIOR employee_id = manager_id;   -- 부모-자식 연결 조건
```

`START WITH`로 시작점(보통 최상위 관리자)을 정하고, `CONNECT BY PRIOR`로 "누가 누구의 부모인지" 연결 규칙을 정합니다. `LEVEL`은 그 행이 몇 단계 깊이에 있는지를 알려줍니다.

## 윈도우 함수

```sql
SELECT
  name, department, salary,
  RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank
FROM employees;
```

`GROUP BY`는 그룹별로 행을 하나로 뭉치지만, 윈도우 함수는 **원래 행을 그대로 유지하면서** 그룹별 순위·누계 같은 계산 결과를 추가로 보여줍니다. `PARTITION BY`(그룹을 나누는 기준), `ORDER BY`(그룹 안에서의 정렬)와 함께 자주 나옵니다.

## NULL 처리 주의

```sql
-- 주의: NULL은 '='로 비교할 수 없음
WHERE salary = NULL   -- 항상 결과 없음(틀림)
WHERE salary IS NULL  -- 올바른 문법
```

**기본 상식**: NULL은 "값이 없다"는 상태 자체이기 때문에 일반 비교 연산자(`=`, `!=`)로는 판정할 수 없고 `IS NULL`/`IS NOT NULL`을 씁니다. `COUNT(컬럼명)`은 NULL을 세지 않지만 `COUNT(*)`는 센다는 차이도 시험에 자주 나옵니다.

## 문자열·숫자·날짜 함수 심화

2과목에서 조인·서브쿼리 다음으로 자주 나오는 것이 내장 함수 문제입니다. 함수별로 실제 결과를 예측하는 연습이 필요합니다.

| 함수 | 예시 | 결과 |
| --- | --- | --- |
| `SUBSTR(문자열, 시작, 길이)` | `SUBSTR('20260817', 5, 2)` | `'08'` |
| `CONCAT` / `\|\|` | `CONCAT('SQL', 'D')` | `'SQLD'` |
| `TRIM` | `TRIM('  abc  ')` | `'abc'` |
| `LPAD(문자열, 길이, 채움문자)` | `LPAD('7', 3, '0')` | `'007'` |
| `ROUND(숫자, 자리수)` | `ROUND(1234.567, 1)` | `1234.6` |
| `TRUNC(숫자, 자리수)` | `TRUNC(1234.567, 1)` | `1234.5` |
| `CEIL` / `FLOOR` | `CEIL(4.1)` / `FLOOR(4.9)` | `5` / `4` |
| `MOD(숫자, 나눌수)` | `MOD(10, 3)` | `1` |
| `NVL(값, 대체값)` | `NVL(NULL, 0)` | `0` |
| `COALESCE(값1, 값2, ...)` | `COALESCE(NULL, NULL, 3)` | 첫 번째 NULL이 아닌 값 `3` |
| `DECODE(값, 조건1, 결과1, 기본값)` | `DECODE(등급, 'A', 100, 0)` | 등급이 'A'면 100, 아니면 0 |
| `TO_CHAR(날짜, 포맷)` | `TO_CHAR(SYSDATE, 'YYYY-MM-DD')` | `'2026-08-17'` |
| `MONTHS_BETWEEN(날짜1, 날짜2)` | 두 날짜 사이의 개월 수 | 소수점까지 계산 |

**`ROUND` vs `TRUNC` 자주 나오는 함정**: `ROUND`는 반올림, `TRUNC`는 그냥 잘라냅니다. `ROUND(1234.567, 1)`은 소수 둘째 자리(6)를 반올림해 `1234.6`이 되지만, `TRUNC(1234.567, 1)`은 그냥 잘라 `1234.5`가 됩니다. `NVL`과 `COALESCE`는 둘 다 NULL 대체 함수지만, `NVL`은 인자가 정확히 2개, `COALESCE`는 여러 개를 순서대로 검사해 첫 NULL이 아닌 값을 반환한다는 차이가 있습니다.

## 조인 결과 예측 — 계산 문제 유형 풀이

시험에는 표를 주고 "이 조인의 결과 행 수(또는 값)는?"을 직접 세어보게 하는 문제가 나옵니다. 예시로 연습합니다.

```text
[emp 테이블]                  [dept 테이블]
emp_id | name  | dept_id      dept_id | dept_name
1      | 철수  | 10           10      | 개발팀
2      | 영희  | 20           20      | 영업팀
3      | 민수  | NULL         30      | 인사팀
```

| 조인 | 결과 행 수 | 이유 |
| --- | --- | --- |
| `INNER JOIN` (emp.dept_id = dept.dept_id) | 2행 | 민수(dept_id=NULL)는 매칭 안 됨, 인사팀(30)은 emp에 없어서 제외 |
| `LEFT OUTER JOIN` (emp 기준) | 3행 | emp 전부 유지, 민수는 dept 쪽이 NULL로 채워짐 |
| `RIGHT OUTER JOIN` (dept 기준) | 3행 | dept 전부 유지, 인사팀(30)은 emp 쪽이 NULL로 채워짐 |
| `FULL OUTER JOIN` | 4행 | 양쪽에서 매칭 안 된 행(민수, 인사팀)까지 모두 NULL로 채워 포함 |
| `CROSS JOIN` | 3×3 = 9행 | 조건 없이 모든 조합(카티션 곱) |

**기본 상식**: 조인 결과 행 수를 예측하는 문제는 "조인 조건에 안 걸리는 행이 어느 쪽에 있는지", "그 행을 살릴지 버릴지"를 표로 직접 그려보면 실수가 줄어듭니다. 특히 `NULL`은 어떤 값과도 `=` 비교가 되지 않으므로(민수의 dept_id가 NULL이면 어떤 dept_id와도 매칭되지 않음) INNER JOIN에서 자동으로 빠진다는 점이 자주 출제됩니다.

## 트랜잭션 격리수준(Isolation Level)

여러 트랜잭션이 동시에 실행될 때 서로 얼마나 영향을 주고받을지 정하는 수준입니다. ACID의 I(Isolation, 고립성)와 직결됩니다.

| 격리수준 | 설명 | 발생 가능한 문제 |
| --- | --- | --- |
| READ UNCOMMITTED | 다른 트랜잭션이 커밋하지 않은 데이터도 읽을 수 있음 | Dirty Read(더티 리드) |
| READ COMMITTED | 커밋된 데이터만 읽음(대부분 DBMS 기본값) | Non-Repeatable Read(반복 조회 시 값이 바뀜) |
| REPEATABLE READ | 트랜잭션 시작 시점 기준으로 같은 행은 계속 같은 값 보장 | Phantom Read(새로 추가된 행이 조회될 수 있음) |
| SERIALIZABLE | 트랜잭션을 순차 실행한 것처럼 완전히 격리 | 동시성 저하(성능 부담 가장 큼) |

**기본 상식**: 격리수준이 높아질수록(READ UNCOMMITTED → SERIALIZABLE) 데이터 정합성은 좋아지지만 동시성(성능)은 떨어지는 트레이드오프가 있습니다. Dirty Read는 "커밋 전 값을 읽어서 생기는 문제", Non-Repeatable Read는 "같은 행을 두 번 읽었는데 그 사이 값이 바뀐 문제", Phantom Read는 "같은 조건으로 두 번 조회했는데 새로 추가된 행이 나타나는 문제"로 구분해서 외우면 헷갈리지 않습니다.

## DCL 심화 — 권한 부여와 회수

```sql
-- 사용자에게 특정 테이블 조회·수정 권한 부여
GRANT SELECT, UPDATE ON employees TO user_kim;

-- 부여한 권한을 다른 사용자에게도 넘겨줄 수 있는 권한까지 포함
GRANT SELECT ON employees TO user_kim WITH GRANT OPTION;

-- 권한 회수
REVOKE UPDATE ON employees FROM user_kim;
```

**기본 상식**: `WITH GRANT OPTION`을 붙이면 권한을 받은 사용자가 그 권한을 다시 다른 사용자에게 부여할 수 있습니다. `REVOKE`로 원래 권한을 회수하면, `WITH GRANT OPTION`으로 전달된 하위 권한도 함께 회수되는 것이 일반적입니다(DBMS에 따라 CASCADE 옵션으로 명시하기도 함).

## 관리 구문 — SELECT 말고도 SQL이 하는 일

지금까지 다룬 SELECT는 데이터를 "조회"하는 구문(DML)입니다. SQLD는 데이터를 정의하고, 권한을 주고, 트랜잭션을 마무리하는 구문도 따로 다룹니다.

| 분류 | 대표 구문 | 하는 일 |
| --- | --- | --- |
| DDL(데이터 정의어) | `CREATE`, `ALTER`, `DROP` | 테이블 등 객체 자체를 만들고 바꾸고 지움 |
| DML(데이터 조작어) | `SELECT`, `INSERT`, `UPDATE`, `DELETE` | 테이블 안의 데이터를 조회·추가·수정·삭제 |
| DCL(데이터 제어어) | `GRANT`, `REVOKE` | 다른 사용자에게 권한을 주거나 뺏음 |
| TCL(트랜잭션 제어어) | `COMMIT`, `ROLLBACK`, `SAVEPOINT` | 트랜잭션을 확정하거나 되돌림 |

```sql
BEGIN;
UPDATE accounts SET balance = balance - 1000 WHERE id = 1;
SAVEPOINT before_deposit;               -- 되돌아올 지점 표시
UPDATE accounts SET balance = balance + 1000 WHERE id = 2;
ROLLBACK TO before_deposit;             -- 두 번째 UPDATE만 취소
COMMIT;                                  -- 첫 번째 UPDATE만 최종 반영
```

**기본 상식**: `DROP`은 테이블 구조 자체를 삭제(되돌리기 어려움), `DELETE`는 데이터만 삭제(구조는 남음), `TRUNCATE`는 데이터를 전부 비우되 구조는 남기고 삭제 로그를 거의 남기지 않아 `DELETE`보다 빠르다는 차이가 자주 출제됩니다.

---

# 4. 연습문제

> ⚠️ 아래 문제는 개념 이해를 돕기 위해 직접 만든 연습문제이며, 실제 SQLD 기출문제가 아닙니다.

**문제 1.** 다음 중 제3정규형(3NF)을 만족하지 않는 상황은?
A) 기본키가 아닌 두 컬럼이 서로 종속 관계에 있다
B) 한 컬럼에 여러 값이 들어있다
C) 기본키 일부에만 종속된 컬럼이 있다
D) 모든 컬럼이 기본키에 완전 함수 종속되어 있다

**문제 2.** `LEFT OUTER JOIN`에 대한 설명으로 옳은 것은?
A) 양쪽 테이블에 모두 값이 있는 행만 반환한다
B) 왼쪽 테이블의 모든 행을 반환하고, 매칭되지 않으면 오른쪽 값은 NULL로 채운다
C) 오른쪽 테이블의 모든 행을 반환한다
D) 두 테이블의 교집합만 반환한다

**문제 3.** 테이블의 데이터는 모두 삭제하지만 테이블 구조 자체는 남기고, `DELETE`보다 빠르게 동작하는 구문은?
A) `DROP TABLE`
B) `TRUNCATE TABLE`
C) `ALTER TABLE`
D) `ROLLBACK`

**문제 4.** 두 SELECT 결과를 합치되, 중복된 행도 그대로 남기고 싶을 때 쓰는 것은?
A) `UNION`
B) `UNION ALL`
C) `INTERSECT`
D) `MINUS`

**문제 5.** 바깥 쿼리의 각 행마다 그 값을 참조해서 다시 실행되는 서브쿼리를 가리키는 말은?
A) 단일 행 서브쿼리
B) 다중 행 서브쿼리
C) 상관 서브쿼리
D) 스칼라 서브쿼리

**정답**: 1번 A / 2번 B / 3번 B / 4번 B / 5번 C

---

# 5. 실전 연습문제 (정답 클릭 확인)

> ⚠️ 이 섹션의 문제는 실제 기출 유형·난이도를 참고해 새로 만든 오리지널 연습문제이며, 실제 기출문제 원문이 아닙니다. 정답을 클릭하면 해설이 펼쳐집니다.

**Q1.** 다음 중 이행적 함수 종속을 제거해 제3정규형(3NF)을 만족시키는 과정에서 하는 일로 가장 알맞은 것은?
A) 반복되는 그룹을 별도 테이블로 분리한다
B) 기본키 일부에만 종속된 속성을 분리한다
C) 기본키가 아닌 속성이 다른 비키 속성에 종속된 관계를 분리한다
D) 후보키를 기본키로 지정한다

<details class="quiz-answer">
<summary>정답 보기</summary>
<div class="quiz-answer-body">
<p><span class="quiz-correct">정답: C</span></p>
<p>1NF는 반복 그룹 제거, 2NF는 부분 함수 종속 제거, 3NF는 비키 속성 간 종속(이행적 종속)을 제거하는 단계입니다.</p>
</div>
</details>

**Q2.** `SELECT dept, AVG(salary) FROM emp GROUP BY dept HAVING AVG(salary) > 3000;` 실행 순서로 옳은 것은?
A) SELECT → FROM → GROUP BY → HAVING
B) FROM → GROUP BY → HAVING → SELECT
C) FROM → HAVING → GROUP BY → SELECT
D) GROUP BY → FROM → SELECT → HAVING

<details class="quiz-answer">
<summary>정답 보기</summary>
<div class="quiz-answer-body">
<p><span class="quiz-correct">정답: B</span></p>
<p>SQL은 FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY 순으로 처리됩니다.</p>
</div>
</details>

**Q3.** 두 테이블을 조인할 때 왼쪽 테이블의 모든 행을 반환하고, 오른쪽에 매칭되는 값이 없으면 NULL로 채우는 조인은?
A) INNER JOIN
B) RIGHT OUTER JOIN
C) LEFT OUTER JOIN
D) CROSS JOIN

<details class="quiz-answer">
<summary>정답 보기</summary>
<div class="quiz-answer-body">
<p><span class="quiz-correct">정답: C</span></p>
<p>LEFT OUTER JOIN은 왼쪽 테이블 기준으로 전부 반환하고, 매칭이 없으면 오른쪽 컬럼을 NULL로 채웁니다.</p>
</div>
</details>

**Q4.** `WHERE dept_id IN (SELECT dept_id FROM dept WHERE region = 'SEOUL')`에서 서브쿼리의 종류는?
A) 단일 행 서브쿼리
B) 다중 행 서브쿼리
C) 상관 서브쿼리
D) 스칼라 서브쿼리

<details class="quiz-answer">
<summary>정답 보기</summary>
<div class="quiz-answer-body">
<p><span class="quiz-correct">정답: B</span></p>
<p>IN 연산자와 함께 여러 값을 반환할 수 있는 서브쿼리이므로 다중 행 서브쿼리입니다.</p>
</div>
</details>

**Q5.** 다음 중 슈퍼타입/서브타입 모델링에서 '1:1(개별 테이블)' 방식의 특징으로 옳은 것은?
A) 하나의 테이블에 모든 속성을 몰아넣는다
B) 서브타입마다 별도 테이블을 만들고 PK를 FK로도 사용한다
C) 슈퍼타입 자체를 아예 없애고 각 서브타입에 공통 속성을 중복 저장한다
D) 관계형 모델에서는 사용할 수 없다

<details class="quiz-answer">
<summary>정답 보기</summary>
<div class="quiz-answer-body">
<p><span class="quiz-correct">정답: B</span></p>
<p>개별 테이블(1:1) 방식은 슈퍼타입·서브타입을 각각 테이블로 만들고, 서브타입 테이블의 PK가 곧 슈퍼타입을 참조하는 FK가 됩니다.</p>
</div>
</details>

**Q6.** `UNION`과 `UNION ALL`의 차이로 옳은 것은?
A) UNION ALL이 중복을 제거하고 UNION은 유지한다
B) UNION이 중복을 제거하고 UNION ALL은 유지한다
C) 둘 다 중복을 제거한다
D) 둘 다 중복을 유지한다

<details class="quiz-answer">
<summary>정답 보기</summary>
<div class="quiz-answer-body">
<p><span class="quiz-correct">정답: B</span></p>
<p>UNION은 결과를 합친 뒤 중복 제거 연산까지 수행하고, UNION ALL은 중복 제거 없이 그대로 합쳐 더 빠릅니다.</p>
</div>
</details>

**Q7.** 윈도우 함수에서 같은 그룹 내 순위를 매기되, 동점자에게 같은 순위를 주고 다음 순위를 건너뛰는 함수는?
A) ROW_NUMBER()
B) RANK()
C) DENSE_RANK()
D) NTILE()

<details class="quiz-answer">
<summary>정답 보기</summary>
<div class="quiz-answer-body">
<p><span class="quiz-correct">정답: B</span></p>
<p>RANK()는 동점에 같은 순위를 부여하고 다음 순위를 건너뜁니다(1,2,2,4). 건너뛰지 않는 것은 DENSE_RANK(), 동점 없이 순번만 매기는 것은 ROW_NUMBER()입니다.</p>
</div>
</details>

**Q8.** (OX) `DELETE FROM table;`은 테이블 구조를 삭제하지 않지만, `DROP TABLE table;`은 테이블 구조 자체를 삭제한다.

<details class="quiz-answer">
<summary>정답 보기</summary>
<div class="quiz-answer-body">
<p><span class="quiz-correct">정답: O</span></p>
<p>DELETE는 데이터(행)만 지우고 구조는 남기며, DROP은 테이블 정의 자체를 제거합니다.</p>
</div>
</details>

**Q9.** (OX) 상관 서브쿼리(Correlated Subquery)는 바깥 쿼리와 무관하게 한 번만 실행된다.

<details class="quiz-answer">
<summary>정답 보기</summary>
<div class="quiz-answer-body">
<p><span class="quiz-correct">정답: X</span></p>
<p>상관 서브쿼리는 바깥 쿼리의 각 행마다 그 행의 값을 참조해 반복 실행됩니다. 한 번만 실행되는 것은 비상관 서브쿼리입니다.</p>
</div>
</details>

**Q10.** (단답형) 부모 엔터티의 기본키가 자식 엔터티의 기본키 일부로 상속되어, 부모 없이는 자식이 존재할 수 없는 강한 종속 관계를 무엇이라 하는가?

<details class="quiz-answer">
<summary>정답 보기</summary>
<div class="quiz-answer-body">
<p><span class="quiz-correct">정답: 식별자 관계(Identifying Relationship)</span></p>
<p>식별자 관계는 부모의 PK가 자식의 PK 구성요소로 포함되는 강한 종속 관계이며, 반대로 부모 PK가 자식의 일반 컬럼(FK)으로만 쓰이면 비식별자 관계입니다.</p>
</div>
</details>

**Q11.** 다음 중 집계함수와 함께 사용할 때, GROUP BY로 묶인 결과에 대한 조건을 지정하는 절은?
A) WHERE
B) HAVING
C) ORDER BY
D) QUALIFY

<details class="quiz-answer">
<summary>정답 보기</summary>
<div class="quiz-answer-body">
<p><span class="quiz-correct">정답: B</span></p>
<p>WHERE는 그룹화 전 개별 행을 필터링하고, HAVING은 GROUP BY로 집계된 결과(그룹)에 대한 조건을 지정합니다. 집계함수는 HAVING 절에서만 조건으로 사용할 수 있습니다.</p>
</div>
</details>

**Q12.** 정규화 단계 중, 기본키가 아닌 속성이 기본키 전체가 아니라 일부에만 종속되는 부분 함수 종속을 제거하는 단계는?
A) 제1정규형(1NF)
B) 제2정규형(2NF)
C) 제3정규형(3NF)
D) BCNF

<details class="quiz-answer">
<summary>정답 보기</summary>
<div class="quiz-answer-body">
<p><span class="quiz-correct">정답: B</span></p>
<p>제2정규형은 복합키(2개 이상 컬럼으로 구성된 기본키)를 가진 테이블에서, 기본키의 일부에만 종속되는 속성(부분 함수 종속)을 별도 테이블로 분리합니다.</p>
</div>
</details>

**Q13.** 다음 중 두 테이블에 공통으로 존재하는 값만 결과로 반환하는 조인은?
A) LEFT OUTER JOIN
B) RIGHT OUTER JOIN
C) INNER JOIN
D) FULL OUTER JOIN

<details class="quiz-answer">
<summary>정답 보기</summary>
<div class="quiz-answer-body">
<p><span class="quiz-correct">정답: C</span></p>
<p>INNER JOIN은 조인 조건을 만족하는(양쪽 테이블에 모두 존재하는) 행만 반환합니다. OUTER JOIN 계열은 한쪽 또는 양쪽에 없는 값도 NULL로 채워 포함합니다.</p>
</div>
</details>

**Q14.** `CASE WHEN score >= 90 THEN 'A' WHEN score >= 80 THEN 'B' ELSE 'C' END`와 같은 SQL 구문의 용도로 가장 알맞은 것은?
A) 여러 테이블을 하나로 합침
B) 조건에 따라 다른 값을 반환(조건부 분기)
C) 중복된 행을 제거
D) 데이터 타입을 변환

<details class="quiz-answer">
<summary>정답 보기</summary>
<div class="quiz-answer-body">
<p><span class="quiz-correct">정답: B</span></p>
<p>CASE WHEN 구문은 프로그래밍 언어의 if-else처럼, 조건에 따라 SELECT 결과 값을 다르게 반환하는 조건부 분기 표현식입니다.</p>
</div>
</details>

**Q15.** 하나의 엔터티가 자기 자신을 참조하는 관계(예: 직원 테이블에서 상급자도 직원인 경우)를 나타내는 모델링 개념은?
A) 슈퍼타입/서브타입
B) 순환관계(Recursive Relationship, 자기참조 관계)
C) 다대다 관계
D) 배타적 관계

<details class="quiz-answer">
<summary>정답 보기</summary>
<div class="quiz-answer-body">
<p><span class="quiz-correct">정답: B</span></p>
<p>순환관계(자기참조 관계)는 하나의 엔터티 내에서 인스턴스끼리 관계를 맺는 경우로, 조직도의 상하 관계, 게시글의 댓글-대댓글 구조 등이 대표적인 예입니다.</p>
</div>
</details>

**Q16.** (OX) 인덱스(Index)를 생성하면 SELECT 조회 성능은 향상되지만, INSERT/UPDATE/DELETE 시에는 인덱스도 함께 갱신해야 하므로 쓰기 성능에는 부담이 될 수 있다.

<details class="quiz-answer">
<summary>정답 보기</summary>
<div class="quiz-answer-body">
<p><span class="quiz-correct">정답: O</span></p>
<p>인덱스는 조회 속도를 높이는 대가로, 데이터 변경 시마다 인덱스 구조(B-Tree 등)도 함께 갱신해야 하므로 쓰기 작업의 오버헤드가 늘어납니다.</p>
</div>
</details>

**Q17.** (단답형) 하나의 SQL문 안에 포함된 또 다른 SELECT문으로, 괄호로 감싸 다른 쿼리의 일부(WHERE, FROM 등)로 사용되는 것을 무엇이라 하는가?

<details class="quiz-answer">
<summary>정답 보기</summary>
<div class="quiz-answer-body">
<p><span class="quiz-correct">정답: 서브쿼리(Subquery)</span></p>
<p>서브쿼리는 사용 위치에 따라 스칼라 서브쿼리(SELECT 절), 인라인 뷰(FROM 절), 중첩 서브쿼리(WHERE 절) 등으로 구분되며, 바깥 쿼리와의 연관 여부에 따라 상관/비상관 서브쿼리로도 나뉩니다.</p>
</div>
</details>

---

# 6. 합격 꿀팁

- **2과목(SQL)에 시간을 더 배분하세요.** 1과목(모델링)보다 문항 수·배점이 훨씬 큽니다.
- SQL 문제를 풀 때 눈으로만 읽지 말고, 실행 순서(FROM→WHERE→GROUP BY→HAVING→SELECT→ORDER BY)대로 손으로 직접 중간 결과를 적어보며 채점하세요. 몇 번만 해보면 몸에 붙습니다.
- 정규화 단계·조인 종류처럼 헷갈리는 개념은 나만의 비교표를 직접 만들어두면, 시험장에서 "이게 뭐였더라" 하는 시간을 줄여줍니다.
- 가능하면 무료로 설치할 수 있는 DB(MySQL 등)에 연습문제의 쿼리를 직접 돌려보세요. 이론으로만 외운 것과 실제로 결과를 눈으로 본 것은 오래 남는 정도가 다릅니다.

---

# 7. 자주 하는 실수

- 정규화 단계별 정의를 실무 감각으로만 어림짐작해서 헷갈림
- SQL 실행 순서를 모르고 작성 순서(SELECT부터)로 착각
- NULL을 `=`로 비교하려다 오답
- 조인 종류별 결과 차이를 직접 손으로 안 그려보고 암기만 함
- 단일 행 서브쿼리 자리에 여러 값을 반환하는 서브쿼리를 넣어 오류
- `UNION`과 `UNION ALL`을 성능 차이 없이 아무거나 사용

---

# 8. 실전 체크리스트

- [ ] 정규화 1~3단계 조건을 예시와 함께 설명할 수 있는가
- [ ] 식별자 관계와 비식별자 관계를 구분할 수 있는가
- [ ] SQL의 실제 실행 순서(FROM→WHERE→GROUP BY→HAVING→SELECT→ORDER BY)를 아는가
- [ ] 조인 4종류의 결과 차이를 직접 그려서 구분할 수 있는가
- [ ] 서브쿼리 종류(단일행/다중행/상관)별로 어떤 연산자와 함께 쓰는지 아는가
- [ ] `UNION`과 `UNION ALL`의 차이를 설명할 수 있는가
- [ ] 윈도우 함수와 GROUP BY의 차이를 설명할 수 있는가
- [ ] DDL/DML/DCL/TCL 네 가지 분류와 대표 구문을 아는가
- [ ] 최신 시험 공고(문항 수, 합격 기준, 접수 일정)를 공식 사이트에서 확인했는가

---

# 9. 진짜 기출문제는 여기서

공식 기출문제·자료는 [한국데이터산업진흥원 데이터자격검정(dataq.or.kr)](https://www.dataq.or.kr)에서 확인하세요. 사이트 접속 후 자료실 메뉴에서 SQLD 기출문제를 내려받을 수 있습니다(정확한 하위 경로는 사이트 개편에 따라 바뀔 수 있어 직접 메뉴를 찾아 들어가는 것을 권장합니다). 이 문서는 시험 범위와 개념 정리만 제공합니다.

---

# 10. AI로 나만의 모의고사 만들기

아래 프롬프트를 ChatGPT, Claude 등 AI 챗봇에 그대로 복사해서 붙여넣으면 이 문서 범위에 맞는 추가 연습문제를 새로 만들어줍니다. 실제 기출문제가 아닌 창작 문제이므로, 감 잡기·복습용으로 활용하고 진짜 기출은 9번 섹션의 공식 링크를 이용하세요.

```text
너는 SQLD(SQL 개발자) 자격증 출제 전문가야. 아래 조건으로 실전 모의고사를 만들어줘.
- 과목: 1과목 데이터 모델링의 이해(엔터티·정규화·ERD), 2과목 SQL 기본 및 활용(조인·서브쿼리·윈도우 함수 등)
- 문제 유형: 객관식(4지선다) 8문제 + 단답형 2문제, 총 10문제
- 난이도: 실제 SQLD 시험과 비슷한 수준
- 각 문제 아래에 정답과 해설을 함께 제시해줘
- 이 문제들은 네가 새로 만든 창작 문제이며 실제 기출문제 원문이 아님을 마지막에 명시해줘
- 특히 정규화, 조인, 윈도우 함수, 서브쿼리 영역에서 고르게 출제해줘
```

---

# 11. 자주 헷갈리는 개념 정리

| 헷갈리는 짝 | 구분 |
| --- | --- |
| WHERE vs HAVING | WHERE는 그룹화 전 개별 행을 필터링, HAVING은 GROUP BY로 묶인 후 집계 결과를 필터링 |
| INNER JOIN vs OUTER JOIN | INNER는 양쪽 다 일치하는 행만, OUTER(LEFT/RIGHT/FULL)는 일치하지 않아도 한쪽(또는 양쪽) 행을 NULL로 채워 포함 |
| DELETE vs TRUNCATE vs DROP | DELETE는 조건별 행 삭제(롤백 가능, WHERE 사용 가능), TRUNCATE는 테이블 전체 행 삭제(구조는 유지, 롤백 대체로 불가), DROP은 테이블 자체를 삭제 |
| 제1정규형 vs 제2정규형 vs 제3정규형 | 1NF는 원자값만 허용(반복 그룹 제거), 2NF는 부분 함수 종속 제거(복합키의 일부에만 종속된 속성 분리), 3NF는 이행 함수 종속 제거(비키 속성이 다른 비키 속성에 종속되는 것 제거) |
| 서브쿼리 vs 뷰(VIEW) | 서브쿼리는 쿼리 안에 일회성으로 포함된 쿼리, 뷰는 쿼리 자체를 저장해두고 테이블처럼 재사용하는 가상 테이블 |
| 집계함수 vs 윈도우 함수 | 집계함수(SUM, COUNT 등)는 GROUP BY로 여러 행을 한 행으로 요약, 윈도우 함수는 행을 그대로 유지하면서 그룹별 계산값을 각 행에 함께 표시(`OVER(PARTITION BY ...)`) |

---

# 12. 시험 직전 최종 점검 리스트

- [ ] 정규화 1~3정규형을 예시 테이블로 직접 분해할 수 있는가
- [ ] ERD에서 관계의 카디널리티(1:1, 1:N, N:M)를 구분할 수 있는가
- [ ] JOIN 종류별로 결과 행이 어떻게 달라지는지 표로 그려볼 수 있는가
- [ ] 서브쿼리(스칼라, 상관 서브쿼리)와 조인의 차이·성능 차이를 설명할 수 있는가
- [ ] 윈도우 함수(`ROW_NUMBER`, `RANK`, `DENSE_RANK`)의 결과 차이를 예시로 구분할 수 있는가
- [ ] 트랜잭션의 4가지 속성(ACID)을 각각 한 문장으로 설명할 수 있는가
