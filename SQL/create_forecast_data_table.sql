CREATE TABLE forecast_data (
DateIssue date NOT NULL,
DateForecast int NOT NULL,
ReportingArea varchar(100) NOT NULL,
StateCode varchar(5) NOT NULL,
Longitude FLOAT NOT NULL,
Latitude FLOAT NOT NULL,
ParameterName varchar(20) NOT NULL,
AQI int NOT NULL,
AQI_Number int NOT NULL,
AQI_Classification varchar(20) NOT NULL,
ForecastYear year GENERATED ALWAYS AS (year(DateForecast)),
ForecastMonth int GENERATED ALWAYS AS (month(DateForecast)),
ForecastDay int GENERATED ALWAYS AS (day(DateForecast)),
City varchar(50) GENERATED ALWAYS AS (case when (ReportingArea = _utf8mb4'Central LA CO') then _utf8mb4'Los Angeles' when (ReportingArea = _utf8mb4'S San Gabriel Vly') then _utf8mb4'Pico Rivera' when (ReportingArea = _utf8mb4'W San Gabriel Vly') then _utf8mb4'Pasadena' when (ReportingArea = _utf8mb4'South Coastal LA') then _utf8mb4'Long Beach' when (ReportingArea = _utf8mb4'SW Coastal LA') then _utf8mb4'Hawthorne' when (`ReportingArea` = _utf8mb4'S Central LA CO') then _utf8mb4'Compton' end) VIRTUAL,
Action_Days tinyint(1) GENERATED ALWAYS AS(case when (AQI_Classification = _utf8mb4'Unhealthy') then true when (AQI_Classification = _utf8mb4'Unhealthy for Sensitive Groups') then true when (AQI_Classification = _utf8mb4'Very Unhealthy') then true when (AQI_Classification = _utf8mb4'Hazardous') then true else false end) VIRTUAL
) ENGINE=InnoDB;
