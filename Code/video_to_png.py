import cv2
import os

def extract_frames(video_path, output_folder):
    """
    Extract every frame from a video and save them as images.
    
    :param video_path: Path to the input video file.
    :param output_folder: Folder where images will be saved.
    """
    # Check if the file is a video of format .avi
    if not video_path.lower().endswith('.avi'):
        print(f"Error: {video_path} is not a .avi file.")
        return
    
    # Get the video file name without extension
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    
    # Create a new folder in the output directory with the name of the video
    video_output_folder = output_folder
    os.makedirs(video_output_folder, exist_ok=True)
    
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
        
        frame_filename = os.path.join(video_output_folder, f"frame_{frame_count:05d}.png")
        cv2.imwrite(frame_filename, frame)
        
        frame_count += 1
    
    cap.release()
    print(f"Saved {frame_count} frames to {video_output_folder}")

def extract_frames_from_folder(videos_folder, output_folder):
    """
    Extract frames from all videos in a given folder and save them as images.
    
    :param videos_folder: Folder containing video files.
    :param output_folder: Folder where images will be saved.
    """
    # Get a list of all video files in the folder
    video_files = [f for f in os.listdir(videos_folder) if os.path.isfile(os.path.join(videos_folder, f))]
    
    for video_file in video_files:
        video_path = os.path.join(videos_folder, video_file)
        extract_frames(video_path, output_folder)

# Example usage
videos_folder = "Code/frames/week7"  # Folder containing video files
output_folder = "Code/frames/week7"  # Folder where images will be saved

extract_frames_from_folder(videos_folder, output_folder)
