from airflow.decorators import task, dag
from airflow.operators.bash import BashOperator
from datetime import datetime

@dag(start_date=datetime(2022, 1, 1), schedule_interval="@daily", catchup=False)
def docker_dag():
    extractor = BashOperator(
        task_id = "extractor",
        bash_command = "docker run --rm -v /datalake:/datalake -v /assets:/assets -it $(docker build -q ../../extractor)"
    )
    
    transformer = BashOperator(
        task_id = "transformer",
        bash_command = "docker run --rm -v /datalake:/datalake -it $(docker build -q ../../transformer)"
    )

    extractor >> transformer

dag = docker_dag()