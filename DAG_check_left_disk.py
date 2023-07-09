from airflow import DAG
from datetime import datetime
import check_left_disk

with DAG(
    dag_id = 'DAG_check_left_disk',
    start_date = datetime(2023,5,30),
    catchup=False,
    tags=['mornitoring'],
    schedule = '5 * * * *'
) as dag:
    check_left_disk(None, None)
