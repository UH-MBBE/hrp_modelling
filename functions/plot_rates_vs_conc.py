import matplotlib.pyplot as plt

def plot_rates_vs_conc(smoothed_df, rates_df, compound='phe', cutoff=0):
    plt.figure(figsize=(8, 6))

    # define the colors and markers for each ratio and trial
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

    relevant_cols = [col for col in smoothed_df.columns if compound in col]

    # loop over the relevant columns and plot the measured and smoothed data
    for col in relevant_cols:
        # get the color and marker for each ratio and trial
        color = ratio_to_color[col.split(' ')[0]]
        marker = trial_to_marker[col.split(' ')[2]]

        # isolate the ratio to use in legend
        label = col.split(' ')[0]

        plt.plot(smoothed_df[col], rates_df[f'{col} rate'], marker=marker, color=color, linewidth=.5, markersize=4, label=label)

    # Add a dashed line at y = cutoff value
    plt.axhline(y=cutoff, color='red', linestyle='--', linewidth=1)

    # Setting labels, title, and legend
    compound_name = 'Phenol' if compound == 'phe' else 'BPA'
    plt.xlabel(f'{compound_name} Concentration (µM)', y=0.05)
    plt.ylabel(f'Enzymatic Rate (µM/min)', x=0.05)
    plt.title(f'The Effect of Hydrogen Peroxide:{compound_name} Ratio\n on Enzymatic Rate vs. {compound_name} Concentration', y=1.01)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=12)

    # ensure the both axes starts at 0
    plt.ylim(0, 25)
    plt.xlim(0)

    # save to figures directory
    plt.savefig(f'../figures/rates_vs_conc_{compound}.png', bbox_inches='tight', dpi=300)

    plt.show()
