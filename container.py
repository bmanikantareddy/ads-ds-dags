from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 12),
}

with DAG('docker_operator_example', 
         default_args=default_args,
         schedule_interval=None,
         catchup=False) as dag:

    # t1 = DockerOperator(
    #     task_id='docker_task',
    #     image='custom-docker-image:latest',
    #     command='/bin/bash /path/to/shell/script.sh',
    #     network_mode='bridge',
    #     api_version='auto',
    #     auto_remove=True,
    #     tty=True,
    #     volumes=['/var/run/docker.sock:/var/run/docker.sock']
    # )

    t2 = DockerOperator(
        task_id='docker_task_2',
        image='python:3.8-slim-buster',
        command='echo "Hello, Airflow!"',
        network_mode='bridge',
        api_version='auto',
        auto_remove=True,
        tty=True,
        docker_url='tcp://localhost:2375',
        environment={
            'DOCKER_TLS_CERTDIR': '',
        },
    )

    #t1 >> t2

t2