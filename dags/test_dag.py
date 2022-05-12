from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.operators.python import PythonOperator

from airflow.providers.amazon.aws.hooks.s3 import S3Hook

AWS_S3_CONN_ID = "aws_default"
MYSQL_CONN_ID = "mysql_default"


def s3_extract():
    source_s3_bucket = "reports"
    source_s3 = S3Hook(AWS_S3_CONN_ID)
    key_list = source_s3.list_keys(source_s3_bucket)
    print(key_list)
    mysql_hook = MySqlHook(mysql_conn_id=MYSQL_CONN_ID)
    conn = mysql_hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    test_str = cursor.fetchall()
    print(test_str)
    test_2 = source_s3.read_key('test.csv', 'reports')
    print(test_2)


with DAG(
        dag_id="s3_extract",
        start_date=datetime(2022, 2, 12),
        schedule_interval=timedelta(days=1),
        catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id="s3_extract_task",
        python_callable=s3_extract)

    t1
