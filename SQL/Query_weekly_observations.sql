SELECT DISTINCT * FROM air_pollution.air_now_data
WHERE DateObserved BETWEEN (CURDATE() - 7) AND CURDATE() AND ParameterName='O3';