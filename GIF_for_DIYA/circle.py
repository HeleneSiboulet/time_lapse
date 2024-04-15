#!/usr/bin/env python3

from PIL import Image, ImageDraw

# Create a new image with black background
img_size = (64, 64)
background_color = (0, 0, 0)
circle_color = (0, 255, 0)
circle_diameter = 30
circle_radius = circle_diameter // 2

image = Image.new('RGB', img_size, background_color)
draw = ImageDraw.Draw(image)

# Calculate the position of the circle
circle_x = (img_size[0] - circle_diameter) // 2
circle_y = (img_size[1] - circle_diameter) // 2

# Draw the circle
draw.ellipse((circle_x, circle_y, circle_x + circle_diameter, circle_y + circle_diameter), fill=circle_color)

# Save the image
image.save('green_circle.png')
