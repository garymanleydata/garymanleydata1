
import streamlit as st 
import pandas as pd
import snowflake.connector
import plotly.express as px
import datetime

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
 
query = ('SELECT ACTIVITY_DATE ,  sum(DISTANCE_KM) distance_km, sum(moving_time_minutes) move_minutes FROM STRAVA_ACTIVITIES_STAR_FACT WHERE "TYPE" IN (\'Run\',\'Walk\') GROUP BY  ACTIVITY_DATE order by ACTIVITY_DATE')
cur = conn.cursor().execute(query)
df = pd.DataFrame.from_records(iter(cur), columns=[x[0] for x in cur.description])
#df2 = df
df = df[df.ACTIVITY_DATE.between(start_date, end_date)]
df = df.rename(columns={'ACTIVITY_DATE':'index'}).set_index('index')
df

st.write('This is a line_chart.')
st.line_chart(df)

st.write('This is a bar chart with plotly.')

query = ('SELECT ACTIVITY_DATE , "TYPE",  sum(DISTANCE_KM) distance_km, sum(moving_time_minutes) move_minutes FROM STRAVA_ACTIVITIES_STAR_FACT WHERE "TYPE" IN (\'Run\',\'Walk\') GROUP BY  ACTIVITY_DATE , "TYPE" order by ACTIVITY_DATE')
cur = conn.cursor().execute(query)
df2 = pd.DataFrame.from_records(iter(cur), columns=[x[0] for x in cur.description])
df2 = df2[df2.ACTIVITY_DATE.between(start_date, end_date)]
fig = px.bar(df2, x='ACTIVITY_DATE', y='DISTANCE_KM', color = "TYPE")
st.plotly_chart(fig, use_container_width=True, sharing="streamlit")