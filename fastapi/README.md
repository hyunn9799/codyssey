# 프로젝트 기반 할 일 관리 서비스

FastAPI, SQLAlchemy, Jinja2를 사용해서 만든 프로젝트 기반 할 일 관리 웹 서비스입니다.
이전 미션에서 구현한 단일 Todo CRUD를 확장하여, 로그인/로그아웃, 접근 제어, 모델 간 연관관계, 할 일 상태 변경 기능을 추가했습니다.

이 서비스는 사용자가 로그인한 뒤 자신의 프로젝트를 생성하고, 각 프로젝트 안에서 할 일을 등록, 조회, 수정, 삭제할 수 있도록 구성되어 있습니다.
또한 할 일의 완료/미완료 상태를 변경할 수 있어 단순 CRUD를 넘어 상태 변경 중심의 비즈니스 흐름을 포함합니다.

---

## 1. 주요 기능

* 사용자 로그인 / 로그아웃
* 세션 기반 인증
* 로그인하지 않은 사용자의 보호 페이지 접근 차단
* 로그인 상태에 따른 화면 표시 변경
* 프로젝트 생성 및 목록 조회
* 프로젝트 상세 화면에서 해당 프로젝트의 할 일 목록 조회
* 할 일 등록 / 상세 조회 / 수정 / 삭제
* 할 일 완료 / 미완료 상태 변경
* Jinja2 기반 서버 사이드 렌더링
* SQLite + SQLAlchemy ORM 기반 데이터 저장
* Router / Service / Repository / Model 계층 분리

---

## 2. 사용 기술

| 항목       | 내용                         |
| -------- | -------------------------- |
| 언어       | Python 3.12                |
| 웹 프레임워크  | FastAPI                    |
| 서버 실행    | Uvicorn                    |
| ORM      | SQLAlchemy                 |
| 데이터베이스   | SQLite                     |
| 템플릿 엔진   | Jinja2                     |
| 폼 데이터 처리 | python-multipart           |
| 인증 방식    | SessionMiddleware 기반 세션 인증 |
| 패키지 관리   | uv                         |

패키지 버전은 아래 명령어로 확인할 수 있습니다.

```bash
uv pip list
```

예시:

| 패키지              | 버전         |
| ---------------- | ---------- |
| fastapi          | 프로젝트 환경 기준 |
| uvicorn          | 프로젝트 환경 기준 |
| sqlalchemy       | 프로젝트 환경 기준 |
| jinja2           | 프로젝트 환경 기준 |
| python-multipart | 프로젝트 환경 기준 |
| starlette        | 프로젝트 환경 기준 |

---

## 3. 프로젝트 구조

```text
todo-auth-app/
├─ main.py
├─ database.py
├─ todo.db
├─ auth/
│  ├─ __init__.py
│  ├─ session.py
│  └─ dependencies.py
├─ models/
│  ├─ user.py
│  ├─ project.py
│  └─ task.py
├─ repositories/
│  ├─ user_repository.py
│  ├─ project_repository.py
│  └─ task_repository.py
├─ services/
│  ├─ auth_service.py
│  ├─ project_service.py
│  └─ task_service.py
├─ routers/
│  ├─ home_router.py
│  ├─ auth_router.py
│  ├─ project_router.py
│  └─ task_router.py
├─ templates/
│  ├─ home.html
│  ├─ login.html
│  ├─ projects/
│  │  ├─ list.html
│  │  ├─ new.html
│  │  └─ detail.html
│  └─ tasks/
│     ├─ new.html
│     ├─ detail.html
│     └─ edit.html
└─ static/
   └─ css/
      └─ style.css
```

---

## 4. 실행 방법

### 1) 프로젝트 폴더로 이동

```bash
cd todo-auth-app
```

### 2) 의존성 설치

```bash
uv sync
```

또는 필요한 패키지를 직접 추가할 경우:

```bash
uv add fastapi uvicorn sqlalchemy jinja2 python-multipart itsdangerous
```

세션 기능은 Starlette의 `SessionMiddleware`를 사용합니다.

### 3) 서버 실행

