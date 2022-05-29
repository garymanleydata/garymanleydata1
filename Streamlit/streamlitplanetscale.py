# -*- coding: utf-8 -*-
"""
Created on Sun May 29 11:49:19 2022

@author: garym
"""


import streamlit as st 
import pandas as pd
import snowflake.connector
import plotly.express as px
import datetime
import pandasql as ps
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import mysql.connector
from sqlalchemy import create_engine

# setup initial page config
st.set_page_config(
    page_title="Gary Manley Legoland Dashboard",
    page_icon="✅",
    layout="wide",
)

# setup snowflake config
#def init_connection(db):
#    if db == 'snowflake':
#        return snowflake.connector.connect(**st.secrets["snowflake"])
 #   if db == 'mySQL': 
 #       return mysql.connector.connect(**st.secrets["planetscale"])#, connect_args={'ssl':True})    


mySQLconn = create_engine("mysql+mysqldb://"+st.secrets["MYSQLSUER2"]+":"+st.secrets["MYSQLPWD2"]+'@'+st.secrets["MYSQLHOST2"]+"/"+st.secrets["MYSQLDB2"] , connect_args={'ssl':True});


#mySQLconn = init_connection('mySQL') 

parkrunQuery = ('SELECT * FROM testing')
toSnow = pd.read_sql_query(parkrunQuery,mySQLconn);

toSnow