from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from docker.types import Mount

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 11),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'docker_executor',
    default_args=default_args,
    description='A simple example of using the DockerOperator to run a Docker container with a shell script',
    schedule_interval=timedelta(days=1),
)

# docker_command = """
#     #!/bin/bash
#     ls -alrt /opt/airflow/secrets
#     if ! command -v zip &> /dev/null; then
#         echo "zip is not installed, installing..."
#         apt-get update && apt-get install -y zip
#     fi
#     git clone https://bmanikantareddy%40gmail.com:$(cat /opt/airflow/secretsgit_token)@github.com/bmanikantareddy/jenkinslib.git data_science_gcp
#     # Add additional git and gcloud commands here
#     cd data_science_gcp 
#     zip -r mani_op.zip vars/
#     gcloud auth activate-service-account --key-file=/opt/airflow/secretsserene-voltage-379516-e80562c44542.json
#     gsutil cp mani.zip gs://airflow_dag_bucket
# """ 

docker_command = """
    #!/bin/bash
    echo 'Hello, world!'
    ls -alrt /opt/airflow/secrets
"""

docker_task = DockerOperator(
    task_id='docker_task',
    image='ubuntu',
    api_version='auto',
    docker_url='TCP://docker-socket-proxy:2375',
    command='/bin/sh -c "/opt/airflow/secrets/script.sh"',
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
