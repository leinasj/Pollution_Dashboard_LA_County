import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv
import requests

load_dotenv()

import mysql.connector
from mysql.connector import errorcode

def get_observation(zipcode):
    cnx = mysql.connector.connect(user='root', password=os.environ.get('MY_SQL_DB_PASS'),
                              host='127.0.0.1',
                              database='air_pollution')
    cursor = cnx.cursor()

    add_observation = ("INSERT INTO air_now_data "
                "(DateObserved, HourObserved, LocalTimeZOne, ReportingArea, StateCode, Latitude, Longitude, ParameterName, AQI, AQI_Number, AQI_Classification) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

    response = requests.get(f'https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode={zipcode}&distance=25&API_KEY={os.environ.get("AIR_NOW_API_KEY")}')

    for i in response.json():
        observation = (i['DateObserved'], i['HourObserved'], i['LocalTimeZone'], i['ReportingArea'], i['StateCode'], i['Latitude'], i['Longitude'], i['ParameterName'], i['AQI'], i['Category']['Number'], i['Category']['Name'])
        cursor.execute(add_observation, observation)

    # Make sure data is committed to the database
    cnx.commit()

    cursor.close()
    cnx.close()