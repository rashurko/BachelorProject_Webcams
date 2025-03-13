import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def count_distinct_sums(file_path):
    # Read the file into a DataFrame
    df = pd.read_csv(file_path, delim_whitespace=True)
    
    # Get distinct sum values and their occurrences
    sum_counts = df['sum'].value_counts().to_dict()
    
    return sum_counts

def count_distinct_sizes(file_path):
    # Read the file into a DataFrame
    df = pd.read_csv(file_path, delim_whitespace=True)
    
    # Get distinct size values and their occurrences
    size_counts = df['size'].value_counts().to_dict()
    
    return size_counts

def count_sums_for_given_size(file_path, target_size):
    # Read the file into a DataFrame
    df = pd.read_csv(file_path, delim_whitespace=True)
    
    # Filter the DataFrame for the given size
    filtered_df = df[df['size'] == target_size]
    
    # Get distinct sum values and their occurrences for the filtered DataFrame
    sum_counts = filtered_df['sum'].value_counts().to_dict()
    
    return sum_counts

def plot_sum_histogram(sum_counts, save_path, bin_step):
    # Convert sum occurrences to a list for histogram
    sums = list(sum_counts.keys())
    occurrences = list(sum_counts.values())
    
    # Create histogram bins
    if len(sums) == 0:
        print("No data to plot.")
        return

    bins = range(int(min(sums)), int(max(sums)) + bin_step, bin_step)
    
    # Create subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    
    # Plot histogram with log(occurrences)
    ax1.hist(sums, bins=bins, weights=np.log(occurrences), edgecolor='black', alpha=0.7, label='Histogram')
    sorted_sums = sorted(sum_counts.keys())
    sorted_occurrences = [sum_counts[sum_val] for sum_val in sorted_sums]
    ax1.vlines(sorted_sums, 0, np.log(sorted_occurrences), color='red', label='Vertical Lines')
    ax1.set_xlabel('Brightness')
    ax1.set_ylabel('log(Count)')
    ax1.legend()
    
    # Annotate peaks for log(occurrences)
    #for i in range(1, len(sorted_occurrences) - 1):
    #    if sorted_occurrences[i] > sorted_occurrences[i - 1] and sorted_occurrences[i] > sorted_occurrences[i + 1]:
    #        ax1.text(sorted_sums[i], np.log(sorted_occurrences[i]), str(sorted_sums[i]), ha='center', va='bottom')
    
    # Plot histogram with occurrences
    ax2.hist(sums, bins=bins, weights=occurrences, edgecolor='black', alpha=0.7, label='Histogram')
    ax2.vlines(sorted_sums, 0, sorted_occurrences, color='red', label='Vertical Lines')
    ax2.set_xlabel('Brightness')
    ax2.set_ylabel('Count')
    ax2.legend()
    
    # Annotate peaks for occurrences
    #for i in range(1, len(sorted_occurrences) - 1):
    #    if sorted_occurrences[i] > sorted_occurrences[i - 1] and sorted_occurrences[i] > sorted_occurrences[i + 1]:
    #        ax2.text(sorted_sums[i], sorted_occurrences[i], str(sorted_sums[i]), ha='center', va='bottom')
    
    # Save the plot
    plt.savefig(save_path)
    plt.close()

def plot_size_histogram(size_counts, save_path, bin_step):
    # Convert size occurrences to a list for histogram
    sizes = list(size_counts.keys())
    occurrences = list(size_counts.values())
    
    # Create histogram bins
    if len(sizes) == 0:
        print("No data to plot.")
        return

    bins = range(int(min(sizes)), int(max(sizes)) + bin_step, bin_step)
    
    # Plot histogram
    plt.figure(figsize=(10, 5))
    plt.hist(sizes, bins=bins, weights=np.log(occurrences), edgecolor='black', alpha=0.7, label='Histogram')
    
    # Plot vertical lines
    sorted_sizes = sorted(size_counts.keys())
    sorted_occurrences = [size_counts[size_val] for size_val in sorted_sizes]
    plt.vlines(sorted_sizes, 0, np.log(sorted_occurrences), color='red', label='Vertical Lines')
    
    # Annotate peaks
    #for i in range(1, len(sorted_occurrences) - 1):
    #    if sorted_occurrences[i] > sorted_occurrences[i - 1] and sorted_occurrences[i] > sorted_occurrences[i + 1]:
    #        plt.text(sorted_sizes[i], np.log(sorted_occurrences[i]), str(sorted_sizes[i]), ha='center', va='bottom')
    
    plt.xlabel('Size')
    plt.ylabel('log(Count)')
    plt.legend()
    
    # Save the plot
    plt.savefig(save_path)
    plt.close()

def generate_histograms_for_all_subfolders(base_folder, bin_step, target_size, subfolder_depth=1):
    """
    Generate histograms for every .dat file in all subfolders of the given folder.
    
    :param base_folder: The base folder containing subfolders with .dat files.
    :param bin_step: The step size for histogram bins.
    :param target_size: The size of clusters to filter for the third plot.
    :param subfolder_depth: Number of subfolders to traverse to get to the .dat files.
    """
    for root, dirs, files in os.walk(base_folder):
        # Calculate the depth of the current directory
        depth = root[len(base_folder):].count(os.sep)
        
        if depth == subfolder_depth:
            for file in files:
                if file.endswith('.dat'):
                    file_path = os.path.join(root, file)
                    sum_occurrences = count_distinct_sums(file_path)
                    size_occurrences = count_distinct_sizes(file_path)
                    filtered_sum_occurrences = count_sums_for_given_size(file_path, target_size)
                    
                    # Create results folder in the current directory
                    results_folder = root
                    os.makedirs(results_folder, exist_ok=True)
                    
                    # Define the save path for the histogram plots
                    sum_save_path = os.path.join(results_folder, f"{os.path.splitext(file)[0]}_sum_occurrences_plot.png")
                    size_save_path = os.path.join(results_folder, f"{os.path.splitext(file)[0]}_size_occurrences_plot.png")
                    filtered_sum_save_path = os.path.join(results_folder, f"{os.path.splitext(file)[0]}_{target_size}px_sum_occurrences_plot.png")
                    
                    # Generate and save the histogram plots
                    plot_sum_histogram(sum_occurrences, sum_save_path, bin_step)
                    plot_size_histogram(size_occurrences, size_save_path, 1)
                    plot_sum_histogram(filtered_sum_occurrences, filtered_sum_save_path, bin_step)
                    print(f"Saved histogram for {file_path} to {sum_save_path}")
                    print(f"Saved size histogram for {file_path} to {size_save_path}")
                    print(f"Saved filtered sum histogram for {file_path} to {filtered_sum_save_path}")
