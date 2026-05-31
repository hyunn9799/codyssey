# Linux 서버 운영 및 시스템 관제 자동화 과제 수행 내역서

## 1. 과제 개요

Linux 환경에서 다중 사용자 및 그룹 권한 체계를 구축하고, SSH 보안 설정, 방화벽 정책 구성, 애플리케이션 실행 환경 설정, 시스템 관제 자동화 스크립트 개발 및 Cron 기반 자동 실행 환경을 구축

---

# 2. 개발 환경

| 항목         | 내용                          |
| ---------- | --------------------------- |
| OS         | Ubuntu (OrbStack Container) |
| Shell      | Bash                        |
| SSH        | OpenSSH Server              |
| Firewall   | UFW                         |
| Scheduler  | Cron                        |
| Monitoring | Shell Script                |

---

# 3. 시스템 환경 구축

## 3-1. Ubuntu 컨테이너 생성

```bash
orb create ubuntu agent-ubuntu
```

생성 확인

```bash
orb list
```

---

## 3-2. 필수 패키지 설치

```bash
sudo apt update

sudo apt install -y \
unzip vim sudo acl ufw cron \
openssh-server procps iproute2 net-tools
```

설치 목적

* SSH 서버 운영
* ACL 권한 관리
* 방화벽 설정
* 시스템 모니터링
* Cron 자동화

---

# 4. 계정 및 그룹 구성

## 생성 그룹

```bash
sudo groupadd agent-common
sudo groupadd agent-core
```

| 그룹명          | 설명           |
| ------------ | ------------ |
| agent-common | 전체 사용자 공유 그룹 |
| agent-core   | 운영 핵심 그룹     |

---

## 생성 계정

```bash
sudo useradd -m -s /bin/bash agent-admin
sudo useradd -m -s /bin/bash agent-dev
sudo useradd -m -s /bin/bash agent-test
```

---

## 그룹 할당

```bash
sudo usermod -aG agent-common,agent-core agent-admin
sudo usermod -aG agent-common,agent-core agent-dev
sudo usermod -aG agent-common agent-test
```

---

## 계정 확인

```bash
id agent-admin
id agent-dev
id agent-test
```

(결과 화면 첨부)

---

# 5. 디렉토리 구조 구성

## 생성 디렉토리

```bash
sudo mkdir -p /home/agent-admin/agent-app/upload_files
sudo mkdir -p /home/agent-admin/agent-app/api_keys
sudo mkdir -p /home/agent-admin/agent-app/bin

sudo mkdir -p /var/log/agent-app
```

최종 구조

```text
/home/agent-admin/agent-app
├── upload_files
├── api_keys
└── bin

/var/log/agent-app
```

---

# 6. 애플리케이션 배치

```bash
sudo cp -r ~/agent-task/agent-app \
/home/agent-admin/agent-app/
```

---

# 7. 권한 설정

## 소유권 설정

```bash
sudo chown -R agent-admin:agent-core \
/home/agent-admin/agent-app

sudo chown agent-admin:agent-common \
/home/agent-admin/agent-app/upload_files

sudo chown agent-admin:agent-core \
/home/agent-admin/agent-app/api_keys

sudo chown agent-admin:agent-core \
/var/log/agent-app
```

---

## 권한 설정

```bash
sudo chmod 750 /home/agent-admin/agent-app

sudo chmod 770 \
/home/agent-admin/agent-app/upload_files

sudo chmod 770 \
/home/agent-admin/agent-app/api_keys

sudo chmod 770 \
/var/log/agent-app
```

---

# 8. 키 파일 생성

```bash
echo "agent_api_key_test" \
| sudo tee \
/home/agent-admin/agent-app/api_keys/t_secret.key
```

권한 설정

```bash
sudo chmod 660 \
/home/agent-admin/agent-app/api_keys/t_secret.key
```

확인

```bash
sudo -u agent-admin cat \
/home/agent-admin/agent-app/api_keys/t_secret.key
```

---

# 9. 환경 변수 설정

```bash
export AGENT_HOME=/home/agent-admin/agent-app

export AGENT_PORT=15034

export AGENT_UPLOAD_DIR=$AGENT_HOME/upload_files

export AGENT_KEY_PATH=$AGENT_HOME/api_keys

export AGENT_LOG_DIR=/var/log/agent-app
```

---

# 10. 애플리케이션 실행

현재 시스템 아키텍처 확인

```bash
uname -m
```

결과

```text
x86_64
```

실행

```bash
cd ~/agent-app/agent-app

./agent-app-linux-x86
```

성공 기준

```text
All Boot Checks Passed!

Agent READY
```

![alt text](image.png)

---

# 11. SSH 보안 설정

## SSH 포트 변경

![alt text](image-1.png)


파일 수정

```bash
sudo vim /etc/ssh/sshd_config
```

설정

```text
Port 20022

PermitRootLogin no
```
![alt text](image-2.png)
적용

