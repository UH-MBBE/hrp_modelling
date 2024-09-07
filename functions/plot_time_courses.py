import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Define the Michaelis-Menten equation with offsets
def michaelis_menten_with_offsets(S, t, Vmax, Km, offset_conc, offset_rate):
    # Apply the offset concentration only when calculating the rate
    effective_S = S - offset_conc
    
    # Calculate the reaction rate using the Michaelis-Menten equation
    rate = (Vmax * effective_S) / (Km + effective_S) + offset_rate
    
    # Negative because substrate is consumed
    dSdt = -rate
    return dSdt

# Define a function to generate time course data for a trial
def generate_time_course(trial_data, initial_conc=100):
    # Extract parameters from the trial data
    Vmax = trial_data['Vmax']
    Km = trial_data['Km']
    offset_conc = trial_data['Offset Concentration']
    offset_rate = trial_data['Offset Rate']
    max_time = 90
    # max_time = trial_data['Max Time']
    
    # Generate time points from 0 to max_time
    time_points = np.linspace(0, max_time, max_time + 1)
    time_points = np.linspace(0, max_time, max_time + 1)
    
    # Initial substrate concentration is explicitly set to 1
    S0 = initial_conc
    
    # Use odeint to solve the ODE for substrate concentration over time
    S_t = odeint(michaelis_menten_with_offsets, S0, time_points, args=(Vmax, Km, offset_conc, offset_rate))
    
    # Flatten the substrate concentrations (odeint returns 2D arrays)
    S_t = S_t.flatten()
    
    # Return the time points and substrate concentrations
    return time_points, S_t

# Function to plot time courses for multiple trials of the same compound
def plot_time_courses(param_df, measurement_df, compound='phe', max_time=20):
    """
    Plots the time courses for multiple trials of the same compound.
    Each trial is plotted with different colors and markers.
    """
    # Define colors and markers for different HRP:Hydrogen Peroxide ratios and trials
    ratio_to_color = {
        '1:1': 'green',
        '2:1': 'blue',
        '3:1': 'orange',
    }
    trial_to_marker = {
        '1': 'o',
        '2': 's',
        '3': '^',
    }
    
    plt.figure(figsize=(8, 6))

    # shorten measurement_df to only go up to 20 minutes
    measurement_df = measurement_df[measurement_df['time'] <= max_time]
    
    for _, row in param_df.iterrows():
        trial = row
        trial_label = trial['Trial']

        # Only process trials for the chosen compound
        if compound not in trial_label:
            continue

        measured_trial = measurement_df[trial_label]

        # Generate time course data
        time_points, S_t = generate_time_course(trial)

        # shorten to max_time
        time_points = time_points[:max_time + 1]
        S_t = S_t[:max_time + 1]

        # Extract the color and marker for plotting based on the trial
        ratio = trial_label.split(' ')[0]  # Extract HRP:Hydrogen Peroxide ratio
        trial_num = trial_label.split(' ')[2]  # Extract trial number
        
        color = ratio_to_color.get(ratio, 'black')  # Default to black if not found
        marker = trial_to_marker.get(trial_num, 'o')  # Default to 'o' marker if not found

        # Plot the substrate concentrations over time
        plt.plot(time_points, S_t, marker=None, color=color, linestyle='--', linewidth=1)
        plt.scatter(measurement_df['time'], measured_trial, marker=marker, color=color, label=trial_label)

    # Set labels, title, and legend
    compound_name = 'Phenol' if compound == 'phe' else 'BPA'
    unit = 'mM' if compound == 'phe' else 'µM'

    plt.xlabel('Time (min)')
    plt.ylabel(f'Substrate Concentration ({unit})')
    plt.title(f'{compound_name} Time Course Substrate Concentration Michaelis-Menten Fitting')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()

    # save to figures directory
    plt.savefig(f'../figures/time_course_fit_{compound}.png', bbox_inches='tight', dpi=300)

    plt.show()