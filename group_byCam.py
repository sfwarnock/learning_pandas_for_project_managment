# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 06:46:12 2018

@author: 175272
"""

import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
import json

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


period_BCWP = period_DataFrame.loc['Period Total Earned', headerValues]
period_BCWS = period_DataFrame.loc['Period Total Planned', headerValues]
period_ACWP = period_DataFrame.loc['Period Total Cost', headerValues]

period_EVMetrics = pd.concat([period_BCWP, period_BCWS, period_ACWP], axis=1).to_dict()
with open('period_EVMetrics.json', 'w') as outfile:
    json.dump(period_EVMetrics, outfile, sort_keys = True, indent = 4, ensure_ascii=False)

unfiltered_camGroupByChargeCode = data_file.groupby('CAM')['Charge Code'].apply(list).to_dict()
camByChargeCode = {cam: list(set(chargecode)) for cam, chargecode in unfiltered_camGroupByChargeCode.items()}
with open('camByChargeCode.json', 'w') as outfile:
    json.dump(camByChargeCode, outfile, sort_keys = True, indent = 4, ensure_ascii=False)

