
import streamlit as st 
import pandas as pd
import snowflake.connector
import plotly.express as px
import datetime
import pandasql as ps
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

st.set_page_config(
    page_title="Gary Manley Data Dashboard",
    page_icon="✅",
    layout="wide",
)

def init_connection():
    return snowflake.connector.connect(**st.secrets["snowflake"])

conn = init_connection()

option = st.sidebar.selectbox("Which Dashboard?", ('Strava Data', 'Strength Data', 'parkrun results'), 0)

st.header(option)
# dashboard title
st.title("Gary Manley Data Dashboard")

if option == 'Strava Data':
    with st.sidebar:
        displayoption = st.multiselect("Pick Data to Display", ('Full Table', 'Distance / Time Line', 'Run/Walk Split'),default = ('Distance / Time Line', 'Run/Walk Split'))
        st.write('Pick a date range:')
        today = datetime.date.today()
        prev_date = today + datetime.timedelta(days=-30)
        start_date = st.date_input('Start date', prev_date)
        end_date = st.date_input('End date', today)
        if start_date < end_date:
            st.success('Start date: `%s`\n\nEnd date:`%s`' % (start_date, end_date))
        else:
            st.error('Error: End date must fall after start date.')

    query = ('SELECT UPLOAD_ID, "TYPE" as ACTIVITY_TYPE ,ACTIVITY_DATE,DISTANCE_METRES,DISTANCE_KM,DISTANCE_MILES,MOVING_TIME_SECONDS,MOVING_TIME_MINUTES,TOTAL_ELEVATION_GAIN,AVERAGE_SPEED,AVERAGE_CADENCE,AVERAGE_HEARTRATE,MAX_SPEED,MAX_HEARTRATE,DATE_DAY,DATE_YEAR,DATE_MONTH,DATE_QUARTER,DAY_OF_WEEK,DAY_OF_YEAR,WEEK_OF_DAY,DAY_NAME,LAG_DATE_1,YEAR_MONTH FROM STRAVA_ACTIVITIES_STAR_FACT')
    cur = conn.cursor().execute(query)
    df = pd.DataFrame.from_records(iter(cur), columns=[x[0] for x in cur.description])
    df = df[df.ACTIVITY_DATE.between(start_date, end_date)]

    df[['ACTIVITY_TYPE', 'ACTIVITY_DATE', 'DATE_DAY','DAY_NAME','LAG_DATE_1','YEAR_MONTH' ]] = df[['ACTIVITY_TYPE', 'ACTIVITY_DATE', 'DATE_DAY','DAY_NAME','LAG_DATE_1','YEAR_MONTH']].astype(str)
    
    dfMetric = ps.sqldf('SELECT ROUND(sum(DISTANCE_KM),1) distance_km , ROUND(sum(MOVING_TIME_MINUTES),1) total_move, ROUND(sum(TOTAL_ELEVATION_GAIN),1) total_elevation FROM df WHERE ACTIVITY_TYPE IN (\'Run\',\'Walk\') ')
    
    
    col1, col2, col3 = st.columns(3)
    TotalDistance = dfMetric.iat[0,0]
    col1.metric('Total Distance Logged', dfMetric.iat[0,0])
    col2.metric("Total Minutes Logged", dfMetric.iat[0,1])
    col3.metric("Total Elevation Gain", dfMetric.iat[0,2])

    if 'Full Table' in displayoption:
        
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination()
        gridOptions = gb.build()

        AgGrid(df, gridOptions=gridOptions)

    if 'Distance / Time Line' in displayoption:

        st.write('This is a line_chart using Streamlit')
        dfTable  = ps.sqldf('SELECT ACTIVITY_DATE ,  sum(DISTANCE_KM) distance_km, sum(moving_time_minutes) move_minutes FROM df WHERE ACTIVITY_TYPE IN (\'Run\',\'Walk\') GROUP BY  ACTIVITY_DATE order by ACTIVITY_DATE')
        dfTable = dfTable.rename(columns={'ACTIVITY_DATE':'index'}).set_index('index')
        st.line_chart(dfTable)

    if 'Run/Walk Split' in displayoption:
        st.write('This is a bar chart with plotly.')
        dfStacked  = ps.sqldf('SELECT ACTIVITY_DATE , ACTIVITY_TYPE,  sum(DISTANCE_KM) distance_km, sum(moving_time_minutes) move_minutes FROM df WHERE ACTIVITY_TYPE IN (\'Run\',\'Walk\') GROUP BY  ACTIVITY_DATE , ACTIVITY_TYPE order by ACTIVITY_DATE')
        fig = px.bar(dfStacked, x='ACTIVITY_DATE', y='distance_km', color = "ACTIVITY_TYPE")
        st.plotly_chart(fig, use_container_width=True, sharing="streamlit")