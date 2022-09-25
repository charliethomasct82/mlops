##############################################################################
# Import necessary modules

import pandas as pd
import os
import sqlite3
from sqlite3 import Error
from significant_categorical_level import list_platform,list_medium,list_source
from city_tier_mapping import *
from constants import *
from utils import *
from data_validation_checks import *
from schema import *
# #############################################################################


from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta
from utils import *


###############################################################################
# Define default arguments and DAG
###############################################################################

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022,7,30),
    'retries' : 1, 
    'retry_delay' : timedelta(seconds=5)
}


ML_data_cleaning_dag = DAG(
                dag_id = 'Lead_Scoring_Data_Engineering_Pipeline',
                default_args = default_args,
                description = 'DAG to run data pipeline for lead scoring',
                schedule_interval = '@daily',
                catchup = False
)

###############################################################################
# Create a task for build_dbs() function with task_id 'building_db'
###############################################################################
op_create_db = PythonOperator(task_id='building_db', 
                            python_callable=utils.build_dbs,
                            op_kwargs={'db_path': DB_PATH, 'db_file_name': LEAD_SCORING_DB_FILE_NAME},
                            dag=dag)
###############################################################################
# Create a task for raw_data_schema_check() function with task_id 'checking_raw_data_schema'
###############################################################################
op_raw_data_schema_check = PythonOperator(task_id='checking_raw_data_schema', 
                            python_callable=utils.raw_data_schema_check,
                            op_kwargs={'db_path': DB_PATH, 'db_file_name': LEAD_SCORING_DB_FILE_NAME},
                            dag=dag)
###############################################################################
# Create a task for load_data_into_db() function with task_id 'loading_data'
##############################################################################
op_load_data = PythonOperator(task_id='loading_data', 
                            python_callable=utils.load_data_into_db,
                              op_kwargs={'db_path': DB_PATH, 'db_file_name': LEAD_SCORING_DB_FILE_NAME, 'data_directory':DATA_DIRECTORY},
                            dag=dag)
###############################################################################
# Create a task for map_city_tier() function with task_id 'mapping_city_tier'
###############################################################################
op_map_city_tier = PythonOperator(task_id='map_city', 
                            python_callable=utils.map_city_tier,
                            op_kwargs={'db_path': DB_PATH, 'db_file_name': LEAD_SCORING_DB_FILE_NAME},
                            dag=dag)
###############################################################################
# Create a task for map_categorical_vars() function with task_id 'mapping_categorical_vars'
###############################################################################
op_map_categorical_vars = PythonOperator(task_id='mapping_categorical_vars', 
                            python_callable=utils.map_categorical_vars,
                            op_kwargs={'db_path': DB_PATH, 'db_file_name': LEAD_SCORING_DB_FILE_NAME},
                            dag=dag)
###############################################################################
# Create a task for interactions_mapping() function with task_id 'mapping_interactions'
###############################################################################
op_interactions_mapping = PythonOperator(task_id='mapping_interactions', 
                            python_callable=utils.interactions_mapping,
                            op_kwargs={'db_path': DB_PATH, 'db_file_name': LEAD_SCORING_DB_FILE_NAME},
                            dag=dag)
###############################################################################
# Create a task for model_input_schema_check() function with task_id 'checking_model_inputs_schema'
###############################################################################
op_model_input_schema_check = PythonOperator(task_id='checking_model_inputs_schema', 
                            python_callable=utils.model_input_schema_check,
                            op_kwargs={'db_path': DB_PATH, 'db_file_name': LEAD_SCORING_DB_FILE_NAME},
                            dag=dag)
###############################################################################
# Define the relation between the tasks
###############################################################################

# op_init.set_downstream(op_create_db)
op_create_db.set_downstream(op_raw_data_schema_check)

# op_init.set_downstream(op_create_db)
op_raw_data_schema_check.set_downstream(op_load_data)

# op_init.set_downstream(op_create_db)
op_load_data.set_downstream(op_map_city_tier)

# op_init.set_downstream(op_create_db)
op_map_city_tier.set_downstream(op_map_categorical_vars)

# op_init.set_downstream(op_create_db)
op_map_categorical_vars.set_downstream(op_interactions_mapping)

# op_init.set_downstream(op_create_db)
op_interactions_mapping.set_downstream(op_model_input_schema_check)

