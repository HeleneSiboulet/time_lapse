from PIL import Image

# Define the green pixel color
pixel_color = (50, 0, 0)

# Create a new 1x1 pixel image
image = Image.new('RGB', (64, 64), (0,0,0))
# Change the color of the pixel at (32, 32) to red
image.putpixel((32, 32), pixel_color)

# Save the image
image.save('one_red_pixel.png')
