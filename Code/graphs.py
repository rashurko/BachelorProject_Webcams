import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

def plot_pixel_brightness_distribution(video_filename, subtract_image_path = None):
    folder = "results"
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
    
    # Plot the brightness distribution
    brightness_vals = np.linspace(0, 100, 256)
    plt.figure(figsize=(10, 5))
    plt.plot(brightness_vals, brightness_counts["red"], color='red', label='Red', linestyle = '-')
    plt.plot(brightness_vals, brightness_counts["green"], color='green', label='Green', linestyle = 'dotted')
    plt.plot(brightness_vals, brightness_counts["blue"], color='blue', label='Blue', linestyle = 'dashed')
    plt.xlabel("Pixel Brightness")
    plt.ylabel("Count")
    plt.title("Pixel Brightness Distribution")
    plt.legend()
    plt.show()

plot_pixel_brightness_distribution('video_20250226_155047.avi', 'results/offset_20250226_155041.png')
