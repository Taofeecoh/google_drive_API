from datetime import timedelta

import pendulum
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils import timezone

from app import gspread_conn, to_s3, transform_col_names

now = timezone.utcnow()
a_date = timezone.datetime(2025, 6, 8)

args = {
    'owner': 'Taofeecoh',
    'start_date': pendulum.datetime(2025, 6, 8, tz="CET"),
    'retries': 3,
    'retry_delay': timedelta(minutes=1)
}


with DAG(
    dag_id='googlesheets_xcom_dag',
    default_args=args,
    schedule_interval='0 17 * * *',
    catchup=False
) as dag:

    connect_to_driveAPI = PythonOperator(
        task_id='connect_to_driveAPI',
        provide_context=True,
        python_callable=gspread_conn
    )

    transform_data = PythonOperator(
        task_id='transform_data',
        python_callable=transform_col_names
    )

    load_to_s3 = PythonOperator(
        task_id="load_to_s3",
        python_callable=to_s3,
    )

connect_to_driveAPI >> transform_data >> load_to_s3
