SELECT DISTINCT DateForecast as 'Date', City, ParameterName, AQI, AQI_Classification FROM air_pollution.forecast_data
WHERE DateForecast BETWEEN curdate() AND (curdate()+1) AND ParameterName = 'O3';