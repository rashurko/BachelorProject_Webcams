import cv2
import os
import time

def record_video(frame_width=640, frame_height=480, fps=30, duration=10, name = 'video'):
    # Create results folder if it doesn't exist
    folder = "results"
    os.makedirs(folder, exist_ok=True)
    
    # Generate timestamped filename
    output_filename = os.path.join(folder, time.strftime(f"{name}_%Y%m%d_%H%M%S.avi"))
    
    # Open the default webcam
    cap = cv2.VideoCapture(0)
    
    # Set frame width and height
    cap.set(3, frame_width)
    cap.set(4, frame_height)
    
    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    out = cv2.VideoWriter(output_filename, fourcc, fps, (frame_width, frame_height))
    
    print("Recording... Press 'q' to stop.")
    
    start_time = time.time()
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Write the frame to the output file
        out.write(frame)
        
        # Show the recording in a window
        cv2.imshow('Recording', frame)
        
        # Check if duration is exceeded
        if time.time() - start_time >= duration:
            break
        
        # Press 'q' to stop recording
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Recording stopped. Video saved as", output_filename)


record_video(duration=10)
