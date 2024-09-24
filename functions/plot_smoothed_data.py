import matplotlib.pyplot as plt

def plot_smoothed_data(measured_df, smoothed_df, compound='phe'):
    plt.figure(figsize=(8, 6))

    # get the time points for the measured and smoothed data to use as the x-axis
    measured_time = measured_df['time'].values
    smoothed_time = smoothed_df['time'].values

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

    # make list of columns from measured data to plot
    relevant_columns = [col for col in measured_df.columns if compound in col]

    # loop over the relevant columns and plot the measured and smoothed data
    for col in relevant_columns:
        # get the color and marker for each ratio and trial
        color = ratio_to_color[col.split(' ')[0]]
        marker = trial_to_marker[col.split(' ')[-1]]
        
        # isolate the ratio to use in legend
        label = col.split(' ')[0]

        plt.scatter(measured_time, measured_df[col], color=color, label=label, marker=marker)
        plt.plot(smoothed_time, smoothed_df[f'{col} smoothed'], color=color, linewidth=.1, marker='o', markersize=.5)
        
    # Setting labels, title, and legend
    compound_name = 'Phenol' if compound == 'phe' else 'BPA'
    plt.xlabel('Time (minutes)', y=0.05)
    plt.ylabel(f'Relative {compound_name} Concentration', x=0.05)
    plt.title(f'Effect of Hydrogen Peroxide:{compound_name} Ratio on {compound_name} Removal', y=1.05)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=12)

    # ensure the y axis starts at 0
    plt.ylim(0, 1)

    # save to figures directory
    plt.savefig(f'../figures/smoothed_{compound}.png', bbox_inches='tight', dpi=300)
    
    plt.show()