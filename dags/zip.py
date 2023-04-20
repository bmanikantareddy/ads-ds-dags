from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2023, 4, 7)
}

with DAG('zip_dag', default_args=default_args, schedule_interval=None) as dag:
    
    # Define the BashOperator to install the zip package
    install_zip = BashOperator(
        task_id='install_zip',
        bash_command='apt-get update && apt-get install -y zip'
    )
    
    # Define the task that uses the zip command
    zip_files = BashOperator(
        task_id='zip_files',
        bash_command='echo test > /tmp/test && zip -r /tmp/file.zip /tmp/'
    )
    
    # Set the dependencies
    install_zip >> zip_files
