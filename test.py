import numpy as np
import pandas as pd

data = pd.read_csv('accumRainfall.csv', encoding = 'utf-16', sep = '\t')
data['parsed_date'] = pd.to_datetime(data['unixdatetime'], unit = 's')

date_idx = pd.date_range(data['parsed_date'][0], data['parsed_date'].iloc[-1])
data = data.set_index('parsed_date')
data.drop(labels = ['unixdatetime'], axis = 1, inplace = True)

fill_data = data.reindex(date_idx, fill_value = 0.001)
fill_data['ratio'] = fill_data.groupby(fill_data.index.month).apply(lambda x: x / float(x.sum()))

grouped = fill_data.groupby(fill_data.index.month)

month = grouped.get_group(3)

month_arr = np.array(month['ratio'].tolist()).reshape(-1)
matrix = np.zeros((month.shape[0], 24))

np.fill_diagonal(matrix, month_arr, wrap=True)
mean = fill_data.resample('M').mean()


fill_el = np.where(matrix == 0)
matrix_fill = np.zeros(matrix.shape)

np.where(matrix_fill == 0, 0, 0)


for (i, j) in zip(fill_el[0], fill_el[1]):
        matrix_fill[i][j] = mean.value[2] * np.mean(matrix[i]) * np.mean(matrix[j])

second_idx = pd.date_range(fill_data.index[0], fill_data.index[-1], freq = 'h')
full_data = data.reindex(second_idx)


'''for (missing_idx, fill_val) in zip(full_data[full_data['value'].isnull()].index, matrix_fill.reshape(-1)):
    full_data['value'][missing_idx] = fill_val
'''
month_data = full_data.groupby(full_data.index.month).get_group(3)
print(month_data)

missing_idx = month_data[month_data['value'].isnull()].index # list of the missing indices
for fill_idx, df_idx in enumerate(missing_idx):
    month_data.loc[df_idx, 'value'] = matrix_fill.reshape(-1)[fill_idx]


print(month_data)







