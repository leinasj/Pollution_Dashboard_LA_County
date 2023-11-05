from my_sql_db_connection import get_observation
import time

def main():
    # zipcodes for LA County
    zipcodes = ['90004', '90280','90040']
    
    while True:
        for code in zipcodes:
            get_observation(code)
        time.sleep(10800)
        
if __name__ == "__main__":
    main()