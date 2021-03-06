SERVERNAME = 'ROBERT\SQLEXPRESS'
DATABASEBANE = 'rain'
USER = 'sa'
PASSWORD = 'sa'
CURSOR_FILE = 'E:/Projects/MM/Rainfall_Analysis/cursor.txt'

import pyodbc
import os
import pandas as pd


def load_SQL():
    ''' load data from SQL Server database.
        the variable cursor stores the latest time load from sql server last time. It is 0 for the initial time.
    '''

    cursor = 0

    # If CURSOR_FILE doesn't exist, this is the first time to load data from sql server, create cursor file.
    # If it exists, read the current cursor
    if not os.path.exists(CURSOR_FILE):
        cursor = 0
        f = open(CURSOR_FILE, 'a')
        f.close()
    else:
        with open(CURSOR_FILE, 'r') as f:
            cursor = f.read()

    #     dbcon = pyodbc.connect('DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (SERVERNAME, DATABASEBANE, USER, PASSWORD))
    # Windows
    dbcon = pyodbc.connect('Trusted_Connection=yes', driver='{SQL Server}', server='ROBERT\SQLEXPRESS', database='rain')

    str_sql = 'select * from dbo.accumRainfall where unixdatetime > ' + str(cursor)
    # print(str_sql)
    df_newrain = pd.read_sql_query(str_sql, dbcon)
    dbcon.close()

    # If there is new data,save the new cursor
    if len(df_newrain) > 0:
        with open(CURSOR_FILE, 'w') as f:
            f.write(str(max(df_newrain.unixdatetime)))

    return df_newrain