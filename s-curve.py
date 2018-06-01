# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 08:19:04 2018

@author: Scott Warnock
"""

# s-curve.py

import pandas as pd
#import matplotlib.pyplot as plt


# Read file.
data_file = pd.read_csv('cumalative_data1.csv').fillna(0)

data_file.plot(x = 0, y = ['BCWS','BCWP','ACWP'], kind = 'line', title = "Project to-date")