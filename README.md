# docker-airflow 

> forked from puckel/docker-airflow

참고 : 

    github repo : https://github.com/puckel/docker-airflow

    docker image : https://hub.docker.com/r/puckel/docker-airflow

## 컨테이너 생성 with LocalExecutor

$ docker-compose up -d

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

0. ver 1.10.3으로 업데이트

참고 : https://github.com/alvyl/docker-airflow/tree/bump-version-v1.10.3

다른 사용자가 만들어 둔 1.10.3 버전을 기반으로 전체적인 수정작업

1. config/airflow.cfg 수정

``` python
executor = LocalExecutor

sql_alchemy_conn = postgresql+psycopg2://airflow:airflow@docker-airflow_postgres_1:5432/airflow
```

2. Dockerfile 수정

추가 : 

    apt-get install vim procps 
    # procps: ps command 용도
    pip install boto3
    pip install psycopg2-binary

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