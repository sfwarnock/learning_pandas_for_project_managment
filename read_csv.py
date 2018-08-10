# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 13:33:46 2018

@author: Scott Warnock
"""

import pandas as pd
#import numpy as np

#import matplotlib.pyplot as plt

# read data file.
data_file = pd.read_csv('datafile.csv').fillna(0)
    
# make list from header for pivot_table values.
headerValues = data_file.columns.values[6:].tolist()

# Pviot table datatable by CAM and charge code.
table = pd.pivot_table(data_file, values = headerValues, index=['CAM','Charge Code','Value Type'])
print (table)

table['Grand Total'] = table.sum(axis = 1)

camTotals = table.sum(level = ['CAM','Value Type'])
print(camTotals)