SELECT DISTINCT DateForecast as 'Date', City, ParameterName, AQI, AQI_Classification FROM air_pollution.forecast_data
WHERE DateForecast = (curdate()+1) AND ParameterName = 'O3';