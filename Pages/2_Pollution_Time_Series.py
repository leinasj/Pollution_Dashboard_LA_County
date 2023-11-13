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
# start = st.sidebar.date_input("Start Date", value = '2000-01-01', min_value = '2000-01-01', max_value = datetime.datetime.today(), format = 'YYYY-MM-DD')
# end = st.sidebar.date_input("End Date", value = datetime.datetime.today(), min_value = '2000-01-01', max_value = datetime.datetime.today(), format = 'YYYY-MM-DD')

with open('SQL\Time_Series_Pollution.sql', 'r') as s:
    sql_query = s.read()

# Connect to 'air_pollution' MySQL database instance with user credentials 
cnx = mysql.connector.connect(user='root', password=os.environ.get('MY_SQL_DB_PASS'),
                            host='127.0.0.1',
                            database='air_pollution')
# Instatiate cursor for execution of SQL queries 
cursor = cnx.cursor()

columns = ["DateObserved", "City", "AQI", "AQI_Classification", "DateMonth"]

cursor.execute(sql_query)
x = cursor.fetchall()
x = pd.DataFrame(x, columns=columns)

# #greater than the start date and smaller than the end date
# mask = (x['DateObserved'] > start) & (x['DateObserved'] <= end)
# x = x.loc[mask]

# fig = plt.figure(figsize=(10, 4))
fig = px.line(x, x = "DateObserved", y ="AQI", color = "City", title = f"Los Angeles County Time Series ({min(x['DateObserved'])})-({max(x['DateObserved'])})")
fig.add_hline(y=50, line_width=3, line_dash="dash", line_color="green")
fig.add_hline(y=100, line_width=3, line_dash="dash", line_color="yellow")
fig.add_hline(y=150, line_width=3, line_dash="dash", line_color="orange")
fig.add_hline(y=200, line_width=3, line_dash="dash", line_color="red")
fig.add_annotation(x="2023-01-01", y=25, text="Good", showarrow = False)
fig.add_annotation(x="2023-01-01", y=75, text="Moderate", showarrow = False)
fig.add_annotation(x="2023-01-01", y=125, text="Unhealthy for Sensitive Groups", showarrow = False)
fig.add_annotation(x="2023-01-01", y=175, text="Unhealthy", showarrow = False)
fig.add_annotation(x="2023-01-01", y=210, text="Hazardous", showarrow = False)

st.plotly_chart(fig)


