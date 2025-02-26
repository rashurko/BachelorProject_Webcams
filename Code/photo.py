import cv2
import os

def capture_photo(folder, width, height, name = 'photo', camera_index=0):
    os.makedirs(folder, exist_ok=True)  # Ensure the folder exists
    filename = os.path.join(folder, name + ".png")  # Generate timestamped filename
    
    cap = cv2.VideoCapture(camera_index)  # Open the webcam

    # Set resolution to width x height
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    ret, frame = cap.read()  # Capture a frame
    if ret:
        cv2.imwrite(filename, frame)  # Save the photo
        print(f"Photo saved as {filename}")
    else:
        print("Error: Could not capture image.")
    
    cap.release()  # Release the camera
    cv2.destroyAllWindows()
