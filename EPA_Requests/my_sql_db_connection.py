import mysql.connector
import os
from dotenv import load_dotenv
import requests

load_dotenv()


def get_current_observation(zipcode:str):
    try:
        # Connect to 'air_pollution' MySQL database instance with user credentials 
        cnx = mysql.connector.connect(user='root', password=os.environ.get('MY_SQL_DB_PASS'),
                                host='127.0.0.1',
                                database='air_pollution')
        # Instatiate cursor for execution of SQL queries 
        cursor = cnx.cursor()
        # Define SQL query to insert new observations into MySQL database
        add_observation = ("INSERT INTO air_now_data "
                    "(DateObserved, HourObserved, LocalTimeZOne, ReportingArea, StateCode, Latitude, Longitude, ParameterName, AQI, AQI_Number, AQI_Classification) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")
        # API call to airnowapi to get payload response of AQI data from Los Angeles County monitoring sites
        response = requests.get(f'https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode={zipcode}&distance=10&API_KEY={os.environ.get("AIR_NOW_API_KEY")}')
        # Iterate through JSON response for unique observations, typically monitors will return multiple unique parameters (O3, PM2, PM2.5) 
        for i in response.json():
            observation = (i['DateObserved'], i['HourObserved'], i['LocalTimeZone'], i['ReportingArea'], i['StateCode'], i['Latitude'], i['Longitude'], i['ParameterName'], i['AQI'], i['Category']['Number'], i['Category']['Name'])
            # Upload new observations to database table
            cursor.execute(add_observation, observation)

        # Make sure data is committed to the database
        cnx.commit()
    except Exception as e:
        print(e)
    
    finally:
        # Close cursor and connection
        cursor.close()
        cnx.close()
        
def get_historical_observation(zipcode:str, date:str):
    try:
        # Connect to 'air_pollution' MySQL database instance with user credentials 
        cnx = mysql.connector.connect(user='root', password=os.environ.get('MY_SQL_DB_PASS'),
                              host='127.0.0.1',
                              database='air_pollution')
        # Instatiate cursor for execution of SQL queries 
        cursor = cnx.cursor()
        # Define SQL query to insert new observations into MySQL database
        add_observation = ("INSERT INTO air_now_data "
                    "(DateObserved, HourObserved, LocalTimeZOne, ReportingArea, StateCode, Latitude, Longitude, ParameterName, AQI, AQI_Number, AQI_Classification) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")
        # API call to airnowapi to get payload response of AQI data from Los Angeles County monitoring sites
        response = requests.get(f'https://www.airnowapi.org//aq/observation/zipCode/historical/?format=application/json&zipCode={zipcode}&date={date}T00-0000&distance=10&API_KEY={os.environ.get("AIR_NOW_API_KEY")}')
        # Iterate through JSON response for unique observations, typically monitors will return multiple unique parameters (O3, PM2, PM2.5) 
        for i in response.json():
            observation = (i['DateObserved'], i['HourObserved'], i['LocalTimeZone'], i['ReportingArea'], i['StateCode'], i['Latitude'], i['Longitude'], i['ParameterName'], i['AQI'], i['Category']['Number'], i['Category']['Name'])
            # Upload new observations to database table
            cursor.execute(add_observation, observation)

        # Make sure data is committed to the database
        cnx.commit()
    except Exception as e:
        print(e)
    
    finally:
        # Close cursor and connection
        cursor.close()
        cnx.close()