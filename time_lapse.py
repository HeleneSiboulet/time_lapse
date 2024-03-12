import time
import os
import cv2

folder_path = "./pictures/test2"
device = "/dev/video4"
interval_between_pictures = 1        # in second

start_time = time.time()
number_pictures_taken = 0
if not os.path.exists(folder_path):
     os.makedirs(folder_path)

## Initial setting for the camera
# Initialize the camera with the device index
cap = cv2.VideoCapture(device)
# Check if the webcam is opened correctly
if not cap.isOpened():
     raise IOError(f"Cannot open camera {device}")
# Set the resolution (optional, remove if you want default resolution)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
cap.set(cv2.CAP_PROP_BRIGHTNESS, 0)
cap.set(cv2.CAP_PROP_SATURATION, 128)


## The following parameters have been chosen with tests
GFP_Contrast = 0
GFP_Hue = 17
GFP_Gamma = 110
GFP_Gain = 80

mCherry_Contrast = 30
mCherry_Hue = -30
mCherry_Gamma = 150
mCherry_Gain = 70

def capture_image(image_path, device, color : str):
     # Set the parameters of the camera
     cap.set(cv2.CAP_PROP_CONTRAST, globals()[color + "_Contrast"])
     cap.set(cv2.CAP_PROP_HUE, globals()[color + "_Hue"])
     cap.set(cv2.CAP_PROP_GAMMA, globals()[color + "_Gamma"])
     cap.set(cv2.CAP_PROP_GAIN, globals()[color + "_Gain"])

     # Warm the camera up
     warm_up_time = 90
     for _ in range(warm_up_time):
        ret, _ = cap.read()
     # capture one frame
     ret, frame = cap.read()
     if ret:
          # write to file
          cv2.imwrite(image_path, frame)
     else:
          print("Error: no frame captured")


if __name__ == "__main__":
     while True:
          if ((number_pictures_taken * interval_between_pictures) <= (time.time() - start_time) ) :
               #print(time.time() - start_time)
               number_pictures_taken += 1
               timestamp = time.strftime("%Y%m%d-%H%M%S")
               image_path = folder_path + "/" + f"{timestamp}.jpg"
               capture_image(image_path, device, "GFP")
               print(time.time() - start_time)
               print(f"Captured {image_path}")
               time.sleep(0.1)
