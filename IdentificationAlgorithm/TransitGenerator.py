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
Generates linspace based on cadences and the length between cadences (minutes)
"""
def sampling_range(cadences, cadence_length_minutes=30):
    duration_minutes = cadences*cadence_length_minutes
    return np.linspace(0, duration_minutes, cadences)

"""
sample_space: np.linspace for the samples of light taken. 

p: dictionary of the following required values
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

returns: np array flux
"""
def simulated_lightcurve(
        sample_space,
        p,
        limb_darkening=LimbDarkening.QUADRATIC,
        ld_coeff=[[], [0.3], [0.1, 0.3], [0.5, 0.1, 0.1, -0.1]],
        noise_function = lambda x: [f - np.random.normal(0,0.0004) for f in x]
        ):
    params = batman.TransitParams()
    params.t0 = p["t0"] 
    params.per = p["per"]
    params.rp = p["rp"]
    params.a = p["a"]
    params.inc = p["inc"]
    params.ecc = p["ecc"]
    params.w = p["w"]
    
    ld = limb_darkening.value
    params.u = ld_coeff[ld]
    params.limb_dark = ["uniform", "linear", "quadratic", "nonlinear"][ld]

    m = batman.TransitModel(params, sample_space)
    flux = noise_function(m.light_curve(params))

    return flux


def row_to_lightcurve(header, row, length=3197):
    p = {}

    must_contain = ["t0","per","rp","a","inc","ecc","w"]
    for attribute in must_contain:
        if attribute not in header:
            raise ValueError("Need header to contain {}".format(must_contain))
        p[attribute] = row[header.index(attribute)]

    sample_space = sampling_range(length)

    return simulated_lightcurve(sample_space, p)
    



