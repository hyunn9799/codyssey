# FastAPI Todo CRUD 웹 서비스

FastAPI와 SQLAlchemy를 사용해서 만든 간단한 할 일 관리 웹 애플리케이션입니다.
브라우저에서 할 일을 등록하고, 목록 조회, 상세 조회, 수정, 삭제까지 할 수 있도록 구현했습니다.

이번 프로젝트에서는 단순히 기능을 만드는 것보다, 요청이 들어왔을 때 Router, Service, Repository, DB, Template으로 흐르는 구조를 이해하는 데 초점을 두었습니다.

## 주요 기능

* 홈 화면 조회
* 할 일 목록 조회
* 할 일 상세 조회
* 새 할 일 등록
* 기존 할 일 수정
* 할 일 삭제
* POST 요청 이후 Redirect 적용
* SQLite DB 저장
* Jinja2 기반 서버 사이드 렌더링

## 사용 기술

* Python 3.12
* FastAPI
* Uvicorn
* SQLAlchemy
* SQLite
* Jinja2
* python-multipart

## 프로젝트 구조

```text
todo-crud-fastapi/
├─ main.py
├─ database.py
├─ pyproject.toml
├─ todo.db
├─ models/
│  └─ task.py
├─ repositories/
│  └─ task_repository.py
├─ services/
│  └─ task_service.py
├─ routers/
│  ├─ __init__.py
│  ├─ home_router.py
│  └─ task_router.py
└─ templates/
   ├─ home.html
   └─ tasks/
      ├─ list.html
      ├─ new.html
      ├─ detail.html
      └─ edit.html
```

## 실행 방법

### 1. 프로젝트 폴더로 이동

```bash
cd todo-crud-fastapi
```

### 2. 의존성 설치

이 프로젝트는 `uv`를 사용해서 패키지를 관리했습니다.

```bash
uv sync
```

또는 필요한 패키지를 직접 추가하려면 아래 명령어를 사용할 수 있습니다.

```bash
uv add fastapi uvicorn sqlalchemy jinja2 python-multipart
```

### 3. 서버 실행

```bash
uv run uvicorn main:app --reload
```

서버가 정상적으로 실행되면 아래 주소로 접속할 수 있습니다.

```text
http://127.0.0.1:8000
```

## 화면 흐름

### 홈 화면

```text
GET /
```

앱 소개와 함께 할 일 목록, 새 할 일 작성 화면으로 이동할 수 있는 링크를 제공합니다.

### 할 일 목록

```text
GET /tasks
```

DB에 저장된 할 일 목록을 조회해서 화면에 보여줍니다.

### 새 할 일 작성 화면

```text
GET /tasks/new
```

할 일 제목, 설명, 마감일을 입력할 수 있는 폼을 보여줍니다.

### 할 일 등록 처리

```text
POST /tasks
```

HTML Form으로 전달된 데이터를 받아서 DB에 저장합니다.
저장 후에는 `RedirectResponse`를 사용해 `/tasks` 목록 화면으로 이동합니다.

### 할 일 상세 화면

```text
GET /tasks/{task_id}
```

선택한 할 일의 제목, 설명, 마감일, 완료 여부, 작성일시를 보여줍니다.

### 할 일 수정 화면

```text
GET /tasks/{task_id}/edit
```

기존 할 일 정보를 폼에 미리 채워서 보여줍니다.

### 할 일 수정 처리

```text
POST /tasks/{task_id}/edit
```

수정된 폼 데이터를 받아 DB 내용을 변경합니다.
수정 후에는 상세 화면으로 리다이렉트합니다.

### 할 일 삭제 처리

```text
POST /tasks/{task_id}/delete
```

선택한 할 일을 삭제하고 목록 화면으로 리다이렉트합니다.

## 데이터 모델

할 일은 `Task` 모델로 관리합니다.

| 필드명         | 설명        |
| ----------- | --------- |
| id          | 할 일 고유 번호 |
| title       | 할 일 제목    |
| description | 할 일 설명    |
| is_done     | 완료 여부     |
| due_date    | 마감일       |
| created_at  | 작성일시      |

## 레이어 분리

이번 프로젝트에서는 역할을 나누기 위해 Router, Service, Repository 구조를 사용했습니다.

### Router

브라우저 요청을 받고, 템플릿 응답이나 리다이렉트 응답을 반환합니다.
폼 데이터 수신, 화면 이동 처리도 Router에서 담당합니다.

### Service

입력값 검증이나 간단한 업무 규칙을 처리합니다.
예를 들어 할 일 제목의 앞뒤 공백을 제거하고, 제목이 비어 있으면 저장하지 않도록 처리했습니다.

### Repository

SQLAlchemy Session을 사용해서 실제 DB 조회, 저장, 수정, 삭제를 담당합니다.

## PRG 패턴 적용

등록, 수정, 삭제 요청은 모두 POST 방식으로 처리했습니다.
그리고 처리 후에는 바로 화면을 렌더링하지 않고 `RedirectResponse`를 사용해 GET 요청으로 이동하도록 했습니다.

예를 들어 할 일을 등록하면 다음과 같은 흐름으로 동작합니다.

```text
POST /tasks
→ DB 저장
→ Redirect 303
→ GET /tasks
```

이렇게 하면 사용자가 새로고침을 하더라도 같은 등록 요청이 반복해서 실행되는 문제를 줄일 수 있습니다.

## DB 확인

프로젝트 실행 후 `todo.db` 파일이 생성됩니다.
SQLite DB Browser나 Python의 sqlite3 모듈을 사용해서 저장된 데이터를 직접 확인할 수 있습니다.

예시:

```bash
uv run python
```

```python
import sqlite3

conn = sqlite3.connect("todo.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM tasks;")
print(cursor.fetchall())

conn.close()
```

## 학습한 점

이번 과제를 통해 브라우저 요청이 FastAPI 서버로 들어온 뒤, Router, Service, Repository를 거쳐 DB에 저장되고 다시 템플릿으로 렌더링되는 흐름을 직접 확인할 수 있었습니다.

특히 GET과 POST의 역할 차이, HTML Form 데이터 처리, SQLAlchemy ORM 기반 CRUD, 그리고 POST 이후 Redirect를 적용하는 이유를 코드로 이해할 수 있었습니다.
