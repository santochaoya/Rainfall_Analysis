# Rainfall Analysis


## About
This is a rainfall analysis based on time series model, from observations of each day(extract unixdatetime in 's')

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

$$ mean * w1 * w2 $$


&nbsp;
`mean` : mean of each month  
`w1` : rainfall ratio of every day  
`w2` : rainfall ratio of every hour

### 2. Fit the Time series : ARIMA Model
improt the csv data to fit the ARIMA Model

![alt text](https://github.com/santochaoya/Rainfall_Analysis/blob/master/1.jpg)
As the image shown, observations are no trend

* After ADF test which observations p-value is so small and t statistic are far from the intervel
I use observations to fit the ARIMA model.

* Set the parameters of AR and MA models
![alt text](https://github.com/santochaoya/Rainfall_Analysis/blob/master/2.jpg)
![alt text](https://github.com/santochaoya/Rainfall_Analysis/blob/master/3.jpg)

Shown on the picture, the parameters might be 2 and 1.

* Select the parameters by minimal BIC and AIC, then I can parameters p = 1, q = 1.

* fit the ARIMA model, check if the residuals has no statistically significant.
![alt text](https://github.com/santochaoya/Rainfall_Analysis/blob/master/4.jpg)
![alt text](https://github.com/santochaoya/Rainfall_Analysis/blob/master/5.jpg)
* prediction with ARIMA
![alt text](https://github.com/santochaoya/Rainfall_Analysis/blob/master/6.jpg)


## 3. Document of Code
* `sql_ser.py` load file through SQL Server, first run `load_SQL()` will load csv file from SQL, run it again when for getting updates of the databases.
* `rainfall_analysis.py` has imported SQL Server and other python files, can be run directly. 

    There is a small dataset for testing which has been commented.
    

working on trying...
extract unixdatetime in 'ms', sensor clear to 0 from some moment, to figure out more tasks





