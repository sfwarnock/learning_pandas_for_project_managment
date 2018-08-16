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
name = data_file.CAM.dropna().tolist()
cam = []
for name in name:
    if name not in cam:
        cam.append(name)
print(cam)

# make list from header for pivot_table values.
headerValues = data_file.columns.values[6:].tolist()

# Pviot table datatable by CAM and charge code.
table = pd.pivot_table(data_file, values = headerValues, index=['CAM','Charge Code','Value Type'])

table['Grand Total'] = table.sum(axis = 1); print(table)

camTotals = table.sum(level = ['CAM','Value Type'])
print(camTotals)