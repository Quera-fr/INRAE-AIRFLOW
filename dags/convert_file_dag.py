from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.bash_operator import BashOperator

from datetime import datetime, timedelta
import os

# --------------------


# Fonction vérifiant les dossier convert et documents et renvoyant vers la tâche appropriée
def files_check():
    list_docs = os.listdir(f'/root/airflow/data/documents')
    list_convert_docs = os.listdir(f'/root/airflow/data/convert_documents')

    for doc in list_docs:
        try:
            if doc.split('.pdf')[0] not in list_convert_docs:
                print("Document à convertir", doc.split('.pdf')[0])
                return doc.split('.pdf')[0]
            else:
                print("Document déjà converti", doc.split('.pdf')[0])
        except:
            print("Error")


# Fonction permettant d'écrire dans le fichier waiting.sh la commande de conversion
# os.system(f'echo "marker_single /root/airflow/data/documents/{document} --output_dir /root/airflow/data/convert_documents" > ./data/waiting.sh')
def data_preparation(ti):
    doc = ti.xcom_pull(task_ids='task_check_files')
    print(doc)

    if doc !=None:

        try:
            os.mkdir(f'/root/airflow/data/convert_documents/{doc}')
            os.system(f'echo "marker_single /root/airflow/data/documents/{doc}.pdf --output_dir /root/airflow/data/convert_documents/" > ./data/waiting.sh')
        except:
            print('Le dossier existe déjà.')



# Fonction affichant un message de fin de conversion
def end_dag():
    print(f'Conversion terminée')

# --------------------

# Definition du DAG
with DAG(
    'convert_documents',
    start_date=datetime(2025, 1, 1),
    schedule_interval= '@once',
    catchup=False,
    end_date=datetime(2025, 10, 10),
    max_active_tasks=1,
    max_active_runs=1):
    pass


    # Tâches 1 : Lister les fichiers dans le dossier convert et documents
    task_check_files = PythonOperator(
        task_id='task_check_files',
        python_callable=files_check)


# Tâches 2 : Ecrire dans le fichier waiting.sh la commande de conversion
    task_data_preparation = PythonOperator(
        task_id='task_data_preparation',
        python_callable=data_preparation)


# Tâches 3 : Conversion des fichiers avec un bash operator
# bash_command="bash '/root/airflow/data/waiting.sh'"
    task_convert_documents = BashOperator(
        task_id='task_convert_documents',
        bash_command="bash '/root/airflow/data/waiting.sh'")




# Tâches 4 : Affichage d'un message de fin
    task_end_dag = PythonOperator(
        task_id='task_end_dag',
        python_callable=end_dag)



# Execution du DAG
task_check_files >> task_data_preparation >> task_convert_documents >> task_end_dag