from datetime import timedelta

import pendulum
from airflow.decorators import dag
from airflow.operators.dummy import DummyOperator

from plugins.helpers import SqlQueries
from plugins.operators import (StageToRedshiftOperator, LoadFactOperator,
                               LoadDimensionOperator, DataQualityOperator)

default_args = {
    'owner': 'udacity',
    'depends_on_past': False,
    'start_date': pendulum.now(),
    'retries': 5,
    'retry_delay': timedelta(minutes=3),
    'catchup': False,
    'email_on_retry': False,
}


@dag(
    default_args=default_args,
    description='Load and transform data in Redshift with Airflow',
    schedule_interval='0 * * * *',

)
def final_project():
    start_operator = DummyOperator(task_id='Begin_execution')

    stage_events_to_redshift = StageToRedshiftOperator(
        task_id='Stage_events',
        redshift_conn_id='redshift',
        aws_credentials_id='aws_credentials',
        table='public.staging_events',
        s3_url='s3://datas3-fee5e117/log-data/',
        json_option='s3://datas3-fee5e117/log_json_path.json',
    )

    stage_songs_to_redshift = StageToRedshiftOperator(
        task_id='Stage_songs',
        redshift_conn_id='redshift',
        aws_credentials_id='aws_credentials',
        table='public.staging_songs',
        s3_url='s3://datas3-fee5e117/song-data/',
    )

    load_songplays_table = LoadFactOperator(
        task_id='Load_songplays_fact_table',
        redshift_conn_id='redshift',
        table='public.songplays',
        source_query=SqlQueries.songplay_table_insert,
    )

    load_user_dimension_table = LoadDimensionOperator(
        task_id='Load_user_dim_table',
        redshift_conn_id='redshift',
        table='public.users',
        source_query=SqlQueries.user_table_insert,
        insert_mode='overwrite',
    )

    load_song_dimension_table = LoadDimensionOperator(
        task_id='Load_song_dim_table',
        redshift_conn_id='redshift',
        table='public.songs',
        source_query=SqlQueries.song_table_insert,
        insert_mode='overwrite',
    )

    load_artist_dimension_table = LoadDimensionOperator(
        task_id='Load_artist_dim_table',
        redshift_conn_id='redshift',
        table='public.artists',
        source_query=SqlQueries.artist_table_insert,
        insert_mode='overwrite',
    )

    load_time_dimension_table = LoadDimensionOperator(
        task_id='Load_time_dim_table',
        redshift_conn_id='redshift',
        table='public.time',
        source_query=SqlQueries.time_table_insert,
        insert_mode='overwrite',
    )

    run_quality_checks = DataQualityOperator(
        task_id='Run_data_quality_checks',
        redshift_conn_id='redshift',
        tests_and_expectations=[
            {
                "test": "SELECT COUNT(*) AS null_counts FROM public.songplays WHERE playid IS NULL",
                "expected": 0,
            },
            {
                "test": "SELECT COUNT(*) AS null_counts FROM public.songs WHERE songid IS NULL",
                "expected": 0,
            },
            {
                "test": "SELECT COUNT(*) AS null_counts FROM public.artists WHERE artistid IS NULL",
                "expected": 0,
            },
            {
                "test": "SELECT COUNT(*) AS null_counts FROM public.users WHERE userid IS NULL",
                "expected": 0,
            },
            {
                "test": "SELECT COUNT(*) AS null_counts FROM public.time WHERE start_time IS NULL",
                "expected": 0,
            },
            {
                "test": """SELECT COUNT(*)
                           FROM (SELECT songid, COUNT(*) duplicates
                                 FROM public.songs
                                 GROUP BY songid
                                 HAVING COUNT (*) > 1) sub;""",
                "expected": 0,
            }
        ],
    )

    end_operator = DummyOperator(task_id='End_execution')

    start_operator >> [stage_events_to_redshift, stage_songs_to_redshift] >> load_songplays_table >> [
        load_user_dimension_table, load_song_dimension_table, load_artist_dimension_table,
        load_time_dimension_table] >> run_quality_checks >> end_operator


final_project_dag = final_project()
