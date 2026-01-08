# Docker 환경에서 Agent 간 HTTP 통신 및 네트워크 패킷 분석

## 1. 실습 목표

본 실습의 목표는 Docker 환경에서 Agent 간 HTTP 통신을 구현하고,  
해당 통신이 실제 네트워크 상에서 어떻게 전달되는지를  
패킷 수준에서 확인하는 것이다.

이를 통해 다음을 학습한다.

- Docker 및 Docker Compose 기본 구조 이해
- TCP / HTTP 통신 흐름 복습
- Agent(Client / Server) 구조 개념 이해
- HTTP 통신 시 JSON 데이터 노출 여부 확인

---

## 2. 전체 구성

Docker Compose를 사용하여 다음과 같은 컨테이너를 구성하였다.

- **Agent A (Client)**
  - HTTP POST 요청 생성
  - JSON 형태의 tool-call 메시지 전송

- **Agent B (Server)**
  - `/tool` 엔드포인트 제공
  - JSON 요청 수신 후 JSON 응답 반환

- **Capturer**
  - tcpdump를 이용하여 Agent 간 HTTP 트래픽 캡처
  - pcap 파일로 저장

---

## 3. 프로젝트 폴더 구조

```text
week1-agent-http/
├── agent-a/
│   ├── client.py
│   ├── Dockerfile
│   └── requirements.txt
├── agent-b/
│   ├── server.py
│   ├── Dockerfile
│   └── requirements.txt
├── capture/
│   └── agent_http.pcap
├── screenshots/
│   ├── docker_compose.png
│   ├── client_code.png
│   ├── server_code.png
│   ├── agent_log.png
│   ├── wireshark_request.png
│   └── wireshark_response.png
├── docker-compose.yml
└── README.md
```

---

## 4. 주요 코드 설명

### 4.1 docker-compose.yml

아래는 본 실습에서 사용한 `docker-compose.yml`의 주요 구성이다.

![docker-compose.yml](./screenshots/docker\_compose.png)



`agent-b`  
- 서버 역할의 Agent  
- 컨테이너 내부 8000번 포트를 외부로 포워딩  

`agent-a`  
- 클라이언트 역할의 Agent  
- 환경변수로 서버 주소 설정  
- `depends\_on`을 통해 agent-b 이후 실행  

 `capturer`  
- netshoot 이미지를 사용하여 tcpdump 실행  
- HTTP 트래픽을 pcap 파일로 저장  

---

### 4.2 Agent B (Server)

Agent B는 HTTP 서버 역할을 수행하며 `/tool` 엔드포인트를 제공한다.

![server.py](./screenshots/server\_code.png)



- POST `/tool` 요청 수신
- 요청 Body의 JSON 데이터 파싱
- 수신한 JSON을 로그로 출력
- 요청 데이터를 포함한 JSON 응답 반환

---

### 4.3 Agent A (Client)

Agent A는 HTTP 요청을 생성하는 클라이언트 역할을 수행한다.

![client.py](./screenshots/client\_code.png)



- 서버 주소 설정
- JSON 형태의 tool-call 메시지 생성
- POST `/tool` 요청으로 JSON 전송
- 서버 응답 및 상태 코드 출력

---

## 5. 실행 방법

아래 명령어를 사용하여 Docker Compose로 모든 컨테이너를 빌드 및 실행한다:

```bash

docker compose up --build

```



Agent 간 통신 완료 후 패킷 캡처 종료:

```bash

docker stop capturer

```

---

## 6. 결과

### 6.1 Agent 로그 기반 JSON 확인

아래 로그를 통해 Agent A가 JSON 형태의 메시지를 전송하고, Agent B가 `/tool` 엔드포인트에서 이를 수신한 뒤  
JSON 응답을 반환했음을 확인할 수 있다.

![Agent 로그 기반 JSON 확인](./screenshots/agent\_log.png)

---

### 6.2 네트워크 패킷 분석 (Wireshark)

tcpdump로 생성된 pcap 파일을 Wireshark로 열어 분석하였다.
POST `/tool` 패킷을 선택한 후 **Follow HTTP Stream** 기능을 사용하여 HTTP 통신 내용을 확인하였다.

그 결과, HTTP Body에 포함된 JSON 요청과 응답 데이터가 암호화되지 않은 평문 형태로 전송됨을 확인할 수 있었다.



**HTTP 요청 패킷 (Agent A → Agent B)**

![Wireshark HTTP Request](./screenshots/wireshark\_request.png)



**HTTP 응답 패킷 (Agent B → Agent A)**

![Wireshark HTTP Response](./screenshots/wireshark\_response.png)

---

## 7. 정리

본 실습을 통해 Docker 환경에서 Agent 간 HTTP 통신이 평문 HTTP로 전달되며, JSON 데이터가 네트워크 상에서 그대로 노출됨을 패킷 수준에서 확인하였다.

이를 통해 실제 서비스 환경에서는 HTTPS와 같은 통신 구간 암호화가 필수적임을 이해할 수 있었다.