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

def bins(minTempDifference,minNumIndicies): #populates the binTempArr array with the ending (last) temperature values of each bin
    lastTemp = 0
    numIndicies = 0
    for i in range(0,len(data)): #makes sure each bin is at least 100 Teff wide, and each bin has at least 100 points
        numIndicies += 1
        if data[i] - lastTemp >= minTempDifference and numIndicies >= minNumIndicies:
            lastTemp = data[i]
            binTempArr.append(lastTemp)
            numIndicies = 0


bins(100,100)

#Inner orbital radius of habitable zone
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


"""
t0:     time of inferior conjunction
per:    orbital period
rp:     planet radius (in units of stellar radii)
a:      semi-major axis (in units of stellar radii)
inc:    orbital inclination (in degrees)
ecc:    eccentricity
w:      longitude of periastron (in degrees) - default 0
"""
step_df = pandas.DataFrame(columns=["count","t0" ,"per","rp","a" ,"inc","ecc","w"])
count=0
timeBetweenMeasure=20/(24*60)
t0=0 #time of injunction
orbitalInclination=0
eccentricity=0


steps_p = 50
steps_o = 50

def oradius_range(midTemp, steps=steps_o):
    roi_ =int(roi(midTemp))
    roo_ =int(roo(midTemp))
    stepfinder_oradius = int((roo_-roi_)/50)#Divides oradius into 50 steps
    return range(roi_,roo_,stepfinder_oradius)

def pradius_range(midTemp, steps=steps_p):
    min_planet_pradius = 3390*10**3
    max_planet_pradius = 11467*10**3
    stepfinder_pradius = int((min_planet_pradius + max_planet_pradius)/50)
    return range(roi_,roo_,stepfinder_oradius)


for bins in range (1,len(binTempArr)):
    upper=binTempArr[bins]
    lower=binTempArr[bins-1]
    midTemp=(lower+upper)/2 # Approximation of temperature

    starRadius_ = starRadius(midTemp)
    starMass_ = starMass(midTemp)
    
    for pradius in pradius_range(midTemp):#Planet radius; 50 steps
        for oradius in oradius_range(midTemp):#Orbital radius; 50 steps -> 2500 steps per bin
            transitTime_ =(transitTime(starRadius2,oradius,starMass2))/60 #Minutes
            orbitalPeriod_ =orbitalPeriod(oradius,starMass2)  #Find Units

            params=np.array([count,t0,orbitalPeriod2,pradius,oradius,orbitalInclination,eccentricity,timeBetweenMeasure,transitTime_ ,total_measurements])
            step_df.append({
                "bin_number":bins
                "lower_bin":lower,
                "upper_bin":upper,
                "temperature":midTemp,
                "t0":t0,
                "per":orbitalPeriod2,
                "rp":pradius,
                "a":oradius,
                "inc":orbitalInclination,
                "ecc":eccentricity,
                "w":0
            })

pd.to_csv("bin_params.csv")