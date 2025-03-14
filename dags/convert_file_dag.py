from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python import ShortCircuitOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator


from datetime import datetime, timedelta
import os,subprocess

from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma

def check_new_files(ti):
    folder="/root/airflow/data/documents"
    if os.path.exists(folder):
        print('Folder exists')
        files=os.listdir(folder)
        list_files = [os.path.join(folder,f) for f in files if os.path.isfile(os.path.join(folder,f))]
        if list_files:
            print(list_files)
            ti.xcom_push(key="files", value=list_files)
            return True
        else:
            print(f"Aucun fichier dans {folder}. Arrêt du process.")
            return False
    else:
        print(f"Le dossier {folder} n'existe pas. Arrêt du process.")
        return False

def marker_convert_files(ti):
    files = ti.xcom_pull(task_ids="task_check_new_files", key="files")
    output_dir="/root/airflow/data/convert_documents"
    list_path_converted_md = list()
    if not files:
        print("Aucun fichier à traiter")
        return
    
    for input_file in files:
        print(input_file)
        file_without_ext = os.path.basename(input_file.join(input_file.split('.')[:-1]))
        converted_file_path_md = os.path.join(output_dir,file_without_ext,file_without_ext+".md")
        print(file_without_ext)
        if file_without_ext in os.listdir(output_dir):
            print(f"Conversion déjà effectuée pour {input_file}")
            #list_path_converted_md.append(converted_file_path_md)
        else: 
            command = ["marker_single", input_file, "--output_dir", output_dir]
            try:
                print("Lancement de la conversion !")
                result=subprocess.run(command,check=True,text=True,capture_output=True)
                print("Conversion réussie !")
                print("Sortie:",result.stdout)
                list_path_converted_md.append(converted_file_path_md)
            except subprocess.CalledProcessError as e:
                print("Erreur lors de la conversion :", e.stderr)
                return False
    
    ti.xcom_push(key="list_path_converted_md", value=list_path_converted_md)

# Definition du DAG

with DAG("convert_file_dag",
         start_date=datetime(2025,1,1),
         schedule_interval=timedelta(seconds=240),
         end_date=datetime(2025, 10, 10),
         catchup=False,
         max_active_tasks=1,
         max_active_runs=1,): 

    task_check_new_files=ShortCircuitOperator(task_id='task_check_new_files',python_callable=check_new_files)
    task_convert_marker=PythonOperator(task_id='task_convert_marker',python_callable=marker_convert_files)

    triger_task = TriggerDagRunOperator(
       task_id='trigger_task',
       trigger_dag_id='text_summary_dag',
       trigger_rule= 'all_success'
       )


# Execution du DAG
task_check_new_files >> task_convert_marker >> triger_task