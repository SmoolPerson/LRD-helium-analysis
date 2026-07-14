import pandas as pd
import numpy as np

df = pd.read_csv('flux/fluxes.csv')

df = df.sort_values(by='Observation')

ratios_dict = {"Observation": [], "Flux Ratio": [], "Flux Ratio Error": []}

for i in range(len(df)):
    current_row = df.iloc[i]
    if np.isnan(current_row.loc["Profile Flux-He1_7065A"])  or np.isnan(current_row.loc["Profile Flux-He1_5876A"]):
        continue
    ratio = current_row.loc["Profile Flux-He1_7065A"]/current_row.loc["Profile Flux-He1_5876A"]

    relative_error1 = current_row.loc["Profile Flux Error-He1_5876A"]/current_row.loc["Profile Flux-He1_5876A"]
    relative_error2 = current_row.loc["Profile Flux Error-He1_7065A"]/current_row.loc["Profile Flux-He1_7065A"]
    print(relative_error1, relative_error2)
    ratios_dict["Observation"].append(current_row.loc["Observation"])
    ratios_dict["Flux Ratio"].append(ratio)
    ratios_dict["Flux Ratio Error"].append(ratio * np.sqrt(relative_error1*relative_error1 + relative_error2*relative_error2))

ratios_df = pd.DataFrame(ratios_dict)
ratios_df.to_csv('flux/flux_ratios.csv', index=False)
