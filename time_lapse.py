import time
import os
import cv2
import subprocess

folder_path = "./pictures/test3"     # where to store the pictures
device = "/dev/video4"               # what is the name of the camera, generally /dev/vieo4 or /dev/video2
                                     # you can use "ls /dev/video*" to list video device connected to computer
interval_between_pictures = 1        # in second

start_time = time.time()
number_pictures_taken = 0
if not os.path.exists(folder_path):
     os.makedirs(folder_path)

## Settings for the camera
subprocess.run(["v4l2-ctl", "--device=/dev/video4", "--set-ctrl", "auto_exposure=1"], check=True)
subprocess.run(["v4l2-ctl", "--device=/dev/video4", "--set-ctrl", "exposure_time_absolute=5000"], check=True)
subprocess.run(["v4l2-ctl", "--device=/dev/video4", "--set-ctrl", "white_balance_automatic=1"], check=True)
subprocess.run(["v4l2-ctl", "--device=/dev/video4", "--set-ctrl", "exposure_dynamic_framerate=1"], check=True)

## Define here the default ffmpeg parameters for on live visualisation of the time_lapse
brightness = "0.2"
saturation = "2"
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
          "--stream-to=" + folder_path + "/" + image_name + ".raw"
     ]
     subprocess.run(v4l2_command, stdout=subprocess.DEVNULL) ## run the above defined command in terminal
     ## Now we use ffmpeg for conversion from raw to png
     ffmpeg_command = [
          "ffmpeg",
          "-f", "rawvideo",
          "-pixel_format", "yuyv422",
          "-video_size", "1280x960",
          "-i", folder_path + "/" + image_name + ".raw",
          "-vf", "eq=brightness=" + brightness +
          ":saturation=" + saturation +
          ":contrast=" + contrast,
          "-frames:v", "1",
          folder_path + "/png_" + image_name + ".png"
     ]
     subprocess.run(ffmpeg_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) ## run the above command


if __name__ == "__main__":
     while True:
          if ((number_pictures_taken * interval_between_pictures) <= (time.time() - start_time) ) : ## if it is time to take next picture
               #print(time.time() - start_time)
               number_pictures_taken += 1
               timestamp = time.strftime("%Y%m%d-%H%M%S")     ## so that pictures are named after the time when they are taken
               image_name =f"{timestamp}"  ## where to put image/ how to name it
               capture_image(folder_path, image_name, device)             ## take the picturffmpeg -f rawvideo -pixel_format yuyv422 -video_size 1280x960 -i test.raw -vf "eq=brightness=0.4:gamma=0.7:saturation=30:contrast=0.3" -frames:v 1 test.pnge
               print(f"Captured {image_name}")                      ## print in terminal that picture has been taken sucessfully
               time.sleep(0.1)
          else :
               time.sleep(0.1)
