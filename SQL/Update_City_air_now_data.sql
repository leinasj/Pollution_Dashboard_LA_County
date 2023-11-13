Update air_now_data 
SET City = CASE 
WHEN ReportingArea = 'Central LA CO' THEN 'Los Angeles'
WHEN ReportingArea = 'S San Gabriel Vly' THEN 'Pico Rivera'
WHEN ReportingArea = 'W San Gabriel Vly' THEN 'Pasadena'
WHEN ReportingArea = 'South Coastal LA' THEN 'Long Beach'
WHEN ReportingArea = 'SW Coastal LA' THEN 'Hawthorne'
WHEN ReportingArea = 'S Central LA CO' THEN 'Compton' end;