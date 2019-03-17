import pandas as pd
import numpy as np


def read_file(file_name):
    '''read a file from sql server, convert timestamp to date time'''

    data = pd.read_csv('accumRainfall.csv', encoding='utf-16', sep='\t')
    data['parsed_date'] = pd.to_datetime(data['unixdatetime'], unit='s')

    return data


def extend_df(data):
    '''extend given date time into hourly, return a df with hourly missing value'''

    # extend month df into days: index with missing dates and value with a very small non-zero value
    date_idx = pd.date_range(data['parsed_date'][0], data['parsed_date'].iloc[-1])
    data = data.set_index('parsed_date')
    data.drop(labels=['unixdatetime'], axis=1, inplace=True)
    fill_data = data.reindex(date_idx, fill_value=0.001)

    # extend days df into hours: index with missing hours and value with a processed rainfall value
    second_idx = pd.date_range(fill_data.index[0], fill_data.index[-1], freq='h')
    full_data = data.reindex(second_idx)

    return fill_data, full_data


def create_matrix(grouped, month_name) :
    '''
    (monthly)
    create a zero matrix with row of days and col of hours(24), fill the diagonal with rainfall values
    '''

    #make a matrix of month
    month = grouped.get_group(month_name)

    month_arr = np.array(month.values.tolist()).reshape(-1)
    matrix = np.zeros((month.shape[0], 24))

    #fill diagonal with rainfall values
    np.fill_diagonal(matrix, month_arr, wrap = True)

    return matrix


def process_val(matrix, fill_data, month_name):
    '''
    (monthly)
    make a days * hours(24) zero matrix, convert all the positions which matrix has a 0 to a fill value.

    #fill value:
    fill the each hour by weight1 * weight2 * mean
        # weight_r = ratio of day,
        # weight_c = ratio of hour,
        # mean = mean of each month
    '''

    mean = fill_data.resample('M').mean()

    fill_val = np.where(matrix == 0) #get index of element need to be fill
    matrix_fill = np.zeros(matrix.shape) #make a new zeros matrix

    #conver all the zero values to processed rainfall values
    for (i, j) in zip(fill_val[0], fill_val[1]):
            matrix_fill[i][j] = mean.value[int(month_name) - 1] * np.mean(matrix[i, :]) * np.mean(matrix[:, j])

    return matrix_fill


def data_process(file):
    #read a file
    data = read_file(file)
    #print("========================\nreading data : \n========================\n{}\n".format(data))

    #extend data frame
    fill_data, full_data = extend_df(data)
    #print("========================\nfill data : \n========================\n{}\n".format(fill_data))
    #print("========================\nfull data : \n========================\n{}\n".format(full_data))


    #processe rainfall by month
    grouped = fill_data.groupby(fill_data.index.month)

    fill_arr = []
    for month_name, group in grouped:
        #create matrix of a month
        matrix = create_matrix(grouped, month_name)
        #print(month_name, matrix)

        #fill matrix with processd value
        matrix_fill = process_val(matrix, fill_data, month_name)
        #print(matrix_fill)

        filled_matrix = np.where(matrix, matrix, matrix_fill)
        fill_arr = np.append(fill_arr, filled_matrix)

    full_data['value'] = fill_arr[:-23]

    return full_data

#print(data_process("accumRainfall.csv"))