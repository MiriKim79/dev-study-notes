> **대상:** SELECT/JOIN 정도는 짤 줄 알고, SQLD 자격증을 처음 준비하는 사람
> **목적:** 한국데이터산업진흥원이 주관하는 SQLD(SQL 개발자) 시험 범위를 정리하고, 실무 SQL 지식을 시험에 나오는 형태로 다시 정리합니다
> **사용법:** 시험 정보(문항 수, 합격 기준, 접수 일정)는 회차마다 바뀔 수 있으니 이 문서로 개념을 잡은 뒤 반드시 공식 사이트(데이터자격검정 dataq.or.kr)에서 최신 공고를 확인하세요.

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

# 5. 합격 꿀팁

- **2과목(SQL)에 시간을 더 배분하세요.** 1과목(모델링)보다 문항 수·배점이 훨씬 큽니다.
- SQL 문제를 풀 때 눈으로만 읽지 말고, 실행 순서(FROM→WHERE→GROUP BY→HAVING→SELECT→ORDER BY)대로 손으로 직접 중간 결과를 적어보며 채점하세요. 몇 번만 해보면 몸에 붙습니다.
- 정규화 단계·조인 종류처럼 헷갈리는 개념은 나만의 비교표를 직접 만들어두면, 시험장에서 "이게 뭐였더라" 하는 시간을 줄여줍니다.
- 가능하면 무료로 설치할 수 있는 DB(MySQL 등)에 연습문제의 쿼리를 직접 돌려보세요. 이론으로만 외운 것과 실제로 결과를 눈으로 본 것은 오래 남는 정도가 다릅니다.

---

# 6. 자주 하는 실수

- 정규화 단계별 정의를 실무 감각으로만 어림짐작해서 헷갈림
- SQL 실행 순서를 모르고 작성 순서(SELECT부터)로 착각
- NULL을 `=`로 비교하려다 오답
- 조인 종류별 결과 차이를 직접 손으로 안 그려보고 암기만 함
- 단일 행 서브쿼리 자리에 여러 값을 반환하는 서브쿼리를 넣어 오류
- `UNION`과 `UNION ALL`을 성능 차이 없이 아무거나 사용

---

# 7. 실전 체크리스트

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

# 8. 진짜 기출문제는 여기서

공식 기출문제·자료는 **한국데이터산업진흥원 데이터자격검정(dataq.or.kr)**에서 확인하세요. 이 사이트는 시험 범위와 개념 정리만 제공합니다.
