import batman # sudo pip3 install batman-package
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import rand
from enum import Enum

class LimbDarkening(Enum):
    UNIFORM = 0
    LINEAR = 1
    QUADRATIC = 2
    NONLINEAR = 3


"""
t0:     time of inferior conjunction
per:    orbital period
rp:     planet radius (in units of stellar radii)
a:      semi-major axis (in units of stellar radii)
inc:    orbital inclination (in degrees)
ecc:    eccentricity
w:      longitude of periastron (in degrees)

limb_darkening: The way the lightcurves are smoothed at the bottom. Options are:
 - uniform
 - linear
 - quadratic
 - nonlinear

time_between_measurements: days inbetween samples
total_time: 
"""
def noiseless_lightcurve(t0,per,rp,a,inc,ecc,w,
        limb_darkening=LimbDarkening.QUADRATIC,
        ld_coeff=[[], [0.3], [3.1, 0.3], [0.5, 0.1, 0.1, -0.1]]
        )
    params = batman.TransitParams()
    params.t0 = t0 
    params.per = per
    params.rp = rp 
    params.a = a
    params.inc = inc
    params.ecc = ecc
    params.w = w
    params.u = ld_coeff[limb_darkenings]
    params.limb_dark = ["uniform", "linear", "quadratic", "nonlinear"][limb_darkening]
    
    
