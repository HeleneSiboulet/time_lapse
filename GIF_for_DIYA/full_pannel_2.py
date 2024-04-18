from PIL import Image

# Define the green pixel color
pixel_color = (30, 0, 0)

# Create a new 1x1 pixel image
image = Image.new('RGB', (64, 64), pixel_color)

# Save the image
image.save('6464_red_pixel_30.png')
