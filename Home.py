import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import json
import streamlit.components.v1 as components
import mysql.connector
import os
import datetime
from Images.map_details import define_map
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Los Angeles County Air Pollutants 2000-Present", layout="wide", menu_items={"About":"Made by Leinas"})
st.markdown("<h1 style='text-align: center;'>Los Angeles County Air Pollutants Live Observations</h1>", unsafe_allow_html=True)
st.sidebar.header("Options")


with open('SQL\Query_Daily_Observations.sql', 'r') as s:
    sql_query = s.read()
with open('SQL\Query_air_now_data_columns.sql', 'r') as s:
    columns = s.read()

# Connect to 'air_pollution' MySQL database instance with user credentials 
cnx = mysql.connector.connect(user='root', password=os.environ.get('MY_SQL_DB_PASS'),
                            host='127.0.0.1',
                            database='air_pollution')
# Instatiate cursor for execution of SQL queries 
cursor = cnx.cursor()
cursor.execute(columns)
x = cursor.fetchall()
x= pd.DataFrame(x, columns=['Columns'])
cursor.execute(sql_query)
data = pd.DataFrame(cursor.fetchall(), columns=x['Columns'])
data = data.loc[data['HourObserved'] == max(data['HourObserved'])]
selection = st.sidebar.multiselect(label = "Select Reporting Areas", options = data['ReportingArea'].unique(), default=data['ReportingArea'].unique())
define_map(data.loc[data['ReportingArea'].isin(selection)])
HtmlFile = open("map.html", 'r', encoding='utf-8')
source_code = HtmlFile.read()
components.html(source_code, width=1000, height=600)
st.dataframe(data[['DateObserved', 'HourObserved', 'ReportingArea', 'ParameterName', 'AQI', 'AQI_Classification']])
