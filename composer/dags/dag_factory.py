import os
import json
from airflow import DAG
from datetime import datetime
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor

# Define the folder where JSON configurations are stored
DAGS_FOLDER = "/opt/airflow/dags/json_config"

def create_dag(file_name):
    """Creates an Airflow DAG from a given JSON configuration file."""
    file_path = os.path.join(DAGS_FOLDER, file_name)

    try:
        with open(file_path, "r") as f:
            config = json.load(f)

        dag_id = config.get("dag_id")
        schedule = config.get("schedule")
        datflow_job_nm = config.get("dataflow_job_nm")
        file_prefix = config.get("file_prefix")

        if not dag_id or not schedule:
            print(f"Skipping {file_name}: Missing 'dag_id' or 'schedule'.")
            return None

        default_args = {
            'start_date': datetime(2025, 3, 25),
            'catchup': False
        }

        dag = DAG(
            dag_id=dag_id,
            schedule_interval=schedule,
            default_args=default_args,
            description=f"Dynamically generated DAG from {file_name}",
        )

        # Define sample tasks
        start = EmptyOperator(task_id="start", dag=dag)
        detect_file = FileSensor(task_id='detect_file',mode='poke',poke_interval=30,filepath=f"C:/apache_beam/Input_files/{file_prefix}", timeout = 600)
        df_job = BashOperator(task_id='df_job',bash_command=f"python {datflow_job_nm}.py")
        end = EmptyOperator(task_id="end", dag=dag)
        start >> detect_file >> df_job >> end

        return dag

    except Exception as e:
        print(f"Error processing {file_name}: {e}")
        return None

# Iterate over JSON files in the folder and register DAGs
for file in os.listdir(DAGS_FOLDER):
    if file.endswith(".json"):  # Ensure it's a JSON file
        dag = create_dag(file)
        if dag:
            globals()[dag.dag_id] = dag  # Register DAG dynamically
