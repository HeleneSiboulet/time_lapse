import cv2
import subprocess
import sys

# Set up the FFmpeg command
ffmpeg = 'ffmpeg'
output_filename = 'output.mp4'
ffmpeg_command = [
    ffmpeg,
    '-y',  # Overwrite output file if it exists
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

# Open the FFmpeg process
process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

# Open the webcam
cap = cv2.VideoCapture('/dev/video4')
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    sys.exit()

try:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Write the frame to the FFmpeg process
        process.stdin.write(frame.tobytes())

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
