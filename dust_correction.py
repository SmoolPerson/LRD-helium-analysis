from dust_extinction.averages import G24_SMCAvg
from astropy import units as u
import numpy as np

def dust_correct_flux(obs_wave, flux, z):
    smc = G24_SMCAvg()
    wave = obs_wave/(1 + z)
    flux_modified = flux / smc.extinguish(wave * u.AA, Av=0.5)
    return flux_modified
