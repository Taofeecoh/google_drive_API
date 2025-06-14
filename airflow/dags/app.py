import time

import awswrangler as wr
import boto3
import gspread
import pandas as pd
from airflow.models import Variable

from utils import (first_letters_to_cap, remove_trailing_space,
                   replace_with_underscore)

gspread_auth_path = '/opt/airflow/'
temp_storage_path = '/opt/airflow/tmp/'


def gspread_conn():
    """
    Function to connect to google drive API and extract data from target source
    :returns: success message when ingestion is complete
    """
    filename = f"{gspread_auth_path}gspread-api-462623-c3c3b4126b29.json"
    client = gspread.service_account(filename=filename)
    spreadsheet = client.open("marketing_source")
    worksheet = spreadsheet.sheet1
    rows = worksheet.get_all_values()
    biodata = pd.DataFrame(rows[1:], columns=rows[0])
    print("data ingested successfully!")
    return biodata


def transform_col_names(ti):
    """
    Function to transform list items to snake case format
    :param data_list: takes a list (required)
    :returns: list of items in snake_case
    """
    data_frame = ti.xcom_pull(task_ids='connect_to_driveAPI')
    new_col = []
    data_list = data_frame.columns.to_list()

    for i in data_list:
        i = remove_trailing_space(i)
        i = replace_with_underscore(i)
        i = first_letters_to_cap(i)
        new_col.append(i)
    data_frame.columns = new_col
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
            f"{my_path}googlesheet-xcombiodata-{time.strftime(
                "%Y-%m-%d|%H:%M:%S"
                )}.csv"
            ),
        boto3_session=boto_session(),
        dataset=False
    )
    print("upload to s3 complete!")
