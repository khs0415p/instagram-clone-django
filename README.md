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

- [ ] AWS에 EC2로 서비스

- [ ] github을 이용하여 코드 배포

- [ ] nginx, uwsgi를 이용하여 정상적인 웹서비스

- [ ] CI/CD 자동 배포 해보기

- [ ] 캐시 써보기

