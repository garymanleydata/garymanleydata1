# -*- coding: utf-8 -*-
"""
Created on Sun May 29 11:49:19 2022

@author: garym
"""


import streamlit as st 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
#import datetime
import pandasql as ps
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
import mysql.connector
import requests
import json as j


# setup initial page config
st.set_page_config(
    page_title="Gary Manley Legoland Dashboard",
    page_icon="✅",
    layout="wide",
)

def init_connection(db):
    if db == 'mySQL': 
        return mysql.connector.connect(**st.secrets["planetscale"]) 

mySQLconn = init_connection('mySQL')

option = st.sidebar.selectbox("Which Dashboard?", ('Queue Data', 'Latest Data', 'Closure Rates'), 0)

if option == 'Queue Data':
    st.title("Legoland Queue Data Dashboard")
    
    ridequery = ('SELECT * FROM legoland_avg_ride_wait_v order by hour_logged')
    rideWaits = pd.read_sql_query(ridequery,mySQLconn);
    
    with st.sidebar:
        displayoption = st.multiselect("Pick Land to Display",rideWaits.land_name.unique(),rideWaits.land_name.unique())
        rides = rideWaits.loc[rideWaits['land_name'].isin(displayoption)]
        displayoptionrides = st.multiselect("Pick Rides to Display",rides.ride_name.unique(),rides.ride_name.unique())


    rideWaits = rideWaits.loc[rideWaits['land_name'].isin(displayoption)]
    rideWaits = rideWaits.loc[rideWaits['ride_name'].isin(displayoptionrides)]

    metricsQ = ('select max(`queue.STANDBY.waitTime`) maxTime, round(avg(`queue.STANDBY.waitTime`),1) average from all_ride_data_time where status = "OPERATING"')
    dfMetric = pd.read_sql_query(metricsQ,mySQLconn);

   # setup columns and add a metric to each. 
    col1, col2 = st.columns(2)
    col1.metric('Max Wait Time', dfMetric.iat[0,0])
    col2.metric("Average Wait Time", dfMetric.iat[0,1])

    fig = px.line(rideWaits, x="hour_logged", y="average_wait", color='ride_name')
    st.plotly_chart(fig, use_container_width=True, sharing="streamlit")

    heatmap = go.Figure(data = go.Heatmap(x = rideWaits['hour_logged'] , y = rideWaits['ride_name'], z = rideWaits['average_wait'] ))
    heatmap.update_layout(
        margin=dict(t=200, r=200, b=200, l=200),
        showlegend=True,
        width=1000, height=1000,
        autosize=False)
  
    #heatmap = px.imshow(rideWaits.drop('lands_name', 1))
    st.plotly_chart(heatmap, use_container_width=True, sharing="streamlit")

    ## add table showing the best times to go on each ride
    bestworstquery = ('SELECT * FROM ride_best_worst_times_v')
    bestworstdf = pd.read_sql_query(bestworstquery,mySQLconn);
    bestworstdf = bestworstdf.loc[bestworstdf['land_name'].isin(displayoption)]
    bestworstdf = bestworstdf.loc[bestworstdf['ride_name'].isin(displayoptionrides)]

    gb = GridOptionsBuilder.from_dataframe(bestworstdf)
    gb.configure_pagination()
    gridOptions = gb.build()

    AgGrid(bestworstdf, gridOptions=gridOptions)
    
    
    url = 'https://raw.githubusercontent.com/garymanleydata/garymanleydata1/main/LegolandPython/Legoland.json'
    resp = requests.get(url)
    data  = j.loads(resp.text)    
    
    LegoMap = px.choropleth_mapbox(rideWaits, 
                           geojson=data, 
                           locations='ride_name', 
                           color='average_wait',
                           color_continuous_scale="Viridis",
                           range_color=(0, 120),
                           mapbox_style="carto-positron", 
                           zoom=14, 
                           center = {"lat": 51.4630509  , "lon":  -0.6472471},
                           opacity=0.5 , 
                           featureidkey="properties.name",
                           labels={'Average Wait':'average_wait'}
                                                                         
                          )
    st.plotly_chart(LegoMap, use_container_width=True, sharing="streamlit")

if option == 'Latest Data':
    st.title("Legoland Live Queue Data Dashboard")
    liveQ = ('SELECT * FROM live_wait_times_v')
    livedf = pd.read_sql_query(liveQ,mySQLconn);

    dfMetrics = ps.sqldf('SELECT sum(case when ride_wait_time > -0.5 THEN 1 else 0 end) as RidesOpen, sum(case when ride_wait_time < -0.5 THEN 1 else 0 end) as RidesClosed FROM livedf')

    col1, col2 = st.columns(2)
    col1.metric('Rides Open', dfMetrics.iat[0,0])
    col2.metric("Rides Closed", dfMetrics.iat[0,1])

    gb = GridOptionsBuilder.from_dataframe(livedf)
    gb.configure_pagination()
    gridOptions = gb.build()

    AgGrid(livedf, gridOptions=gridOptions)

    liveMap = ('SELECT * FROM location_lat_lon')
    mapdf = pd.read_sql_query(liveMap,mySQLconn);

 ## make a live data map and a live data by land with columns  
    
## work out best order to go on selected rides. 
## anyway to integrate  map? and plot route for a day