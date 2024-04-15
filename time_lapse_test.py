import time
import os
import cv2
import subprocess

folder_path = "../pictures/delay_testing"     # where to store the pictures
device = "/dev/video4"               # what is the name of the camera, generally /dev/vieo4 or /dev/video2
# you can use "ls /dev/video*" to list video device connected to computer

## Define the durations in seconds
cycle_duration = 60 ## how much time between cycles of taking pictures
sequence_picture_time = [0, 15, 30] ## time where you should begin taking picture after beggining of a cycle
picture_repetition = 3 ##

start_time = time.time()
n_cycle_done = 0

if not os.path.exists(folder_path):
     os.makedirs(folder_path)

##### Initial settings for the camera

# If you have too much / not enough light, modifie the two following parameters
# Exposition time allows for more light to go to the captor, ranges from 1 to 5000, default 650
exposition_time = 5000
# Gain amplifies the signals from captors, may increase noise, ranges from 0 to 100, increase exposition_time first
gain = 20

# For more information on the parameters you can tune on the camera please enter
# v4l2-ctl --device=/dev/video4 --list-ctrls
# in terminal, remplacing --device/dev/video4 by the path of your device

## Camera controlls
def init_camera ():
     # Auto exposure to manual mode (1) to be able to tune manually the exposure time
     subprocess.run(["v4l2-ctl", "--device=" + device, "--set-ctrl", "auto_exposure=1"], check=True)
     # Exposure time to maximum for low-light condition
     subprocess.run(["v4l2-ctl", "--device=" + device, "--set-ctrl", "exposure_time_absolute=" + str(exposition_time)], check=True)
     # Dynamic framerate to false to increse reproducibility
     subprocess.run(["v4l2-ctl", "--device=" + device, "--set-ctrl", "exposure_dynamic_framerate=0"], check=True)

     ## Brightness to default to avoid artificial enhancement or dimming of the image.
     subprocess.run(["v4l2-ctl", "--device=" + device, "--set-ctrl", "brightness=0"], check=True)
     # Contrast to default to maintain natural contrast without software enhancement.
     subprocess.run(["v4l2-ctl", "--device=" + device, "--set-ctrl", "contrast=32"], check=True)
     # Saturation to default to preserve natural color saturation.
     subprocess.run(["v4l2-ctl", "--device=" + device, "--set-ctrl", "saturation=50"], check=True)
     # Hue to default to avoid color shifting.
     subprocess.run(["v4l2-ctl", "--device=" + device, "--set-ctrl", "hue=0"], check=True)
     # Automatic white balance disabled to prevent the camera from adjusting colors based on lighting conditions.
     subprocess.run(["v4l2-ctl", "--device=" + device, "--set-ctrl", "white_balance_automatic=0"], check=True)
     # Gamma to 100 to avoid non-linear brightness adjustments.
     subprocess.run(["v4l2-ctl", "--device=" + device, "--set-ctrl", "gamma=100"], check=True)
     # Gain is an electonic amplificaton of the sensors signal. Sould be increased it in dark environment.
     # Drawbacks :amplifies noise, can make light zones saturated. Ranges from 0 to 100.
     subprocess.run(["v4l2-ctl", "--device=" + device, "--set-ctrl", "gain=" + str(gain)], check=True)
     # Power line frequency to avoid flickering caused by artificial lighting.
     # the value depends on your region (1 for 50 Hz - Europe, 2 for 60 Hz - North America).
     subprocess.run(["v4l2-ctl", "--device=" + device, "--set-ctrl", "power_line_frequency=1"], check=True)
     # White balance temperature to a fixed value for consistent color temperature.
     subprocess.run(["v4l2-ctl", "--device=" + device, "--set-ctrl", "white_balance_temperature=4600"], check=True)
     # Sharpness to the minimum to avoid artificial edge enhancement.
     subprocess.run(["v4l2-ctl", "--device=" + device, "--set-ctrl", "sharpness=1"], check=True)
     # Backlight compensation to 0 to avoid artificial light adjustments on diffrent parts of the picture.
     subprocess.run(["v4l2-ctl", "--device=" + device, "--set-ctrl", "backlight_compensation=0"], check=True)

## Parameter for FFMPEG conversion from raw to png
brightness = "0"
saturation = "1"
contrast = "1"

def capture_image(folder_path, image_name, device):
     ## v4l2 , Video for linux 2, is a linux video API
     ## We define a command that can then be send to the terminal via the subprocess library
     v4l2_command = [
          "v4l2-ctl",
          "--device=" + device,
          "--set-fmt-video=width=1280,height=960,pixelformat=YUYV",
          "--stream-mmap",
          "--stream-count=1",
          "--stream-to=" + folder_path + "/raw_" + image_name + ".raw"
     ]
     subprocess.run(v4l2_command, stdout=subprocess.DEVNULL) ## run the above defined command in terminal
     ## Now we use ffmpeg for conversion from raw to png
     ffmpeg_command = [
          "ffmpeg",
          "-f", "rawvideo",
          "-pixel_format", "yuyv422",
          "-video_size", "1280x960",
          "-i", folder_path + "/raw_" + image_name + ".raw",
          "-vf", "eq=brightness=" + brightness +
          ":saturation=" + saturation +
          ":contrast=" + contrast,
          "-frames:v", "1",
          folder_path + "/png_" + image_name + ".png"
     ]
     subprocess.run(ffmpeg_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) ## run the above command


if __name__ == "__main__":
     init_camera()
     while True:
          for index_in_sequence in range (len(sequence_picture_time)):
               time_next_picture = sequence_picture_time[index_in_sequence] + n_cycle_done * cycle_duration
               print(time_next_picture)
               while (time_next_picture > (time.time() - start_time) ) : ## As long as we wait for next picture
                    time.sleep(0.1)
               # take the pictures, name it according to the time it was taken plus other infos
               print(time.time() - start_time)
               for j in range(picture_repetition) :
                    timestamp = time.strftime("%Y%m%d-%H%M%S")     ## so that pictures are named after the time when they are taken
                    image_name =f"{timestamp}" + "cycle=" + str(n_cycle_done) + "_color=" + str(index_in_sequence) + "_j=" + str(j)
                    capture_image(folder_path, image_name, device)             ## take the picturffmpeg -f rawvideo -pixel_format yuyv422 -video_size 1280x960 -i test.raw -vf "eq=brightness=0.4:gamma=0.7:saturation=30:contrast=0.3" -frames:v 1 test.pnge
               #print(f"{timestamp}")                    ## print in terminal that picture has been taken sucessfully
          n_cycle_done +=1
