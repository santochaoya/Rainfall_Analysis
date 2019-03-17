# Rainfall Analysis


## About
This is a rainfall analysis based on time series model.

* `rainfall_fill.py` : some assumptions of fill the missing values of hourly
* `rainfall_analysis.py` : fit the data to a time series model
* `sql_ser.py` : connect to SQL Server to import new data

&nbsp;

## Procedure
### 1. Fill the missing values

Atfer extract timestamp by units of second, the intervals shows on different days. </br>

`assumption` : values through increment hours interval.

* missing value of days : 0.001, a small non-zero value;
* missing value of hours : 

&nbsp;
`mean` : mean of each month  
`w1` : rainfall ratio of every day  
`w2` : rainfall ratio of every hour

### 2. Fit the Time series : ARIMA Model
improt the csv data to fit the ARIMA Model


