from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python import PythonOperator, get_current_context

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 18),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'params': {
        "branch_name": "adatech_dev",
        "path_name": "folder/sub-folder/file.txt",
        "bucket_name":"gs://adatech-bucket",
        "message": "This is from default params"
    }
}

def get_config_params(**kwargs):
    custom_param= kwargs['dag_run']
    print(custom_param)

dag = DAG(
    'my_dag',
    default_args=default_args,
    description='Example DAG with default input parameters',
    schedule_interval='@daily',
)

# t1 = BashOperator(
#     task_id='print_message',
#     bash_command='echo "The message is {{ dag_run.conf["message"] }}"',
#     dag=dag,
# )


t1 = BashOperator(
    task_id='print_message',
    bash_command='echo -e "The message is branch_name: {{ params.branch_name }} \npath_name: {{ params.path_name }} \nbucket_name: {{ params.bucket_name }} \nmessage: {{ params.message }} \n "',
    params=default_args['params'],  # Use default params if not passed
    dag=dag,
)

config_params = PythonOperator( task_id = "DAG_CONFIG_PARAMS", python_callable = get_config_params )

