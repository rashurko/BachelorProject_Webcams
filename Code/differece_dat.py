import pandas as pd
import os

def remove_common_sum_rows(file1_path, file2_path, output_folder):
    # Read the .dat files into DataFrames
    df1 = pd.read_csv(file1_path, delim_whitespace=True)
    df2 = pd.read_csv(file2_path, delim_whitespace=True)
    
    # Ensure both DataFrames have the 'sum' column
    if 'sum' not in df1.columns or 'sum' not in df2.columns:
        raise ValueError("One or both .dat files do not have a 'sum' column.")
    
    # Identify the common 'sum' values
    common_sums = set(df1['sum']).intersection(set(df2['sum']))
    
    # Remove rows with common 'sum' values from the first DataFrame
    result_df = df1[~df1['sum'].isin(common_sums)]
    
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Create the output file path
    output_file_path = os.path.join(output_folder, 'filtered_clusters.dat')
    
    # Save the result to a new .dat file
    result_df.to_csv(output_file_path, sep='\t', index=False)
    print(f"Filtered result saved to {output_file_path}")

def process_all_folders(base_folder, file2_path):
    for root, dirs, files in os.walk(base_folder):
        for dir_name in dirs:
            folder_path = os.path.join(root, dir_name)
            file1_path = os.path.join(folder_path, 'clusters.dat')
            if os.path.exists(file1_path):
                output_folder = os.path.join(root, f'filtered_{dir_name}')
                remove_common_sum_rows(file1_path, file2_path, output_folder)

# Example usage
base_folder = 'Code/results/basler_results/week5'  # Replace with the actual base folder path
file2_path = 'Code/results/basler_results/week5/Basler_Nothing_100kV_300muA/clusters.dat'
process_all_folders(base_folder, file2_path)