```bash
# 1. 설정 파일 수정 (Vim 에디터 활용)
sudo vim /etc/ssh/sshd_config

# 2. 오타나 설정 오류가 없는지 미리 검사 (아무 말 없으면 통과)
sudo sshd -t

# 3. 안전함이 확인되었으니 안심하고 SSH 서비스에 변경사항 반영
sudo systemctl restart ssh
```

확인

```bash
## grep -E: 확장 정규표현식을 사용하여 여러 패턴을 동시에 검색합니다.
## "^(Port|PermitRootLogin)": 파일의 각 줄 시작(^) 부분이 'Port' 또는 'PermitRootLogin'으로 시작하는 라인만 찾습니다.
## /etc/ssh/sshd_config: 검사할 SSH 설정 파일 경로입니다.
grep -E "^(Port|PermitRootLogin)" /etc/ssh/sshd_config

## ss: 현재 시스템의 소켓(Socket) 상태를 보여주는 네트워크 네트워크 확인 명령어입니다.
## -tulnp 옵션 상세:
##   -t : TCP 프로콜만 확인
##   -u : UDP 프로토콜만 확인 (SSH는 TCP를 쓰지만 습관적으로 같이 자주 씁니다)
##   -l : 연결 요청을 대기 중인(Listening) 포트만 확인
##   -n : 호스트 이름 대신 숫자로 된 포트 번호(예: localhost 대신 127.0.0.1)로 표시
##   -p : 해당 포트를 사용 중인 프로그램 이름(PID/Process Name)을 표시
## | grep ssh: 전체 네트워크 포트 중 'ssh'라는 글자가 포함된 줄만 필터링해서 보여줍니다.
ss -tulnp | grep ssh
```

![alt text](image-3.png)

---

# 12. 방화벽 설정

기본 정책

```bash
## ufw default deny incoming: 외부에서 이 서버로 들어오는(Incoming) 모든 접속을 기본적으로 거부(deny)
##   (내가 허용해 준 포트 외에는 해커를 포함한 그 누구도 접근 불가능)
sudo ufw default deny incoming

## ufw default allow outgoing: 서버 내부에서 외부 인터넷으로 나가는(Outgoing) 모든 요청은 기본적으로 허용(allow)
##   (서버 안에서 패키지를 다운받거나 API를 호출하는 등의 행위는 자유롭게 허용)
sudo ufw default allow outgoing
```

허용 포트

```bash
## 관리자 전용 출입문 (SSH)
sudo ufw allow 20022/tcp

## 외부와 데이터를 주고받기 위한 통로
sudo ufw allow 15034/tcp
```

활성화

```bash
## ufw enable: 설정한 규칙들을 바탕으로 UFW 방화벽을 시스템에 실제로 가동(활성화)
##    (이 명령어를 치면 시스템이 켜질 때마다 방화벽이 자동으로 켜짐)
sudo ufw enable
```

확인

```bash
## ufw status verbose: 현재 방화벽이 켜져 있는지(Active), 그리고 어떤 포트들이 열려있는지 
##   상세한(verbose) 규칙 리스트를 터미널에 쭉 출력해서 보여줌
sudo ufw status verbose
```

![alt text](image-4.png)
---

# 13. 시스템 관제 자동화 스크립트

파일 위치

```text
/home/agent-admin/agent-app/bin/monitor.sh
```

기능

* 프로세스 상태 점검
* 포트 상태 점검
* CPU 사용률 수집
* 메모리 사용률 수집
* 디스크 사용률 수집
* 임계치 경고 출력
* 로그 기록

로그 위치

```text
/var/log/agent-app/monitor.log
```

monitor.log 누적 확인
```bash
tail -n 10 /var/log/agent-app/monitor.log
```
![alt text](image-6.png)
---

# 14. Cron 자동 실행

Cron 매 분 등록

```bash
crontab -e
```

설정

```cron
* * * * * /home/agent-admin/agent-app/bin/monitor.sh >> /var/log/agent-app/monitor_cron.out 2>&1
```

확인

```bash
crontab -l
```

![alt text](image-7.png)

Cron 서비스 확인

```bash
systemctl status cron
```

실제 모니터 로그
![alt text](image-9.png)

cron 실행 로그
![alt text](image-10.png)

파일 생성 여부
```bash
ls -l /var/log/agent-app
```
![alt text](image-11.png)

---

# 15. 결과 검증

## 검증 항목

* [x] 계정 및 그룹 생성
* [x] 디렉토리 구조 생성
* [x] 권한 설정 완료
* [x] 키 파일 생성
* [x] 환경 변수 설정
* [x] Agent Boot Sequence 5단계 통과
* [x] Agent READY 출력 확인
* [x] SSH 포트 20022 적용
* [x] Root 원격 로그인 차단
* [x] UFW 활성화
* [x] 20022/tcp 허용
* [x] 15034/tcp 허용
* [x] monitor.sh 구현
* [x] monitor.log 생성
* [x] Cron 자동 실행 확인

---

# 16. 결론

본 과제를 통해 Linux 환경에서의 계정 및 그룹 기반 권한 관리, SSH 보안 설정, 방화벽 정책 구성, 애플리케이션 실행 환경 설정, 시스템 자원 관제 및 Cron 자동화 운영 환경을 구축

