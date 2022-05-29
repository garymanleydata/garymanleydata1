# -*- coding: utf-8 -*-
"""
Created on Sat May 28 19:14:12 2022

@author: garym
"""

import prefect
from prefect import task, Flow
from dotenv import load_dotenv
load_dotenv()
import requests
import urllib.request, json
import pandas as pd
from flatten_json import flatten 
from sqlalchemy import create_engine
from snowflake.connector.pandas_tools import pd_writer
import os 
from datetime import timedelta

def extract_api_data():
    activites_url = ("https://queue-times.com/parks/27/queue_times.json")
    rideData = requests.get(activites_url).json()

#    rideData = json.loads(jsonurl.read())
    return rideData

def transform(jsonData):
    flattendata = flatten(jsonData)
    normData = pd.json_normalize(flattendata)
    return normData

api_data = extract_api_data()
ride_data= transform(api_data)
print(ride_data)

