SELECT  DISTINCT a1.DateObserved, a1.City, a1.AQI, a1.AQI_Classification, a1.DateMonth, a1.Action_Days
FROM air_now_data a1
WHERE a1.ParameterName IN ('O3', 'OZONE')
AND a1.City IN ('Los Angeles', 'Compton', 'Pico Rivera', 'Long Beach', 'Hawthorne', 'Pasadena')
Union 
SELECT DISTINCT a2.DateObserved, a2.City, a2.O3_AQI, a2.O3_AQI_Classification, a2.DateMonth, a2.Action_Days
FROM air_pollution_2000_2022 a2
WHERE a2.City IN ('Los Angeles', 'Compton', 'Pico Rivera', 'Long Beach', 'Hawthorne', 'Pasadena');