```bash
uv run uvicorn main:app --reload
```

서버 실행 후 아래 주소로 접속합니다.

```text
http://127.0.0.1:8000
```

---

## 5. 테스트 계정

이 프로젝트는 학습용으로 테스트 계정을 자동 생성하도록 구성했습니다.

| 항목    | 값       |
| ----- | ------- |
| 아이디   | test    |
| 비밀번호  | 1234    |
| 표시 이름 | 테스트 사용자 |

서버 시작 시 `users` 테이블에 `test` 계정이 없으면 자동으로 생성됩니다.

현재 프로젝트는 학습 목적이므로 테스트 계정 비밀번호를 평문으로 저장했습니다.
실제 서비스에서는 `passlib`, `bcrypt` 등을 사용해 비밀번호를 해싱해서 저장해야 합니다.

---

## 6. 인증 방식 선택

이 프로젝트는 **세션 기반 인증 방식**을 사용했습니다.

로그인 성공 시 서버는 세션에 현재 사용자의 `user_id`를 저장합니다.

```python
request.session["user_id"] = user.id
```

이후 보호 페이지에 접근할 때마다 세션에서 `user_id`를 꺼내 DB에서 현재 사용자를 조회합니다.

```text
요청 발생
→ 세션에서 user_id 확인
→ DB에서 User 조회
→ 로그인 사용자 여부 판단
```

이번 프로젝트는 Jinja2 기반 SSR 구조이기 때문에 JWT보다 세션 기반 인증이 더 자연스럽다고 판단했습니다.
JWT는 React, Vue 등 별도 프론트엔드와 REST API를 분리하는 구조에서 더 적합하다고 보았습니다.

---

## 7. 공개 / 보호 경로 정책

| 경로                                     | 접근 권한   | 설명                   |
| -------------------------------------- | ------- | -------------------- |
| GET `/`                                | 공개      | 홈 화면                 |
| GET `/login`                           | 공개      | 로그인 화면               |
| POST `/login`                          | 공개      | 로그인 처리               |
| POST `/logout`                         | 로그인 사용자 | 로그아웃 처리              |
| GET `/projects`                        | 로그인 필요  | 내 프로젝트 목록            |
| GET `/projects/new`                    | 로그인 필요  | 새 프로젝트 작성 화면         |
| POST `/projects`                       | 로그인 필요  | 프로젝트 생성              |
| GET `/projects/{project_id}`           | 로그인 필요  | 프로젝트 상세 및 할 일 목록     |
| GET `/projects/{project_id}/tasks/new` | 로그인 필요  | 특정 프로젝트의 새 할 일 작성 화면 |
| POST `/projects/{project_id}/tasks`    | 로그인 필요  | 특정 프로젝트에 할 일 생성      |
| GET `/tasks/{task_id}`                 | 로그인 필요  | 할 일 상세 조회            |
| GET `/tasks/{task_id}/edit`            | 로그인 필요  | 할 일 수정 화면            |
| POST `/tasks/{task_id}/edit`           | 로그인 필요  | 할 일 수정 처리            |
| POST `/tasks/{task_id}/delete`         | 로그인 필요  | 할 일 삭제               |
| POST `/tasks/{task_id}/toggle`         | 로그인 필요  | 완료 / 미완료 상태 변경       |

로그인하지 않은 사용자가 보호 경로에 접근하면 로그인 화면으로 이동합니다.

---

## 8. 모델 설계

이번 프로젝트는 총 3개의 SQLAlchemy ORM 모델을 사용합니다.

### User

사용자 정보를 저장합니다.

| 필드           | 설명         |
| ------------ | ---------- |
| id           | 사용자 고유 번호  |
| username     | 로그인 아이디    |
| password     | 비밀번호       |
| display_name | 화면에 표시할 이름 |

### Project

사용자가 생성한 프로젝트 정보를 저장합니다.

| 필드          | 설명             |
| ----------- | -------------- |
| id          | 프로젝트 고유 번호     |
| user_id     | 프로젝트 소유 사용자 ID |
| name        | 프로젝트 이름        |
| description | 프로젝트 설명        |
| created_at  | 생성일시           |

