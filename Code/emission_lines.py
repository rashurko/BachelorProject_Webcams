import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_top_n_values(base_folder, n=5, output_file='top_n_values_plot.png'):
    """
    Go over folders containing sum_count.dat files, extract the first n values with their counts,
    and plot them with labels corresponding to their folder names.

    :param base_folder: Path to the base folder containing subfolders with sum_count.dat files.
    :param n: Number of top values to plot from each folder.
    :param output_file: Path to save the resulting plot.
    """
    plt.figure(figsize=(12, 8))

    values_all = []
    counts_all = []

    #8 colors for the lines
    colors = ['blue', 'green', 'red', 'navy', 'cyan', 'yellow', 'black', 'magenta']

    # Iterate over all subfolders
    i = 0
    for root, dirs, files in os.walk(base_folder):
        for dir_name in dirs:
            folder_path = os.path.join(root, dir_name)
            file_path = os.path.join(folder_path, 'sum_count.dat')

            # Check if sum_count.dat exists in the folder
            if os.path.exists(file_path):
                # Read the sum_count.dat file
                df = pd.read_csv(file_path, delim_whitespace=True)

                # Ensure the file has the required columns
                if 'Value' in df.columns and 'Count' in df.columns:
                    # Extract counts and values
                    values = df['Value']
                    counts = df['Count']

                    top_values = values[0:n]
                    top_counts = counts[0:n]

                    values_all.extend(top_values)
                    counts_all.extend(top_counts)

                    # Plot vertical lines of each folder in different color
                    plt.vlines(top_values, 0, top_counts, label=dir_name, color=colors[i], alpha=0.5)
                    
                    # Annotate the values with their values
                    if len(top_values) != 0 or len(top_counts) != 0:
                
                        for j in range(n):
                            plt.annotate(f"{top_values[j]}", (top_values[j], top_counts[j]), textcoords="offset points", xytext=(0, 10), ha='center')

                    i += 1
                else:
                    print(f"File {file_path} does not have the required columns: 'Value' and 'Count'.")

    # Plot the data
    plt.xlabel('Brightness')
    plt.ylabel('Count')
    plt.legend()

    # Save the plot into the base_folder
    plot_path = os.path.join(base_folder, output_file)
    plt.savefig(plot_path)
    plt.close()
    print(f"Plot saved to {plot_path}")

    # Save the values and counts in decreasing order to a .dat file
    values_counts_df = pd.DataFrame({'Value': values_all, 'Count': counts_all})
    values_counts_df = values_counts_df.sort_values(by='Count', ascending=False)
    values_counts_df.to_csv(os.path.join(base_folder, 'top_values_counts.dat'), sep='\t', index=False)
    print(f"Top values and counts saved to {base_folder}/top_values_counts.dat")


# Example usage
base_folder = 'Code/results/basler_results/week7/No_Angle/filtered'  # Replace with the actual base folder path
plot_top_n_values(base_folder, n=5, output_file='top_5_values_plot.png')