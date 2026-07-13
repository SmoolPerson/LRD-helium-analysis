import pyneb as pn
import numpy as np
import math
from matplotlib import pyplot as plt
import pandas as pd

STEPS = 50

START_TEMP = 7500
STOP_TEMP = 25000
START_DEN = 1e4
STOP_DEN = 1e13

he1 = pn.RecAtom('He', 1)

temperatures = np.linspace(START_TEMP, STOP_TEMP, num=STEPS)
density = np.linspace(START_DEN, STOP_DEN, num=STEPS)

matrix = np.zeros((STEPS, STEPS))

df = pd.read_csv('flux/flux_ratios.csv')
closest_ratios = [float('inf')] * len(df)
x_coords = [0] * len(df)
y_coords = [0] * len(df)
labels = [df.iloc[i]["Observation"] for i in range(len(df))]

for j in range(STEPS):
    for i in range(STEPS):
        temp = temperatures[i]
        den = density[j]

        he1_5876 = he1.getEmissivity(temp, den, wave=5876)
        he1_7065 = he1.getEmissivity(temp, den, wave=7065)

        matrix[j, i] = he1_5876/he1_7065
        for k in range(len(df)):
            row = df.iloc[k]
            diff = abs(float(row.loc["Flux Ratio"]) - matrix[i][j])
            if diff < closest_ratios[k]:
                closest_ratios[k] = diff
                x_coords[k] = ((i + 0.5) / STEPS)
                y_coords[k] = (((STEPS - j - 1) - 0.5) / STEPS)

ax = plt.gca()
plt.imshow(matrix, extent=[START_TEMP, STOP_TEMP, START_DEN,STOP_DEN], aspect="auto", interpolation="none")
plt.colorbar(label = "Emissivity Ratio")
#for i in range(len(labels)): # not working idk why
    #plt.annotate(labels[i], (x_coords[i], y_coords[i]), xytext=(0.1, 0.9), textcoords='axes points', color="orange", transform=ax.transAxes)
plt.xlabel("Temperature (K)")
plt.ylabel("Density ($cm^{-3}$)")
plt.scatter(x_coords, y_coords, color='red', marker='x', transform=ax.transAxes)
plt.savefig("pyneb_plots/emissivity_matrix.png")
plt.clf()

# final plot
dot_temperatures = []
for coord in x_coords:
    dot_temperatures.append(coord * (STOP_TEMP - START_TEMP) + START_TEMP)

print(dot_temperatures)
print(list(df.loc[:, "Flux Ratio"]))

# plot lines for each density
for i in range(0, STEPS, 5):
    den_val = (i/STEPS) * (STOP_DEN - START_DEN) + START_DEN
    line_plot = []
    for j in range(STEPS):
        line_plot.append(matrix[j, i])
    plt.plot(temperatures, line_plot, linestyle='--', label=f"Density: {den_val:.2e}")

plt.xlabel("Temperature (K)")
plt.ylabel("Emissivity ratio")
plt.legend()
plt.scatter(dot_temperatures, list(df.loc[:, "Flux Ratio"]), color='red', marker='x')
plt.savefig("pyneb_plots/final_plot.png")
