import time
import os
import logging

import awswrangler as wr
import boto3
import gspread
import pandas as pd
from dotenv import load_dotenv
from airflow.models import Variable
from utils.module import to_snakecase

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
