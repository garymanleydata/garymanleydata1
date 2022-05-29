# -*- coding: utf-8 -*-
"""
Created on Sat May 28 14:57:44 2022

@author: garym
"""

from dotenv import load_dotenv
load_dotenv()
import os
import requests 
from flatten_json import flatten 
from sqlalchemy import create_engine
import pandas as pd
import pandasql as ps

MySQLHost = os.environ.get("MYSQLHOST2")
MySQLUser = os.environ.get("MYSQLSUER2")
MySQLPwd = os.environ.get("MYSQLPWD2")
MySQLDB = os.environ.get("MYSQLDB2")

#connection = MySQLdb.connect(host= os.getenv("HOST"),  user=os.getenv("USERNAME"),  passwd= os.getenv("PASSWORD"), db= os.getenv("DATABASE"), ssl_mode = "VERIFY_IDENTITY", ssl      = {   "ca": "/etc/ssl/cert.pem" })

mySQL_conn = create_engine("mysql+mysqldb://"+MySQLUser+":"+MySQLPwd+'@'+MySQLHost+"/"+MySQLDB , connect_args={'ssl':True});
stravaSnow = pd.read_sql_query('select * from testing',mySQL_conn)

def extract_api_data():
    activites_url = ("https://queue-times.com/parks/27/queue_times.json")
    rideData = requests.get(activites_url).json()

#    rideData = json.loads(jsonurl.read())
    return rideData

def transform(jsonData):
    flattendata = flatten(jsonData)
    normData = pd.json_normalize(flattendata)
    return normData

def load_mySQL_data(rideDataFrame,table_name):
    rideDataFrame.to_sql(table_name, con=mySQL_conn, if_exists='append',index=False)
    loaded_ind = 'Y'
    return loaded_ind 

def extract_mySQL_data(source_table):
    allRideData = pd.read_sql_query('select *  from ' + source_table ,mySQL_conn);
    return allRideData

api_data = extract_api_data()
ride_data= transform(api_data)
load_mySQL_data(ride_data,'ride_data')
allRideData = extract_mySQL_data('ride_data')

