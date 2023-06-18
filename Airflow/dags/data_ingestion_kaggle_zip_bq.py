import os
import logging

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from google.cloud import storage
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator
import pyarrow.csv as pv
import pyarrow.parquet as pq
from google.cloud import bigquery

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")

dataset_file = "nifty50-stock-market-data"
dataset_url = f"kaggle datasets download -d rohanrao/{dataset_file}"
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
src_file = f"{path_to_local_home}/{dataset_file}/"
bucket_dir = f'{dataset_file}'
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", 'project2_data')


def format_to_parquet(src_file):
    for filename in os.listdir(src_file):
        if not filename.endswith('.csv'):
            logging.error("Can only accept source files in CSV format, for the moment")
            continue
        print(f"now next iteration: {filename}")
        file_path = os.path.join(src_file, filename)
        print(f"file path succed : {filename}")
        table = pv.read_csv(file_path)
        print(f"table succeed: {filename}")
        pq.write_table(table, file_path.replace('.csv', '.parquet'))
        print(f"write succeed: {filename}")
        os.remove(file_path)  # delete original csv file after converting to parquet

def upload_to_gcs(bucket_name, local_folder, bucket_dir):
    for filename in os.listdir(local_folder):
        
        storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
        storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        file_path = os.path.join(local_folder, filename)
        object_name = f"{bucket_dir}/{filename}"
        blob = bucket.blob(object_name)
        blob.upload_from_filename(file_path)
        
def create_multiple_tables(BIGQUERY_DATASET, BUCKET, SOURCE):
    client = bigquery.Client()
    
    table_ids = []
    for table in os.listdir(SOURCE):
        table_ids.append(table.replace('.parquet', ''))

    for table_id in table_ids:
        table_ref = client.dataset(BIGQUERY_DATASET).table(table_id)
        table = bigquery.Table(table_ref)

        external_config = bigquery.ExternalConfig('PARQUET')
        external_config.source_uris = [f"gs://{BUCKET}/{dataset_file}/{table_id}.parquet"]
        table.external_data_configuration = external_config

        table = client.create_table(table)  # Make an API request.

        print("Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id))



default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="data_ingestion_kaggle_zip_bq",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['dtc-de'],
) as dag:

    download_dataset_task = BashOperator(
        task_id="download_dataset_task",
        bash_command=f"""
        cd {path_to_local_home} &&
        if [ ! -d {dataset_file} ]; then
            mkdir {dataset_file} &&
            cd {dataset_file} &&
            {dataset_url} &&
            unzip {dataset_file}.zip && echo "Task succeeded" || echo "Task failed" && 
            rm {dataset_file}.zip &&
            ls
        else
            cd {dataset_file} &&
            ls
        fi
        """
    )
    
    format_to_parquet_task = PythonOperator(
        task_id="format_to_parquet_task",
        python_callable=format_to_parquet,
        op_kwargs={
            "src_file": src_file,
        },
    )
        
    local_to_gcs_task = PythonOperator(
        task_id="local_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket_name": BUCKET,
            "local_folder": f"{path_to_local_home}/{dataset_file}/",
            "bucket_dir": f"{bucket_dir}"
        },
    )
    
    create_tables_task = PythonOperator(
        task_id='create_tables',
        python_callable=create_multiple_tables,
        op_kwargs={'BIGQUERY_DATASET': BIGQUERY_DATASET, 'BUCKET': BUCKET, 'SOURCE': f"{path_to_local_home}/{dataset_file}/"},
        dag=dag,
    )   

    download_dataset_task >> format_to_parquet_task >> local_to_gcs_task >> create_tables_task
