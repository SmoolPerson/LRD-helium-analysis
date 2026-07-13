import os
import pandas as pd

df = pd.read_csv('flux/fluxes.csv')

df = df.sort_values(by='Observation')

ratios_dict = {"Observation": [], "Flux Ratio": []}

for i in range(len(df) - 1):
    if df.iloc[i, 0] != df.iloc[i+1, 0]:
        continue
    ratio = df.iloc[i, 2]/df.iloc[i+1, 2]
    ratios_dict["Observation"].append(df.iloc[i, 0])
    ratios_dict["Flux Ratio"].append(ratio)

ratios_df = pd.DataFrame(ratios_dict)
ratios_df.to_csv('flux/flux_ratios.csv', index=False)
