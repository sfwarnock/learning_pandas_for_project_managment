# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 13:33:46 2018

@author: Scott Warnock
"""
# make list of CAMs for data processing
#cam_group = data_file.groupby('CAM')
#i = 0
#for cam, group in cam_group:
    #i = i + 1
    #print('Cam', i, cam)
    #print(group)
    
# Pviot table datatable by CAM and charge code.
#table = pd.pivot_table(data_file, values = headerValues, index=['CAM','Charge Code','Value Type'])

#table['Grand Total'] = table.sum(axis = 1); #print(table)

#camTotals = table.sum(level = ['CAM','Value Type'])
#print(camTotals)


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

curentMonth_ACWP = period_DataFrame.loc['Period Total Cost', headerValues[-1]]

# Cumultive Data
cum_DataFrame = period_DataFrame

cum_DataFrame.loc['Cumulative Total Cost'] = cum_DataFrame.loc['Period Total Cost'].cumsum()
cum_DataFrame.loc['Cumulative Planned Value'] = cum_DataFrame.loc['Period Total Planned'].cumsum()
cum_DataFrame.loc['Cumulative Earned Value'] = cum_DataFrame.loc['Period Total Earned'].cumsum()

cum_BCWP = cum_DataFrame.loc['Cumulative Earned Value', headerValues]
cum_BCWS = cum_DataFrame.loc['Cumulative Planned Value', headerValues]
cum_ACWP = cum_DataFrame.loc['Cumulative Total Cost', headerValues]

cum_CV = cum_BCWP - cum_ACWP
cum_CPI = cum_BCWP / cum_ACWP

cum_SV = cum_BCWP - cum_BCWS
cum_SPI = cum_BCWP / cum_BCWS

cum_DataFrame.loc['SPI'] = cum_SPI
cum_DataFrame.loc['SV'] = cum_SV

cum_DataFrame.loc['CPI'] = cum_CPI
cum_DataFrame.loc['CV'] = cum_CV

# bcwr
bac = cum_DataFrame['Total Cost'].sum()
bcwp =cum_DataFrame.loc['Period Total Earned', 'Total Earned']
percent_complete = bcwp / bac                  
bcwr = bac - bcwp                                

cum_todateUI_table = {"Budget at Complete": bac, "BCWP": bcwp, "Percent Complete": percent_complete,
                      "Bugeted Cost of Work Remaining": bcwr}

# eac
acwp = cum_DataFrame.loc['Period Total Cost', 'Total Actual Cost']
bcws = cum_DataFrame.loc['Period Total Planned', 'Total Planned']

cum_todateUI_table["BCWS"] = bcws
cum_todateUI_table["ACWP"] = acwp

eac = acwp + bcwr                           # Estimate at complete
tcpi = bac / eac                            # To Complete Perforamce Index

cum_todateUI_table["EAC"] = eac
cum_todateUI_table["TCPI"] = tcpi

project_CPI = bcwp / acwp
project_SPI = bcwp / bcws
project_CV = bcwp - acwp
project_SV = bcwp - bcws

cum_todateUI_table["CPI"] = project_CPI
cum_todateUI_table["SPI"] = project_SPI
cum_todateUI_table["CV"] = project_CV
cum_todateUI_table["SV"] = project_SV

performance_ETC = acwp + (bcwr * project_CPI)   # Ajusted EAC
cum_todateUI_table["Performance ETC"] = performance_ETC

performance_EAC = acwp + performance_ETC        # Performance EAC
cum_todateUI_table["Performance EAC"] = performance_EAC

performance_tpci = bac / performance_EAC
cum_todateUI_table["Perfromance TCPI"] = performance_tpci

varaince_at_complete = bac - eac
cum_todateUI_table["VAC"] = varaince_at_complete

fig, ax = plt.subplots()
ax.plot(cum_ACWP, color = "Green")
ax.plot(cum_BCWP, color = "Red")
ax.plot(cum_BCWS, color = "Blue")

ax.set(xlabel='Month', ylabel= '$', title= 'Project S-Curve')
ax.legend()
plt.show()

ind = np.arange(len(period_BCWP))
width = 0.25

vegetables = ["CPI", "SPI"]

heatmap_CPI = cum_CPI.tolist()
heatmap_SPI = cum_SPI.tolist()
farmers = (headerValues)

harvest = (heatmap_CPI, heatmap_SPI)

fig, ax = plt.subplots()
im = ax.imshow(harvest)

# We want to show all ticks...
ax.set_xticks(np.arange(len(farmers)))
ax.set_yticks(np.arange(len(vegetables)))
# ... and label them with the respective list entries
ax.set_xticklabels(farmers)
ax.set_yticklabels(vegetables)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), ha="right",
         rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(vegetables)):
    for j in range(len(farmers)):
        text = ax.text(j, i, harvest[i, j],
                       ha="center", va="center", color="w")
        
ax.set_title("Harvest of local farmers (in tons/year)")
fig.tight_layout()
plt.show()



fig, ax = plt.subplots()

bcwsBar = ax.bar(ind - width, period_BCWS, width, color = 'Red', label = 'Planned Value')
bcwpBar = ax.bar(ind, period_BCWP, width, color = 'Blue', label = 'Earned Value')
acwpBar = ax.bar(ind + width, period_ACWP, width, color = 'Green', label = 'Actual Cost')

ax.set_ylabel('$')
ax.set_xlabel('Month')
ax.set_xticks(np.arange(len(headerValues)))
ax.set_xticklabels(headerValues)
ax.set_title('Monthly Planned, Earned, and Actual Cost')
ax.legend()

plt.show()

periodArray_toJSON = cum_DataFrame.loc[cum_DataFrame.index.isin(['Period Total Planned', 'Period Total Earned', 
                                                                 'Period Total Cost'])].to_json(orient = 'index')

cumArray_toJSON = cum_DataFrame.loc[cum_DataFrame.index.isin(['Cumulative Planned Value', 'Cumulative Earned Value',
                                                              'Cumulative Total Cost'])].to_json(orient = 'index')

cumtojson = json.dumps(cum_todateUI_table, indent = 4)

print(cumtojson)
    
    