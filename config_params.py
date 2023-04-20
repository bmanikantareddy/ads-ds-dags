from datetime import datetime as dtime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator, get_current_context
import time 

def get_config_params(**kwargs):
    context= get_current_context()
    print(f"Context Value: {context}")
    logical_date= kwargs["logical_date"]
    custom_param= kwargs['dag_run'].conf.get('custom_parameter')
    todays_date= dtime.now().date()

    if logical_date.date() == todays_date:
        print("Noraml Execution")
    else:
        print("Back-date Execution")
        if custom_param is not None:
            print(f"Custom parameter value is: {custom_param}")
    time.sleep(15) ##sleep for 15 seconds

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    "retries": 0 ,
    'start_date': dtime(2023, 4, 17),
}

with DAG('dag_config_params', default_args=default_args,schedule_interval=None,catchup=False) as dag:
    start = DummyOperator(task_id = 'START')
    config_params = PythonOperator( task_id = "DAG_CONFIG_PARAMS", python_callable = get_config_params )
    end = DummyOperator(task_id = 'END')




