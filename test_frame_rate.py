#!/usr/bin/env python3

import cv2

# Initialize video capture
cap = cv2.VideoCapture('/dev/video4')

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video capture")
    cap.release()
    exit()

# Get the frame rate
fps = cap.get(cv2.CAP_PROP_FPS)
print("Frame Rate:", fps)

# When everything done, release the capture
cap.release()
