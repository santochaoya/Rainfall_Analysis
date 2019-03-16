import pandas as pd
import numpy as np


def create_matrix(grouped, name) :
    '''create a matrix with row of day and col of hours'''

    month = grouped.get_group(name)

    month_arr = np.array(month.values.tolist()).reshape(-1)
    matrix = np.zeros((month.shape[0], 24))

    np.fill_diagonal(matrix, month_arr, wrap = True)

    return matrix


def fill_hours(df):
    '''
    fill the each hour by weight1 * weight2 * mean
    # weight_r = ratio of day,
    # weight_c = ratio of hour,
    # mean = mean of each month
    '''

    #df['ratio'] = df.groupby(df.index.month, level = -0.5).apply(lambda x: x / float(x.sum()))


    #mean = df.resample('M').mean()

    grouped = df.groupby(df.index.month)
    print(grouped.get_group(1))

    for i in df.values[0]:
        if i == 0:
            print(i)






data = pd.read_csv('accumRainfall.csv', encoding = 'utf-16', sep = '\t')
data['parsed_date'] = pd.to_datetime(data['unixdatetime'], unit = 's')

date_idx = pd.date_range(data['parsed_date'][0], data['parsed_date'].iloc[-1])
data = data.set_index('parsed_date')
data.drop(labels = ['unixdatetime'], axis = 1, inplace = True)

fill_data = data.reindex(date_idx, fill_value = 0.001)
#print(fill_data)

second_idx = pd.date_range(fill_data.index[0], fill_data.index[-1], freq = 'h')

full_data = data.reindex(second_idx, fill_value = 0)
mean = full_data.resample('M').mean()





grouped = fill_data.groupby(fill_data.index.month)

for name, group in grouped:
    print(name, create_matrix(grouped, name))


#    print(mean)






#print(fill_hours(full_data))