from my_sql_db_connection import get_historical_observation
from datetime import date, timedelta

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2008, 1, 1)
end_date = date(2009, 1, 1)

# zipcodes for LA County
zipcodes = ['90004', '90280','90040', '90294', '90711', '90717', '91011']
# for code in zipcodes:
for single_date in daterange(start_date, end_date):
    get_historical_observation(zipcodes[4], single_date.strftime("%Y-%m-%d"))
        