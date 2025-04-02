import pandas as pd
import os

def difference_between_dat_files(file1_path, file2_path, output_file_path):
    """
    Calculate the difference between two .dat files based on the 'Value' column and subtract their 'Count'.

    :param file1_path: Path to the first .dat file.
    :param file2_path: Path to the second .dat file.
    :param output_file_path: Path to save the resulting .dat file.
    """
    # Read the .dat files into DataFrames
    df1 = pd.read_csv(file1_path, delim_whitespace=True)
    df2 = pd.read_csv(file2_path, delim_whitespace=True)
    
    # Ensure both DataFrames have the required columns
    required_columns = {'Value', 'Count'}
    if not required_columns.issubset(df1.columns) or not required_columns.issubset(df2.columns):
        raise ValueError(f"One or both .dat files do not have the required columns: {required_columns}")
    
    # Merge the two DataFrames on the 'Value' column
    merged_df = pd.merge(df1, df2, on='Value', how='outer', suffixes=('_file1', '_file2'))
    
    # Fill NaN values with 0 for Count
    merged_df['Count_file1'] = merged_df['Count_file1'].fillna(0)
    merged_df['Count_file2'] = merged_df['Count_file2'].fillna(0)
    
    # Calculate the difference in Count
    merged_df['Count_difference'] = merged_df['Count_file1'] - merged_df['Count_file2']
    
    # Keep only rows where the difference is not zero
    result_df = merged_df[merged_df['Count_difference'] != 0][['Value', 'Count_difference']]
    result_df.rename(columns={'Count_difference': 'Count'}, inplace=True)
    
    # Sort the result by Count in descending order
    result_df = result_df.sort_values(by='Count', ascending=False)
    
    # Save the result to a new .dat file
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    result_df.to_csv(output_file_path, sep='\t', index=False)
    print(f"Difference file saved to {output_file_path}")

def process_all_folders(base_folder, reference_file_path, output_base_folder):
    """
    Process all subfolders in the base folder, calculate the difference for each folder's .dat file
    against the reference file, and save the results.

    :param base_folder: Path to the base folder containing subfolders with .dat files.
    :param reference_file_path: Path to the reference .dat file.
    :param output_base_folder: Path to the base folder where the output files will be saved.
    """
    for root, dirs, files in os.walk(base_folder):
        for dir_name in dirs:
            folder_path = os.path.join(root, dir_name)
            file1_path = os.path.join(folder_path, 'sum_count.dat')  # Assuming the file is named 'sum_count.dat'
            if os.path.exists(file1_path):
                output_folder = os.path.join(output_base_folder, f'filtered_{dir_name}')
                output_file_path = os.path.join(output_folder, 'sum_count.dat')
                try:
                    difference_between_dat_files(file1_path, reference_file_path, output_file_path)
                except ValueError as e:
                    print(f"Skipping folder {folder_path} due to error: {e}")

# Example usage
base_folder = 'Code/results/week7'  # Replace with the actual base folder path
reference_file_path = 'Code/results/week7/Trust_Stand_Angle_130kV_300muA/sum_count.dat'  # Replace with the reference .dat file path
output_base_folder = 'Code/results/week7'  # Replace with the desired output base folder path

process_all_folders(base_folder, reference_file_path, output_base_folder)