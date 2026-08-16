> **대상:** 클라우드·IaC 고급 가이드로 개념은 잡았고, AWS 자격증으로 공식 검증까지 받고 싶은 사람
> **목적:** AWS 공인 자격증 체계와 입문 단계인 Cloud Practitioner의 시험 범위를 정리합니다
> **사용법:** 시험 세부 정보(문항 수, 응시료, 합격 점수)는 자주 바뀌니 이 문서로 범위를 잡은 뒤 반드시 공식 사이트(AWS Certification, AWS Skill Builder)에서 최신 정보를 확인하세요.

---

# 0. 시작 전에 — 자주 나오는 용어

클라우드·IaC 고급 가이드에서 다룬 IaC·컨테이너·쿠버네티스 개념은 이미 안다고 가정합니다. 여기서는 AWS 자격증 범위에서 새로 나오는 용어만 정리합니다.

| 용어 | 쉬운 설명 |
| --- | --- |
| EC2 (Elastic Compute Cloud) | AWS에서 가상 서버를 빌려 쓰는 서비스 |
| S3 (Simple Storage Service) | 파일(이미지, 백업 등)을 저장해두는 AWS의 객체 스토리지 서비스 |
| IAM (Identity and Access Management) | AWS 리소스에 "누가 무엇을 할 수 있는지" 관리하는 서비스 |
| VPC (Virtual Private Cloud) | AWS 안에 격리된 나만의 가상 네트워크 공간을 만드는 서비스 |
| 리전(Region) / 가용 영역(AZ) | 리전은 AWS 데이터센터가 있는 지역(예: 서울), 가용 영역은 그 리전 안의 물리적으로 분리된 데이터센터 단위 |
| RDS (Relational Database Service) | AWS가 대신 운영·관리해주는 관계형 데이터베이스 서비스 |
| 종량제(Pay-as-you-go) | 사용한 만큼만 요금을 내는 클라우드의 기본 과금 방식 |
| Well-Architected Framework | AWS가 제시하는 "잘 설계된 클라우드 시스템"의 기준 프레임워크 |

---

# 1. 자격증 체계

AWS 자격증은 단계별로 나뉩니다. 처음이라면 Cloud Practitioner부터 시작하는 것이 일반적입니다.

| 단계 | 자격증 | 성격 |
| --- | --- | --- |
| 입문 | Cloud Practitioner | 클라우드 개념 전반의 기초 이해 (비개발자도 응시) |
| 어소시에이트 | Solutions Architect Associate 등 | 특정 역할(설계, 운영, 개발) 기준 실무 지식 |
| 프로페셔널/전문 | Solutions Architect Professional 등 | 어소시에이트보다 훨씬 깊은 실무·설계 역량 |

이 문서는 입문 단계인 **Cloud Practitioner** 기준으로 정리합니다.

---

# 2. 시험 구성 (Cloud Practitioner 기준)

시험은 4개 영역(도메인)으로 나뉩니다.

| 도메인 | 다루는 내용 |
| --- | --- |
| Cloud Concepts | 클라우드 컴퓨팅이 뭔지, 온프레미스와의 차이, 클라우드의 장점 |
| Security and Compliance | AWS와 사용자가 각자 책임지는 보안 범위(책임 공유 모델), IAM 기본 |
| Cloud Technology and Services | EC2·S3·RDS·VPC 등 핵심 서비스가 각각 뭘 하는지 |
| Billing, Pricing, and Support | 요금 체계, 예산 관리 도구, 지원 플랜 |

전 영역 객관식이며, 코드를 직접 작성하는 문제는 없습니다.

---

# 3. 핵심 개념

## 책임 공유 모델 (Shared Responsibility Model)

```text
AWS의 책임: 클라우드 자체의 보안 (데이터센터, 하드웨어, 네트워크 인프라)
사용자의 책임: 클라우드 안에서의 보안 (데이터 암호화, IAM 설정, OS 패치 등)
```

**기본 상식**: "클라우드에 올렸으니 AWS가 알아서 보안을 다 챙겨준다"는 흔한 오해입니다. 인프라 자체는 AWS 책임이지만, 그 위에서 무엇을 어떻게 설정하느냐(예: S3 버킷을 실수로 전체 공개로 설정)는 사용자 책임입니다. 시험에서 "이 상황은 누구 책임인가"를 자주 묻습니다.

