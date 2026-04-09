# AI/SW 개발 워크스테이션 구축 
##  실행 환경
- OS: Ubuntu 24.04.4 LTS
- Shell: bash
- Docker: 29.1.3
- Git: 2.43.0

### 버전 확인

```bash
docker --version
docker info
git --version
pwd
```

### 패키지 구조

```bash
workspace/
├─ app/
│  └─ index.html
├─ Dockerfile
├─ README.md
└─ screenshots/
```

##  수행 체크리스트
수행 항목 체크리스트
- [x] 터미널 기본 조작
- [x]파일/디렉터리 권한 확인 및 변경
- [x]Docker 설치 및 기본 점검
- [x]hello-world 실행
- [x]Ubuntu 컨테이너 실행 및 내부 명령 수행
- [x] 이미지/컨테이너/로그/리소스 확인
- [x]Dockerfile 기반 커스텀 이미지 제작
- [x]포트 매핑 후 접속 확인
- [x]바인드 마운트 동작 확인
- [x]Docker 볼륨 영속성 확인
- [x]Git 설정
- [x]GitHub / VS Code 연동
- [x]트러블슈팅 정리

## 현재 위치 및 목록 확인
```bash
pwd
ls
ls -la
```
## 디렉터리 생성 및 이동
```bash
mkdir -p ~/workspace/app
cd ~/workspace
pwd
```

## 파일 생성, 복사, 이동, 이름 변경, 삭제
```bash
touch sample.txt
cp sample.txt sample-copy.txt
mv sample-copy.txt renamed.txt
rm renamed.txt
```

## 파일 내용 확인
```bash
echo "hello workstation" > sample.txt
cat sample.txt
```

## 절대 경로와 상대 경로 정리

절대 경로는 루트(/)부터 시작하는 전체 경로이고,
상대 경로는 현재 위치를 기준으로 작성하는 경로

예를 들어 현재 위치가 /home/user/workspace일 때:

절대 경로: /home/user/workspace/app/index.html
상대 경로: ./app/index.html

절대 경로는 어떤 위치에서 실행하더라도 같은 대상을 정확히 가리킬 때 유리하고,
상대 경로는 프로젝트 내부 구조를 기준으로 간결하게 작성할 때 유리합니다.


### 파일 권한 실습
## 파일 권한 확인
```bash
ls -l sample.txt
```

## 파일 권한 변경

```bash
chmod 644 sample.txt
ls -l sample.txt

chmod 600 sample.txt
ls -l sample.txt
```

##  디렉터리 권한 변경
```bash
mkdir testdir
ls -ld testdir

chmod 755 testdir
ls -ld testdir

chmod 700 testdir
ls -ld testdir
```

## 권한 의미 정리
r: 읽기 권한
w: 쓰기 권한
x: 실행 권한

숫자 표기는 읽기 4, 쓰기 2, 실행 1을 더해서 표현

7 = 4 + 2 + 1 = rwx
6 = 4 + 2 = rw-
5 = 4 + 1 = r-x
4 = 4 = r--

예를 들어:

755 = 소유자 rwx, 그룹 r-x, 기타 r-x
644 = 소유자 rw-, 그룹 r--, 기타 r--

### Docker 설치 및 기본 점검
## Docker 버전 확인
```bash
docker --version

docker info
```

## Docker 기본 운영 명령 수행
## 이미지 및 컨테이너 목록 확인
```bash
docker images
docker ps
docker ps -a
```

## 로그 및 리소스 확인
```bash
docker logs [컨테이너명]
docker stats
```

## hello-world 실행
```bash
docker run hello-world
```

## Ubuntu 컨테이너 실행 및 내부 진입
```bash
docker run -it --name ubuntu-test ubuntu bash
```
```bash
컨테이너 내부에서 실행:

ls
echo "hello from container"
exit
```
## attach 와 exec 차이 정리
attach: 기존 컨테이너의 메인 프로세스에 직접 연결
exec: 실행 중인 컨테이너 내부에서 새 프로세스를 실행

즉, attach는 현재 실행 중인 프로세스에 붙는 개념이고,
exec는 컨테이너 안에서 추가 명령을 실행하는 방식

## 이미지 빌드
```bash
docker build -t my-web:1.0 .
``

## 컨테이너 실행
```bash
docker run -d -p 8080:80 --name my-web my-web:1.0
```

## 포트 매핑 및 접속 확인
## 포트 매핑 실행
```bash
docker run -d -p 8080:80 --name my-web my-web:1.0
```

브라우저 접속 주소:
```bash
http://localhost:8080
```

또는 curl 확인:
```bash
curl http://localhost:8080
```

## Docker 볼륨 영속성 검증
## 볼륨 생성
```bash
docker volume create mydata
```

## 볼륨 연결 컨테이너 실행
```bash
docker run -d --name vol-test -v mydata:/data ubuntu sleep infinity
```
## 데이터 생성
```bash
docker exec -it vol-test bash -lc "echo hi > /data/hello.txt && cat /data/hello.txt"
```

## Git 과 GitHub 차이
Git: 내 컴퓨터에서 버전을 관리하는 도구
GitHub: Git 저장소를 원격으로 올리고 협업하는 플랫폼
