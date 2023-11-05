CREATE TABLE Air_Now_Data (
DateObserved date NOT NULL,
HourObserved int NOT NULL,
LocalTimeZone varchar(10) NOT NULL,
ReportingArea varchar(100) NOT NULL,
StateCode varchar(5) NOT NULL,
Longitude FLOAT NOT NULL,
Latitude FLOAT NOT NULL,
ParameterName varchar(20) NOT NULL,
AQI int NOT NULL,
AQI_Number int NOT NULL,
AQI_Classification varchar(20) NOT NULL
) ENGINE=InnoDB;