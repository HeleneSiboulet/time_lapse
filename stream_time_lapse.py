import cv2
import subprocess
import sys
import time
from datetime import datetime
import numpy as np
import os

# Define the function for when to record and the diffrent chanels
# Durations are in seconds
cycle_duration = 60 * 15
record_duration = 20
warm_up_duration = 10
extra_delay = 5
channel_duration = warm_up_duration + record_duration + extra_delay
start = time.time()
nb_channels = 3
channel_names = ['red', 'green', 'blue']
assert (len(channel_names) == nb_channels)

## Chanelto_record() returns the nb of the channel to record. 0 if not recording.
## And a boolean that indicates if recording is in progress
def channel_to_record() :
    now = ( time.time() - start ) % cycle_duration
    channel = (now // channel_duration) + 1
    if (channel > nb_channels) :
        return (0 , False)
    else :
        where_in_record = now - (channel - 1) * channel_duration
        if (where_in_record >= warm_up_duration) and (where_in_record <= warm_up_duration + record_duration) :
            return (int (channel), True)
        return (int(channel), False)
channel = 0
recording = False


# Choose output path
output_path = '../pictures/sync_test'
if not os.path.exists(output_path):
    os.makedirs(output_path)
for name in channel_names :
    if not os.path.exists(output_path + '/' + name) :
        os.makedirs(output_path + '/' + name)
output_filename = "tl_video.mp4"

# Define a FFMPEG command that allows to store the video flux
ffmpeg = 'ffmpeg'
ffmpeg_command = [
    ffmpeg,
    '-y',  # Overwrite output file if it exists
    '-loglevel', 'warning',  # Show only warnings and error messages
    '-f', 'rawvideo',  # Input format
    '-vcodec', 'rawvideo',  # Input codec
    '-s', '1280x960',  # Size of one frame
    '-pix_fmt', 'bgr24',  # Input pixel format
    '-r', '30',  # Frames per second
    '-i', '-',  # The input comes from a pipe
    '-an',  # No audio
    '-vcodec', 'mpeg4',  # Output codec
    output_filename
]
#process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE) #uncomment if you want to record the video

## Define functions to initialize the parameters of the camera
## Otherwise the camera remember the parameters set for its last use
device = '/dev/video4' # remplace with the camera name according to your computer
def set_camera_user_settings () :
    # Brightness to default to avoid artificial enhancement or dimming of the image.
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
    # Gain is an electonic amplificaton of the sensors signal. Keep to 0 or picture would be saturated
    subprocess.run(["v4l2-ctl", "--device=" + device, "--set-ctrl", "gain=0"], check=True)
    # Power line frequency to avoid flickering caused by artificial lighting.
    # the value depends on your region (1 for 50 Hz - Europe, 2 for 60 Hz - North America).
    subprocess.run(["v4l2-ctl", "--device=" + device, "--set-ctrl", "power_line_frequency=1"], check=True)
    # White balance temperature to a fixed value for consistent color temperature.
    subprocess.run(["v4l2-ctl", "--device=" + device, "--set-ctrl", "white_balance_temperature=4600"], check=True)
    # Sharpness to the minimum to avoid artificial edge enhancement.
    subprocess.run(["v4l2-ctl", "--device=" + device, "--set-ctrl", "sharpness=1"], check=True)
    # Backlight compensation to 0 to avoid artificial light adjustments on diffrent parts of the picture.
    subprocess.run(["v4l2-ctl", "--device=" + device, "--set-ctrl", "backlight_compensation=0"], check=True)
def set_camera_controls () :
    # Auto exposure to manual mode (1) to be able to tune manually the exposure time
    subprocess.run(["v4l2-ctl", "--device=" + device, "--set-ctrl", "auto_exposure=1"], check=True)
    # Exposure time to maximum for better images in low-light condition
    subprocess.run(["v4l2-ctl", "--device=" + device, "--set-ctrl", "exposure_time_absolute=5000"], check=True)
    # Dynamic framerate to false to increse reproducibility
    subprocess.run(["v4l2-ctl", "--device=" + device, "--set-ctrl", "exposure_dynamic_framerate=0"], check=True)
    # Auto exposure to aperture_priority mode (2)? for the camera to adapt the ISO by itself
    subprocess.run(["v4l2-ctl", "--device=" + device, "--set-ctrl", "auto_exposure=3"], check=True)




# Open the webcam using open cv
cap = cv2.VideoCapture('/dev/video4')
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    sys.exit()
set_camera_user_settings()
set_camera_controls()


# Make a list a frame that will be averaged to a png
list_frame = []
def average_frames (list_of_frames) : # compute the average of sevral frames
    accumulator = np.zeros_like(list_frame[0], dtype=np.float32)
    for fram in list_of_frames:
        accumulator += fram.astype(np.float32)
    average_fram = accumulator / len(list_frame)
    # Convert the average frame back to the original dtype (e.g., uint8)
    average_fram = average_fram.astype(np.uint8)
    return (average_fram)

try:
    print ('Beginning to stream')
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:   # If image could not be captured
            print("Error: Could not read frame.")
            break
        # Shall we record smth and what ?
        previous_recording = recording
        (channel, recording) = channel_to_record()
        # depending on if we should record or not
        match (previous_recording, recording) :
            ## beggining to record
            case (False, True) :
                list_frame = []
            ## recoding in progress
            case (True, True) :
                #process.stdin.write(frame.tobytes()) # save video
                list_frame.append(frame)
            ## stop recording and save picture
            case (True, False) :
                average_frame = average_frames(list_frame)
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                output_name = f"output_{timestamp}.png"
                cv2.imwrite(output_path + '/' + channel_names[channel - 1]+ '/' + output_name, average_frame)
                print( "Image Captured  " + channel_names[channel - 1] + f" {timestamp}" )

        # Display the frame for on time tracking
        cv2.imshow('Webcam Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("Streaming stopped")

# When everything done, release the capture and close FFmpeg
cap.release()
cv2.destroyAllWindows()
#process.stdin.close()
#process.wait()
#print(f"Video saved as {output_filename}")
