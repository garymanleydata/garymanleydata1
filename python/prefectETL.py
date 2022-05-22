# -*- coding: utf-8 -*-
"""
Created on Sat May 21 20:25:39 2022

@author: garym
"""
import prefect
from prefect import task, Flow
from dotenv import load_dotenv
load_dotenv()
import urllib.request, json
import pandas as pd
from flatten_json import flatten 
from sqlalchemy import create_engine
from snowflake.connector.pandas_tools import pd_writer
import os 

# Load Keys
#weather
weatherkey = os.environ.get("WEATHER_API_KEY") 
#mySQL
MySQLHost = os.environ.get("MYSQLHOST")
MySQLUser = os.environ.get("MYSQLSUER")
MySQLPwd = os.environ.get("MYSQLPWD")
MySQLDB = os.environ.get("MYSQLDB")
#Snowflake
SnowAcc = os.environ.get("SNOWACC")
SnowUser = os.environ.get("SNOWUSER")
SnowPwd = os.environ.get("SNOWPWD")
SnowDB = os.environ.get("SNOWDB")
SnowWH = os.environ.get("SNOWWH")
SnowSchema = os.environ.get("SNOWSCHEMA")

# setup database connection strings
mySQL_conn = create_engine("mysql+mysqldb://"+MySQLUser+":"+MySQLPwd+'@'+MySQLHost+"/"+MySQLDB);
Snowengine = create_engine(
        'snowflake://{user}:{password}@{account}/{db}/{schema}?warehouse={warehouse}'.format(
                user= SnowUser,
                password= SnowPwd,
                account= SnowAcc,
                warehouse= SnowWH,
                db= SnowDB,
                schema=SnowSchema ))

@task
def extract_api_data():
    jsonurl = urllib.request.urlopen("http://api.weatherapi.com/v1/current.json?key="+weatherkey+"&q=BN266NH&aqi=yes")
    weatherdatajson = json.loads(jsonurl.read())
    return weatherdatajson

@task
def transform(weatherdatajson):
    flattendata = flatten(weatherdatajson)
    normWeatherData = pd.json_normalize(flattendata)
    return normWeatherData

@task
def load_mySQL_data(normWeatherData):
    normWeatherData.to_sql('stg_weather', con=mySQL_conn, if_exists='append',index=False)
    loaded_ind = 'Y'
    return loaded_ind 

@task    
def extract_mySQL_data(loaded_ind):
    if loaded_ind == 'Y' :  
        toSnow = pd.read_sql_query('select distinct location_name locationName, location_region LocationRegion , location_country LocationCountry , location_lat Latitude , location_lon Longitude , current_last_updated currentLastUpdated , current_temp_c currentTempC , current_condition_text currentCondText, current_wind_mph windMph , current_precip_mm rainMM , current_humidity Humidity , current_cloud Cloud , current_feelslike_c FeelsLikeC  from stg_weather',mySQL_conn)
    return toSnow

@task
def load_live_data(toSnow):
    toSnow.to_sql('stg_weather', con=Snowengine, if_exists='replace',index=False, method=pd_writer)
    
with Flow("Weather-ETL") as flow:
    weatherdatajson = extract_api_data()
    normWeatherData = transform(weatherdatajson)
    loadedmySQL = load_mySQL_data(normWeatherData)
    frommySQL = extract_mySQL_data(loadedmySQL)  
    end = load_live_data(frommySQL)

