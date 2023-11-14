import streamlit as st
import mysql.connector
import os
from dotenv import load_dotenv
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import datetime
load_dotenv()


st.set_page_config(page_title="Pollution Time Series", layout="wide", menu_items={"About":"Made by Leinas"})

st.sidebar.header("Options")

with open('SQL\Time_Series_Pollution.sql', 'r') as s:
    sql_query = s.read()

# Connect to 'air_pollution' MySQL database instance with user credentials 
cnx = mysql.connector.connect(user='root', password=os.environ.get('MY_SQL_DB_PASS'),
                            host='127.0.0.1',
                            database='air_pollution')
# Instatiate cursor for execution of SQL queries 
cursor = cnx.cursor()

columns = ["Date", "City", "AQI", "AQI_Classification", "Month", "Action Days"]

cursor.execute(sql_query)
x = cursor.fetchall()
x = pd.DataFrame(x, columns=columns)

# Add selectbox for city if multiple are extracted from DB
city = st.sidebar.selectbox(label = "**City**", options = x['City'].unique())
start = st.sidebar.date_input("**Start Date**", value = min(x.loc[x['City']==city]['Date']), min_value = min(x.loc[x['City']==city]['Date']), max_value = datetime.datetime.today(), format = 'MM/DD/YYYY')
end = st.sidebar.date_input("**End Date**", value = datetime.datetime.today(), min_value = min(x.loc[x['City']==city]['Date']), max_value = datetime.datetime.today(), format = 'MM/DD/YYYY')
# Filter data based on start and end dates selected by user 
mask = (x['Date'] >=start) & (x['Date'] <= end)
x = x.loc[(mask) & (x['City']==city)]
# Add count of action days that occur in date range
action_days = x.loc[(x['Action Days']==1) & (x['AQI_Classification']!="Unhealthy for Sensitive Groups")]
st.sidebar.write(f"Number of Action Days: <b>{len(action_days)}</b> <br>(Days that AQI falls in Unhealthy, Very Unhealthy or Hazardous Classification)", unsafe_allow_html=True)

# Calculate mid-point for annotation sliding based on date range
mid_point = start + (end - start)/2
# Plot Time Series
fig = px.line(x.sort_values('Date'), x = "Date", y ="AQI", color = "City", title = f"{city} Air Quality Index (AQI) Time Series ({min(x['Date'])})-({max(x['Date'])})")
# AQI Classification lines for reference points of AQI values
fig.add_hline(y=50, line_width=3, line_dash="dash", line_color="green")
fig.add_hline(y=100, line_width=3, line_dash="dash", line_color="yellow")
fig.add_hline(y=150, line_width=3, line_dash="dash", line_color="orange")
fig.add_hline(y=200, line_width=3, line_dash="dash", line_color="red")
fig.add_annotation(x=mid_point, y=25, text="Good", showarrow = False)
fig.add_annotation(x=mid_point, y=75, text="Moderate", showarrow = False)
fig.add_annotation(x=mid_point, y=125, text="Unhealthy for Sensitive Groups", showarrow = False)
fig.add_annotation(x=mid_point, y=175, text="Unhealthy", showarrow = False)
fig.add_annotation(x=mid_point, y=210, text="Very Unhealthy/Hazardous", showarrow = False)

st.plotly_chart(fig)

