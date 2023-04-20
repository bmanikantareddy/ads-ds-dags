from datetime import timedelta
from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'dim_promotion',
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(2),
)

docker_command = """
    #!/bin/bash
    if ! command -v zip &> /dev/null; then
        echo "zip is not installed, installing..."
        apt-get update && apt-get install -y zip
    fi
    ls -alrt /etc/secrets/
    git clone https://bmanikantareddy%40gmail.com:$(cat /etc/secrets/git_token)@github.com/bmanikantareddy/jenkinslib.git data_science_gcp
    # Add additional git and gcloud commands here
    cd data_science_gcp 
    zip -r mani_op.zip vars/
    gcloud auth activate-service-account --key-file=/etc/secrets/serene-voltage-379516-e80562c44542.json
    gsutil cp mani.zip gs://airflow_dag_bucket
""" 

dop = DockerOperator(
    api_version='1.37',
    docker_url='TCP://docker-socket-proxy:2375',
    #command='ls -alrt /etc/secrets/',
    command='echo "Hello, world!" && hostname && ls -al /var/run/docker.sock && ls -l /etc/secrets',
    #volumes=['/etc/secrets:/etc/secrets'],
    image='ubuntu',
    network_mode='bridge',
    task_id='docker_op_tester',
    dag=dag,
)