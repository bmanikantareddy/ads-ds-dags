from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

default_args = {
    'owner': 'kondalroa',
    'start_date': datetime(2023, 4, 6)
}

dag = DAG('gcs_copy', default_args=default_args)

# install gcloud 

install_gcloud_and_authenticate = BashOperator(
    task_id='install_gcloud_and_authenticate',
    bash_command='sudo apt-get update && sudo apt-get install -y curl && curl https://sdk.cloud.google.com | bash && exec -l $SHELL && echo "{{ var.value.gcp_service_acc }}" > /tmp/service_account.json && gcloud auth activate-service-account --key-file=/tmp/service_account.json',
    dag=dag
)

# # Check if gcloud is installed
# check_gcloud_installed = BashOperator(
#     task_id='check_gcloud_installed',
#     #bash_command='if which gcloud >/dev/null 2>&1 ; then echo "gcloud is installed" ; else echo "gcloud is not installed" ; exit 1 ; fi',
#     bash_command='hostname',
#     dag=dag
# )

# # Use the BashOperator to write the contents of the service account variable to a file
# write_service_account_file = BashOperator(
#     task_id='write_service_account_file',
#     bash_command='echo "{{ var.value.gcp_service_acc }}" > /Users/bmanikantareddy/temp/service_account.json',
#     dag=dag
# )

# Use the BashOperator to authenticate with the service account
# authenticate = BashOperator(
#     task_id='authenticate',
#     bash_command='gcloud auth activate-service-account --key-file=/Users/bmanikantareddy/temp/service_account.json',
#     dag=dag
# )

# Clone a git repo from GitHub
clone_repo = BashOperator(
    task_id='clone_repo',
    bash_command='git clone https://github.com/uber/Python-Sample-Application.git',
    dag=dag
)

# Zip a folder from the cloned directory
zip_folder = BashOperator(
    task_id='zip_folder',
    bash_command='cd Python-Sample-Application && zip -r myzip.zip test',
    dag=dag
)

# Use gsutil to copy the zip file to a GCS bucket
upload_to_gcs = BashOperator(
    task_id='upload_to_gcs',
    bash_command='gsutil cp Python-Sample-Application.git/myzip.zip gs://airflow_dag_bucket',
    dag=dag
)

install_gcloud_and_authenticate >> clone_repo >> zip_folder >> upload_to_gcs
