import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def analyze_image_brightness(image_path):
    """
    Analyze each pixel of a given image and return a 2D array of the brightness sums of the three colors (r, g, b).
    
    :param image_path: Path to the input image file.
    :return: 2D array of brightness sums.
    """
    # Read the image
    image = cv2.imread(image_path)
    
    if image is None:
        raise ValueError(f"Error: Could not open or find the image at {image_path}")
    
    # Convert the image to RGB format (OpenCV reads images in BGR format by default)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Calculate the brightness sum for each pixel
    brightness_sums = np.sum(image_rgb, axis=2)
    
    return brightness_sums, image_rgb

def analyze_folder_brightness(folder_path, format='.png'):
    """
    Analyze all images in a given folder and return the mean 2D array of brightness sums and the average image.
    
    :param folder_path: Path to the folder containing image files.
    :return: 2D array of mean brightness sums, average image.
    """
    total_brightness_sums = None
    total_image = None
    image_count = 0
    
    # Iterate over all files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        # Check if the file is an image (you can add more extensions if needed)
        if file_name.lower().endswith((format)):
            brightness_sums, image_rgb = analyze_image_brightness(file_path)
            
            if total_brightness_sums is None:
                total_brightness_sums = brightness_sums
                total_image = image_rgb.astype(np.float64)
            else:
                total_brightness_sums += brightness_sums
                total_image += image_rgb.astype(np.float64)
            
            image_count += 1
    
    if total_brightness_sums is not None and image_count > 0:
        mean_brightness_sums = total_brightness_sums / image_count
        average_image = (total_image / image_count).astype(np.uint8)
    else:
        mean_brightness_sums = None
        average_image = None
    
    return mean_brightness_sums, average_image

def plot_brightness_3d(mean_brightness_sums, output_folder, folder_name):
    """
    Plot the mean brightness sums in a 3D graph and save it in a given folder.
    Also save the mean brightness sums as a .dat file.
    
    :param mean_brightness_sums: 2D array of mean brightness sums.
    :param output_folder: Folder where the plot and .dat file will be saved.
    :param folder_name: Name of the folder containing the analyzed images.
    """
    # Create a new folder in the output directory with the name of the analyzed folder
    results_folder = os.path.join(output_folder, folder_name)
    os.makedirs(results_folder, exist_ok=True)
    
    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Get the dimensions of the brightness sums array
    x_dim, y_dim = mean_brightness_sums.shape
    
    # Create meshgrid for plotting
    x = np.arange(x_dim)
    y = np.arange(y_dim)
    x, y = np.meshgrid(x, y)
    
    # Plot the surface
    ax.plot_surface(x, y, mean_brightness_sums.T, cmap='hot', edgecolor='k', linewidth=0.1, antialiased=True)
    
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Mean Brightness')

    ax.view_init(elev=25, azim=45)
    
    # Save the plot
    plot_path = os.path.join(results_folder, 'darkcurrent_3d_plot.png')
    plt.savefig(plot_path)
    plt.close()
    print(f"Saved 3D brightness plot to {plot_path}")
    

def save_average_image(average_image, output_folder, folder_name):
    """
    Save the average image in a given folder.
    
    :param average_image: The average image to be saved.
    :param output_folder: Folder where the image will be saved.
    :param folder_name: Name of the folder containing the analyzed images.
    """
    # Create a new folder in the output directory with the name of the analyzed folder
    results_folder = os.path.join(output_folder, folder_name)
    os.makedirs(results_folder, exist_ok=True)
    
    # Save the average image
    image_path = os.path.join(results_folder, 'average_darkcurrent.png')
    cv2.imwrite(image_path, cv2.cvtColor(average_image, cv2.COLOR_RGB2BGR))
    print(f"Saved average image to {image_path}")

def analyze_and_plot_all_folders(base_folder, output_folder, subfolder_depth=1, format='.png'):
    """
    Analyze and plot brightness sums for all subfolders in a given base folder.
    
    :param base_folder: The base folder containing subfolders with image files.
    :param output_folder: Folder where the plots and .dat files will be saved.
    :param subfolder_depth: Number of subfolders to traverse to get to the images.
    :param format: Image format to be analyzed (default is '.png').
    """
    for root, dirs, files in os.walk(base_folder):
        # Calculate the depth of the current directory
        depth = root[len(base_folder):].count(os.sep)
        
        if depth == subfolder_depth and os.path.basename(root) == "DarkCurrent":
            parent_folder_name = os.path.basename(os.path.dirname(root))
            folder_name = os.path.basename(root)
           
            combined_folder_name = parent_folder_name
            
            mean_brightness_sums, average_image = analyze_folder_brightness(root, format)
            if mean_brightness_sums is not None:
                plot_brightness_3d(mean_brightness_sums, output_folder, combined_folder_name)
                save_average_image(average_image, output_folder, combined_folder_name)
