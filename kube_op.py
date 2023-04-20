from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.models import Variable

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
    'kubernetes_executor',
    default_args=default_args,
    description='A simple example of using the KubernetesPodOperator to run a Docker container with a shell script',
    schedule_interval=timedelta(days=1),
)

docker_command = """
    #!/bin/bash

    # Check if zip is installed and install it if it's not
    if ! command -v zip &> /dev/null; then
        echo "zip is not installed, installing..."
        apt-get update && apt-get install -y zip
    fi

    git clone https://bmanikantareddy%40gmail.com:$GITHUB_TOKEN@github.com/bmanikantareddy/jenkinslib.git
    # Add additional git and gcloud commands here
    cd jenkinslib 
    zip -r mani.zip vars/
    echo $GCLOUD_CREDENTIALS > /tmp/gcp_service
    gcloud auth activate-service-account --key-file=/tmp/gcp_service
    rm -rf /tmp/gcp_service
    gsutil cp mani.zip gs://airflow_dag_bucket
""" 


k8s_op = KubernetesPodOperator(
    task_id='kubernetes_task',
    image='docker.io/google/cloud-sdk:latest',
    namespace='default',
    name='kubernetes_pod',
    cmds=['/bin/bash', '-c'],
    arguments=[docker_command],
    env_vars={
        'GITHUB_TOKEN': Variable.get('git_token'),
        'GCLOUD_CREDENTIALS': Variable.get('gcp_service_acc')
    },
    image_pull_policy='IfNotPresent',
    is_delete_operator_pod=True,
    get_logs=True,
    dag=dag
)

k8s_op
