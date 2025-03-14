from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.bash_operator import BashOperator

from datetime import datetime, timedelta
import os

from utiles.functions import n



# --------------------


# Fonction vérifiant les dossier convert et documents et renvoyant vers la tâche appropriée
def check_file():
    print(n)
    list_documents = os.listdir('/root/airflow/data/documents')
    list_documents_covert = os.listdir('/root/airflow/data/convert_documents')

    for doc in list_documents:
        if doc.split('.pdf')[0] not in list_documents_covert:
            print('Fichier à convertir', doc)
            return doc.split('.pdf')[0]
    
    



# Fonction permettant d'écrire dans le fichier waiting.sh la commande de conversion
# os.system(f'echo "marker_single /root/airflow/data/documents/{document} --output_dir /root/airflow/data/convert_documents" > ./data/waiting.sh')
def data_preparation(ti):
    doc = ti.xcom_pull(task_ids='task_chek_file')
    print(doc)

    try :
        os.makedirs(f'/root/airflow/data/convert_documents/{doc}')
        os.system(f'echo "marker_single /root/airflow/data/documents/{doc}.pdf --output_dir /root/airflow/data/convert_documents/" > ./data/waiting.sh')
    except:
        pass





# Fonction affichant un message de fin de conversion




# --------------------


# Definition du DAG

with DAG(
    'convert_pdf_dag',
    start_date=datetime(2025, 1, 1),
    schedule_interval='@once',
        max_active_tasks=1,
    max_active_runs=1

    ):
    pass



# Tâches 1 : Lister les fichiers dans le dossier convert et documents
    task_chek_file = PythonOperator(
        task_id ='task_chek_file',
        python_callable= check_file
    )


# Tâches 2 : Ecrire dans le fichier waiting.sh la commande de conversion
    task_data_preparation = PythonOperator(
        task_id ='task_data_preparation',
        python_callable= data_preparation
    )
    


# Tâches 3 : Conversion des fichiers avec un bash operator

task_convert = BashOperator(
    task_id ='task_convert',
    bash_command="bash '/root/airflow/data/waiting.sh'"

)




# Tâches 4 : Affichage d'un message de fin



# Execution du DAG
task_chek_file >> task_data_preparation >> task_convert