import cv2
import subprocess
import sys
import time
from datetime import datetime
import numpy as np
import os

# Choose output path
output_path = '../pictures/stream'
if not os.path.exists(output_path):
    os.makedirs(output_path)
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
process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

# Open the webcam using open cv
cap = cv2.VideoCapture('/dev/video4')
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    sys.exit()

# Define the function for when to record
cycle_duration = 5
record_duration = 2
start = time.time()
recording_in_progress = False
def should_record() :
    now = time.time() - start
    return ((now % cycle_duration) <= record_duration)

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
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Write the frame to the FFmpeg process
        if (should_record()) :
            if  ( not recording_in_progress) :          # Begin to record
                recording_in_progress = True
                list_frame = []
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

            else :                                      # Recording in progress
                process.stdin.write(frame.tobytes())
                list_frame.append(frame)

        else :
            if (recording_in_progress) :                # Stop recording
                recording_in_progress = False
                average_frame = average_frames(list_frame)
                output_name = f"output_{timestamp}.png"
                cv2.imwrite(output_path + '/' + output_name, average_frame)
                print( "Image Captured  " + f"{timestamp}" )
            else :                                      # Not recording
                continue

        # Display the frame (optional)
        cv2.imshow('Webcam Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("Streaming stopped")

# When everything done, release the capture and close FFmpeg
cap.release()
cv2.destroyAllWindows()
process.stdin.close()
process.wait()

print(f"Video saved as {output_filename}")
