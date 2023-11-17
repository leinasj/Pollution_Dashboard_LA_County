from my_sql_db_connection import get_forecast_prediction
from datetime import date, timedelta
import time

def main():
    date_var = date.today() + timedelta(days = 1)
    # zipcodes for LA County
    zipcodes = ['90004', '90280','90040', '90294', '90711', '90717', '91011']
        
    while True:
        # for code in zipcodes:
        for code in zipcodes:
            get_forecast_prediction(code, date_var.strftime("%Y-%m-%d"))
        time.sleep(86400)
        
if __name__ == "__main__":
    main()