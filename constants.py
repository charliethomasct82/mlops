# You can create more variables according to your project. The following are the basic variables that have been provided to you
import pandas as pd
DB_PATH ='C:/Users/44775/Desktop/Assignment/01_data_pipeline/scripts'
DB_FILE_NAME ='utils_output.db'

DATA_DIRECTORY = 'C:/Users/44775/Desktop/Assignment/01_data_pipeline/scripts/data'
INTERACTION_MAPPING =pd.read_csv('C:/Users/44775/Desktop/Assignment/01_data_pipeline/scripts/interaction_mapping.csv')
INDEX_COLUMNS = ['first_platform_c','first_utm_medium_c', 'first_utm_source_c', 'total_leads_dropped',
       'referred_lead', 'app_complete_flag','city_tier']
INTERACTION_MAPPING=pd.read_csv('C:\\Users\\44775\\Desktop\\Assignment\\01_data_pipeline\\scripts\\interaction_mapping.csv')

#df_event_mapping=pd.read_csv('C:\\Users\\44775\\Desktop\\Assignment\\01_data_pipeline\\notebooks\\Maps\\interaction_mapping.csv',index_col[0])
INDEX_COLUMNS = ['created_date','first_platform_c','first_utm_medium_c','first_utm_source_c','total_leads_dropped','referred_lead', 'app_complete_flag','city_tier']

INPUT_FILE_NAME= '/leadscoring.csv'
MODEL_INPUT_FILE_NAME='/cleaned_data.csv'

LEAD_SCORING_DB_FILE_NAME='lead_scoring_data_cleaning.db' 

UNIT_TEST_DB_FILE_NAME = '/unit_test_cases.db'








