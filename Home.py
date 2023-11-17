import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
import mysql.connector
import os
import datetime
from datetime import timedelta 
from Visualizations.map_details import define_map
from Visualizations.plot_time_series import plot_ts
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Los Angeles County Air Pollutants 2000-Present", layout="wide", menu_items={"About":"Made by Leinas"}, initial_sidebar_state="collapsed")
st.markdown("<h1 style='text-align: center;'>Los Angeles County Air Pollutants Dashboard</h1>", unsafe_allow_html=True)


with open('SQL\Query_Daily_Observations.sql', 'r') as s:
    sql_query = s.read()

columns = ["Date", "HourObserved", "LocalTimeZone", "Reporting Area",
           "StateCode", "Longitude", "Latitude", "ParameterName",
           "AQI", "AQI_Number", "AQI_Classification", "DateYear", "DateMonth", "DateDay", "City", "Action_Days"]

# Connect to 'air_pollution' MySQL database instance with user credentials 
cnx = mysql.connector.connect(user='root', password=os.environ.get('MY_SQL_DB_PASS'),
                            host='127.0.0.1',
                            database='air_pollution')

# Instatiate cursor for execution of SQL queries 
cursor = cnx.cursor()

cursor.execute(sql_query)

live_data = pd.DataFrame(cursor.fetchall(), columns=columns)
live_data = live_data.loc[live_data['HourObserved'] == max(live_data['HourObserved'])]
define_map(live_data.loc[live_data['City'].isin(live_data['City'].unique())])
HtmlFile = open("map.html", 'r', encoding='utf-8')
source_code = HtmlFile.read()


st.subheader(f"**Los Angeles County Live Observations**")
components.html(source_code, width=1000, height=400)

with open('SQL\Query_weekly_observations.sql', 'r') as s:
    sql_query = s.read()

cursor.execute(sql_query)

data = pd.DataFrame(cursor.fetchall(), columns=columns)
# data = data.loc[data['HourObserved'] == max(data['HourObserved'])]
# Calculate mid-point for annotation sliding based on date range
mid_point = min(data['Date']) + (max(data['Date']) - min(data['Date']))/2

st.divider()
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(plot_ts(mid_point, data, "7 Day Air Quality Index (AQI) Monitoring", chart_type='scatter'), use_container_width=True, height= 200)

columns = ["Date", "City", "Pollutant", "AQI", "AQI_Classification"]

with open('SQL\Query_Forecast.sql', 'r') as s:
    sql_query = s.read()

cursor.execute(sql_query)
data = pd.DataFrame(cursor.fetchall(), columns = columns)
with col2:
    st.subheader("Tomorrow's AQI Forecast")
    if data.empty:
        st.write("Forecast Unavailable at the moment, come back later :)")
    else:
        
        st.dataframe(data.sort_values(by = 'City'), use_container_width=True, hide_index=True)
    
columns = ["Date", "City", "AQI", "AQI_Classification", "Month", "Action Days"]

with open('SQL\Time_Series_Pollution.sql', 'r') as s:
    sql_query = s.read()

cursor.execute(sql_query)
x = cursor.fetchall()
x = pd.DataFrame(x, columns=columns)

st.divider()
    
col3, col4, col5= st.columns(3)

with col3:
    # Add selectbox for city if multiple are extracted from DB
    city = st.selectbox(label = "**City**", options = x['City'].unique())
with col4:    
    start = st.date_input("**Start Date**", value = min(x.loc[x['City']==city]['Date']), min_value = min(x.loc[x['City']==city]['Date']), max_value = datetime.datetime.today(), format = 'MM/DD/YYYY')
with col5:
    end = st.date_input("**End Date**", value = datetime.datetime.today(), min_value = min(x.loc[x['City']==city]['Date']), max_value = datetime.datetime.today(), format = 'MM/DD/YYYY')

# Filter data based on start and end dates selected by user 
mask = (x['Date'] >=start) & (x['Date'] <= end)
x = x.loc[(mask)]


col7, col8 = st.columns([1, 1])
x = x.loc[(x['City']==city)]
with col7:
    st.subheader("Highest AQI Days")
    # x.groupby('City').get_group(city).agg({'max'})
    # x2 = x2.loc[(x2['Date'].isin(x2.groupby('City').agg('max')['Date']))]
    # st.dataframe(x.sort_values(by="City"), hide_index=True, use_container_width=True)
    



fig = px.pie(x, values='AQI_Classification', names='Month', title='Distribution of AQI Classes')
st.plotly_chart(fig, use_container_width=True)
# Add count of action days that occur in date range
action_days = x.loc[(x['Action Days']==1) & (x['AQI_Classification']!="Unhealthy for Sensitive Groups")]

# Calculate mid-point for annotation sliding based on date range
mid_point = start + (end - start)/2



with col8:
    st.plotly_chart(plot_ts(mid_point, x, title = f"{city} AQI Time Series ({min(x['Date'])})-({max(x['Date'])})", chart_type='line'), use_container_width=True)
    st.write(f"Number of Action Days: <b>{len(action_days)}</b> <br>(Days that AQI falls in Unhealthy, Very Unhealthy or Hazardous Classification)", unsafe_allow_html=True)

