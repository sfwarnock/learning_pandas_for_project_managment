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
csv_header = data_file.columns.values.tolist()
headerValues = data_file.columns.values[6:].tolist()

# ev_metrictypes
acwp = data_file.loc[data_file['Value Type'] == 'ACWP']
acwp.loc['Period Total Cost', headerValues] = acwp[headerValues].sum()
acwp['Total Actual Cost'] = acwp.loc[:,headerValues].sum(axis=1)
acwp_header = acwp.columns.values.tolist()
for columnHeaders in acwp_header:
    if columnHeaders not in csv_header:
        csv_header.append(columnHeaders)
    if columnHeaders in csv_header:
        continue

bcwp = data_file.loc[data_file['Value Type'] == 'BCWP']
bcwp.loc['Period Total Earned', headerValues] = bcwp[headerValues].sum()    
bcwp['Total Earned'] = bcwp.loc[:,headerValues].sum(axis=1)
bcwp_header = bcwp.columns.values.tolist()
for columnHeaders in bcwp_header:
    if columnHeaders not in csv_header:
        csv_header.append(columnHeaders)
    if columnHeaders in csv_header:
        continue

bcws = data_file.loc[data_file['Value Type'] == 'BCWS']
bcws.loc['Period Total Planned', headerValues] = bcws[headerValues].sum()
bcws['Total Planned'] = bcws.loc[:,headerValues].sum(axis=1)
bcws_header = bcws.columns.values.tolist()
for columnHeaders in bcws_header:
    if columnHeaders not in csv_header:
        csv_header.append(columnHeaders)
    if columnHeaders in csv_header:
        continue

period_DataFrame = pd.concat([acwp, bcwp, bcws], sort = True).sort_values(by='CAM').reindex(columns = csv_header).fillna(0)

# fiter by chargecode
filter_ChargeCode = pd.pivot_table(period_DataFrame, values = csv_header, index=['Charge Code', 'CAM', 'Value Type'])
print(filter_ChargeCode)

# filter by CAM
filter_CAM = pd.pivot_table(period_DataFrame, values = csv_header, index=['CAM', 'Charge Code', 'Value Type'])
print(filter_CAM)

period_BCWP = period_DataFrame.loc['Period Total Earned', headerValues]
period_BCWS = period_DataFrame.loc['Period Total Planned', headerValues]
period_ACWP = period_DataFrame.loc['Period Total Cost', headerValues]

period_SPI = period_BCWP / period_BCWS
period_SV = period_BCWP - period_BCWS

period_CPI = period_BCWP / period_ACWP
period_CV = period_BCWP - period_ACWP

period_DataFrame.loc['Period SV'] = period_SV
period_DataFrame.loc['Period SPI'] = period_SPI

period_DataFrame.loc['Period CV'] = period_CV
period_DataFrame.loc['Period CPI'] = period_CPI

# Cumualtive Data
cum_DataFrame = period_DataFrame

cum_DataFrame.loc['Cumualative Total Cost'] = cum_DataFrame.loc['Period Total Cost'].cumsum()
cum_DataFrame.loc['Cumualative Planned Value'] = cum_DataFrame.loc['Period Total Planned'].cumsum()
cum_DataFrame.loc['Cumualative Earned Value'] = cum_DataFrame.loc['Period Total Earned'].cumsum()

# make list of CAMs for data processing
cam_group = data_file.groupby('CAM')
i = 0
for cam, group in cam_group:
    i = i + 1
    #print('Cam', i, cam)
    #print(group)
    
# Pviot table datatable by CAM and charge code.
table = pd.pivot_table(data_file, values = headerValues, index=['CAM','Charge Code','Value Type'])

table['Grand Total'] = table.sum(axis = 1); #print(table)

camTotals = table.sum(level = ['CAM','Value Type'])
#print(camTotals)