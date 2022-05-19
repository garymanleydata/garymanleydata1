# -*- coding: utf-8 -*-
"""
Version Number ||| Mod By  ||| Version Date
---------------------------------------------------------
1.00           |||  GM     ||| 19 May  2022

"""
from dotenv import load_dotenv
load_dotenv()
import os 
from sqlalchemy import create_engine
import requests
import urllib3
import pandas as pd
from snowflake.connector.pandas_tools import pd_writer
import pandasql as ps
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

MySQLHost = os.environ.get("MYSQLHOST")
MySQLUser = os.environ.get("MYSQLSUER")
MySQLPwd = os.environ.get("MYSQLPWD")
MySQLDB = os.environ.get("MYSQLDB")
SnowAcc = os.environ.get("SNOWACC")
SnowUser = os.environ.get("SNOWUSER")
SnowPwd = os.environ.get("SNOWPWD")
SnowDB = os.environ.get("SNOWDB")
SnowWH = os.environ.get("SNOWWH")
SnowSchema = os.environ.get("SNOWSCHEMA")
StravaClient = os.environ.get("STRAVACLIENT")
StravaRefresh = os.environ.get("STRAVAREFRESH")
StravaSecret = os.environ.get("STRAVASECRET")

mySQL_conn = create_engine("mysql+mysqldb://"+MySQLUser+":"+MySQLPwd+'@'+MySQLHost+"/"+MySQLDB);
Snowengine = create_engine(
        'snowflake://{user}:{password}@{account}/{db}/{schema}?warehouse={warehouse}'.format(
                user= SnowUser,
                password= SnowPwd,
                account= SnowAcc,
                warehouse= SnowWH,
                db= SnowDB,
                schema=SnowSchema ))


def stravaPipe():
    auth_url = "https://www.strava.com/oauth/token"
    activites_url = "https://www.strava.com/api/v3/athlete/activities"

    payload = {
        'client_id': StravaClient,
        'client_secret': StravaSecret,
        'refresh_token': StravaRefresh,
        'grant_type': "refresh_token",
        'f': 'json'
            }   

    res = requests.post(auth_url, data=payload, verify=False)
    access_token = res.json()['access_token']

    header = {'Authorization': 'Bearer ' + access_token}
    param = {'per_page': 200, 'page': 1}
    my_strava = requests.get(activites_url, headers=header, params=param).json()

    normStravaData = pd.json_normalize(my_strava)

    normStravaData = normStravaData.drop(['map.summary_polyline','flagged'	,'gear_id'	,'start_latlng'	,'end_latlng'], axis=1)
    stravaLimited = ps.sqldf("select name,	distance,	moving_time,	elapsed_time,	total_elevation_gain,	type, id,	start_date_local,average_speed,	max_speed,	average_cadence,	average_heartrate,	max_heartrate,elev_high,	elev_low,	upload_id,	upload_id_str FROM normStravaData")
    stravaLimited.to_sql('pre_stg_strava', con=mySQL_conn, if_exists='replace',index=False)
    ## need to add in SQL in here to extract the data from pre stg
    stravaDelta = pd.read_sql_query('select * from stg_strava_v',mySQL_conn)
    delta = stravaDelta.shape[0]
    
    print(str(delta) + " rows inserted")
    
    stravaDelta.to_sql('stg_strava', con=mySQL_conn, if_exists='append',index=False)
    stravaSnow = pd.read_sql_query('select * from stg_strava',mySQL_conn)
    stravaSnow.columns = stravaSnow.columns.str.upper()
    stravaSnow.to_sql('stg_strava', con=Snowengine, if_exists='replace',index=False, method=pd_writer);
    print('Snowflake Load Completed')
    

