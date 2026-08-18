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

`any`는 타입 검사를 사실상 꺼버립니다. 컴파일은 통과하지만 실행 중 오류가 그대로 발생할 수 있어, TypeScript를 쓰는 의미가 상당 부분 사라집니다.

`any`를 무조건 쓰면 안 되는 것은 아닙니다. JavaScript 코드를 TypeScript로 마이그레이션하는 과도기, 타입 정의가 없는 오래된 라이브러리를 감쌀 때처럼 정말 타입을 특정하기 어려운 예외적인 상황에서는 임시로 `any`를 쓰기도 합니다. 다만 이런 경우에도 "왜 `any`를 썼는지" 주석을 남기고, 가능하면 아래 `unknown` + 타입 가드로 좁혀서 사용 범위를 최소화하는 것이 안전합니다.

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

---

# 8. 더 많은 유틸리티 타입

`Pick`/`Omit`/`Partial` 외에도 실무에서 자주 쓰는 유틸리티 타입들이 있습니다.

```ts
interface Course {
  id: number;
  title: string;
  price: number;
  tags: string[];
}

type RequiredCourse = Required<Course>;
// 모든 속성을 필수로(반대로 옵셔널을 강제로 채워야 하는 상황에 사용)

type CourseRecord = Record<string, Course>;
// { [key: string]: Course } — id를 키로 하는 강의 맵을 표현할 때 유용

type CourseKeys = keyof Course;
// "id" | "title" | "price" | "tags" — 속성 이름들의 Union

type PriceType = Course["price"];
// number — 특정 속성의 타입만 뽑아옴(Indexed Access Type)

type Extracted = Extract<"a" | "b" | "c", "a" | "c">;   // "a" | "c"
type Excluded = Exclude<"a" | "b" | "c", "a">;           // "b" | "c"

type NonNullableTitle = NonNullable<string | null | undefined>;  // string
```

**실무 팁**: `Record<string, Course>`처럼 "id를 키로 하는 맵"을 다룰 때는, 검색 속도(배열의 `find`보다 객체 조회가 빠름)를 챙기면서도 `keyof`/`Record`로 타입 안전성을 유지할 수 있습니다.

---

# 9. 함수 타입과 오버로드

## 함수 타입 표현

```ts
type Fetcher = (url: string) => Promise<Response>;

const fetchCourse: Fetcher = async (url) => {
  return fetch(url);
};

// 콜백 함수의 타입도 명시적으로
function onSuccess(callback: (data: Course) => void) {
  // ...
}
```

## 함수 오버로드(Overload) — 입력에 따라 반환 타입이 달라질 때

함수 오버로드란, 같은 함수라도 "숫자 하나를 넣으면 결과 하나, 배열을 넣으면 결과 배열"처럼 인자 형태에 따라 반환 타입이 달라짐을 TypeScript에게 미리 알려주는 방법입니다. 아래처럼 실제 구현부 위에 가능한 호출 형태를 나열해 둡니다.

```ts
function getCourse(id: number): Course;
function getCourse(ids: number[]): Course[];
function getCourse(idOrIds: number | number[]): Course | Course[] {
  if (Array.isArray(idOrIds)) {
    return idOrIds.map((id) => findCourse(id));
  }
  return findCourse(idOrIds);
}

const one = getCourse(1);       // Course
const many = getCourse([1, 2]); // Course[]
```

호출하는 쪽에서 넘긴 인자 형태에 따라 TypeScript가 정확한 반환 타입을 추론해 줍니다. Union으로만 처리하면 호출부에서 매번 타입을 좁혀야 하는 번거로움을 줄일 수 있습니다.

---

# 10. 타입 좁히기(Narrowing) 심화

## 판별 유니온(Discriminated Union)

"로딩 중 / 성공 / 실패"처럼 상태가 여러 개고 상태마다 가진 필드가 다를 때, 모든 상태에 공통으로 들어있는 필드(아래 예의 `status`)를 기준으로 분기하면 TypeScript가 각 분기 안에서 나머지 필드까지 정확한 타입으로 좁혀줍니다. 이런 공통 필드를 "판별자(discriminant)"라고 부릅니다.

```ts
type LoadingState = { status: "loading" };
type SuccessState = { status: "success"; data: Course[] };
type ErrorState = { status: "error"; message: string };

type FetchState = LoadingState | SuccessState | ErrorState;

function render(state: FetchState) {
  switch (state.status) {
    case "loading":
      return "불러오는 중...";
    case "success":
      return state.data.map((c) => c.title).join(", ");   // data 접근 가능
    case "error":
      return state.message;                                 // message 접근 가능
  }
}
```

각 `case` 블록 안에서는 TypeScript가 `state`를 해당 타입으로 정확히 좁혀주므로, `success`가 아닌데 `data`에 접근하는 실수를 컴파일 시점에 막아줍니다. `switch`에 없는 케이스가 생기면(새 상태 추가) 아래처럼 컴파일 에러로 알아챌 수 있습니다.

