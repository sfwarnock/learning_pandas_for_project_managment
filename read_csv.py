# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 13:33:46 2018

@author: Scott Warnock
"""

import pandas as pd

# Read file.
data_file = pd.read_csv('datafile.csv').fillna(0)

# Sum one coloumn.
#df1 = data_file['Mar-18'].sum()

# Sum one coloumn with new total row of summed column.
#data_file.loc['Total'] = pd.Series(data_file['Total Cost'].sum(), index = ['Total Cost']);print(data_file)

# Total timephased data rows. Sum all rows with months.
data_file['Total Sum'] = data_file['Mar-18'] + data_file['Apr-18'] + data_file['May-18'] + data_file['Jun-18'] + data_file['Jul-18'] + data_file['Aug-18']

#df['Total'] = df['Mar-18'] + df['Apr-18']

#[0:15], 'May-18':[0:15],'Jun-18':[0:15], 'Jul-18':[0:15], 'Aug-18':[0:15]})

#   Sum all timephases columns.
#data_file.loc['Total'] = pd.Series(data_file['Total Cost'].sum(), index = ['Total Cost']);print(data_file)