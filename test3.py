import pandas as pd


data = pd.read_csv("accumRainfall.csv", encoding = 'utf-16', sep = '\t')
data['parsed_date'] = pd.to_datetime(data['unixdatetime'], unit = 'ms')

date_idx = pd.date_range(data['parsed_date'][0], data['parsed_date'].iloc[-1])
data = data.set_index('parsed_date')
data.drop(labels = ['unixdatetime'], axis = 1, inplace = True)


interval = []
inter_val = []

for i in range(data.shape[0] - 1):
    interval_time = data.index[i + 1] - data.index[i]
    intervel_value = abs(data.values[i + 1] - data.values[i])
    interval.append(interval_time)
    inter_val.append(intervel_value)

interval.append('NaN')
inter_val.append('NaN')

data['interval'] = interval
data['inter_val'] = inter_val

print(data)

