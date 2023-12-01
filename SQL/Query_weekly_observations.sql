SELECT DISTINCT * FROM air_pollution.air_now_data
WHERE DATE_SUB(CURDATE(),INTERVAL 7 DAY) <=DateObserved AND ParameterName='O3';