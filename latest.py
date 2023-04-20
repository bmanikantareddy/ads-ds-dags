from datetime import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.bash_operator import BashOperator


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 4, 13)
}

with DAG('sample_doc_op', default_args=default_args, schedule_interval=None) as dag:

    t1 = BashOperator(
        task_id='list_files',
        bash_command='ls /opt/airflow/secrets',
        xcom_push=True
    )

    t2 = DockerOperator(
        task_id='docker_task',
        image='python:3.7-slim',
        api_version='auto',
        auto_remove=True,
        command='/bin/sleep 30',
        docker_url='tcp://docker-socket-proxy:2375',
        network_mode='bridge',
        mounts=['./secrets:/opt/airflow/secrets', '/var/run/docker.sock:/var/run/docker.sock'],
        environment={'API_KEY': 'xxxxxxxxx'},
    )

    t1 >> t2
