import pyneb as pn
import numpy as np
import math
from matplotlib import pyplot as plt
import pandas as pd
import sys

STEPS = 100

START_TEMP = 5500
STOP_TEMP = 25000
START_DEN = 9.5
STOP_DEN = 13
ERROR_COLOR = "blue"

he1 = pn.RecAtom('He', 1)

df = None
if len(sys.argv) >= 2 and sys.argv[1] == "--dust-correction":
    df = pd.read_csv('../flux/flux_ratios_corrected.csv')
    ERROR_COLOR = "red"
else:
    df = pd.read_csv('../flux/flux_ratios.csv')

closest_ratios = [float('inf')] * len(df)
x_coords = [0] * len(df)

def record_value(val, i):
    for k in range(len(df)):
        row = df.iloc[k]
        diff = abs(float(row.loc["Flux Ratio"]) - val)
        if diff < closest_ratios[k]:
            closest_ratios[k] = diff
            x_coords[k] = ((i + 0.5) / STEPS) * (STOP_TEMP - START_TEMP) + START_TEMP

def populate_matrix(temperatures, density):
    matrix = np.zeros((STEPS, STEPS))

    for j in range(STEPS):
        for i in range(STEPS):
            temp = temperatures[i]
            den = density[j]

            he1_5876 = he1.getEmissivity(temp, den, wave=5876)
            he1_7065 = he1.getEmissivity(temp, den, wave=7065)

            matrix[j, i] = he1_7065/he1_5876
            if abs(temp - 10000) > 3000:
                continue
            record_value(matrix[j, i], i)
    return matrix

def plot_density_lines(matrix, density, temperatures):
    # plot lines for each density
    density_scale = density[1]/density[0]
    den_val = density[0]
    for i in range(0, STEPS, 10):
        line_plot = []
        for j in range(STEPS):
            line_plot.append(matrix[i, j])
        plt.plot(temperatures, line_plot, linestyle='dashed', label=f"{den_val/1e11:.3f}")
        den_val *= math.pow(density_scale, 10)


def set_axes():
    plt.xlabel("Temperature (K)")
    plt.ylabel("Flux ratio (He I $\\lambda$7065/He I $\\lambda$5876)")
    plt.legend(title="Density ($10^{11} cm^{-3}$)")

def plot_points(temperatures):
    labels = df.loc[:, "Observation"]
    for i in range(len(labels)): # not working idk why
        x_coord = x_coords[i]
        y_coord = df.loc[:, "Flux Ratio"][i]
        plt.annotate(labels[i][7:], (x_coord, y_coord), textcoords='offset points', xytext=(5, 5), color="orange", fontsize=15, xycoords="data")
    plt.errorbar(x_coords, list(df.loc[:, "Flux Ratio"]), yerr=list(df.loc[:, "Flux Ratio Error"]), fmt='o', capsize=6, color=ERROR_COLOR)
    if len(sys.argv) >= 2 and sys.argv[1] == "--dust-correction":
        plt.savefig("../pyneb_plots/final_plot_dust_correction.png")
    else:
        plt.savefig("../pyneb_plots/final_plot.png")

def main():
    temperatures = np.linspace(START_TEMP, STOP_TEMP, num=STEPS)
    density = np.logspace(START_DEN, STOP_DEN, num=STEPS)

    matrix = populate_matrix(temperatures, density)
    plot_density_lines(matrix, density, temperatures)
    set_axes()
    plot_points(temperatures)

if __name__ == "__main__":
    main()