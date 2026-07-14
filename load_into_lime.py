from astropy.io import fits
from astropy import units as u
from matplotlib import pyplot as plt
import lime
import numpy as np
import os
import pandas as pd

REDSHIFT_VALUES = {1794: 3.681, 161695: 5.666, 169045: 5.239, 33842: 5.287, 101208: 5.682, 101393: 3.850, 100424: 4.953, 102364: 4.542, 35829: 6.684, 20504: 5.276}
columns = {"Observation": [], "Profile Flux-He1_7065A": [], "Profile Flux Error-He1_7065A": [], "Profile Flux-He1_5876A": [], "Profile Flux Error-He1_5876A": []}

def get_data_files():
    data_files = os.listdir('data')
    all_data = []
    for data_file in data_files:
        # the name of the astronomical object
        dot_id = data_file[14:23]
        # the unique identifier for each data file
        plot_name = data_file[8:11] + '_' + dot_id + data_file[37:40]
        all_data.append((data_file, dot_id, plot_name))
    return all_data

def load(dot):
    hdul = fits.open('data/' + dot)

    wave = hdul[1].data["WAVELENGTH"]
    flux = hdul[1].data["FLUX"]
    error = hdul[1].data["FLUX_ERROR"]

    # converting wave units to angstrom to avoid errors
    wave = np.array([w * 10000 for w in wave])

    # converting flux units to FLAM instead of Jansky to avoid integration errors
    fixed_flux = []
    fixed_flux_err = []
    for i in range(len(flux)):
        fixed_flux.append((flux[i] * u.Jy).to(u.erg / (u.cm * u.cm * u.s * u.AA), equivalencies=u.spectral_density(wave[i] * u.AA)).value)
        fixed_flux_err.append((error[i] * u.Jy).to(u.erg / (u.cm * u.cm * u.s * u.AA), equivalencies=u.spectral_density(wave[i] * u.AA)).value)
    return (wave, np.array(fixed_flux), np.array(fixed_flux_err))

def profile(spec, plot_name, actual_lines, line):
    if line in list(actual_lines['wavelength'].keys()):
        # Gaussian profile seems to work best through trial/error
        spec.fit.bands(line, profile='g')

        # Retrieve measurements from dataframe
        profile_flux = spec.frame.loc[line, 'profile_flux']
        profile_flux_err = spec.frame.loc[line, 'profile_flux_err']

        # the three sigma rule
        if profile_flux > 2 * profile_flux_err:
            
            spec.plot.bands(fname='plots/profile-' + plot_name + '-' + line + '.png')
            return (profile_flux, profile_flux_err)
    return (None, None)

def write_data(profile_flux, profile_flux_error, line_name):
    if (profile_flux is not None and profile_flux < profile_flux_error * 2):
        profile_flux = None
        profile_flux_error = None
    
    columns['Profile Flux-' + line_name].append(profile_flux)
    columns['Profile Flux Error-' + line_name].append(profile_flux_error)

def analyze(data_file, dot_id, plot_name):
    wave, flux, error = load(data_file)
    print("Loading: ", plot_name)
    spec = lime.Spectrum(wave, flux, error, redshift=REDSHIFT_VALUES[int(dot_id)], units_flux='FLAM')

    # Starts with a large tolerance of 3 standard devs, then gradually tightens the continuum
    spec.fit.continuum([3, 3, 3], [3.0, 2.0, 1.0])

    possible_lines = spec.retrieve.lines_frame()
    actual_lines = spec.infer.peaks_troughs(possible_lines)
    #print("Actual Lines:", actual_lines)

    # Also finds the flux
    profile_flux1, profile_flux_error1 = profile(spec, plot_name, actual_lines, 'He1_7065A')

    profile_flux2, profile_flux_error2 = profile(spec, plot_name, actual_lines, 'He1_5876A')

    columns['Observation'].append(plot_name)

    write_data(profile_flux1, profile_flux_error1, "He1_7065A")
    write_data(profile_flux2, profile_flux_erro21, "He1_5876A")

    spec.plot.spectrum(bands=actual_lines, show_cont=True, fname='spectrum-plots/detected_lines-' + plot_name + '.png')


def main():
    little_red_dots = get_data_files()

    for data_file, dot_id, plot_name in little_red_dots:
        analyze(data_file, dot_id, plot_name)

    df = pd.DataFrame(columns)
    df.to_csv('flux/fluxes.csv', index=False)

if __name__ == "__main__":
    main()