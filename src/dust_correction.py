from dust_extinction.averages import G24_SMCAvg
from astropy import units as u
import numpy as np

HALPHA_FLUX = {20504: 1.455e-16, 35829: 4.454e-17, 102364: 1.913e-17, 100424: 1.3235e-17, 101393: 6.2e-18, 101208: 9.42e-18, 33842: 1.31e-17, 169045: 2.1e-17, 161695: 1.853e-18, 1794: 1.473e-17}
HBETA_FLUX = {20504: 1.133e-17, 35829: 7.973e-18, 102364: 6.10e-19, 100424: 4.66e-19, 101393: 0, 101208: 1.86e-19, 33842: 5.57e-19, 169045: 5.09e-18, 161695: 6.4e-19, 1794: 3.35e-18}

def dust_correct_flux(obs_wave, flux, z, dot_id):
    if HBETA_FLUX[dot_id] == 0:
        return flux # don't dust correct if we dont have proper measurements
    
    # initialize dust correction
    smc = G24_SMCAvg()
    # correct wavelength for redshift temporarily for dust calculations
    wave = obs_wave/(1 + z)

    # calculate ebv value to pass to .extinguish
    ehbha = 2.5 * np.log10((HALPHA_FLUX[dot_id]/HBETA_FLUX[dot_id])/2.86)
    av = ehbha/(smc(4861 * u.AA) - smc(6563 * u.AA))

    flux_modified = flux / smc.extinguish(wave * u.AA, Av=av)
    return flux_modified
