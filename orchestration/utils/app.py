import time
import os
import logging

import awswrangler as wr
import boto3
import gspread
import pandas as pd
from dotenv import load_dotenv
from airflow.models import Variable
from orchestration.utils.module import to_snakecase

load_dotenv()

client = gspread.service_account_from_dict(
        Variable.get("CREDENTIALS_AIRFLOW_GSERVICE", deserialize_json=True)
    )

spreadsheet_source = "marketing_source"
timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
bucket_key = "s3://tao-general-ingestion/xcom-googlesheet-dump/"
file_path = "{}marketing-googlesheet-data-{}.csv".format(bucket_key, timestamp)
logging.basicConfig(
    filename="logfile.log",
    level=logging.INFO,
    format='%(levelname)s:%(message)s:%(asctime)s')


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


def googlesheet_to_s3(
        client, 
        spreadsheet_name, 
        file_path
        ):
    
    """
    Function to connect to google drive API and extract data
    :params client: instance of connection to googlesheet API
    :params spreadsheet_name: the target spreadsheet.
    :params file_path: 
        Amazon s3 path to write file to e.g("s3://bucket_name/directory/filename.extension")
    :returns: success message when ingestion is complete
    """
    try:
        spreadsheet = client.open(spreadsheet_name)
        if spreadsheet:
            logging.info("spreadsheet found...")
            worksheet = spreadsheet.sheet1.get_all_records()
            data = pd.DataFrame(worksheet)
            logging.info("ingested successfully!:")
            columns_list = data.columns.to_list()

            # used to_snakecase to transform columns
            columns_list = to_snakecase(columns_list)
            data.columns = columns_list
            logging.info("Column names updated successfully!")
            wr.s3.to_csv(
                df=data,
                path=file_path,
                dataset=False,
                boto3_session=boto_session()
            )
            logging.info("upload to s3 complete!")
        else:
            logging.info("spreadsheet does not exist!")
    except Exception as e:
        logging.info(e)


# def transform_col_names(ti):
#     """
#     Function to transform list items to snake_case format
#     :params ti: airflow task instance to pull data from
#     :returns: list of items in snake_case
#     """
#     data_frame = ti.xcom_pull(task_ids='connect_to_driveAPI')
#     data_list = data_frame.columns.to_list()
#     col = to_snakecase(data_list=data_list)
#     data_frame.columns = col
#     print("Column names updated successfully!")
#     return data_frame


# def to_s3(ti):
#     """
#     Function to write DataFrame to S3 in parquet format.
#     :return: completion messsage when upload is completed successfully
#     """
#     data_frame = ti.xcom_pull(task_ids="transform_data")
#     my_path = "s3://tao-general-ingestion/xcom-googlesheet-dump/"
#     wr.s3.to_csv(
#         df=data_frame,
#         path=(
#             f"{my_path}marketing-googlesheet-data-{time.strftime(
#                 "%Y-%m-%d|%H:%M:%S"
#                 )}.csv"
#             ),
#         boto3_session=boto_session(),
#         dataset=False
#     )
#     print("upload to s3 complete!")
