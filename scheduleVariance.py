# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 07:55:49 2018

@author: Scott Warnock
"""

# scheduleVariance.py

def main():
    bcws = eval(input("Enter the cumalative planned value: "))
    bcwp = eval(input("Enter the cumalative earned value: "))
    acwp = eval(input("Enter the cumalative actual cost to date: "))
    
    spi = bcwp / bcws
    
    print("Your cumalative SPI is: ", spi)
    
    if spi > 1:
        print("Your project is currently ahead of schedule.")
    elif spi < 1:
        print("Your project is currently behind schedule.")
    else:
        print("Your project is currently on-track.")
    
main()