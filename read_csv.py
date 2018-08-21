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

acwp = data_file.loc[data_file['Value Type'] == 'ACWP']
bcwp = data_file.loc[data_file['Value Type'] == 'BCWP']
bcws = data_file.loc[data_file['Value Type'] == 'BCWS']

# make list of CAMs for data processing
cam_group = data_file.groupby('CAM')
i = 0
for cam, group in cam_group:
    i = i + 1
    print('Cam', i, cam)
    print(group)
    
# make list from header for pivot_table values.
headerValues = data_file.columns.values[6:].tolist()

# Pviot table datatable by CAM and charge code.
table = pd.pivot_table(data_file, values = headerValues, index=['CAM','Charge Code','Value Type'])

table['Grand Total'] = table.sum(axis = 1); print(table)

camTotals = table.sum(level = ['CAM','Value Type'])
print(camTotals)