# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 13:33:46 2018

@author: Scott Warnock
"""

import pandas as pd

# Read file.
data_file = pd.read_csv('datafile.csv')

# Sum one coloumn.
df1 = data_file['Mar-18'].sum()

# Sum one coloumn with new total row of summed column.
data_file.loc['Total'] = pd.Series(data_file['Total Cost'].sum(), index = ['Total Cost']);print(data_file)