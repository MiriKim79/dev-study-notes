> **대상:** JavaScript 변수·함수·비동기 처리에 익숙하고, TypeScript 기본 타입 표기(`: string`, `: number`)는 써봤지만 실전 활용은 처음인 사람
> **목적:** 타입을 "귀찮은 표기"가 아니라 "버그를 미리 잡아주는 도구"로 쓰는 방법을 정리합니다

---

# 0. 시작 전에 — 자주 나오는 용어

JavaScript 기본 문법과 `: string`/`: number` 같은 기본 타입 표기는 이미 안다고 가정합니다. 여기서는 이 문서에서 새로 나오는 용어만 정리합니다.

| 용어 | 쉬운 설명 |
| --- | --- |
| 컴파일 시점(Compile Time) | 코드를 실제로 실행하기 전, TypeScript가 타입에 오류가 없는지 미리 검사하는 단계 |
| 런타임(Runtime) | 코드가 실제로 실행되는 시점. 컴파일 시점 검사를 통과해도 런타임에는 값이 다를 수 있음 |
| Union 타입 | "이 값 아니면 저 값"처럼 여러 타입 중 하나만 될 수 있음을 표현하는 것(`"a" \| "b"`) |
| Intersection 타입 | 여러 타입의 속성을 모두 합쳐야 하는 타입을 표현하는 것(`A & B`) |
| Generic(제네릭) | 함수·타입을 만들 때 실제 타입을 나중에 결정할 수 있도록 매개변수처럼 비워두는 것 |
| 유틸리티 타입 | 이미 정의한 타입을 변형해서 새 타입을 쉽게 만들어주는 TypeScript 내장 도구(`Pick`, `Omit`, `Partial` 등) |
| 타입 단언(Type Assertion, `as`) | "이 값은 이 타입이 맞다"고 TypeScript에게 직접 알려주는 것. 실제로 맞는지 검증해주진 않음 |
| 런타임 검증(Runtime Validation) | 실행 중에 실제 값이 기대한 형태가 맞는지 코드로 직접 확인하는 것 |
| `any` | 타입 검사를 사실상 꺼버리는 타입. 아무 값이나 허용해 오류를 놓치기 쉬움 |
| `unknown` | `any`처럼 타입을 모를 때 쓰지만, 실제로 무엇인지 확인(타입 좁히기)하기 전까지는 사용을 막아주는 안전한 타입 |
| 타입 가드(Type Guard) | `typeof`, `in` 같은 조건문으로 "이 값이 실제로 어떤 타입인지"를 좁혀나가는 것 |

---

# 1. Union, Intersection, Generic

## Union — "이거 아니면 저거"

```ts
type Status = "loading" | "success" | "error";

function renderMessage(status: Status) {
  if (status === "loading") return "불러오는 중...";
  if (status === "success") return "완료";
  return "오류가 발생했습니다";
}
```

문자열을 아무거나 받는 대신, 가능한 값을 정해두면 오타(`"lodaing"`)를 컴파일 시점에 바로 잡아줍니다.

## Intersection — "이것도 저것도 다"

```ts
type Timestamped = { createdAt: string };
type Course = { id: number; title: string };

type CourseWithTimestamp = Course & Timestamped;
// { id, title, createdAt }을 모두 가져야 함
```

## Generic — 타입을 매개변수처럼

```ts
function getFirst<T>(list: T[]): T | undefined {
  return list[0];
}

getFirst<number>([1, 2, 3]);        // number | undefined
getFirst<string>(["a", "b"]);       // string | undefined
```

같은 로직을 타입별로 중복 작성하지 않고, "이 함수는 어떤 타입의 배열이든 받아서 같은 타입을 돌려준다"는 관계를 표현합니다.

---

# 2. interface vs type

둘 다 객체의 모양을 정의하지만 용도가 조금 다릅니다.

| | `interface` | `type` |
| --- | --- | --- |
| 객체 모양 정의 | 가능 | 가능 |
| Union/Intersection | 불가 | 가능 |
| 같은 이름 재선언(병합) | 가능 (선언 병합) | 불가 |
| 라이브러리 확장 | 유리 (외부 타입에 속성 추가 가능) | 불가 |

```ts
interface Course {
  id: number;
  title: string;
}

type CourseStatus = "draft" | "published";   // Union은 interface로 불가능, type만 가능
```

**실무 팁**: 팀 컨벤션에 따라 다르지만, "객체·클래스 모양"은 `interface`, "Union이나 여러 타입을 조합"할 때는 `type`을 쓰는 것이 흔한 관례입니다. 정답이 하나만 있는 문제는 아니므로 팀 안에서 통일합니다.

---

# 3. 유틸리티 타입

