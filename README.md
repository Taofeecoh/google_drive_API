# 🌐 Google Drive ETL with Apache Airflow

A functional lightweight ETL pipeline that connects to Google Drive API, extracts data from a freqeuntly updated spreadsheet, applies layers of transformations methods and loads the data into Aamzon S3 bucket. This project is orchestrated with Airflow for daily automation.

## Features
* 🔐 A `python` script that connects to google drive API leveraging `gspread` library
* 📊 Scans for target spreadsheet, opens and extract data from target sheet.
* 📊 Formats extracted data as `pandas` dataframe
* 🧹 Dataframe columns are further extracted and formated as `snake_case`
* ☁️ Transformed dataframe is loaded to Amazon s3 bucket via `bot3 session`
* ⏰ Tasks to run daily, fully automated by Airflow.
* 🔄 Tasks communicate with each other via Airflow XCom

## 📌 Tech Stack: 
Python | Apache Airflow | Boto3 | Google Drive API | Boto3

## 📁 Project Structure


# IMAGE WORKFLOW IMAGE

## ⚙️ Installation










![alt text](<WhatsApp Image 2025-06-09 at 11.46.55_9b200611.jpg>)
![alt text](image.png)
![alt text](image-1.png)