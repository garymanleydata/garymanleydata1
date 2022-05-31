# -*- coding: utf-8 -*-
"""
Created on Tue May 31 09:10:36 2022

@author: garym
"""

import pandas as pd
import json as j
import streamlit as st
import mysql.connector

def init_connection(db):
    if db == 'mySQL': 
        return mysql.connector.connect(**st.secrets["planetscale"]) 

mySQLconn = init_connection('mySQL')
ridequery = ('SELECT * FROM legoland_overall_waits_v')
rideWaits = pd.read_sql_query(ridequery,mySQLconn);
# Opening JSON file
f = open(r'C:\Users\garym\Documents\GitHub\garymanleydata\LegolandPython\Legoland.json')
  
# returns JSON object as 
# a dictionary
data = j.load(f)

#df = pd.read_json(r'C:\Users\garym\Documents\GitHub\garymanleydata\LegolandPython\Legoland.json')

import plotly.express as px

fig = px.choropleth_mapbox(rideWaits, 
                           geojson=data, 
                           locations='ride_name', 
                           color='average_wait',
                           color_continuous_scale="Viridis",
                           range_color=(0, 120),
                           mapbox_style="carto-positron", 
                           zoom=16, 
                           center = {"lat": 51.4630509  , "lon":  -0.6472471},
                           opacity=0.5 , 
                           featureidkey="properties.name",
                           labels={'Average Wait':'average_wait'}
                                                                         
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#from plotly.offline import download_plotlyjs, init_notebook_mode,  plot
# plot(fig)