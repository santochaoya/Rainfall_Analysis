import pandas as pd
import matplotlib as plt

idx = pd.date_range('09-01-2013', '09-30-2013')

s = pd.Series({'09-02-2013': 2,
               '09-03-2013': 10,
               '09-06-2013': 5,
               '09-07-2013': 1,
               '09-30-2013':5})
s.index = pd.DatetimeIndex(s.index)

s = s.reindex(idx, fill_value=s.interpolate())

print(s)