## 핵심 서비스 한눈에

```text
컴퓨팅: EC2(가상 서버), Lambda(서버 없이 코드만 실행 — 서버리스)
스토리지: S3(파일 저장), EBS(EC2에 붙이는 디스크)
데이터베이스: RDS(관계형 DB 관리형 서비스)
네트워크: VPC(가상 네트워크), Route 53(DNS)
```

## Well-Architected Framework — 6개 기둥

```text
운영 우수성(Operational Excellence)
보안(Security)
안정성(Reliability)
성능 효율성(Performance Efficiency)
비용 최적화(Cost Optimization)
지속 가능성(Sustainability)
```

이 사이트의 성능·스케일 고급 가이드, 보안 심화 가이드에서 다룬 내용들이 이 프레임워크의 각 기둥과 실제로 맞닿아 있습니다.

## 요금 구조

```text
종량제(Pay-as-you-go): 쓴 만큼만 지불, 약정 없음
예약 인스턴스(Reserved): 1~3년 약정으로 할인
Savings Plans: 사용량 약정으로 유연하게 할인
```

**기본 상식**: 클라우드의 핵심 가치 중 하나는 "초기 투자 비용(CAPEX) 없이 사용한 만큼만 비용(OPEX)을 낸다"는 것입니다. 이 개념 자체가 시험에서 자주 출제됩니다.

---

# 4. 연습문제

> ⚠️ 아래 문제는 개념 이해를 돕기 위해 직접 만든 연습문제이며, 실제 AWS 공인 자격증 기출문제가 아닙니다.

**문제 1.** 책임 공유 모델에서 고객(사용자)의 책임에 해당하는 것은?
A) 데이터센터의 물리적 보안
B) 네트워크 인프라 장비 관리
C) S3 버킷의 접근 권한 설정
D) 하드웨어 장애 대응

**문제 2.** 사용한 만큼만 비용을 지불하며 약정이 없는 AWS의 기본 요금 방식은?
A) Reserved Instance
B) Savings Plans
C) Pay-as-you-go
D) Spot Instance

**정답**: 1번 C / 2번 C

---

# 5. 합격 꿀팁

- **AWS 공식 무료 학습 자료(AWS Skill Builder)를 가장 먼저 활용하세요.** Cloud Practitioner를 겨냥한 무료 강의·연습 문제가 공식으로 제공됩니다.
- 서비스 이름을 암기만 하지 말고, **무료 티어로 직접 콘솔에서 EC2 인스턴스 하나, S3 버킷 하나를 만들어보세요.** 눈으로 한 번 본 개념은 암기 카드보다 오래 남습니다.
- 서비스가 많아 헷갈리기 쉬우니, "이 서비스는 한 단어로 뭘 하는 서비스인가"를 카드처럼 정리해두세요(EC2=서버, S3=저장, RDS=DB, VPC=네트워크).
- 책임 공유 모델 문제가 자주 나옵니다. "이 상황은 AWS 책임인가 내 책임인가"를 판단하는 연습을 특히 많이 해두세요.

---

# 6. 자주 하는 실수

- "클라우드에 올리면 보안은 AWS가 다 책임진다"고 오해
- EC2와 Lambda(서버리스)의 차이를 모르고 아무 문제에나 EC2를 답으로 고름
- 리전과 가용 영역(AZ)을 같은 개념으로 혼동
- 요금제 종류(종량제/예약/Savings Plans)의 특징을 안 외우고 이름만 봄

---

# 7. 실전 체크리스트

- [ ] 책임 공유 모델에서 AWS 책임과 사용자 책임을 구분할 수 있는가
- [ ] EC2·S3·RDS·VPC가 각각 뭘 하는 서비스인지 한 줄로 설명할 수 있는가
- [ ] 리전과 가용 영역의 차이를 아는가
- [ ] Well-Architected Framework 6개 기둥을 나열할 수 있는가
- [ ] 최신 시험 범위·응시료를 공식 사이트에서 확인했는가

---

# 8. 진짜 기출문제는 여기서

공식 학습 자료와 연습 문제는 **AWS Skill Builder(skillbuilder.aws)**, 자격증 안내는 **AWS Certification(aws.amazon.com/certification)**에서 확인하세요. 이 사이트는 시험 범위와 개념 정리만 제공합니다.
