from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator

from datetime import datetime, timedelta

import random

def print_start_dag():
    n = random.randint(0, 50)
    print('Strating DAg')
    return n


def print_second_dag(ti):
    ti.xcom_push(key='MY_KEY', value=32)
    print('Second Dag !!!!!!')


def brach_dag():
    return random.choice(['task_A', 'task_B'])



def print_task_A(ti):
    key = ti.xcom_pull(task_ids='task_print_second_dag', key='MY_KEY')
    print(key)
    print('Tâche exécutée A !!!!')


def print_task_B():
    print('Tâche exécutée B !!!!')


with DAG("my_dag", 
         start_date=datetime(2025, 1, 1),
         schedule_interval=timedelta(seconds=30),
         catchup=False,
         end_date=datetime(2025, 10, 10),
         max_active_tasks=1,
         max_active_runs=1
         ):
    
    task_starting_dag = PythonOperator(task_id='task_starting_dag', python_callable=print_start_dag)
    
    task_print_second_dag = PythonOperator(task_id='task_print_second_dag', python_callable=print_second_dag )

    task_branch = BranchPythonOperator(task_id='task_branch', python_callable=brach_dag)

    task_A = PythonOperator(task_id='task_A', python_callable=print_task_A)

    task_B = PythonOperator(task_id='task_B', python_callable=print_task_B)

    task_bash = BashOperator(task_id='task_bash', bash_command="echo 'Bonjour' >> /root/airflow/hello.txt",
                             trigger_rule='one_success')


task_starting_dag >> task_print_second_dag >> task_branch >> [task_A, task_B] >> task_bash


# Possibilités schedule_interval

# '@once' : une seule exécution
# '@hourly' : toutes les heures
# '@daily' : tous les jours
# '@weekly' : toutes les semaines
# '@monthly' : tous les mois
# '@yearly' : tous les ans
#  timedelta(seconds=10) : toutes les 10 secondes


# all_success : déclenche le DAG si toutes les tâches précédentes ont réussi
# all_failed : déclenche le DAG si toutes les tâches précédentes ont échoué
# all_done : déclenche le DAG si toutes les tâches précédentes sont terminées
# one_success : déclenche le DAG si une tâche précédente a réussi
# one_failed : déclenche le DAG si une tâche précédente a échoué
# none_failed : déclenche le DAG si aucune tâche précédente n'a échoué
# none_skipped : déclenche le DAG si aucune tâche précédente n'a été ignorée
# none_failed_or_skipped : déclenche le DAG si aucune tâche précédente n'a échoué ou n'a été ignorée
# dummy : déclenche le DAG si la tâche précédente est une tâche factice
    