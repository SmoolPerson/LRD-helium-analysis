# LRD Helium Analysis

## Explanation

This project aims to plot and calculate flux ratios of the He I 5876 and He I 7065 lines in the spectrum of Little Red Dots (LRDs). It then compares each flux ratio to a predicted matrix of density and temperature values to provide an estimate of those metrics. It is still a work in progress, so not all programs behave as intended currently. The data used for this program is not available to the public.

## Usage

`git clone https://github.com/SmoolPerson/LRD-helium-analysis.git`

`cd LRD-helium-analysis`

Install Python and venv using your package manager (these may already be installed by default, but only on some systems). For debian systems, the command would be:

`sudo apt install python3 python3-venv`

Initialize and setup the virtual environment:

`python3 -m venv ./.venv`

`source ./.venv/bin/activate`

`pip install lime-stable pyneb astropy`

If you want to view a plot of one of the data files:

`python3 load_and_plot.py`

If you want to calculate flux values and make plots:

`python3 load_into_lime.py`

`python3 calculate_ratios.py`

If you want to compare calculated flux ratios with theoretical values:

`python3 pyneb_analysis.py`

## Credits

I want to credit Ian Bishop (https://github.com/DiagonalSquares) for helping me debug parts of my program. Big thanks to Kelcey Davis, who helped me understand and catch irregularities in my data, and served as a mentor throughout the project.
