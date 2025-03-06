import cv2
import os

def extract_frames(video_path, output_folder):
    """
    Extract every frame from a video and save them as images.
    
    :param video_path: Path to the input video file.
    :param output_folder: Folder where images will be saved.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        frame_filename = os.path.join(output_folder, f"frame_{frame_count:05d}.png")
        cv2.imwrite(frame_filename, frame)
        
        frame_count += 1
    
    cap.release()
    print(f"Saved {frame_count} frames to {output_folder}")

# Example usage
video_path = "Code/results/week 3/cheap_60mm_100kV_300µA_2025-02-27_15-03-27.avi"  # Change this to your video file path
output_folder = "Code/frames"  # Folder where images will be saved

extract_frames(video_path, output_folder)
