FROM apache/airflow:2.11.0
WORKDIR /app
COPY requirements.txt  /app/ 
# COPY gspread-api-462623-c3c3b4126b29.json /opt/airflow/
RUN pip install -r requirements.txt
