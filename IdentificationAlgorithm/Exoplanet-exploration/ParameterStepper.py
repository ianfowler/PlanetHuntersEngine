import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import csv 
import random
import math

temp = pd.read_csv('KeplerFinal.txt') #insert real path
temp = temp.dropna().sort_values(by=['Teff']) #Table sorted by Teff least to greatest
data = list(temp['Teff']) 


binTempArr = [data[0]]

def bins(minTempDifference,minNumIndicies):
    lastTemp = 0
    numIndicies = 0
    for i in range(0,len(data)): #makes sure each bin is at least 100 Teff wide, and each bin has at least 100 points
        numIndicies += 1
        if data[i] - lastTemp >= minTempDifference and numIndicies >= minNumIndicies:
            lastTemp = data[i]
            binTempArr.append(lastTemp)
            numIndicies = 0


bins(100,100)

#Inner orbital radius
def roi(temp):
    return (0.62817*temp**3)-(1235.15*temp**2)
#Outer orbital radius
def roo(temp):
    return (1.52*temp**3)-(2988.75*temp**2)

def starRadius(temp):
    return (temp*1.8395*10**5)-3.6169*10**8

def starMass(temp):
    return (2.85187*10**22*temp**2)+(3.70772*10**26*temp)-9.76855*10**29

def transitTime(starRadius,randOrbital,starMass):
    return (2*starRadius*math.sqrt((randOrbital*10**11)/(starMass*6.67)))

def transitDepth(planetRadius,starRadius):
    return (planetRadius**2)/(starRadius**2)

def orbitalPeriod(randOrbital,starMass):
    return (2*math.pi*randOrbital**1.5)*math.sqrt((randOrbital*10^11)/(starMass*6.67))

multiarray=[]
labels=np.array(["Count","Time of Injunction" ,"Orbital Period","Planet radius","Orbital radius" ,"Orbital Inclination","Eccentricity","Time Between Measurements","Transit Time","# of Measurements"])
multiarray.append(labels)

count=0
timeBetweenMeasure=20/(24*60)
TOJ=0
orbitalInclination=0
eccentricity=0
for bins in range (1,len(binTempArr)):
    upper=binTempArr[bins]
    lower=binTempArr[bins-1]
    midTemp=(lower+upper)/2
    roi2=roi(midTemp)
    roo2=roo(midTemp)
    starRadius2=starRadius(midTemp)
    starMass2=starMass(midTemp)
    stepfinder=((roo2-roi2)/50)#Divides oradius into 50 steps
    for pradius in range (3390*10**3,11467*10**3,160000):#About 50 steps
        for oradius in range (int(roi2),int(roo2),int(stepfinder)):
            transitTime2=(transitTime(starRadius2,oradius,starMass2))/60 #Minutes
            orbitalPeriod2=orbitalPeriod(oradius,starMass2)  #Find Units
            total_measurements = transitTime2 / timeBetweenMeasure
            count=count+1         
            params=np.array([count,TOJ,orbitalPeriod2,pradius,oradius,orbitalInclination,eccentricity,timeBetweenMeasure,transitTime2,total_measurements])
            multiarray.append(params)
multiarray=np.array(multiarray)

with open("BinAnalysis.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(multiarray)

#Comment