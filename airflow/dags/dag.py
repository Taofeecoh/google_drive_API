from datetime import datetime, timedelta

from airflow.models import DAG, Variable
from airflow.operators.python_operator import PythonOperator
from app import gspread_conn, transform_col_names, to_s3

args = {
    'owner': 'Taofeecoh',
    'start_date': datetime(2025, 6, 8),
    'retries': 3,
    'retry_delay': timedelta(minutes=1)
}


dag = DAG(
    dag_id='googlesheets_dag',
    default_args=args,
    schedule_interval='0 17 * * *',
    catchup=False
)

connect_to_driveAPI = PythonOperator(
    task_id='connect_to_driveAPI',
    provide_context=True,
    python_callable=gspread_conn,
    dag=dag,
)

transform_data = PythonOperator(
    task_id='transform_data',
    python_callable=transform_col_names,
    dag=dag,
)

load_to_s3 = PythonOperator(
    task_id="load_to_s3",
    python_callable=to_s3,
    dag=dag
)

connect_to_driveAPI >> transform_data >> load_to_s3
