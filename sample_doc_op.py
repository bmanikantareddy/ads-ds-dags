from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime
from docker.types import Mount


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 4, 13)
}

with DAG('docker_dind_example', default_args=default_args, schedule_interval=None) as dag:

    docker_task = DockerOperator(
        task_id='docker_task',
        image='ubuntu',
        api_version='auto',
        docker_url='TCP://docker-socket-proxy:2375',
        #command='/bin/sh -c "cat /opt/airflow/secrets/script.sh"',
        command='/bin/sh -c "ls /opt/airflow/secrets/"',
        network_mode='bridge',
        auto_remove=True,
        dag=dag,
        #volumes=['./secrets:/opt/airflow/secrets'],
        mount_tmp_dir=False,
        mounts=[
            Mount(source="/Users/bmanikantareddy/Documents/kondalrao/walmart/secrets",target="/opt/airflow/secrets",type="bind")
        ] 
        
    )

    docker_task
