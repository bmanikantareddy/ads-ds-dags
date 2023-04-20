from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from google.cloud import storage
from airflow.models import Variable
from google.oauth2 import service_account



default_args = {
    'owner': 'kondalrao',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 7),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}

dag = DAG(
    'mydag',
    default_args=default_args,
    description='Upload a file to Google Cloud Storage',
    schedule_interval=None,
)

zip_folder = BashOperator(
    task_id='zip_folder',
    #bash_command='echo -e "test1 \n test2 \n\n test3" > test.txt && zip -r myzip.zip test.txt',
    bash_command='echo -e "test1 \n test2 \n\n test3" > /tmp/test.txt',
    dag=dag
)
def upload_file_to_gcs():
    # Set your GCS bucket name and file path
    bucket_name = 'airflow_dag_bucket'
    file_path = '/tmp/test.txt'
    
    Variable.get('gcp_service_acc')
    # Get the service account key file from an Airflow variable
    keyfile_dict = Variable.get('gcp_service_acc', deserialize_json=True)

    # Create a Credentials object from the service account key file
    credentials = service_account.Credentials.from_service_account_info(keyfile_dict)

    # Initialize the GCS client with the credentials
    client = storage.Client(credentials=credentials)

    # Get the bucket
    bucket = client.get_bucket(bucket_name)

    # Create a blob object with the name of the file you want to upload
    blob = bucket.blob('test.txt')

    # Upload the file to GCS
    blob.upload_from_filename(file_path)

upload_file_task = PythonOperator(
    task_id='upload_file_task',
    python_callable=upload_file_to_gcs,
    dag=dag
)

zip_folder >> upload_file_task
