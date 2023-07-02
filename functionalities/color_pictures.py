from deoldify.visualize import get_image_colorizer

# Load the black and white image
bw_image_path = 'image.jpg'

# Colorize the image using DeOldify
colorizer = get_image_colorizer(artistic=True)
colorized_image = colorizer.get_transformed_image(bw_image_path)

# Display the colorized image
colorized_image.show()
