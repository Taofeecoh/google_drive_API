import os
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
    os.makedirs(temp_storage_path, exist_ok=True)
    biodata.to_csv(
        temp_storage_path+"googlesheet-biodata.csv",
        index=False,
        index_label=False
        )
    print("data ingested successfully!")


def transform_col_names():
    new_col = []

    data = pd.read_csv(temp_storage_path+"googlesheet-biodata.csv")
    df = pd.DataFrame(data)
    data_list = df.columns.to_list()

    for i in data_list:
        i = remove_trailing_space(i)
        i = replace_with_underscore(i)
        i = first_letters_to_cap(i)
        new_col.append(i)
    df.columns = new_col
    df.to_csv(
        temp_storage_path+"googlesheet-biodata.csv",
        index=False,
        index_label=False
        )
    print("Column names updated successfully!")


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


def to_s3():
    """
    Function to write DataFrame to S3 in parquet format.
    :return: completion messsage when upload is completed successfully
    """
    my_path = "s3://tao-general-ingestion/airflow-googlesheet-dump/"
    data = pd.read_csv(temp_storage_path+'googlesheet-biodata.csv')
    data = pd.DataFrame(data)
    wr.s3.to_csv(
        df=data,
        path=(
            f"{my_path}googlesheet-biodata-{time.strftime(
                "%Y-%m-%d|%H:%M:%S"
                )}.csv"
            ),
        boto3_session=boto_session(),
        dataset=False
    )
    print("upload complete!")
