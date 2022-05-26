# -*- coding: utf-8 -*-
"""
Created on Thu May 26 15:55:57 2022

@author: garym
"""


import streamlit as st 
import pandas as pd
import snowflake.connector
import plotly.express as px
import datetime
import pandasql as ps

st.set_page_config(
    page_title="Strava Data Dashboard",
    page_icon="✅",
    layout="wide",
)

# dashboard title
st.title("Gary Manley Strava Data Dashboard")
st.markdown('Streamlit is **_really_ cool**.')

today = datetime.date.today()
prev_date = today + datetime.timedelta(days=-30)
start_date = st.date_input('Start date', prev_date)
end_date = st.date_input('End date', today)
if start_date < end_date:
    st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
else:
    st.error('Error: End date must fall after start date.')

def init_connection():
    return snowflake.connector.connect(**st.secrets["snowflake"])

#Snowengine = create_engine(init_connection())

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

#rows = run_query("SELECT * from STRAVA_ACTIVITIES_STAR_FACT;")
# Print results.
#for row in rows:
#    st.write(f"{row[0]} has a :{row[1]}:")
 
query = ('SELECT UPLOAD_ID, "TYPE" as ACTIVITY_TYPE ,ACTIVITY_DATE,DISTANCE_METRES,DISTANCE_KM,DISTANCE_MILES,MOVING_TIME_SECONDS,MOVING_TIME_MINUTES,TOTAL_ELEVATION_GAIN,AVERAGE_SPEED,AVERAGE_CADENCE,AVERAGE_HEARTRATE,MAX_SPEED,MAX_HEARTRATE,DATE_DAY,DATE_YEAR,DATE_MONTH,DATE_QUARTER,DAY_OF_WEEK,DAY_OF_YEAR,WEEK_OF_DAY,DAY_NAME,LAG_DATE_1,YEAR_MONTH FROM STRAVA_ACTIVITIES_STAR_FACT')
cur = conn.cursor().execute(query)
df = pd.DataFrame.from_records(iter(cur), columns=[x[0] for x in cur.description])
df = df[df.ACTIVITY_DATE.between(start_date, end_date)]

df[['ACTIVITY_TYPE', 'ACTIVITY_DATE', 'DATE_DAY','DAY_NAME','LAG_DATE_1','YEAR_MONTH' ]] = df[['ACTIVITY_TYPE', 'ACTIVITY_DATE', 'DATE_DAY','DAY_NAME','LAG_DATE_1','YEAR_MONTH']].astype(str)
dfTable  = ps.sqldf('SELECT ACTIVITY_DATE ,  sum(DISTANCE_KM) distance_km, sum(moving_time_minutes) move_minutes FROM df WHERE ACTIVITY_TYPE IN (\'Run\',\'Walk\') GROUP BY  ACTIVITY_DATE order by ACTIVITY_DATE')
dfTable = dfTable.rename(columns={'ACTIVITY_DATE':'index'}).set_index('index')
dfTable
