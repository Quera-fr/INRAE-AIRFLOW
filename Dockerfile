FROM continuumio/miniconda3

WORKDIR /root/airflow

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY airflow.cfg .

COPY airflow.db . 

COPY plugins/ plugins/

COPY dags/ dags/

CMD airflow standalone