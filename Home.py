import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
import mysql.connector
import os
import datetime
from datetime import timedelta 
from Visualizations.map_details import define_map
from Visualizations.plot_time_series import plot_ts
from dotenv import load_dotenv
load_dotenv()

hide_streamlit_style = """ <style> footer {visibility: hidden;} </style> """
st.set_page_config(page_title="Los Angeles County Air Pollutants 2000-Present",page_icon="Visualizations/air_pollution.png", layout="wide", menu_items={"About":"Made by Leinas"}, initial_sidebar_state="collapsed")
st.markdown("<h1 style='text-align: center;'>Los Angeles County Air Pollutants Dashboard</h1>", unsafe_allow_html=True)
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

with open('SQL/Query_Daily_Observations.sql', 'r') as s:
    sql_query = s.read()

columns = ["Date", "HourObserved", "LocalTimeZone", "Reporting Area",
           "StateCode", "Longitude", "Latitude", "ParameterName",
           "AQI", "AQI_Number", "AQI_Classification", "DateYear", "DateMonth", "DateDay", "City", "Action_Days"]

# Connect to 'air_pollution' MySQL database instance with user credentials 
conn = st.connection('mysql', type='sql')


live_data = pd.DataFrame(conn.query(sql_query), columns=columns)
live_data = live_data.loc[live_data['HourObserved'] == max(live_data['HourObserved'])]
define_map(live_data.loc[live_data['City'].isin(live_data['City'].unique())])
HtmlFile = open("map.html", 'r', encoding='utf-8')
source_code = HtmlFile.read()


st.subheader(f"**Los Angeles County Live Observations**")
st.caption(f"**Last Observation made at {live_data['HourObserved'].unique()[0]}:00 {live_data['LocalTimeZone'].unique()[0]}, {live_data['Date'].unique()[0].isoformat()}**")
components.html(source_code, width=1000, height=400)

with open('SQL/Query_weekly_observations.sql', 'r') as s:
    sql_query = s.read()

data = pd.DataFrame(conn.query(sql_query), columns=columns)
# Calculate mid-point for annotation sliding based on date range
mid_point = min(data['Date']) + (max(data['Date']) - min(data['Date']))/2

st.divider()

#****** 7-Day AQI Monitoring and AQI Forecast ******

cities = np.append(data['City'].unique(), "Select All")
col1, col2 = st.columns(2)
with col1:
    # Add selectbox for city if multiple are extracted from DB
    city1 = st.selectbox(label = "**City**", options = np.roll(cities,1))
    if city1 != 'Select All':
        data = data.loc[data['City']==city1]
    st.plotly_chart(plot_ts(mid_point, data, "7 Day Air Quality Index (AQI) Monitoring", chart_type='scatter'), use_container_width=True, height= 200)

columns = ["Date", "City", "Pollutant", "AQI", "AQI_Classification"]

with open('SQL/Query_Forecast.sql', 'r') as s:
    sql_query = s.read()

data = pd.DataFrame(conn.query(sql_query), columns = columns)
with col2:
    
    if data.loc[data['Date'] == datetime.date.today() + timedelta(days=1)].empty:
        st.subheader("Today's AQI Forecast")
        st.dataframe(data.loc[data['Date'] == datetime.date.today()].sort_values(by = 'City'), use_container_width=True, hide_index=True)
    else:
        st.subheader("Today's AQI Forecast")
        st.dataframe(data.loc[data['Date'] == datetime.date.today()].sort_values(by = 'City'), use_container_width=True, hide_index=True)
        st.subheader("Tomorrow's AQI Forecast")    
        st.dataframe(data.loc[data['Date'] == datetime.date.today()+ timedelta(days=1)].sort_values(by = 'City'), use_container_width=True, hide_index=True)
    
columns = ["Date", "City", "AQI", "AQI_Classification", "Month", "Action Days"]

with open('SQL/Time_Series_Pollution.sql', 'r') as s:
    sql_query = s.read()

x = pd.DataFrame(conn.query(sql_query), columns=columns)

st.divider()

#****** Select Boxes for Filtering ******
    
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
x = x.loc[(mask) & (x['City']==city)]
x['Action Days'] = x['Action Days'].replace({0:"No", 1:"Yes"})
#****** Highest AQI Days and Time Series in Date Range ******
# Add count of action days that occur in date range
action_days = x.loc[(x['Action Days']=="Yes")]

# Calculate mid-point for annotation sliding based on date range
mid_point = min(x['Date']) + (end - min(x['Date']))/2

st.plotly_chart(plot_ts(mid_point, x, title = f"{city} AQI Time Series ({min(x['Date'])})-({max(x['Date'])})", chart_type='line'), use_container_width=True)
st.write(f"Number of Action Days: <b>{len(action_days)}</b> <br>(Days that AQI falls in Unhealthy for Sensitive Groups, Unhealthy, Very Unhealthy or Hazardous Classification)", unsafe_allow_html=True)
col7, col8 = st.columns(2)
with col7:
    st.caption(f"Highest AQI Days per Month in {city}")
    idx = x.groupby('Month')['AQI'].idxmax()
    max_AQI = x.loc[idx]
    st.dataframe(max_AQI.sort_values(by="Month")[["Date", "AQI", "AQI_Classification", "Month", "Action Days"]], hide_index=True, use_container_width=True, height=450)

color_map = ['green','yellow','orange','red','purple', 'maroon']
classification_map = ["Good", "Moderate", "Unhealthy for Sensitive Groups", "Unhealthy", "Very Unhealthy/Hazardous"]
with col8:
    fig = go.Figure(data=[go.Pie(labels=classification_map, values=x['AQI_Classification'].sort_values().value_counts(normalize=False), hole=.3)])
    fig.update_layout(title=f"Distribution of AQI Classes for {city} ({min(x['Date'])})-({max(x['Date'])})")
    fig.update_traces(marker=dict(colors=color_map),hoverinfo='label+percent', textinfo='percent',textposition='inside')
    st.plotly_chart(fig, use_container_width=True)
