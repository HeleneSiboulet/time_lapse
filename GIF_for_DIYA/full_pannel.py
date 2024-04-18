from PIL import Image

# Define the green pixel color
pixel_color = (5, 0, 0)

# Create a new 1x1 pixel image
image = Image.new('RGB', (1, 1), pixel_color)

# Save the image
image.save('red_pixel_5.png')
