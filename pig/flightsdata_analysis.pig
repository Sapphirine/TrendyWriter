-- Load data from local path into a table. 
flights = LOAD '/Users/Marcus/Downloads/ASA/JSM2006/DataExpo/DataSet/Nasa/Files/cloudhigh1.txt' USING PigStorage(' ') AS (id ,time1 ,time2 ,time3 ,time4 ,time5 ,time6 ,time7 ,time8 ,time9 ,time10 ,time11 ,time12 ,time13 ,time14 ,time15 ,time16 ,time17 ,time18 ,time19 ,time20 ,time21 ,time22 ,time23 ,time24);

-- Filter by condition: time1 > 13.00
filtered_flights = FILTER flights BY (double)time1 > 13.00; 

-- Order by column: time24
ordered_flights = ORDER filtered_flights BY time24;

-- Show current data
DUMP ordered_flights;

-- Store current data
STORE ordered_flights INTO '/Users/Marcus/Desktop/new_flights'; 
