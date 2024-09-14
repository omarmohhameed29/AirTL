import sys
import os
import logging
from sqlalchemy import create_engine
import pandas as pd
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import timedelta, datetime
from airflow.utils.trigger_rule import TriggerRule
from airflow.utils.task_group import TaskGroup

# Add the path to the plugins directory
sys.path.append(os.path.join(os.path.dirname(__file__), '../plugins'))
from fotmob_scrapper import extract, transform
from mail_util import send_success_mail, send_failure_mail

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def pre_execute_callback(context):
    logging.info("Preparing to send email")
    logging.info(f"SMTP connection details: {context['task_instance'].task.conn_id}")

def insert_into_table_task_func(**kwargs):
    """
    Insert transformed data into Postgres matches table using PostgresHook.
    """
    ti = kwargs['ti']
    df = ti.xcom_pull(task_ids='transform')  # Pull DataFrame from XCom
    if df is not None:
        hook = PostgresHook(postgres_conn_id='postgres_conn')  # Connection ID configured in Airflow
        conn = hook.get_conn()
        cursor = conn.cursor()

        # Insert DataFrame into Postgres table
        for _, row in df.iterrows():
            print(row)
            insert_query = """
            INSERT INTO matches (
                away_team, home_team, round, cancelled, finished, match_date, country, name,
                selected_season, type, home_score, away_score
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, tuple(row))
        conn.commit()

        logger.info("Data inserted into Postgres successfully!")
        cursor.close()
        conn.close()
    else:
        logger.error("No data to insert into Postgres.")

default_args = {
    'owner': 'omar',
    'email': ['omarmohhameed828@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': False,
    'max_retry_delay': timedelta(hours=1),
    'start_date': datetime(2024, 9, 14),
    'end_date': datetime(2024, 12, 31),
    'schedule_interval': '@daily',
    'catchup': False,
    'pool': 'default_pool'
}

with DAG(
    "AirTL",
    default_args=default_args,
    description="DAG tutorial",
    template_searchpath=['plugins']
) as dag:

    # Extract task
    extract_task = PythonOperator(
        task_id="extract",
        python_callable=extract
    )

    # Transform task function
    def transform_task_func(**kwargs):
        ti = kwargs['ti']
        extracted_data = ti.xcom_pull(task_ids='extract')
        if extracted_data is not None:
            transformed_data = transform(extracted_data)
            return transformed_data
        else:
            logger.error("No data to transform.")
            return None

    # Transform task
    transform_task = PythonOperator(
        task_id="transform",
        python_callable=transform_task_func
    )

    with TaskGroup(group_id='load') as load:
        # Create table in Postgres
        create_table_task = PostgresOperator(
            task_id="create_table",
            postgres_conn_id='postgres_conn',  # Connection ID configured in Airflow
            sql="create_table.sql"
        )

        # Load transformed data into the Postgres table using PostgresHook
        insert_into_table_task = PythonOperator(
            task_id='insert_to_table',
            python_callable=insert_into_table_task_func
        )

        create_table_task >> insert_into_table_task

    email_task = PythonOperator(
        task_id='send_success_email',
        python_callable=send_success_mail
    )

    failure_email_task = EmailOperator(
        task_id="failure_email",
        to=["om0558064@gmail.com"],
        subject="Task Failed in Airflow DAG",
        html_content="<h3>One or more tasks in your Airflow DAG have failed.</h3>",
        trigger_rule=TriggerRule.ONE_FAILED
    )

    # Task sequence
    extract_task >> transform_task >> load >> email_task
    [extract_task, transform_task, load] >> failure_email_task
