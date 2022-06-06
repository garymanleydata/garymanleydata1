# -*- coding: utf-8 -*-
"""
Created on Sun May 29 11:49:19 2022

Long term to do: 
    ## want to be able to filter by weather (need to add Legoland weather to weather extract script)
    ## Add Last Updated to the live Dashboard 
    ## Add photos - can I use plotly events and PIL?

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
import datetime
import json as j
from streamlit_plotly_events import plotly_events


# setup initial page config
st.set_page_config(
    page_title="Legoland Dashboard",
    page_icon="✅",
    layout="wide",
)

def init_connection(db):
    if db == 'mySQL': 
        return mysql.connector.connect(**st.secrets["planetscale"]) 

mySQLconn = init_connection('mySQL')

option = st.sidebar.selectbox("Which Dashboard?", ('Queue Data', 'Latest Data', 'Ride Closures'), 0)

if option == 'Queue Data':
    st.title("Legoland Queue Data Dashboard")
    
    ridequery = ('SELECT * FROM legoland_avg_ride_wait_v where hour_logged < 19 order by hour_logged')
    rideWaits = pd.read_sql_query(ridequery,mySQLconn);
    
    with st.sidebar:
        peakOption = st.sidebar.selectbox("What times would you like to see?", ('All Data', 'Peak Data', 'Off-Peak Data'), 0)
        displayoption = st.multiselect("Pick Land to Display",rideWaits.land_name.unique(),rideWaits.land_name.unique())
        rides = rideWaits.loc[rideWaits['land_name'].isin(displayoption)]
        displayoptionrides = st.multiselect("Pick Rides to Display",rides.ride_name.unique(),rides.ride_name.unique())


    rideWaits = rideWaits.loc[rideWaits['land_name'].isin(displayoption)]
    rideWaits = rideWaits.loc[rideWaits['ride_name'].isin(displayoptionrides)]

    metricsQ = ('select max(`queue.STANDBY.waitTime`) maxTime, round(avg(`queue.STANDBY.waitTime`),1) average from all_ride_data_time where status = "OPERATING"')
    dfMetric = pd.read_sql_query(metricsQ,mySQLconn);

   # setup columns and add a metric to each. 
    col1, col2 = st.columns(2)
    col1.metric('Max Wait Time (All)', dfMetric.iat[0,0])
    col2.metric("Average Wait Time (All)", dfMetric.iat[0,1])


    if peakOption == 'All Data':
        fig = px.line(rideWaits, x="hour_logged", y="average_wait", color='ride_name',
        color_discrete_sequence=px.colors.qualitative.Alphabet)
        measure_name = "average_wait"
    elif peakOption == 'Peak Data':
        fig = px.line(rideWaits, x="hour_logged", y="average_wait_peak", color='ride_name',
        color_discrete_sequence=px.colors.qualitative.Alphabet)
        measure_name = "average_wait_peak"
    elif peakOption == 'Off-Peak Data':
        fig = px.line(rideWaits, x="hour_logged", y="average_wait_off_peak", color='ride_name',
        color_discrete_sequence=px.colors.qualitative.Alphabet)
        measure_name = "average_wait_off_peak"

    st.write('Average Ride Waits by hour')
    st.plotly_chart(fig, use_container_width=True, sharing="streamlit")
    
    figmulti = px.line(
        rideWaits, 
        x='hour_logged', 
 #       y='average_wait', 
        y=measure_name, 
        facet_col='ride_name', 
        facet_col_wrap=3, 
        color='ride_name', 
        width=1000,
        height=2000,
        facet_row_spacing=0.04, # default is 0.07 when facet_col_wrap is used
        facet_col_spacing=0.04,
        color_discrete_sequence=px.colors.qualitative.Alphabet
        )   
    figmulti.update_layout(showlegend=False)
    st.plotly_chart(figmulti, use_container_width=True, sharing="streamlit")
    

    trace = go.Heatmap(x = rideWaits['hour_logged'] , y = rideWaits['ride_name'], z = rideWaits[measure_name] , 
        colorscale='Geyser', 
        hovertemplate='Hour Logged: %{x}<br>Ride Name: %{y}<br>Ride Wait: %{z}<extra></extra>')
    data = [trace]
    layout = go.Layout(xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Hour Logged',
            )),
        yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
        text='Ride Name',)),        
        margin=dict(t=200, r=200, b=200, l=200),
        showlegend=True,
        width=1000, height=1000,
        autosize=False)
    
    f6 = go.Figure(data, layout=layout)
    st.write('Heat Maps of Rides by Hour')  
    st.plotly_chart(f6, use_container_width=True, sharing="streamlit")
    

    ## add table showing the best times to go on each ride
    bestworstquery = ('SELECT * FROM ride_best_worst_times_v')
    bestworstdf = pd.read_sql_query(bestworstquery,mySQLconn);
    bestworstdf = bestworstdf.loc[bestworstdf['land_name'].isin(displayoption)]
    bestworstdf = bestworstdf.loc[bestworstdf['ride_name'].isin(displayoptionrides)]

    gb = GridOptionsBuilder.from_dataframe(bestworstdf)
    gb.configure_pagination()
    gridOptions = gb.build()
    st.write('Rides - Best and Worst times')  
    AgGrid(bestworstdf, gridOptions=gridOptions)

    allridequery = ('SELECT * FROM legoland_overall_waits_v order by ride_name')
    allrideWaits = pd.read_sql_query(allridequery,mySQLconn);
    
    
    url = 'https://raw.githubusercontent.com/garymanleydata/garymanleydata1/main/LegolandPython/Legoland.json'
    resp = requests.get(url)
    data  = j.loads(resp.text)    
    
    LegoMap = px.choropleth_mapbox(allrideWaits, 
                           geojson=data, 
                           locations='ride_name', 
                           color=measure_name,
                           color_continuous_scale="Geyser",
                           range_color=(0, 70),
                           mapbox_style="carto-positron", 
                           zoom=14, 
                           center = {"lat": 51.4630509  , "lon":  -0.6472471},
                           opacity=0.5 , 
                           featureidkey="properties.name",
                           labels={'Average Wait':'average_wait'}
                                                                         
                          )
    st.markdown('Map with **Average Times**.')
    st.plotly_chart(LegoMap, use_container_width=True, sharing="streamlit")

if option == 'Latest Data':
    st.title("Legoland Live Queue Data Dashboard")
    ## add a header here with last uodated time 
    
    ## add queue times per land per popular rides in columns 
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

    dayridequery = ('SELECT * FROM legoland_avg_ride_wait_today_v order by hour_logged')
    dayrideWaits = pd.read_sql_query(dayridequery,mySQLconn);

    if dayrideWaits.empty:
        st.markdown('No Data available for Today')
    else:
        st.markdown('Queue Times-- **Today Only**.')
        figmultiday = px.line(
            dayrideWaits, 
            x='hour_logged', 
            y='average_wait', 
            facet_col='ride_name', 
            facet_col_wrap=3, 
            color='ride_name', 
            width=1000,
            height=2000,
            facet_row_spacing=0.04, # default is 0.07 when facet_col_wrap is used
            facet_col_spacing=0.04
            )   
        figmultiday.update_layout(showlegend=False)
        st.plotly_chart(figmultiday, use_container_width=True, sharing="streamlit")


        ## make a live data map  
        url = 'https://raw.githubusercontent.com/garymanleydata/garymanleydata1/main/LegolandPython/Legoland.json'
        resp = requests.get(url)
        data  = j.loads(resp.text)    
    
        LegoMapLive = px.choropleth_mapbox(livedf, 
                           geojson=data, 
                           locations='ride_name', 
                           color='ride_wait_time',
                           color_continuous_scale="Geyser",
                           range_color=(0, 70),
                           mapbox_style="carto-positron", 
                           zoom=14, 
                           center = {"lat": 51.4630509  , "lon":  -0.6472471},
                           opacity=0.5 , 
                           featureidkey="properties.name",
                           labels={'Current Wait':'ride_wait_time'}
                                                                         
                          )
        st.markdown('Map with **Live Times**.')
        st.plotly_chart(LegoMapLive, use_container_width=True, sharing="streamlit")

if option == 'Ride Closures':
    with st.sidebar:
        st.write('Pick a date or range:')
        today = datetime.date.today()
        prev_date = today + datetime.timedelta(days=-7)
        start_date = st.date_input('Start date', prev_date)
        end_date = st.date_input('End date', today)
        if start_date < end_date:
            st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
        else:
            st.error('Error: End date must fall after start date.')

    st.title("Legoland Ride Closure Dashboard")    
    dfExpectedClosures = pd.read_html('https://www.legoland.co.uk/plan-your-day/useful-guides/ride-availability/')[0]
    dfExpectedClosures.set_axis(['Ride Name', 'Closure Comment'], axis=1, inplace=True)
    gb = GridOptionsBuilder.from_dataframe(dfExpectedClosures)
    gb.configure_pagination()
    gridOptions = gb.build()
    st.write('Planned Closures Today')  
    AgGrid(dfExpectedClosures, gridOptions=gridOptions)


    query = ('SELECT land_name, ride_name, run_date, log_time FROM legoland_closures_v')
    df  = pd.read_sql_query(query,mySQLconn);
    # filter data to the dates selected
    df = df[df.run_date.between(start_date, end_date)]

    
    dfTotals = ps.sqldf('SELECT  land_name, ride_name, run_date, count(*) closure_pings FROM df group by land_name, ride_name, run_date having count(*) > 3 order by run_date, ride_name')
    dfList = ps.sqldf('SELECT  ride_name, min(run_date) min_date FROM dfTotals group by ride_name order by min_date, ride_name')
    figbar = px.bar(dfTotals, x='run_date', y='closure_pings', color = "ride_name",  barmode='group')
    selected_points = plotly_events(figbar)
    if selected_points:
        selectedData = pd.DataFrame(selected_points)     
        extract = selected_points[[0][0]]
        index_of_selected = extract['curveNumber']
        date_of_selected = extract['x']
        dfSelect = dfList.filter(items = [index_of_selected], axis=0)
             
        dfSelected= ps.sqldf("SELECT df.land_name, df.ride_name, df.run_date, df.log_time FROM df INNER JOIN dfSelect on df.ride_name = dfSelect.ride_name and df.run_date = '"+ date_of_selected + "'")
        
        gb = GridOptionsBuilder.from_dataframe(dfSelected)
        gb.configure_pagination()
        gridOptions = gb.build()
        AgGrid(dfSelected, gridOptions=gridOptions)
        
        ## Output for testing only
        #selectedData
        #extract
        #index_of_selected
        #date_of_selected
        #dfList
        
    else:    
 
       st.write('Select a point in graph to display the data')          
 
## best rides to go on now page 


    # Compare averages and current queue times to work out best rides to go on now
    
    # on live dashboard have it show above / below average and rating as to which best rides to go on compared to average 
    