### Task

프로젝트에 속한 할 일 정보를 저장합니다.

| 필드          | 설명              |
| ----------- | --------------- |
| id          | 할 일 고유 번호       |
| project_id  | 할 일이 속한 프로젝트 ID |
| title       | 할 일 제목          |
| description | 할 일 설명          |
| is_done     | 완료 여부           |
| due_date    | 마감일             |
| created_at  | 생성일시            |

---

## 9. 모델 간 연관관계

이번 프로젝트의 도메인 관계는 다음과 같습니다.

```text
User 1 : N Project
Project 1 : N Task
```

즉 한 명의 사용자는 여러 프로젝트를 가질 수 있고, 하나의 프로젝트는 여러 할 일을 가질 수 있습니다.

### User - Project 관계

`projects.user_id`가 `users.id`를 참조합니다.

```text
users.id
← projects.user_id
```

Python 객체에서는 다음과 같이 접근할 수 있습니다.

```python
user.projects
project.user
```

### Project - Task 관계

`tasks.project_id`가 `projects.id`를 참조합니다.

```text
projects.id
← tasks.project_id
```

Python 객체에서는 다음과 같이 접근할 수 있습니다.

```python
project.tasks
task.project
```

프로젝트 상세 화면에서는 `project.tasks`를 사용해서 해당 프로젝트에 속한 할 일 목록을 함께 출력합니다.
이를 통해 연관관계 데이터를 화면에서 확인할 수 있습니다.

---

## 10. 부모 삭제 시 자식 처리 정책

`User → Project`, `Project → Task` 관계에는 `cascade="all, delete-orphan"` 정책을 사용했습니다.

이 정책을 선택한 이유는 프로젝트 기반 할 일 관리 서비스에서 부모 데이터가 사라졌을 때, 그에 속한 자식 데이터만 남아 있으면 의미가 불명확해지기 때문입니다.

예를 들어 Project가 삭제되었는데 그 Project에 속한 Task만 남아 있으면, 해당 Task가 어느 프로젝트에 속했는지 알 수 없습니다.
따라서 부모가 삭제될 때 자식도 함께 정리되도록 설정했습니다.

---

## 11. 주요 화면 흐름

### 로그인 전

```text
GET /
→ 홈 화면
→ 로그인 버튼 표시
```

비로그인 상태에서 `/projects`에 직접 접근하면 로그인 화면으로 이동합니다.

```text
GET /projects
→ 로그인 상태 확인
→ 비로그인 상태
→ GET /login
```

### 로그인

```text
GET /login
→ 로그인 폼 출력

POST /login
→ 아이디 / 비밀번호 검증
→ 성공 시 session["user_id"] 저장
→ GET /projects
```

### 프로젝트 생성

```text
GET /projects/new
→ 새 프로젝트 작성 폼

POST /projects
→ current_user.id를 user_id로 사용
→ 프로젝트 저장
→ GET /projects
```

프로젝트 생성 시 `user_id`는 폼에서 입력받지 않습니다.
로그인 세션에서 확인한 `current_user.id`를 사용하여 현재 로그인한 사용자의 프로젝트로 저장합니다.

### 프로젝트 상세 및 할 일 목록

```text
GET /projects/{project_id}
→ 현재 로그인한 사용자의 프로젝트인지 확인
→ 프로젝트 정보 출력
→ project.tasks로 할 일 목록 출력
```

### 할 일 생성

```text
GET /projects/{project_id}/tasks/new
→ 특정 프로젝트에 새 할 일 작성

POST /projects/{project_id}/tasks
→ 해당 프로젝트가 현재 로그인한 사용자의 프로젝트인지 확인
→ 할 일 저장
→ GET /projects/{project_id}
```

### 할 일 상태 변경

```text
POST /tasks/{task_id}/toggle
→ 로그인 확인
→ 현재 사용자의 Task인지 확인
→ is_done 값을 반대로 변경
→ GET /projects/{project_id}
```

할 일의 상태는 다음과 같이 변경됩니다.

```text
미완료(False) → 완료(True)
완료(True) → 미완료(False)
```

