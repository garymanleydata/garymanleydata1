
import streamlit as st 
import pandas as pd
from sqlalchemy import create_engine
from snowflake.connector.pandas_tools import pd_writer

# setup database connection strings
import snowflake.connector

st.set_page_config(
    page_title="Strava Data Dashboard",
    page_icon="✅",
    layout="wide",
)

# dashboard title
st.title("Gary Manley Strava Data Dashboard")

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
df = df.rename(columns={'ACTIVITY_DATE':'index'}).set_index('index')
df

st.write('This is a line_chart.')
st.line_chart(df)