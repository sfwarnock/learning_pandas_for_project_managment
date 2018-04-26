# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 13:33:46 2018

@author: Scott Warnock
"""

import pandas as pd

# Read file.
data_file = pd.read_csv('datafile.csv').fillna(0)

# Total timephased data rows. Sum all rows with months.
data_file['Total Sum'] = data_file['Mar-18'] + data_file['Apr-18'] + data_file['May-18'] + data_file['Jun-18'] + data_file['Jul-18'] + data_file['Aug-18']

# Sum all coloumns with budgeted ammounts.
data_file.loc['Total TPD'] = pd.Series(data_file[['Total Cost', 'Mar-18','Apr-18','May-18','Jun-18','Jul-18','Aug-18','Total Sum']].sum(), 
             index = ['Total Cost', 'Mar-18','Apr-18','May-18','Jun-18','Jul-18','Aug-18','Total Sum']);print(data_file)

# Make a list of all Cams.
def cams():
    name = data_file.CAM.tolist()
    cam = []

    for name in name:
        if name not in cam:
            cam.append(name)
    print (cam)
    
cams()