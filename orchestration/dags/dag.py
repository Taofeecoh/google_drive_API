import time
from datetime import timedelta

import gspread
import pendulum
from airflow.models import DAG, Variable
from airflow.operators.python import PythonOperator
from airflow.utils import timezone

import airflow_variable
from utils.app import googlesheet_to_s3

now = timezone.utcnow()
a_date = timezone.datetime(2025, 6, 8)
airflow_vars = airflow_variable

client = gspread.service_account_from_dict(
        Variable.get("CREDENTIALS_AIRFLOW_GSERVICE", deserialize_json=True)
    )
spreadsheet_source = "marketing_source"
timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
bucket_key = "s3://tao-general-ingestion/xcom-googlesheet-dump/"
file_path = "{}marketing-googlesheet-data-{}.csv".format(bucket_key, timestamp)


args = {
    'owner': 'Taofeecoh',
    'start_date': pendulum.datetime(2025, 6, 8, tz="CET"),
    'retries': 3,
    'retry_delay': timedelta(minutes=1)
}


with DAG(
    dag_id='googlesheets_xcom',
    default_args=args,
    schedule_interval='0 17 * * *',
    catchup=False
) as dag:

    connect_to_driveAPI = PythonOperator(
        task_id='connect_to_driveAPI',
        provide_context=True,
        python_callable=googlesheet_to_s3,
        op_kwargs={
            "client": client,
            "spreadsheet_name": spreadsheet_source,
            "file_path": file_path
        }

    )


connect_to_driveAPI
