from astropy.io import fits
from matplotlib import pyplot as plt

fits_filename = '../data/f170lp_g235h_s000001794_x1d_nodded-bg_P1_errescaled.fits'
hdul = fits.open(fits_filename)

wave = hdul[1].data["WAVELENGTH"]
flux = hdul[1].data["FLUX"]
error = hdul[1].data["FLUX_ERROR"]

fig, ax = plt.subplots()
ax.plot(wave, flux, drawstyle='steps-mid')
ax.set_title('Helium Plot')
ax.set_xlabel(r'Wavelength ($\mu$m)')
ax.set_ylabel('Flux (Jy)')

plt.savefig("../plots/wave_flux.png")