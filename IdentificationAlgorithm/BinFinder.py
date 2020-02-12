import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import csv 
import random
import math
import os

temp = pd.read_csv('KeplerFinal.txt') #insert real path
temp = temp.dropna().sort_values(by=['Teff']) #Table sorted by Teff least to greatest
data = list(temp['Teff']) 
binTempArr = [data[0]]

def bins(minTempDifference,minNumIndicies): #populates the binTempArr array with the ending (last) temperature values of each bin
    lastTemp = 0
    numIndicies = 0
    for i in range(0,len(data)): #makes sure each bin is at least 100 Teff wide, and each bin has at least 100 points
        numIndicies += 1
        if data[i] - lastTemp >= minTempDifference and numIndicies >= minNumIndicies:
            lastTemp = data[i]
            binTempArr.append(lastTemp)
            numIndicies = 0

    return binTempArr


