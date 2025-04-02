import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def count_column(file_path, column, output_folder):
    #Read the file
    df = pd.read_csv(file_path, delim_whitespace=True)

    #Filter out rows with value of 0
    df = df[df[column] != 0]

    #Makes a new .dat file with the count of the column
    count = df[column].count()
    #Occurences of each value in the column
    new_df = pd.DataFrame(df[column].value_counts()).reset_index()
    new_df.columns = ['Value', 'Count']
    new_df = new_df.sort_values(by='Count', ascending=False)
    output_file_path = os.path.join(output_folder, f'{column}_count.dat')
    new_df.to_csv(output_file_path, sep='\t', index=False)
    print(f"Count of {column} saved to {output_file_path}")

def plot_count(file_path):
    """
    Plot the counts from the .dat file as vertical lines.
    Positive and negative counts are plotted separately.
    """
    df = pd.read_csv(file_path, delim_whitespace=True)

    # Separate positive and negative counts
    positive_counts = df[df['Count'] >= 0]
    negative_counts = df[df['Count'] < 0]

    # Counts sorted by value
    positive_counts_sorted = positive_counts.sort_values(by='Value')
    negative_counts_sorted = negative_counts.sort_values(by='Value')

    # Make new 2 subfigures
    fig, ax = plt.subplots(2, 1, figsize=(10, 10))

    # Plot positive counts
    ax[0].vlines(positive_counts['Value'], 0, positive_counts['Count'], color='skyblue', linewidth=0.3, alpha=0.9, label='Positive Counts')
    ax[0].vlines(negative_counts['Value'], 0, negative_counts['Count'], color='red', linewidth=0.3, alpha=0.9, label='Negative Counts')
    ax[0].set_xlabel('Brightness')
    ax[0].set_ylabel('Count')
    ax[0].legend()

    # Plot the continuous line
    #ax[0][1].plot(positive_counts_sorted['Value'], positive_counts_sorted['Count'], color='skyblue', linewidth=0.3, alpha=0.9)
    #ax[0][1].plot(negative_counts_sorted['Value'], negative_counts_sorted['Count'], color='red', linewidth=0.3, alpha=0.9)

    # Plot log of counts
    ax[1].vlines(positive_counts['Value'], 0, np.log10(positive_counts['Count']), color='skyblue', linewidth=0.3, alpha=0.9, label='Positive Counts')
    ax[1].vlines(negative_counts['Value'], 0, np.log10(negative_counts['Count'].abs()), color='red', linewidth=0.3, alpha=0.9, label='Negative Counts')
    ax[1].set_xlabel('Brightness')
    ax[1].set_ylabel('log(Count)')
    ax[1].legend()

    # Save the plot
    plot_path = file_path.replace('.dat', '.png')
    plt.savefig(plot_path)
    plt.close()
    print(f"Plot saved to {plot_path}")

def plot_histogram(file_path, bin_width):
    """
    Create a histogram from the .dat file using the Value and Count columns.
    The histogram will match the one in cluster_analysis.py.
    Bins with negative counts are plotted as absolute values and in red color.
    """
    df = pd.read_csv(file_path, delim_whitespace=True)

    # Check if the DataFrame is empty
    if df.empty:
        print("Dataframe is empty")
        return

    # Extract values and counts sorted by value
    values = df['Value']
    counts = df['Count']
    values = values.sort_values()
    counts = counts[values.index]

    # Create histogram bins
    bins = np.arange(min(values), max(values) + bin_width, bin_width)

    # Aggregate counts into bins
    binned_counts = np.array([counts[(values >= bins[i]) & (values < bins[i + 1])].sum() for i in range(len(bins) - 1)])

    # Bin centers
    bins_c = (bins[:-1] + bins[1:]) / 2

    # Create subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

    # Plot histogram with occurrences
    for i in range(len(bins_c)):
        if binned_counts[i] >= 0:
            ax1.bar(bins_c[i], binned_counts[i], width=bin_width, color='skyblue', alpha=0.7)
        else:
            ax1.bar(bins_c[i], binned_counts[i], width=bin_width, color='red', alpha=0.7)

    ax1.set_xlabel('Brightness')
    ax1.set_ylabel('Count')

    # Plot histogram with log(occurrences)
    for i in range(len(bins_c)):
        if binned_counts[i] >= 0:
            ax2.bar(bins_c[i], np.log10(binned_counts[i]), width=bin_width, color='skyblue', alpha=0.7)
        elif binned_counts[i] != 0:
            ax2.bar(bins_c[i], np.log10(abs(binned_counts[i])), width=bin_width, color='red', alpha=0.7)
    ax2.set_xlabel('Brightness')
    ax2.set_ylabel('log(Count)')

    # Save the plot with "_hist" added to the name
    plot_path = file_path.replace('.dat', f'{bin_width}_hist.png')
    plt.savefig(plot_path)
    plt.close()
    print(f"Plot saved to {plot_path}")

def process_all_folders(base_folder, bin_width=1):
    columns = ['sum', 'sum_r', 'sum_g', 'sum_b']
    for root, dirs, files in os.walk(base_folder):
        for dir_name in dirs:
            folder_path = os.path.join(root, dir_name)
            file_path = os.path.join(folder_path, 'clusters.dat')
            if os.path.exists(file_path):
                output_folder = folder_path
                for column in columns:
                    count_column(file_path, column, output_folder)
    
    #Plot the count for each column sum, sum_r, sum_g, sum_b
    for root, dirs, files in os.walk(base_folder):
        for dir_name in dirs:
            for column in columns:
                file_path = os.path.join(root, dir_name, f'{column}_count.dat')
                if os.path.exists(file_path):
                    plot_count(file_path)
                    plot_histogram(file_path, 1)
                    plot_histogram(file_path, bin_width)


    