dfProcessed  = ps.sqldf("""
                        select 	lands_0_id as land_id, 
		lands_0_name as lands_name, 
		lands_0_rides_0_Id as ride_id, 
		lands_0_rides_0_name as ride_name,
		lands_0_rides_0_is_open as is_open,
		lands_0_rides_0_last_updated as log_time, 
		lands_0_rides_0_wait_time as ride_wait_time		
        from allRideData 
union all
select 	lands_1_id as land_id, 
		lands_1_name as lands_name, 
		lands_1_rides_0_Id as ride_id, 
		lands_1_rides_0_name as ride_name,
		lands_1_rides_0_is_open as is_open,
		lands_1_rides_0_last_updated as log_time,  
		lands_1_rides_0_wait_time as ride_wait_time		
        from allRideData 
union  all
select 	lands_1_id as land_id, 
		lands_1_name as lands_name, 
		lands_1_rides_1_Id as ride_id, 
		lands_1_rides_1_name as ride_name,
		lands_1_rides_1_is_open as is_open,
		lands_1_rides_1_last_updated as log_time,
		lands_1_rides_1_wait_time as ride_wait_time		
        from allRideData 
union all 
select 	lands_1_id as land_id, 
		lands_1_name as lands_name, 
		lands_1_rides_2_Id as ride_id, 
		lands_1_rides_2_name as ride_name,
		lands_1_rides_2_is_open as is_open,
		lands_1_rides_2_last_updated as log_time, 
		lands_1_rides_2_wait_time as ride_wait_time		
from allRideData
union all 
select 	lands_1_id as land_id, 
		lands_1_name as lands_name, 
		lands_1_rides_3_Id as ride_id, 
		lands_1_rides_3_name as ride_name,
		lands_1_rides_3_is_open as is_open,
		lands_1_rides_3_last_updated as log_time, 
		lands_1_rides_3_wait_time as ride_wait_time		
from allRideData
union all 
select 	lands_1_id as land_id, 
		lands_1_name as lands_name, 
		lands_1_rides_4_Id as ride_id, 
		lands_1_rides_4_name as ride_name,
		lands_1_rides_4_is_open as is_open,
		lands_1_rides_4_last_updated as log_time, 
		lands_1_rides_4_wait_time as ride_wait_time		
from allRideData
union all 
select 	lands_1_id as land_id, 
		lands_1_name as lands_name, 
		lands_1_rides_5_Id as ride_id, 
		lands_1_rides_5_name as ride_name,
		lands_1_rides_5_is_open as is_open,
		lands_1_rides_5_last_updated as log_time, 
		lands_1_rides_5_wait_time as ride_wait_time		
from allRideData
union all 
select 	lands_1_id as land_id, 
		lands_1_name as lands_name, 
		lands_1_rides_6_Id as ride_id, 
		lands_1_rides_6_name as ride_name,
		lands_1_rides_6_is_open as is_open,
		lands_1_rides_6_last_updated as log_time, 
		lands_1_rides_6_wait_time as ride_wait_time		
from allRideData 
union all 
select 	lands_2_id as land_id, 
		lands_2_name as lands_name, 
		lands_2_rides_0_Id as ride_id, 
		lands_2_rides_0_name as ride_name,
		lands_2_rides_0_is_open as is_open,
		lands_2_rides_0_last_updated as log_time, 
		lands_2_rides_0_wait_time as ride_wait_time		
from allRideData 
union all 
select 	lands_2_id as land_id, 
		lands_2_name as lands_name, 
		lands_2_rides_1_Id as ride_id, 
		lands_2_rides_1_name as ride_name,
		lands_2_rides_1_is_open as is_open,
		lands_2_rides_1_last_updated as log_time, 
		lands_2_rides_1_wait_time as ride_wait_time		
from allRideData 
union all 
select 	lands_3_id as land_id, 
		lands_3_name as lands_name, 
		lands_3_rides_0_Id as ride_id, 
		lands_3_rides_0_name as ride_name,
		lands_3_rides_0_is_open as is_open,
		lands_3_rides_0_last_updated as log_time, 
		lands_3_rides_0_wait_time as ride_wait_time		
from allRideData 
union all
select 	lands_4_id as land_id, 
		lands_4_name as lands_name, 
		lands_4_rides_0_Id as ride_id, 
		lands_4_rides_0_name as ride_name,
		lands_4_rides_0_is_open as is_open,
		lands_4_rides_0_last_updated as log_time, 
		lands_4_rides_0_wait_time as ride_wait_time		
        from allRideData 
union all
select 	lands_4_id as land_id, 
		lands_4_name as lands_name, 
		lands_4_rides_0_Id as ride_id, 
		lands_4_rides_0_name as ride_name,
		lands_4_rides_0_is_open as is_open,
		lands_4_rides_0_last_updated as log_time,  
		lands_4_rides_0_wait_time as ride_wait_time		
        from allRideData 
union  all
select 	lands_4_id as land_id, 
		lands_4_name as lands_name, 
		lands_4_rides_1_Id as ride_id, 
		lands_4_rides_1_name as ride_name,
		lands_4_rides_1_is_open as is_open,
		lands_4_rides_1_last_updated as log_time,
		lands_4_rides_1_wait_time as ride_wait_time		
        from allRideData 
union all 
select 	lands_4_id as land_id, 
		lands_4_name as lands_name, 
		lands_4_rides_2_Id as ride_id, 
		lands_4_rides_2_name as ride_name,
		lands_4_rides_2_is_open as is_open,
		lands_4_rides_2_last_updated as log_time, 
		lands_4_rides_2_wait_time as ride_wait_time		
from allRideData
union all 
select 	lands_4_id as land_id, 
		lands_4_name as lands_name, 
		lands_4_rides_3_Id as ride_idq, 
		lands_4_rides_3_name as ride_name,
		lands_4_rides_3_is_open as is_open,
		lands_4_rides_3_last_updated as log_time, 
		lands_4_rides_3_wait_time as ride_wait_time		
from allRideData
union all 
select 	lands_4_id as land_id, 
		lands_4_name as lands_name, 
		lands_4_rides_4_Id as ride_idq, 
		lands_4_rides_4_name as ride_name,
		lands_4_rides_4_is_open as is_open,
		lands_4_rides_4_last_updated as log_time, 
		lands_4_rides_4_wait_time as ride_wait_time		
from allRideData
union all
select 	lands_5_id as land_id, 
		lands_5_name as lands_name, 
		lands_5_rides_0_Id as ride_id, 
		lands_5_rides_0_name as ride_name,
		lands_5_rides_0_is_open as is_open,
		lands_5_rides_0_last_updated as log_time,  
		lands_5_rides_0_wait_time as ride_wait_time		
        from allRideData 
union  all
select 	lands_5_id as land_id, 
		lands_5_name as lands_name, 
		lands_5_rides_1_Id as ride_id, 
		lands_5_rides_1_name as ride_name,
		lands_5_rides_1_is_open as is_open,
		lands_5_rides_1_last_updated as log_time,
		lands_5_rides_1_wait_time as ride_wait_time		
        from allRideData 
union all 
select 	lands_5_id as land_id, 
		lands_5_name as lands_name, 
		lands_5_rides_2_Id as ride_id, 
		lands_5_rides_2_name as ride_name,
		lands_5_rides_2_is_open as is_open,
		lands_5_rides_2_last_updated as log_time, 
		lands_5_rides_2_wait_time as ride_wait_time		
from allRideData
union all
select 	lands_6_id as land_id, 
		lands_6_name as lands_name, 
		lands_6_rides_0_Id as ride_id, 
		lands_6_rides_0_name as ride_name,
		lands_6_rides_0_is_open as is_open,
		lands_6_rides_0_last_updated as log_time,  
		lands_6_rides_0_wait_time as ride_wait_time		
        from allRideData 
union  all
select 	lands_6_id as land_id, 
		lands_6_name as lands_name, 
		lands_6_rides_1_Id as ride_id, 
		lands_6_rides_1_name as ride_name,
		lands_6_rides_1_is_open as is_open,
		lands_6_rides_1_last_updated as log_time,
		lands_6_rides_1_wait_time as ride_wait_time		
        from allRideData 
union all
select 	lands_7_id as land_id, 
		lands_7_name as lands_name, 
		lands_7_rides_0_Id as ride_id, 
		lands_7_rides_0_name as ride_name,
		lands_7_rides_0_is_open as is_open,
		lands_7_rides_0_last_updated as log_time,  
		lands_7_rides_0_wait_time as ride_wait_time		
        from allRideData 
union  all
select 	lands_7_id as land_id, 
		lands_7_name as lands_name, 
		lands_7_rides_1_Id as ride_id, 
		lands_7_rides_1_name as ride_name,
		lands_7_rides_1_is_open as is_open,
		lands_7_rides_1_last_updated as log_time,
		lands_7_rides_1_wait_time as ride_wait_time		
        from allRideData 
union all 
select 	lands_7_id as land_id, 
		lands_7_name as lands_name, 
		lands_7_rides_2_Id as ride_id, 
		lands_7_rides_2_name as ride_name,
		lands_7_rides_2_is_open as is_open,
		lands_7_rides_2_last_updated as log_time, 
		lands_7_rides_2_wait_time as ride_wait_time		
from allRideData
union all 
select 	lands_7_id as land_id, 
		lands_7_name as lands_name, 
		lands_7_rides_3_Id as ride_id, 
		lands_7_rides_3_name as ride_name,
		lands_7_rides_3_is_open as is_open,
		lands_7_rides_3_last_updated as log_time, 
		lands_7_rides_3_wait_time as ride_wait_time		
from allRideData
union all 
select 	lands_7_id as land_id, 
		lands_7_name as lands_name, 
		lands_7_rides_4_Id as ride_id, 
		lands_7_rides_4_name as ride_name,
		lands_7_rides_4_is_open as is_open,
		lands_7_rides_4_last_updated as log_time, 
		lands_7_rides_4_wait_time as ride_wait_time		
from allRideData
union all 
select 	lands_7_id as land_id, 
		lands_7_name as lands_name, 
		lands_7_rides_5_Id as ride_id, 
		lands_7_rides_5_name as ride_name,
		lands_7_rides_5_is_open as is_open,
		lands_7_rides_5_last_updated as log_time, 
		lands_7_rides_5_wait_time as ride_wait_time		
from allRideData
union all
select 	lands_8_id as land_id, 
		lands_8_name as lands_name, 
		lands_8_rides_0_Id as ride_id, 
		lands_8_rides_0_name as ride_name,
		lands_8_rides_0_is_open as is_open,
		lands_8_rides_0_last_updated as log_time,  
		lands_8_rides_0_wait_time as ride_wait_time		
        from allRideData 
union  all
select 	lands_8_id as land_id, 
		lands_8_name as lands_name, 
		lands_8_rides_1_Id as ride_idq, 
		lands_8_rides_1_name as ride_name,
		lands_8_rides_1_is_open as is_open,
		lands_8_rides_1_last_updated as log_time,
		lands_8_rides_1_wait_time as ride_wait_time		
        from allRideData 
union all 
select 	lands_8_id as land_id, 
		lands_8_name as lands_name, 
		lands_8_rides_2_Id as ride_idq, 
		lands_8_rides_2_name as ride_name,
		lands_8_rides_2_is_open as is_open,
		lands_8_rides_2_last_updated as log_time, 
		lands_8_rides_2_wait_time as ride_wait_time		
from allRideData
union all
select 	lands_9_id as land_id, 
		lands_9_name as lands_name, 
		lands_9_rides_0_Id as ride_idq, 
		lands_9_rides_0_name as ride_name,
		lands_9_rides_0_is_open as is_open,
		lands_9_rides_0_last_updated as log_time,  
		lands_9_rides_0_wait_time as ride_wait_time		
        from allRideData 
union  all
select 	lands_9_id as land_id, 
		lands_9_name as lands_name, 
		lands_9_rides_1_Id as ride_idq, 
		lands_9_rides_1_name as ride_name,
		lands_9_rides_1_is_open as is_open,
		lands_9_rides_1_last_updated as log_time,
		lands_9_rides_1_wait_time as ride_wait_time		
        from allRideData 
union all
select 	lands_10_id as land_id, 
		lands_10_name as lands_name, 
		lands_10_rides_0_Id as ride_idq, 
		lands_10_rides_0_name as ride_name,
		lands_10_rides_0_is_open as is_open,
		lands_10_rides_0_last_updated as log_time,  
		lands_10_rides_0_wait_time as ride_wait_time		
        from allRideData 
union  all
select 	lands_10_id as land_id, 
		lands_10_name as lands_name, 
		lands_10_rides_1_Id as ride_idq, 
		lands_10_rides_1_name as ride_name,
		lands_10_rides_1_is_open as is_open,
		lands_10_rides_1_last_updated as log_time,
		lands_10_rides_1_wait_time as ride_wait_time		
        from allRideData 
union all
select 	99 as land_id, 
		'Show' as lands_name, 
		rides_0_Id as ride_idq, 
		rides_0_name as ride_name,
		rides_0_is_open as is_open,
		rides_0_last_updated as log_time,  
		rides_0_wait_time as ride_wait_time		
        from allRideData 
union  all
select 	99 as land_id, 
		'Show' as lands_name, 
		rides_1_Id as ride_idq, 
		rides_1_name as ride_name,
		rides_1_is_open as is_open,
		rides_1_last_updated as log_time,
		rides_1_wait_time as ride_wait_time		
        from allRideData 
union all 
select 	99 as land_id, 
		'Show' as lands_name,
		rides_2_Id as ride_idq, 
		rides_2_name as ride_name,
		rides_2_is_open as is_open,
		rides_2_last_updated as log_time, 
		rides_2_wait_time as ride_wait_time		
from allRideData                       """)
                        

dfProcessed.to_sql('wait_time_fact', con=mySQL_conn, if_exists='replace',index=False)
    