import pandas as pd
import os

def remove_common_sum_rows(file1_path, file2_path, output_folder, column='sum'):
    # Read the .dat files into DataFrames
    df1 = pd.read_csv(file1_path, delim_whitespace=True)
    df2 = pd.read_csv(file2_path, delim_whitespace=True)
    
    # Ensure both DataFrames have the specified column
    if column not in df1.columns or column not in df2.columns:
        raise ValueError(f"One or both .dat files do not have a '{column}' column.")
    
    # Identify the common values in the specified column
    common_values = set(df1[column]).intersection(set(df2[column]))
    
    # Remove rows with common values from the first DataFrame
    result_df = df1[~df1[column].isin(common_values)]
    
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Create the output file path
    output_file_path = os.path.join(output_folder, f'filtered_clusters_{column}.dat')
    
    # Save the result to a new .dat file
    result_df.to_csv(output_file_path, sep='\t', index=False)
    print(f"Filtered result for {column} saved to {output_file_path}")

def process_all_folders(base_folder, file2_path):
    columns = ['sum', 'sum_r', 'sum_g', 'sum_b']
    for root, dirs, files in os.walk(base_folder):
        for dir_name in dirs:
            folder_path = os.path.join(root, dir_name)
            file1_path = os.path.join(folder_path, 'clusters.dat')
            if os.path.exists(file1_path):
                output_folder = os.path.join(root, f'filtered_{dir_name}')
                for column in columns:
                    remove_common_sum_rows(file1_path, file2_path, output_folder, column)

# Example usage
base_folder = 'Code/results/basler_results/week5'  # Replace with the actual base folder path
file2_path = 'Code/results/basler_results/week5/Basler_Nothing_100kV_300muA/clusters.dat'
process_all_folders(base_folder, file2_path)


