import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def count_distinct_sums(file_path, column='sum'):
    # Read the file into a DataFrame
    df = pd.read_csv(file_path, delim_whitespace=True)
    
    # Filter out rows with brightness (sum) value of 0
    df = df[df[column] != 0]
    
    # Get distinct sum values and their occurrences
    sum_counts = df[column].value_counts().to_dict()
    
    return sum_counts

def count_distinct_sizes(file_path):
    # Read the file into a DataFrame
    df = pd.read_csv(file_path, delim_whitespace=True)
    
    # Filter out rows with brightness (sum) value of 0
    df = df[df['sum'] != 0]
    
    # Get distinct size values and their occurrences
    size_counts = df['size'].value_counts().to_dict()
    
    return size_counts

def count_sums_for_given_size(file_path, target_size, column='sum'):
    # Read the file into a DataFrame
    df = pd.read_csv(file_path, delim_whitespace=True)
    
    # Filter out rows with brightness (sum) value of 0
    df = df[df[column] != 0]
    
    # Filter the DataFrame for the given size
    filtered_df = df[df['size'] == target_size]
    
    # Get distinct sum values and their occurrences for the filtered DataFrame
    sum_counts = filtered_df[column].value_counts().to_dict()
    
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

    

def save_brightness_occurrences(sum_counts, save_path):
    # Sort the sum counts by occurrences
    sorted_sum_counts = sorted(sum_counts.items(), key=lambda item: item[1], reverse=True)
    
    # Save the sorted sum counts to a .txt file
    with open(save_path, 'w') as f:
        f.write('Brightness\tOccurrences\n')
        for sum_val, count in sorted_sum_counts:
            f.write(f'{sum_val}\t{count}\n')
    print(f"Brightness occurrences saved to {save_path}")

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
                    
                    # Generate and save the histogram plots for sum
                    sum_occurrences = count_distinct_sums(file_path, column='sum')
                    size_occurrences = count_distinct_sizes(file_path)
                    filtered_sum_occurrences = count_sums_for_given_size(file_path, target_size, column='sum')
                    
                    results_folder = root
                    os.makedirs(results_folder, exist_ok=True)
                    
                    sum_save_path = os.path.join(results_folder, f"{os.path.splitext(file)[0]}_sum_occurrences_plot.png")
                    size_save_path = os.path.join(results_folder, f"{os.path.splitext(file)[0]}_size_occurrences_plot.png")
                    filtered_sum_save_path = os.path.join(results_folder, f"{os.path.splitext(file)[0]}_{target_size}px_sum_occurrences_plot.png")
                    brightness_save_path = os.path.join(results_folder, f"{os.path.splitext(file)[0]}_brightness_occurrences.txt")
                    
                    plot_sum_histogram(sum_occurrences, sum_save_path, bin_step)
                    plot_size_histogram(size_occurrences, size_save_path, 1)
                    plot_sum_histogram(filtered_sum_occurrences, filtered_sum_save_path, bin_step)
                    save_brightness_occurrences(sum_occurrences, brightness_save_path)
                    
                    print(f"Saved histogram for {file_path} to {sum_save_path}")
                    print(f"Saved size histogram for {file_path} to {size_save_path}")
                    print(f"Saved filtered sum histogram for {file_path} to {filtered_sum_save_path}")
                    print(f"Saved brightness occurrences for {file_path} to {brightness_save_path}")
                    
                    # Generate and save the histogram plots for sum_r
                    sum_r_occurrences = count_distinct_sums(file_path, column='sum_r')
                    filtered_sum_r_occurrences = count_sums_for_given_size(file_path, target_size, column='sum_r')
                    
                    sum_r_save_path = os.path.join(results_folder, f"{os.path.splitext(file)[0]}_sum_r_occurrences_plot.png")
                    filtered_sum_r_save_path = os.path.join(results_folder, f"{os.path.splitext(file)[0]}_{target_size}px_sum_r_occurrences_plot.png")
                    brightness_r_save_path = os.path.join(results_folder, f"{os.path.splitext(file)[0]}_brightness_r_occurrences.txt")
                    
                    plot_sum_histogram(sum_r_occurrences, sum_r_save_path, bin_step)
                    plot_sum_histogram(filtered_sum_r_occurrences, filtered_sum_r_save_path, bin_step)
                    save_brightness_occurrences(sum_r_occurrences, brightness_r_save_path)
                    
                    print(f"Saved histogram for {file_path} to {sum_r_save_path}")
                    print(f"Saved filtered sum histogram for {file_path} to {filtered_sum_r_save_path}")
                    print(f"Saved brightness occurrences for {file_path} to {brightness_r_save_path}")
                    
                    # Generate and save the histogram plots for sum_g
                    sum_g_occurrences = count_distinct_sums(file_path, column='sum_g')
                    filtered_sum_g_occurrences = count_sums_for_given_size(file_path, target_size, column='sum_g')
                    
                    sum_g_save_path = os.path.join(results_folder, f"{os.path.splitext(file)[0]}_sum_g_occurrences_plot.png")
                    filtered_sum_g_save_path = os.path.join(results_folder, f"{os.path.splitext(file)[0]}_{target_size}px_sum_g_occurrences_plot.png")
                    brightness_g_save_path = os.path.join(results_folder, f"{os.path.splitext(file)[0]}_brightness_g_occurrences.txt")
                    
                    plot_sum_histogram(sum_g_occurrences, sum_g_save_path, bin_step)
                    plot_sum_histogram(filtered_sum_g_occurrences, filtered_sum_g_save_path, bin_step)
                    save_brightness_occurrences(sum_g_occurrences, brightness_g_save_path)
                    
                    print(f"Saved histogram for {file_path} to {sum_g_save_path}")
                    print(f"Saved filtered sum histogram for {file_path} to {filtered_sum_g_save_path}")
                    print(f"Saved brightness occurrences for {file_path} to {brightness_g_save_path}")
                    
                    # Generate and save the histogram plots for sum_b
                    sum_b_occurrences = count_distinct_sums(file_path, column='sum_b')
                    filtered_sum_b_occurrences = count_sums_for_given_size(file_path, target_size, column='sum_b')
                    
                    sum_b_save_path = os.path.join(results_folder, f"{os.path.splitext(file)[0]}_sum_b_occurrences_plot.png")
                    filtered_sum_b_save_path = os.path.join(results_folder, f"{os.path.splitext(file)[0]}_{target_size}px_sum_b_occurrences_plot.png")
                    brightness_b_save_path = os.path.join(results_folder, f"{os.path.splitext(file)[0]}_brightness_b_occurrences.txt")
                    
                    plot_sum_histogram(sum_b_occurrences, sum_b_save_path, bin_step)
                    plot_sum_histogram(filtered_sum_b_occurrences, filtered_sum_b_save_path, bin_step)
                    save_brightness_occurrences(sum_b_occurrences, brightness_b_save_path)
                    
                    print(f"Saved histogram for {file_path} to {sum_b_save_path}")
                    print(f"Saved filtered sum histogram for {file_path} to {filtered_sum_b_save_path}")
                    print(f"Saved brightness occurrences for {file_path} to {brightness_b_save_path}")

