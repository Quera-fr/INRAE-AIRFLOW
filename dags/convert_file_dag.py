from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.bash_operator import BashOperator

from datetime import datetime, timedelta
import os



# --------------------


# Fonction vérifiant les dossier convert et documents et renvoyant vers la tâche appropriée



# Fonction permettant d'écrire dans le fichier waiting.sh la commande de conversion
# os.system(f'echo "marker_single /root/airflow/data/documents/{document} --output_dir /root/airflow/data/convert_documents" > ./data/waiting.sh')



# Fonction affichant un message de fin de conversion




# --------------------




# Definition du DAG




# Tâches 1 : Lister les fichiers dans le dossier convert et documents



# Tâches 2 : Ecrire dans le fichier waiting.sh la commande de conversion


# Tâches 3 : Conversion des fichiers avec un bash operator
# bash_command="bash '/root/airflow/data/waiting.sh'"




# Tâches 4 : Affichage d'un message de fin



# Execution du DAG