상태 변경 후 프로젝트 상세 화면으로 이동하여 변경 결과를 확인할 수 있습니다.

---

## 12. 인증과 인가 처리

이번 프로젝트에서는 인증과 인가를 분리해서 처리했습니다.

### 인증

인증은 “현재 사용자가 로그인했는가?”를 확인하는 과정입니다.

`get_current_user()` 함수는 세션에서 `user_id`를 꺼내 현재 로그인한 사용자를 조회합니다.

```text
세션에 user_id 있음
→ 로그인 사용자

세션에 user_id 없음
→ 비로그인 사용자
```

### 인가

인가는 “로그인한 사용자가 이 데이터에 접근해도 되는가?”를 확인하는 과정입니다.

예를 들어 Task 수정, 삭제, 상태 변경 시에는 단순히 로그인 여부만 확인하지 않고, 해당 Task가 현재 로그인한 사용자의 Project에 속하는지 확인합니다.

```text
Task
→ Project
→ User
```

이를 위해 Task 조회 시 Project와 join하여 `Project.user_id == current_user.id` 조건을 확인합니다.

---

## 13. 레이어 구조

### Router

브라우저 요청을 받고, Form 데이터를 수신하며, 화면 렌더링 또는 Redirect를 처리합니다.

예:

```text
GET /projects
POST /login
POST /tasks/{task_id}/toggle
```

### Service

입력값 정리, 검증, 상태 변경 요청 등 비즈니스 로직을 담당합니다.

예:

```text
프로젝트 이름 공백 제거
할 일 제목 공백 제거
할 일 완료/미완료 상태 변경 요청
```

### Repository

SQLAlchemy Session을 사용해 실제 DB 조회, 저장, 수정, 삭제를 수행합니다.

예:

```text
db.query(...)
db.add(...)
db.commit()
db.delete(...)
```

### Model

SQLAlchemy ORM 클래스로 DB 테이블 구조와 연관관계를 정의합니다.

### Template

Jinja2 템플릿으로 서버에서 HTML을 렌더링합니다.

---

## 14. PRG 패턴 적용

등록, 수정, 삭제, 상태 변경 요청은 모두 POST로 처리하고, 처리 후에는 Redirect를 적용했습니다.

예:

```text
POST /tasks/{task_id}/toggle
→ 상태 변경
→ Redirect 303
→ GET /projects/{project_id}
```

이렇게 하면 새로고침 시 같은 POST 요청이 반복되는 문제를 줄일 수 있습니다.

---

## 15. DB 확인 방법

SQLite DB 파일은 프로젝트 실행 후 `todo.db`로 생성됩니다.

Python에서 직접 확인할 수 있습니다.

```bash
uv run python
```

```python
import sqlite3

conn = sqlite3.connect("todo.db")
cursor = conn.cursor()

cursor.execute("SELECT id, username, display_name FROM users;")
print(cursor.fetchall())

cursor.execute("SELECT id, user_id, name FROM projects;")
print(cursor.fetchall())

cursor.execute("SELECT id, project_id, title, is_done FROM tasks;")
print(cursor.fetchall())

conn.close()
```

---

## 16. 학습한 점

이번 프로젝트를 통해 단일 모델 CRUD에서 한 단계 확장하여 인증, 인가, 연관관계, 상태 변경 로직을 함께 다루는 흐름을 경험했습니다.

특히 로그인 상태 확인과 데이터 접근 권한 확인이 다르다는 점을 코드로 구분했습니다.

```text
인증: 현재 사용자가 로그인했는가?
인가: 로그인한 사용자가 이 데이터에 접근할 수 있는가?
```

또한 `User → Project → Task` 구조를 통해 1:N 관계를 SQLAlchemy ORM으로 매핑하고, `project.tasks`를 사용해 연관관계 데이터를 화면에 출력했습니다.

상태 변경 기능은 `Task.is_done` 값을 반대로 바꾸는 방식으로 구현했습니다. 이를 통해 단순 CRUD 외에도 서비스 안에서 데이터 상태가 바뀌는 비즈니스 흐름을 구현할 수 있었습니다.
