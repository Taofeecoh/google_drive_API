import time

import awswrangler as wr
import boto3
import gspread
import pandas as pd
from airflow.models import Variable


def gspread_conn():
    """
    Function to connect to google drive API and extract data from target source
    :returns: success message when ingestion is complete
    """

    client = gspread.service_account_from_dict(
        Variable.get("CREDENTIALS_AIRFLOW_GSERVICE", deserialize_json=True)
    )
    try:
        spreadsheet = client.open("marketing_source")
        if spreadsheet:
            worksheet = spreadsheet.sheet1
            data = worksheet.get_all_records()
            if data:
                marketing_data = pd.DataFrame(data)
            else:
                print("data not found!")
        else:
            print("worksheet does not exist!")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("data ingested successfully!")
    return marketing_data


def transform_col_names(ti):
    """
    Function to transform list items to snake_case format
    :params ti: airflow task instance to pull data from
    :returns: list of items in snake_case
    """
    data_frame = ti.xcom_pull(task_ids='connect_to_driveAPI')
    data_list = data_frame.columns.to_list()
    col = [col.strip().replace(" ", "_").lower() for col in data_list]
    data_frame.columns = col
    print("Column names updated successfully!")
    return data_frame


def boto_session():
    """
    Function to create a boto3 session.
    :return: A boto3 session object.
    """

    session = boto3.Session(
        aws_access_key_id=Variable.get("AWS_KEY_ID"),
        aws_secret_access_key=Variable.get("AWS_SECRET_KEY"),
        region_name="eu-west-1"
    )
    return session


def to_s3(ti):
    """
    Function to write DataFrame to S3 in parquet format.
    :return: completion messsage when upload is completed successfully
    """
    data_frame = ti.xcom_pull(task_ids="transform_data")
    my_path = "s3://tao-general-ingestion/xcom-googlesheet-dump/"
    wr.s3.to_csv(
        df=data_frame,
        path=(
            f"{my_path}marketing-googlesheet-data-{time.strftime(
                "%Y-%m-%d|%H:%M:%S"
                )}.csv"
            ),
        boto3_session=boto_session(),
        dataset=False
    )
    print("upload to s3 complete!")
