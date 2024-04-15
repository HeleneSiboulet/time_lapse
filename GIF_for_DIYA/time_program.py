from PIL import Image
import imageio
import math
from functools import reduce

# Define the pixel colors
red = (30, 0, 0)
green = (0, 30, 0)
blue = (0, 0, 30)
black = (0, 0, 0)
color_list = [ red, green, blue ]
color_list.append( (0, 0, 0) )

# Define the duration of each color in seconds
cycle_duration = 60
red_duration = 15
green_duration = 15
blue_duration = 15
duration_list = [ red_duration, green_duration, blue_duration ]
pause_duration = cycle_duration - sum(duration_list)
assert(pause_duration >= 0)
duration_list.append(pause_duration)
frame_duration = reduce(math.gcd, duration_list)

# Create images for each color
n_colors = len (color_list)
assert (len(duration_list) == n_colors)
frame_list = []
for color in color_list :
    frame_list.append(Image.new('RGB', (1, 1), color))

# Define the  list of frames
frames = []
for frame_index in range( int(cycle_duration / frame_duration) ) :
    for color_index in range(n_colors) :
        for frame_j in range( int(duration_list[color_index] / frame_duration)):
            frames.append(frame_list[color_index])

# create the GIF
imageio.mimsave('light_exitation.gif', frames, fps= 1/frame_duration)
