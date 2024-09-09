import matplotlib.pyplot as plt
import numpy as np

# Define the Michaelis-Menten equation for fitted curves
def michaelis_menten(S, Vmax, Km):
    return (Vmax * S) / (Km + S)

# Updated function to plot the points and fitted curves with offsets correctly applied
def plot_rates_vs_conc_fit(smoothed_df, rates_df, param_df, compound='phe', cutoff=0):
    plt.figure(figsize=(8, 6))

    # Define the colors and markers for each ratio and trial
    ratio_to_color = {
        '0.5:1': 'black',
        '1:1': 'green',
        '2:1': 'blue',
        '3:1': 'orange',
    }

    trial_to_marker = {
        '1': 'o',
        '2': 's',
        '3': '^',
    }

    # Loop through the param_df to get only the trials included in the DataFrame
    for _, row in param_df.iterrows():
        trial = row['Trial']
        max_time = row['Max Time']
        Vmax = row['Vmax']
        Km = row['Km']
        offset_rate = row['Offset Rate']
        offset_conc = row['Offset Concentration']

        # isolate the ratio to use in legend
        label = trial.split(' ')[0]

        # Extract the compound type from the trial string (e.g., 'phe' or 'BPA')
        if compound not in trial:
            continue  # Skip if the compound is not in the trial

        # Get the corresponding smoothed and rate columns from the smoothed_df and rates_df
        conc_col = f'{trial} smoothed'
        rate_col = f'{trial} smoothed rate'

        # Get data up to the Max Time
        smoothed_concs = smoothed_df[conc_col][:max_time + 1]
        smoothed_rates = rates_df[rate_col][:max_time + 1]

        # Get the color and marker for the current trial
        color = ratio_to_color[trial.split(' ')[0]]
        marker = trial_to_marker[trial.split(' ')[2]]

        # Generate fitted curves using Michaelis-Menten equation
        conc_fit = np.linspace(min(smoothed_concs), max(smoothed_concs), 100)

        # Apply offset concentration and rate
        rate_fit = michaelis_menten(conc_fit - offset_conc, Vmax, Km) + offset_rate

        # Plot the points (no lines connecting them)
        plt.scatter(smoothed_concs, smoothed_rates, marker=marker, color=color, linewidth=.5, s=20, label=label)

        # Plot the fitted curve (with line, no markers)
        plt.plot(conc_fit, rate_fit, color=color, linestyle='--', linewidth=1)

    # Add a dashed line at y = cutoff value
    plt.axhline(y=cutoff, color='red', linestyle='--', linewidth=1)

    # Setting labels, title, and legend
    compound_name = 'Phenol' if compound == 'phe' else 'BPA'
    unit = 'mM' if compound == 'phe' else 'µM'
    plt.xlabel(f'{compound_name} Concentration ({unit})', y=0.05)
    plt.ylabel(f'Enzymatic Rate ({unit}/min)', x=0.05)
    plt.title(f'The Effect of HRP:Hydrogen Peroxide Ratio\n on Enzymatic Rate vs. {compound_name} Concentration', y=1.01)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # ensure the both axes starts at 0
    plt.ylim(0)
    plt.xlim(0)

    # save to figures directory
    plt.savefig(f'../figures/rates_vs_conc_fit_{compound}.png', bbox_inches='tight', dpi=300)

    plt.show()