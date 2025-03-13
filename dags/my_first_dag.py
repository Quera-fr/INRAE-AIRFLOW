from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.bash_operator import BashOperator

from datetime import datetime, timedelta

import random

def random_number(ti):
    ti.xcom_push(key='MY_KEY', value='API_KEY')
    return random.randint(0, 1000)

def random_task():
    return random.choice(["task_1", "task_2"])

def print_hello(ti, name='Kevin'):
    nb = ti.xcom_pull(task_ids="first_task", key='return_value')
    key = ti.xcom_pull(task_ids="first_task", key='MY_KEY')
    print(f"Hello {name}", nb, key)
    return nb


def print_goodbye():
    print("Goodbye")


    

with DAG(
    "my_first_dag",
    start_date=datetime(2025, 1, 1),
    schedule_interval=timedelta(seconds=30),
    end_date=datetime(2025, 10, 10),
    max_active_tasks=1,
    max_active_runs=1

    ):

    first_task = PythonOperator(
        task_id="first_task",
        python_callable=random_number,
    )

    task_bash = BashOperator(
        task_id="task_bash",
        bash_command="echo 'Hello World' >> /root/airflow/text.txt",
    )

    task_random_choice = BranchPythonOperator(task_id="task_random_choice", 
                                              python_callable=random_task)

    task_1 = PythonOperator(task_id="task_1", python_callable=print_hello)

    task_2 = PythonOperator(task_id="task_2", python_callable=print_hello,
                            op_kwargs={"name": "John"})

    task_goodbye = PythonOperator(task_id="task_goodbye", python_callable=print_goodbye, 
                                  trigger_rule="one_success")
    
    first_task >> task_bash >> task_random_choice >> [task_1, task_2] >> task_goodbye




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
    
