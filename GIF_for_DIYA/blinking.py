#!/usr/bin/env python3

from PIL import Image
import imageio
import math
from functools import reduce

# Define the pixel colors
intensity = 100
red = (intensity, 0, 0)
black = (0,0,0)

# Define image
red_image = (Image.new('RGB', (1, 1), red))
black_image = (Image.new('RGB', (1, 1), black))

# Define duration
frame_duration = 60.

# Define the  list of frames
frames = [black_image, red_image]

# create the GIF
imageio.mimsave('blinking.gif', frames, fps= 1/frame_duration)
