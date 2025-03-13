import darkcurrent_plot as dp
import events
import cluster_analysis as ca

base_folder = 'Code/frames/week4'  # Replace with the actual base folder path
output_folder = 'Code/results/week4'  # Folder where the plots and .dat files will be saved
subfolder_depth_dp = 2  # Adjust this value based on the depth of subfolders containing images
type = "png"
output = "clusters.dat"

bin_step = 1  # Step size for histogram bins
target_size = 4  # The size of clusters to filter for the third plot
subfolder_depth_ca = 1  # Adjust this value based on the depth of subfolders containing .dat files

#dp.analyze_and_plot_all_folders(base_folder, output_folder, subfolder_depth_dp, "." + type)

#events.process_folders(base_folder, output_folder, type, output)

ca.generate_histograms_for_all_subfolders(output_folder, bin_step, target_size, subfolder_depth_ca)