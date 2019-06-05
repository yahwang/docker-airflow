# docker-airflow 

> forked from puckel/docker-airflow

참고 : 

    github repo : https://github.com/puckel/docker-airflow

    docker image : https://hub.docker.com/r/puckel/docker-airflow

## 컨테이너 생성 with LocalExecutor

$ docker-compose -f docker-compose-LocalExecutor.yml up -d

## 추가 정보

### 컨테이너 생성 시 사용하는 설정 관련 파일

<img src="./imgs/airflow_setting.png" width="400px" alt="airflow_setting">

### container 정보

- Airflow : docker-airflow_webserver_1 
  
    port: 8080
  
- PostgreSQL : docker-airflow_postgres_1
  
    port: 5432 user: airflow pw: airflow db: airflow
  
- dockerairflow_default라는 네트워크에 연결되어 있음

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

이 부분을 수정해야 airflow + 명령어를 수행할 수 있다. ( SequentialExecutor 오류가 나오는 문제 해결 )

2. Dockerfile 수정

추가 : 

    apt-get install vim procps 
    # procps: ps command 용도
    pip install boto3

삭제 :

    pip install apache-airflow[mysql, ..., 등등] # 불필요한 것 제거
    USER 삭제 # USER 생성 시 dag가 작동이 잘 안 되는 듯...

3. docker-compose-LocalExecutor.yml

``` python
1. version 2에서 version 3.5으로 syntax 변경
2. Dockerfile로 image를 빌드하도록 수정
```