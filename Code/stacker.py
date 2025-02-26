import cv2
import numpy as np
import os
import time

def create_long_exposure(video_filename, subtract_image_path=None, name='long_exposure'):
    # Define folder paths
    folder = "results"
    os.makedirs(folder, exist_ok=True)
    
    # Input video file from results folder
    video_path = os.path.join(folder, video_filename)
    output_image_path = os.path.join(folder, time.strftime(f"{name}_%Y%m%d_%H%M%S.png"))
    
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Get video properties
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Initialize an empty accumulator image
    accumulator = np.zeros((frame_height, frame_width, 3), dtype=np.float32)
    
    # Load the image to subtract if provided
    subtract_image = None
    if subtract_image_path:
        subtract_image = cv2.imread(subtract_image_path).astype(np.float32)
        subtract_image = cv2.resize(subtract_image, (frame_width, frame_height))
    
    frame_index = 0
    
    print("Processing video frames for long exposure effect...")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert frame to float
        frame_float = frame.astype(np.float32)
        
        # Subtract the given image if provided
        if subtract_image is not None:
            frame_float -= subtract_image
        
        # Add to the accumulator
        accumulator += frame_float
        
        frame_index += 1
        if frame_index % 10 == 0:
            print(f"Processed {frame_index}/{frame_count} frames...")
    
    # Normalize the accumulated image
    long_exposure_image = accumulator
    
    # Save the final long-exposure image
    cv2.imwrite(output_image_path, long_exposure_image)
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"Long exposure image saved as {output_image_path}")
    return output_image_path

# Example usage
create_long_exposure("video_20250226_155821.avi", 'results/offset_20250226_155813.png', name = 'long_exposure')
