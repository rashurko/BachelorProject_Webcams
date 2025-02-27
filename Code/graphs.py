import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

def plot_pixel_brightness_distribution(folder, video_filename, subtract_image_path=None, name="graph", title="graph"):
    video_path = os.path.join(folder, video_filename)
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return
    
    brightness_counts = {"red": np.zeros(256), "green": np.zeros(256), "blue": np.zeros(256)}

    # Load the image to subtract if provided
    subtract_image = None
    if subtract_image_path:
        subtract_image = cv2.imread(subtract_image_path).astype(np.float32)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert frame to float for subtraction
        frame = frame.astype(np.float32)
        
        # Subtract image if provided
        if subtract_image is not None:
            frame = cv2.subtract(frame, subtract_image)
            frame = np.clip(frame, 0, 255).astype(np.uint8)
        
        # Split channels
        blue, green, red = cv2.split(frame)
        
        # Update histogram counts
        for i in range(256):
            brightness_counts["red"][i] += np.sum(red == i)
            brightness_counts["green"][i] += np.sum(green == i)
            brightness_counts["blue"][i] += np.sum(blue == i)
    
    cap.release()

    # Plot the brightness distribution in 3 subplots
    brightness_vals = np.linspace(0, 100, 256)
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))  # 3 rows, 1 column
    
    # Red channel plot
    axs[0].plot(brightness_vals, brightness_counts["red"], color='red', label='Red', linestyle='-', alpha=0.5)
    axs[0].set_ylim(0, 60000)
    axs[0].set_xlabel("Pixel Brightness")
    axs[0].set_ylabel("Count")
    axs[0].set_title("Red Channel")
    axs[0].yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

    # Green channel plot
    axs[1].plot(brightness_vals, brightness_counts["green"], color='green', label='Green', linestyle='dotted', alpha=0.5)
    axs[1].set_ylim(0, 60000)
    axs[1].set_xlabel("Pixel Brightness")
    axs[1].set_ylabel("Count")
    axs[1].set_title("Green Channel")
    axs[1].yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

    # Blue channel plot
    axs[2].plot(brightness_vals, brightness_counts["blue"], color='blue', label='Blue', linestyle='dashed', alpha=0.5)
    axs[2].set_ylim(0, 60000)
    axs[2].set_xlabel("Pixel Brightness")
    axs[2].set_ylabel("Count")
    axs[2].set_title("Blue Channel")
    axs[2].yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

    # Adjust the layout and save the figure
    plt.tight_layout()
    plt.subplots_adjust(wspace = 0.33)
    graph_path = os.path.join(folder, f"graph_{name}")
    plt.savefig(graph_path)
    plt.show()

    # Save pixel brightness counts to a text file
    txt_file_path = os.path.join(folder, f"data_{name}.txt")
    with open(txt_file_path, "w") as f:
        f.write("Pixel Brightness Distribution\n")
        f.write(f"Title: {title}\n\n")
        f.write("Red Channel:\n")
        for i in range(256):
            f.write(f"{i}: {brightness_counts['red'][i]}\n")
        
        f.write("\nGreen Channel:\n")
        for i in range(256):
            f.write(f"{i}: {brightness_counts['green'][i]}\n")
        
        f.write("\nBlue Channel:\n")
        for i in range(256):
            f.write(f"{i}: {brightness_counts['blue'][i]}\n")
    
    print(f"Graph saved as {graph_path}")
    print(f"Data saved as {txt_file_path}")
