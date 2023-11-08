SELECT DISTINCT * 
FROM air_now_data WHERE (DateObserved) IN (
 SELECT MAX(DateObserved)
  FROM air_now_data as d) AND ParameterName= 'O3';