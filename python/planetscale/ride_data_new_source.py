# -*- coding: utf-8 -*-
"""
Created on Mon May 30 10:12:30 2022

@author: garym
"""

from dotenv import load_dotenv
load_dotenv()
import os
import requests 
from sqlalchemy import create_engine
import pandas as pd
import schedule
from datetime import datetime, time
import time as t

MySQLHost = os.environ.get("MYSQLHOST2")
MySQLUser = os.environ.get("MYSQLSUER2")
MySQLPwd = os.environ.get("MYSQLPWD2")
MySQLDB = os.environ.get("MYSQLDB2")

#connection = MySQLdb.connect(host= os.getenv("HOST"),  user=os.getenv("USERNAME"),  passwd= os.getenv("PASSWORD"), db= os.getenv("DATABASE"), ssl_mode = "VERIFY_IDENTITY", ssl      = {   "ca": "/etc/ssl/cert.pem" })

mySQL_conn = create_engine("mysql+mysqldb://"+MySQLUser+":"+MySQLPwd+'@'+MySQLHost+"/"+MySQLDB , connect_args={'ssl':True});
stravaSnow = pd.read_sql_query('select * from testing',mySQL_conn)

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time


def extract_api_data():
    activites_url = ("https://api.themeparks.wiki/v1/entity/legolandwindsorresort/live")
    rideData = requests.get(activites_url).json()

#    rideData = json.loads(jsonurl.read())
    return rideData

def transform(jsonData):
    wait_data = pd.json_normalize(jsonData, record_path='liveData')
    return wait_data

def load_mySQL_data(rideDataFrame,table_name):
    rideDataFrame['run_time'] = datetime.utcnow().time()
    rideDataFrame['run_date'] = datetime.utcnow().date()
    rideDataFrame.to_sql(table_name, con=mySQL_conn, if_exists='append',index=False)
    loaded_ind = 'Y'
    return loaded_ind 

def job():
    now = datetime.utcnow().time()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    if is_time_between(time(8,30), time(19,30)):
        api_data = extract_api_data()
        ride_data= transform(api_data)
        load_mySQL_data(ride_data,'all_ride_data_time')
        print('API Data Loaded')
    else: 
        print('Not in time frame')

#api_data = extract_api_data()
#job()
schedule.every(10).minutes.do(job)

while True:
    schedule.run_pending()
    t.sleep(1)
