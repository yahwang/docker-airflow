# docker-airflow 

> forked from puckel/docker-airflow

참고 : 

    github repo : https://github.com/puckel/docker-airflow

    docker image : https://hub.docker.com/r/puckel/docker-airflow

### .env 생성 ( 필수는 아님 )

container restart를 실행해도 Key를 유지하기 위해 임의로 분리

FERNETKEY 생성방법 : https://airflow.readthedocs.io/en/stable/howto/secure-connections.html#securing-connections
    
``` python
pip install cryptography
python -c "from cryptography.fernet import Fernet; FERNET_KEY = Fernet.generate_key().decode(); print(FERNET_KEY)"
```
    
    # .env_dafult 파일 참고
    AIRFLOW__CORE__FERNET_KEY= 발급받은 Key 입력


## 컨테이너 생성 및 실행 with LocalExecutor

    $ docker-compose up -d
    
    # localhost:8080 접속이 가능한 이후, 

    # Admin User 생성 ( airflow 접속 시 로그인을 요구함 )
    $ docker exec airflow_webserver airflow create_user -r Admin -u ...
    
user 생성 함수 확인 : https://airflow.apache.org/docs/stable/cli.html#create_user

## 추가 정보

### 컨테이너 생성 시 사용하는 설정 관련 파일

<img src="./imgs/airflow_setting.png" width="400px" alt="airflow_setting">

### container 정보

- Airflow : airflow_webserver
  
    port: 8080
  
- PostgreSQL : airflow_postgres
  
    port: 5432 user: airflow pw: airflow db: airflow
  
- airflow_network라는 네트워크에 연결되어 있음

- airflow container는 instance 또는 컴퓨터 reboot시 항상 재실행되는 설정이 되어 있음 (.yml에 restart 설정인 듯)

<img src="./imgs/airflow_container.png" width="700px" alt="airflow_container">

### 수정사항

0. Airflow 1.10.3 사용 시 이슈

flask 1.10 이후 버전과 호환 문제가 발생해서 다운그레이드해야 한다.

``` python
pip install Flask==1.10.4
```

1. config/airflow.cfg 수정 ( DB 설정 및 RBAC UI (FAB-based) 적용 )

``` python
load_examples = False

## DB 변경 설정
executor = LocalExecutor
sql_alchemy_conn = postgresql+psycopg2://airflow:airflow@docker-airflow_postgres_1:5432/airflow

## RBAC UI 적용 설정

# https://airflow.apache.org/security.html#web-authentication
authenticate = False
# Use FAB-based webserver with RBAC feature
rbac = True

## worker 설정

# Number of workers to run the Gunicorn web server
workers = 2
# The worker class gunicorn should use. Choices include
# sync (default), eventlet, gevent
worker_class = gevent
```

2. Dockerfile 수정

추가 : 

    apt-get install vim procps 
    # procps: ps command 용도

삭제 :

    pip install apache-airflow[mysql, ..., 등등] # 불필요한 것 제거
    USER 삭제 # USER 생성 시 dag가 작동이 잘 안 되는 듯...

3. script/entrypoint.sh 수정

.env를 통해 AIRFLOW__CORE__FERNET_KEY를 입력받지 않으면 자동으로 생성 및 .bashrc에 저장

추가 : 

    # export FERNET_KEY to Variable
    if [[ -z "$AIRFLOW__CORE__FERNET_KEY" ]]
    then
    AIRFLOW__CORE__FERNET_KEY=${FERNET_KEY:=$(python -c "from cryptography.fernet import Fernet; FERNET_KEY = Fernet.generate_key().decode(); print(FERNET_KEY)")}}
    echo "export AIRFLOW__CORE__FERNET_KEY="$FERNET_KEY >> ~/.bashrc
    source ~/.bashrc
    fi

4. docker-compose-LocalExecutor.yml => docker-compose.yml

``` python
1. version 2에서 version 3.5으로 syntax 변경
2. Dockerfile로 image를 빌드하도록 수정
```