이미 정의한 타입을 변형해서 재사용합니다. 매번 새로 타입을 쓰지 않아도 됩니다.

```ts
interface Course {
  id: number;
  title: string;
  price: number;
  description: string;
}

type CourseSummary = Pick<Course, "id" | "title">;
// { id: number; title: string }

type CourseWithoutId = Omit<Course, "id">;
// { title, price, description }

type PartialCourse = Partial<Course>;
// 모든 속성이 선택적(?)으로 바뀜 — 수정 API의 요청 바디 타입에 유용

type ReadonlyCourse = Readonly<Course>;
// 모든 속성을 수정 불가능하게
```

**실무 팁**: 강의 생성 API 요청 타입은 `Omit<Course, "id">`(id는 서버가 생성), 수정 API 요청 타입은 `Partial<Omit<Course, "id">>`(일부 필드만 보내도 됨)처럼 조합해서 쓰면, `Course` 타입 하나만 정의해두고 여러 상황에 재사용할 수 있습니다.

---

# 4. API 응답을 안전하게 다루기

TypeScript는 컴파일 시점에만 타입을 검사합니다. 서버가 실제로 보내주는 응답이 타입 선언과 다르면(백엔드가 필드를 바꿨거나 버그가 있으면) 런타임에는 조용히 틀린 값이 들어갑니다.

```ts
// 이렇게 타입만 선언하는 것은 "이 모양일 것이다"라는 약속일 뿐, 실제 검증은 아님
type CourseResponse = { id: number; title: string; price: number };

const res = await fetch("/api/courses/1");
const data = (await res.json()) as CourseResponse;   // 실제로는 검증되지 않음
```

zod 같은 런타임 검증 라이브러리를 함께 쓰면, 실제 값이 타입과 다를 때 바로 알아챌 수 있습니다.

```ts
import { z } from "zod";

const CourseSchema = z.object({
  id: z.number(),
  title: z.string(),
  price: z.number(),
});
type Course = z.infer<typeof CourseSchema>;   // 스키마에서 타입을 자동으로 뽑아냄

const res = await fetch("/api/courses/1");
const data = CourseSchema.parse(await res.json());   // 형식이 다르면 여기서 즉시 오류
```

**기본 상식**: `as CourseResponse`(타입 단언)는 "나는 이 값이 이 타입이라고 확신한다"고 TypeScript에게 우기는 것이지, 실제로 그런지 검증해주지 않습니다. 외부(서버, 사용자 입력)에서 오는 데이터는 타입 단언보다 런타임 검증을 우선합니다.

---

# 5. `any`를 피하는 법

## `any`의 문제

```ts
function process(data: any) {
  return data.value.toUpperCase();  // data가 실제로 뭔지 몰라도 컴파일 에러가 안 남
}
```

`any`는 타입 검사를 사실상 꺼버립니다. 컴파일은 통과하지만 실행 중 오류가 그대로 발생할 수 있어, TypeScript를 쓰는 의미가 없어집니다.

## `unknown`과 타입 가드

정말 타입을 모를 때는 `any` 대신 `unknown`을 쓰고, 사용하기 전에 타입을 좁힙니다.

```ts
function process(data: unknown) {
  if (typeof data === "object" && data !== null && "value" in data) {
    // 이 블록 안에서는 data에 value 속성이 있다고 안전하게 좁혀짐
    console.log((data as { value: string }).value);
  }
}
```

`unknown`은 `any`와 달리 "무엇인지 확인하기 전까지는 아무 동작도 허용하지 않아서", 검증을 빼먹는 실수를 컴파일 시점에 막아줍니다.

---

# 6. 자주 하는 실수

- 타입 에러를 없애려고 습관적으로 `any`를 붙임
- 외부 API 응답 타입을 실제 검증 없이 단언(`as`)만으로 처리
- `interface`와 `type`을 프로젝트 안에서 기준 없이 섞어 씀
- 제네릭을 안 쓰고 타입별로 거의 같은 함수를 복사해서 여러 개 만듦
- 컴파일 에러를 이해하지 않고 에러가 없어질 때까지 코드를 무작정 바꿔봄

---

# 7. 실전 체크리스트

- [ ] `any` 대신 구체적인 타입이나 `unknown` + 타입 가드를 쓰는가
- [ ] 외부에서 오는 데이터(API 응답, 사용자 입력)를 런타임에도 검증하는가
- [ ] 반복되는 타입을 유틸리티 타입(`Pick`/`Omit`/`Partial`)으로 재사용하는가
- [ ] `interface`/`type` 사용 기준이 팀 안에서 통일되어 있는가
- [ ] 타입 에러 메시지를 실제로 읽고 원인을 이해한 뒤 수정하는가
