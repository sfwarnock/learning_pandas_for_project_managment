# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 13:33:46 2018

@author: Scott Warnock
"""

import pandas as pd

#import matplotlib.pyplot as plt

# Read file.
data_file = pd.read_csv('datafile.csv').fillna(0)

# Total timephased data rows. Sum all rows with months.
data_file['Total Sum'] = data_file['Mar-18'] + data_file['Apr-18'] + data_file['May-18'] + data_file['Jun-18'] + data_file['Jul-18'] + data_file['Aug-18']

# Sum all coloumns with budgeted ammounts.
data_file.loc['Total TPD'] = pd.Series(data_file[['Total Cost', 'Mar-18','Apr-18','May-18','Jun-18','Jul-18','Aug-18','Total Sum']].sum(), 
             index = ['Total Cost', 'Mar-18','Apr-18','May-18','Jun-18','Jul-18','Aug-18','Total Sum']);print(data_file)

# Make cumalative dataseires for S graphs.
#data_file.loc['Total Cumulative'] = pd.Series(data_file[['Mar-18']].sum(), index = ['Mar-18']);print(data_file)

# Make a list of all Cams.

name = data_file.CAM.dropna().tolist()
cam = []

for name in name:
    if name not in cam:
        cam.append(name)
print(cam)
        
#Generate new dataframe for each cam.
x = 0
camDf = cam[0 + x]

while True:
    if camDf != cam[-1]:
        camDf = data_file[data_file.CAM == camDf]
        x += 1
    else:
        break

#y = data_file[data_file.CAM == cam[x + 1]]
#newDF2 = data_file[data_file.CAM == cam[0 + x]]
#newDF3 = data_file[data_file.CAM == cam[0 + x]]