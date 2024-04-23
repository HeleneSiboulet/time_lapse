#!/usr/bin/env python3

from PIL import Image
import imageio
import math
from functools import reduce

# Define the pixel colors
intensity = 255
intensity = [255, 150, 100, 70, 50, 30, 10, 5, 3]
black = (0,0,0)

# Define image
frames = []
for i in intensity :
    image = (Image.new('RGB', (1,1), (i,0,0)))
    frames.append(image)
black_image = (Image.new('RGB', (1, 1), black))

# Define duration
frame_duration = 40.

# create the GIF
imageio.mimsave('blinking.gif', frames, fps= 1/frame_duration)
