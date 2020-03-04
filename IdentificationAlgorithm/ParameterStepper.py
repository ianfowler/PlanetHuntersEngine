import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import csv 
import random
import math
import os
from BinFinder import *

binTemperatures = bins(100, 100)

STELLAR_RADIUS = 695.7*10**6


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
    return (2*math.pi*randOrbital**1.5)*math.sqrt((randOrbital*10**11)/(starMass*6.67))

def oradius_range(midTemp, steps):
    roi_ = roi(midTemp)
    roo_ = roo(midTemp)
    return np.linspace(min(roi_, roo_), max(roi_, roo_), steps)

def pradius_range(midTemps, steps):
    min_planet_pradius = 3390*10**3
    max_planet_pradius = 11467*10**3
    return np.linspace(min_planet_pradius, max_planet_pradius, steps)

def gen_param_csv(folder_name="bins", length=3197, steps_p=50, steps_o=50, orbitalInclination=90, eccentricity=0, transit_time_minutes=30):
    
    used_existing_directories = False

    try:
        os.mkdir(folder_name)
        os.mkdir(folder_name+"/bin_1")
    except OSError:
        
        print("Using existing directory "+folder_name)

    overwriting = False
    for bin in range(1, len(binTemperatures)):
        try:
            os.mkdir("{}/bin_{}/".format(folder_name,bin))
        except OSError:
            if bin>1:
                overwriting = True

    if overwriting:
        print("Files were overwritten. If this isn't the intended effect, be sure to use a new directory next time.")

    for bin in range (1,len(binTemperatures)):
        rows_list = []

        upper=binTemperatures[bin]
        lower=binTemperatures[bin-1]
        midTemp=(lower+upper)/2 # Approximation of temperature

        starRadius_ = starRadius(midTemp)
        starMass_ = starMass(midTemp)
        

        for pradius in list(pradius_range(midTemp, steps_p)):#Planet radius; 50 steps
            for oradius in list(oradius_range(midTemp, steps_o)):#Orbital radius; 50 steps -> 2500 steps per bin

                orbitalPeriod_ = orbitalPeriod(oradius,starMass_)  #Find Units

                rows_list.append({
                    "bin_number":bin,
                    "lower_bin":lower,
                    "upper_bin":upper,
                    "temperature":midTemp,
                    "t0":int(transit_time_minutes * length / 2.0),
                    "per":orbitalPeriod_,
                    "rp":pradius / STELLAR_RADIUS,
                    "a":oradius / STELLAR_RADIUS,
                    "inc":orbitalInclination,
                    "ecc":eccentricity,
                    "w":0,
                })


        if rows_list:
            pd.DataFrame(rows_list).to_csv("{}/bin_{}/parameters.csv".format(folder_name,bin))
        
        
    
    if used_existing_directories:
        print ("Used existing directories for bins. Files were possibly overwritten") 

