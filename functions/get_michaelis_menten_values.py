from scipy.optimize import curve_fit
import numpy as np

# Define the Michaelis-Menten equation
def michaelis_menten(S, Vmax, Km):
    return (Vmax * S) / (Km + S)

def find_zero_rate_concentration(Vmax, Km, offset_conc, offset_rate, cutoff_rate=0.02):
    # Define a range of substrate concentrations to evaluate the rate
    concs_range = np.linspace(0, 1000, 10000)  # You can adjust the range or granularity if needed

    # Apply the Michaelis-Menten equation to the concentration range
    # rates = michaelis_menten(concs_range, Vmax, Km) + offset_rate

    # Find the concentration where the rate first falls below the cutoff rate
    for conc in range(1000):
        conc = 100 - conc/10

        rate = michaelis_menten(conc - offset_conc, Vmax, Km) + offset_rate

        if rate <= 0:
            return conc

    return None  # If no concentration reaches the cutoff

def get_michaelis_menten_values(trial, smoothed_df, rates_df, cutoff_rate=0.02):
    # find the rates that are before the cutoff rate
    rates = rates_df[f'{trial} smoothed rate']
    rates_with_cutoff = []

    # get all the rates until the rate is below the cutoff
    for rate in rates:
        if rate > cutoff_rate:
            rates_with_cutoff.append(rate)
        else:
            break

    # get the max time
    num_timepoints = len(rates_with_cutoff)

    concs_with_cutoff = list(smoothed_df[f'{trial} smoothed'][:num_timepoints])

    # find the minimum substrate concentration and rate
    offset_conc = min(concs_with_cutoff)
    offset_rate = min(rates_with_cutoff)
    max_time = num_timepoints - 1

    # substract the minimum substrate concentration from all the substrate concentrations
    concs_with_cutoff = [conc - offset_conc for conc in concs_with_cutoff]
    rates_with_cutoff = [rate - offset_rate for rate in rates_with_cutoff]

    # Fit the data using curve_fit
    # Adjusting bounds or providing initial guesses
    popt, pcov = curve_fit(michaelis_menten, concs_with_cutoff, rates_with_cutoff, 
                        p0=[0.15, 1], bounds=(0, 1000))

    # popt contains the optimized values for Vmax and Km
    Vmax, Km = popt

    # find the concentration that corresponds to zero rate
    eq_conc = find_zero_rate_concentration(Vmax, Km, offset_conc, offset_rate, cutoff_rate)

    return trial, Vmax, Km, offset_rate, offset_conc, max_time, eq_conc