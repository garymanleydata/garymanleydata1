# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 17:09:52 2022

@author: garym
"""

import pandas as pd
import pandasql as ps
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import create_engine
import os

def create_date_table(start='2022-01-01', end='2050-12-31'):
         df = pd.DataFrame({"Date": pd.date_range(start, end)})
         df["Day"] = df.Date.dt.day_name()
         df["Week"] = df.Date.dt.isocalendar().week
         df["Quarter"] = df.Date.dt.quarter
         df["Year"] = df.Date.dt.year
         df["Year_half"] = (df.Quarter + 1) // 2
         return df

def load_mySQL_data(rideDataFrame,table_name):
    rideDataFrame.to_sql(table_name, con=mySQL_conn, if_exists='append',index=False)
    loaded_ind = 'Y'
    return loaded_ind 

df = create_date_table()     
df["Peak_ind"] = ""
dfSelected= ps.sqldf('SELECT Date, Day, Week, Quarter, Year, Year_half, Peak_ind FROM df  ')

MySQLHost = os.environ.get("MYSQLHOST2")
MySQLUser = os.environ.get("MYSQLSUER2")
MySQLPwd = os.environ.get("MYSQLPWD2")
MySQLDB = os.environ.get("MYSQLDB2")

#connection = MySQLdb.connect(host= os.getenv("HOST"),  user=os.getenv("USERNAME"),  passwd= os.getenv("PASSWORD"), db= os.getenv("DATABASE"), ssl_mode = "VERIFY_IDENTITY", ssl      = {   "ca": "/etc/ssl/cert.pem" })

mySQL_conn = create_engine("mysql+mysqldb://"+MySQLUser+":"+MySQLPwd+'@'+MySQLHost+"/"+MySQLDB , connect_args={'ssl':True});


load_mySQL_data(dfSelected,'calendar_dim')
        