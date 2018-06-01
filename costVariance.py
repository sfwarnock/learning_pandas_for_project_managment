# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 07:55:49 2018

@author: Scott Warnock
"""

# costVariance.py

def main():
    bcws = eval(input("Enter the cumalative planned value: "))
    bcwp = eval(input("Enter the cumalative earned value: "))
    acwp = eval(input("Enter the cumalative actual cost to date: "))
    
    cpi = bcwp / acwp
    
    print("Your cumalative CPI is: ", round(cpi,2))
    
    if cpi > 1:
        print("Your project is currently under costed.")
    elif cpi < 1:
        print("Your project is currently over costed.")
    else:
        print("Your project costs are inline with you earned value.")
    
main()