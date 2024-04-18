from PIL import Image

# Define the green pixel color
pixel_color = (50, 0, 0)
black = (0, 0, 0)

# Create a new 1x1 pixel image
image = Image.new('RGB', (3, 3), pixel_color)
# Change the color of the pixel at (32, 32) to red
image.putpixel((0, 1), black)
image.putpixel((1, 1), black)
image.putpixel((2, 1), black)

# Save the image
image.save('red_stripes.png')
