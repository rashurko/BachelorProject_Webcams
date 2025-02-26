import time

import photo
import recording
import stacker
import graphs

name = "cheap_0" + "_" + time.strftime("%Y-%m-%d_%H-%M-%S")
save_path = "Code/results"
width, height = 640, 480

photo.capture_photo(save_path, width, height, name)
print("Press ENTER to start recording")
input()

recording.record_video(save_path, width, height, 30, 5, name)

stacker.create_long_exposure(save_path, name + ".avi", save_path + "/" + name + ".png", "long_" + name)

graphs.plot_pixel_brightness_distribution(save_path, name + ".avi", save_path + "/" + "long_" + name + ".png", name, "cheap webcam")