```ts
function assertNever(x: never): never {
  throw new Error("처리하지 않은 케이스: " + x);
}
// switch의 default에서 assertNever(state)를 호출하면,
// 새 상태를 추가했는데 분기 처리를 빠뜨렸을 때 컴파일 에러가 발생합니다.
```

## `is` 타입 가드 함수

```ts
function isCourse(value: unknown): value is Course {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "title" in value
  );
}

function handle(data: unknown) {
  if (isCourse(data)) {
    console.log(data.title);  // 이 블록 안에서는 Course로 좁혀짐
  }
}
```

---

# 11. 제네릭 제약(Generic Constraints)

제네릭이 아무 타입이나 받으면 그 안에서 쓸 수 있는 기능이 제한됩니다. `extends`로 "최소한 이런 속성은 있어야 한다"는 제약을 걸 수 있습니다.

```ts
interface HasId {
  id: number;
}

function findById<T extends HasId>(list: T[], id: number): T | undefined {
  return list.find((item) => item.id === id);
  // T가 HasId를 확장하므로 item.id 접근이 안전함이 보장됨
}

findById<Course>(courses, 1);
```

제약이 없으면(`function findById<T>(...)`) `item.id`에 접근하는 순간 컴파일 에러가 납니다. TypeScript는 "T가 무엇이든 id라는 속성을 가진다"는 보장이 없다고 보기 때문입니다.

---

# 12. 프론트엔드에서 자주 쓰는 타입 패턴

## React 컴포넌트 Props 타입

```ts
interface CourseCardProps {
  course: Course;
  onEnroll?: (courseId: number) => void;   // 선택적 콜백
  children?: React.ReactNode;
}

function CourseCard({ course, onEnroll, children }: CourseCardProps) {
  // ...
}
```

## 이벤트 핸들러 타입

```ts
function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
  console.log(e.target.value);
}

function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
  e.preventDefault();
}
```

## API 훅의 반환 타입을 제네릭으로

```ts
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(url)
      .then((res) => res.json())
      .then((json: T) => setData(json))
      .finally(() => setLoading(false));
  }, [url]);

  return { data, loading };
}

const { data } = useFetch<Course[]>("/api/courses");
```

---

# 13. tsconfig.json 핵심 옵션

```json
{
  "compilerOptions": {
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler"
  }
}
```

| 옵션 | 의미 |
| --- | --- |
| `strict` | `strictNullChecks`, `noImplicitAny` 등 엄격 검사 전체를 켬. 신규 프로젝트는 처음부터 켜두는 것이 좋음 |
| `noUnusedLocals`/`noUnusedParameters` | 안 쓰는 변수·매개변수를 에러로 표시 |
| `noImplicitReturns` | 함수의 일부 경로에서만 값을 반환하면 에러 |
| `skipLibCheck` | `node_modules` 내부 타입 정의 파일 검사를 건너뛰어 빌드 속도 향상 |
| `moduleResolution` | `import` 문을 실제 파일로 찾아가는 방식 설정. `"bundler"`는 Vite·esbuild 같은 번들러 환경에 맞춘 값(TypeScript 5.0 이상 필요). Node.js로 직접 실행하는 프로젝트라면 `"node16"`/`"nodenext"` 등 다른 값을 쓰는데, 정확한 조합은 사용 중인 TypeScript·번들러 버전 문서에서 확인 |

**기본 상식**: `strict: false`인 프로젝트에 나중에 `strict: true`를 켜면 에러가 한 번에 쏟아집니다. 신규 프로젝트는 처음부터 켜두고, 기존 프로젝트는 `strict` 하위 옵션(`strictNullChecks`부터)을 하나씩 켜며 점진적으로 마이그레이션하는 편이 안전합니다.

---

# 14. 자주 만나는 컴파일 에러 읽는 법

| 에러 메시지(요약) | 원인 | 해결 방향 |
| --- | --- | --- |
| `Object is possibly 'null'` | `strictNullChecks`에서 null 가능성을 처리하지 않음 | `if (x !== null)` 체크 또는 `?.` 옵셔널 체이닝 |
| `Type 'X' is not assignable to type 'Y'` | 타입이 서로 호환되지 않음 | 실제로 어떤 타입이어야 하는지 원본 타입 정의를 확인 |
| `Property 'x' does not exist on type 'Y'` | 좁혀지지 않은 Union이거나 오타 | 타입 가드로 좁히거나 속성명 확인 |
| `Argument of type 'X' is not assignable to parameter of type 'Y'` | 함수 호출 시 인자 타입 불일치 | 함수 시그니처와 실제 넘긴 값의 타입을 비교 |
| `Type instantiation is excessively deep` | 제네릭 타입이 과도하게 중첩·재귀됨 | 복잡한 타입을 단순화하거나 중간 타입으로 분리 |

**실무 팁**: 에러 메시지를 끝까지 읽으면 대부분 "무엇을 기대했는데 무엇이 왔는지"가 적혀 있습니다. 메시지를 무시하고 `as any`로 덮어씌우면 당장은 편하지만 같은 종류의 버그가 런타임에 다시 나타납니다.
