# 🌐 Google Drive ETL with Apache Airflow

A functional lightweight ETL pipeline that connects to Google Drive API, extracts data from a freqeuntly updated spreadsheet, applies layers of transformations methods and loads the data into Aamzon S3 bucket. This project is orchestrated with Airflow for daily automation.

## Contents
* [Features](#features)
* [Structure](#-project-structure)
* [Setup](#️-how-to-setup-this-project)
* [Contributions](#-contributions)


## Features
* 🔐 A `python` script that connects to google drive API leveraging `gspread` library
* 📊 Scans for target spreadsheet's existence, opens and extract data from target sheet.
* 📊 Formats extracted data as `pandas` dataframe
* 🧹 Dataframe columns are further extracted and formated as `snake_case`
* ☁️ Loads transformed dataframe to Amazon s3 bucket via `awswrangler`
* ⏰ Tasks to run daily, fully automated by Airflow.
* 🔄 Tasks communicate with each other via Airflow XCom

**📌 Tech Stack:  Python3.12 | Apache Airflow | Docker | Boto3 | Google Drive API | Boto3**

## 📁 Project Structure

![alt text](images/image-2.png)

## ⚙️ How to setup this project
1. Prerequisite: 
    * running `docker desktop` or `docker engine` to containerize Airflow
    * `python 3.12`
    * Google service account credentials
    * Amazon s3 bucket and IAM User access key

2. Clone this repository to your local machine
    ```bash
    git clone https://github.com/Taofeecoh/google_drive_API.git
    ```

3. Change to project's directory 
    ```bash
    cd google_drive_API/orchestration
    ```

4. Create virtual environment
    ```bash
    python3 -m venv .venv
    ```

5. Activate environment
    ```bash
    source .venv/bin/activate  # On Linux
    source .venv\Scripts\activate # On windows
    ```

6. Change your working directory to the project's orchestration directory
    ```bash
    cd google_drive_API/orchestration
    ```

7. Install requirements
    ```bash
    pip install apache-airflow==2.11.0
    pip install -r requirements.txt
    ```

8. Configure airflow
    ```bash
    mkdir -p ./dags ./logs ./plugins ./config
    ```

    ```bash                         
    echo -e "AIRFLOW_UID=$(id -u)" > .env # if you don't have an .env file
    echo -e "AIRFLOW_UID=$(id -u)" >> .env # append if you have an .env file
    ```

9. Spin up airflow docker containers
    ```bash
    docker compose up airflow-init 
    ```
    ```bash
    docker compose up -d
    ```

10. Log into Airflow UI at `localhost:8080` and create `airflow` variables : 
    * `AWS_KEY_ID`
    * `AWS_SECRET_KEY`
    * `CREDENTIALS`

## 🤝 Contributions
Contributions are welcome! Please fork the repository and submit a pull request with your enhancements.


## Known Issue

![alt text](images/image.png)
![alt text](images/image-1.png)