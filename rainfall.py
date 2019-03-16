import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import acf,pacf,plot_acf,plot_pacf
from statsmodels.tsa.arima_model import ARMA
from sklearn.metrics import mean_squared_error


data = pd.read_csv('accumRainfall.csv', encoding = 'utf-16', sep = '\t')
data['parsed_date'] = pd.to_datetime(data['unixdatetime'], unit = 's')

date_idx = pd.date_range(data['parsed_date'][0], data['parsed_date'].iloc[-1])
data = data.set_index('parsed_date')
data.drop(labels = ['unixdatetime'], axis = 1, inplace = True)

print(data)


time_ser = data.reindex(date_idx).interpolate()
#print(time_ser)

'''slice = int(0.75 * time_ser.shape[0])

train_data = time_ser[:slice]
test_data = time_ser[slice:]'''

#monthly_rainfall = time_ser.rolling(30).mean()
#print(monthly_rainfall)

plt.figure(figsize=(15,5))
#monthly_rainfall.plot()
plt.plot(time_ser, marker = '*')
#plt.show()



#ADF test
t = sm.tsa.stattools.adfuller(time_ser.iloc[:, 0])
output = pd.DataFrame(index = ['Test Statistic Value', 'p-value', 'Lags Used', 'Number of Observations Used',
                               'Critical Value(1%)', 'Critical Value(5%)', 'Critical Value(10%)'], columns = ['values'])

output['values']['Test Statistic Value'] = t[0]
output['values']['p-value'] = t[1]
output['values']['Lags Used'] = t[2]
output['values']['Number of Observations Used'] = t[3]
output['values']['Critical Value(1%)'] = t[4]['1%']
output['values']['Critical Value(5%)'] = t[4]['5%']
output['values']['Critical Value(10%)'] = t[4]['10%']

print(output)

#Plot ACF, PACF


plot_acf(time_ser)
plot_pacf(time_ser, method = 'ywm')
plt.show()

d = 0
#(p, q) = (sm.tsa.arma_order_select_ic(train_data, max_ar = 3, max_ma = 3, ic = 'aic')['aic_min_order'])
p, q = 1, 1
#print(p, q)
arma_mod = ARMA(time_ser, (p, d, q)).fit(disp = 1, method = 'mle')
summary = (arma_mod.summary2(alpha = .05, float_format = "%.8f"))
print(summary)

resid = arma_mod.resid
t_resid = sm.tsa.stattools.adfuller(resid)

output_resid = pd.DataFrame(index = ['Test Statistic Value', 'p-value', 'Lags Used', 'Number of Observations Used',
                               'Critical Value(1%)', 'Critical Value(5%)', 'Critical Value(10%)'], columns = ['values'])

output_resid['values']['Test Statistic Value'] = t_resid[0]
output_resid['values']['p-value'] = t_resid[1]
output_resid['values']['Lags Used'] = t_resid[2]
output_resid['values']['Number of Observations Used'] = t_resid[3]
output_resid['values']['Critical Value(1%)'] = t_resid[4]['1%']
output_resid['values']['Critical Value(5%)'] = t_resid[4]['5%']
output_resid['values']['Critical Value(10%)'] = t_resid[4]['10%']

#print(output_resid)


plot_acf(resid)
plot_pacf(resid, method = 'ywm')
#plt.show()

predict_data = arma_mod.predict()
print(predict_data)

mse = mean_squared_error(time_ser, predict_data)
print(mse)

plt.figure(figsize=(15,5))
plt.plot(time_ser, color = 'green') # actual
plt.plot(predict_data, color='red') # predict
plt.show()