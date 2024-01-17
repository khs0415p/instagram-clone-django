# INSTAGRAM Clone

Django를 이용한 간단한 인스타그램 구현과 Ops에 관련한 실습 진행

## 사용법
```
# 가상환경 생성 
python -m venv venv

# 가상환경 실행
source ./venv/Scripts/activate

# 필요 package 설치
pip install -r requirements.txt

# migrate 명령어로 DB 생성
python manage.py makemigrations
python manage.py migrate

# 서버 실행
python manage.py runserver

# 브라우져로 접속
http://127.0.0.1:8000/main/
```

## 기능


- [x] 피드 생성

- [x] 메인 피드 목록

- [x] 회원가입/로그인/로그아웃

- [x] 게시물 작성

- [x] 유저 프로필 관리

- [x] 좋아요/북마크

- [x] 댓글

- [x] 프로필 사진 변경

## Ops

- [x] AWS에 EC2로 서비스

  ```
  - aws ec2 생성 (프리티어)
  - pip 설치 (sudo apt update -> sudo apt install python3-pip)
  - 가상 환경 분리할 필요 없기 때문에 requirements 설치 및 서버 실행
  - 서버 실행 시 외부랑 연결될 수 있도록 0.0.0.0:8000로 실행

  - 인스턴스 생성시 어디서든 접속이 가능하도록 설정한 것 처럼, 8000번 포트에 대한 설정을 해주어야함
  - 보안 탭에서 인바운드(ec2로 들어오는 경우)규칙을 8000번 포트에 대한 접근을 허용하도록 설정
  - 컴퓨터 및 핸드폰으로 접속 여부 확인
  ```

- [ ] nginx, uwsgi를 이용하여 정상적인 웹서비스

- [ ] CI/CD 자동 배포 해보기

- [ ] 캐시 써보기

