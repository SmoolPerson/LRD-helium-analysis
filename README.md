# LRD Helium Analysis

## Explanation

This project utilizes Helium emission spectra to calculate the density and temperature of Little Red Dots. The program computes the ratio between the flux values of He I 7065Å and He I 5876Å using the observed spectra. Then, it compares these values to a matrix of theoretical ratios simulated under a variety of astronomical conditions. It finally creates plots under pyneb_plots of the end result with the predicted temperatures and densities. Additional options are available in order to support dust correction for the spectra.

## Data

The 1D spectra used in this work are courtesy of the OCEANS collaboration. The OCEANS program (program ID 8410, PI Raymond Simons) is publicly accessible on the MAST database. The extractions used in this work will be made available in the coming months. For a full description of the reductions used in this work, see [Davis et al., 2026](https://arxiv.org/pdf/2606.00258).

## Usage

`git clone https://github.com/SmoolPerson/LRD-helium-analysis.git`

`cd LRD-helium-analysis`

Once the data is publicly released, download and move it to the data directory. A possible command sequence could be `wget "https://<data-url>" && unzip <data-file-name> && mv <data-file-name> data"`

Install Python and venv using your package manager (these may already be installed by default, but only on some systems). For debian systems, the command would be:

`sudo apt install python3 python3-venv`


Initialize and setup the virtual environment:

`python3 -m venv ./.venv`

You may need to use `./.venv/bin/activate.fish` for the fish shell.

`source ./.venv/bin/activate`

`pip install lime-stable pyneb astropy numpy pandas matplotlib scipy dust_extinction`

`cd src`


If you want to calculate flux values and make plots identifying emission lines (flux values are stored in flux/ while plots are stored in plots/):

`python3 load_into_lime.py`

`python3 calculate_ratios.py`

Pass the flag `--fake-data` into load_into_lime.py to use synthetic data for testing.

Pass the flag `--dust-correction` into both python files in order to perform dust correction.

These two options are mutually exclusive as the Hydrogen lines are not present in the fake data.


If you want to compare calculated flux ratios with theoretical values (plots created in pyneb_plots/):

`python3 pyneb_analysis.py`

Use the flag `--dust-correction` to generate a plot of only dust corrected items.

## Credits

I want to credit Ian Bishop (https://github.com/DiagonalSquares) for helping me debug parts of my program. I am very grateful to Kelcey Davis, who helped me understand and catch irregularities in my data, and served as a mentor throughout the project. The work in this project was done under the Institute for Computing in Research.
