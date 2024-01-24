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
  - aws EC2 생성 (프리티어)
  
  - pip 설치 (sudo apt update -> sudo apt install python3-pip)
  
  - 가상 환경 분리할 필요 없기 때문에 requirements 설치 및 서버 실행
  
  - 서버 실행 시 외부랑 연결될 수 있도록 0.0.0.0:8000로 실행


  - 인스턴스 생성시 어디서든 접속이 가능하도록 설정한 것 처럼, 8000번 포트에 대한 설정을 해주어야함
  
  - 보안 탭에서 인바운드(EC2로 들어오는 경우)규칙을 8000번 포트에 대한 접근을 허용하도록 설정
  
  - 컴퓨터 및 핸드폰으로 접속 여부 확인
  ```

- [x] nginx, uwsgi를 이용하여 정상적인 웹서비스
  - 기존 : 클라이언트 -> 장고(EC2)
  - 시도할것 : 클라이언트 -> nginx(EC2 웹서버) -> uwsgi -> 장고(EC2)
  - why ? : 정적인 WEB 서버와 동적인 WAS 서버의 분리 / 로드 밸런싱 / 라우팅 / 캐싱 등의 이점이 많음
  
  ```
  - uwsgi 설치 : pip install uwsgi (uwsgi는 윈도우에서 지원이 안됨)
  
  - uwsgi로 서버 실행 : uwsgi --http :8000 --module instagram.wsgi (wsgi.py 파일이 있는 경로)
  
  - 여기까지 uwsgi라는 인터페이스를 통해 django 서버를 띄운 상태 (클라이언트 -> uwsgi -> django)
  

  - 웹서버를 위한 nginx 설치 : sudo apt-get install nginx
  
  - nginx는 설치와 동시에 실행이 됨 (확인 : sudo systemctl status nginx)
  
  - EC2에서 인바운드 규칙에 80번 포트를 열어 웹서버(nginx)에 접근할 수 있도록 함
  
  - EC2의 IP로 접근하면 nginx가 떠있는 것을 확인할 수 있음


  - 클라이언트와 nginx는 연결이 되었지만, nginx와 uwsgi의 연결을 해주어야 함
  
  - 홈 경로에서 vi uwsgi.ini 파일을 생성
  
  - uwsgi 실행 : uwsgi -i uwsgi.ini
  
  - nginx 설정도 해주어야 함
  
  - nginx /etc/nginx/sites-available/default 파일을 수정하여 설정
  
  - nginx는 이미 실행중이기 때문에 설정을 적용하기 위해 재실행 : sudo systemctl restart nginx
  
  - Bad Gateway 오류가 뜬다면 /etc/nginx/nginx.conf 파일에서 user www-data를 user ubuntu로 변경
  ```

  - uwsgi.ini
    ```
    [uwsgi]
    # nginx와 uwsgi의 통신을 무엇으로 할지 설정, socket 또는 port(네트워크)
    socket = /home/ubuntu/uwsgi.sock
    master = true
    processes = 1
    threads = 2
    # wsgi file을 설정하기 위한 명령어
    chdir = /home/ubuntu/instagram-clone-django
    wsgi-file = instagram/wsgi.py
    # socket을 파일로 관리하기 때문에 파일 권한 설정
    chmod-socket = 666
    # 로그나 기타 설정 파일들에 대한 삭제 유무
    vacuum = true
    # 로그 파일 위치
    logger = file:/tmp/uwsgi.log
    # python site packages 위치
    pythonpath = /home/ubuntu/.local/lib/python3.10/site-packages
    ```

  - default
    ```
    # nginx가 바라볼 대상
    upstream django {
          server unix:///home/ubuntu/uwsgi.sock;
    }
    # nginx 서버의 기본 설정
    server {
            listen  80;
            server_name localhost;
            charset utf-8;
            # 클라이언트와 nginx가 통신할때 데이터의 크기
            client_max_body_size    80M;
    
            # uwsgi를 사용하기 때문에 아래의 설정이 팔요
            location / {
                    uwsgi_pass django;
                    include /etc/nginx/uwsgi_params;
            }
    }
    ```
    
- [x] uwsgi 자동 실행하도록 하기
  ```
  - nginx처럼 uwsgi도 자동으로 실행되도록 설정
  
  - /lib/systemd/system에서 uwsgi.service 파일 작성
  
  - /etc/systemd/system에서 sudo ln -s /lib/systemd/system/uwsgi.service uwsgi.service로 심볼릭 링크 생성

  - service를 systemctl에 등록 : sudo systemctl daemon-reload
  ```

  - uwsgi.service
    ```
    [Unit]
    Description=Django uWSGI service
    After=syslog.target
    
    [Service]
    # uwsgi의 절대경로를 사용해야함
    ExecStart=/home/ubuntu/.local/bin/uwsgi -i /home/ubuntu/uwsgi.ini

    # 항상 재실행
    Restart=always
    KillSignal=SIGNOUT
    Type=notify
    StandardError=syslog
    NotifyAccess=all
    
    [Install]
    WantedBy=multi-user.target
    ```
  
- [x] AWS RDS 사용해보기
  ```
  - EC2와 마찬가지로 RDS 서비스에서 데이터베이스(Aurora MySQL) 생성
  
  - 과금 방지를 위해 스토리지 자동 조정, 모니터링, 백업, 자동 업그레이드 등 해제
  
  - 데이터베이스 생성 후 인바운드 규칙 생성
  
  - 생성 된 데이터베이스의 엔드포인트(호스트)를 복사하여 데이터베이스 툴로 접근이 가능한지 확인

  - Django database 설정도 변경 후, EC2 서버에 배포 후 migrate

  - 데이터베이스 툴로 적용이 되었는지 확인 후 uwsgi를 재실행
  ```

- [x] secret 정보들 숨기기
  ```
  - uwsgi.ini 파일에 환경 변수를 적어줄 수 있음

  - uwsgi로 실행시키는 장고 서버는 env=MYSQL_HOST=database-....과 같은 형식으로 파일을 작성하면 환경변수 등록 가능

  - uwsgi.ini 파일은 서버에 존재하기 때문에 외부로 노출될 위험이 적음

  - 환경변수 적용을 위해 uwsgi 재실행
  ```

- [x] 테스트 코드 적용하기
  ```
  - 이전까지 실습 셋팅은 AWS의 RDS를 바라보게 설정되어 있기 때문에 개발과 배포 환경 각각의 settings.py 생성
    - ex) settings.py (배포), settings_local.py(개발)

  - 해당 settings 파일을 적용하기 위해 python manage.py runserver --settings=instagram.settings_local로 실행

  - migrate와 같은 명령어도 위와 같이 settings 인자로 실행 가능
  
  - CI/CD 실습을 위한 Django test 코드 작성
  
  - Django는 앱을 생성하면 기본적인 tests.py 파일을 제공해줌

  - python manage.py test --settings=instagram.settings_local로 테스트 실행 (성공시 OK, 실패시 FAILED 정보를 제공)
  ```
  
  
- [x] CI 해보기

  - Github Actions 탭에서 다양한 Action 생성
     
  - 우리는 Django Action을 사용 또는 실제 개발 환경에서 직접 Action을 만들 수 있음 (경로는 무조건 .github/workflows/action.yaml)
     
  - Github에서는 Action들을 실행할 runner를 제공해주지만 기업에서는 self hosted runner로 다른 컴퓨터 적용 가능
    
  - CI workflow는 .github/workflows에서 확인 가능


- [x] CD 해보기

  - CD를 하기 위한 workflow는 개발 환경에서 .github/workflows 폴더에 직접 생성
     
  - CD 작업은 CI가 끝나면 진행하기 때문에 `on` 부분에 `workflow_run` 옵션을 이용하여 CI가 끝난 후 실행되도록 설정
     
  - CD는 SSH(기존 applyboy/ssh 사용)를 이용하여 EC2서버에 접속하고, git pull과 서버 재실행을 해줌
     
  - SSH 접속을 위한 중요 정보들은 github actions의 secrets로 관리할 수 있음 (settings -> secrets and bariables -> actions)
     
  - EC2에 접근할 때 사용하는 host, username, key를 secrets으로 저장
     
  - 이후, Actions가 잘 동작하는지 확인
     
  - CI/CD는 위와 같이 활용하는것 뿐만 아니라 CI때 Docker 이미지를 만들어 CD때 배포하는 등 다양하게 활용할 수 있음


- [ ] 캐시 써보기

- [ ] AWS route53 ssl 인증서 등록 해보기

