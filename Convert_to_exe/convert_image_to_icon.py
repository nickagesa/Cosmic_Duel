# Convert a PNG image to ICO format using Pillow
# Ensure you have Pillow installed: pip install Pillow

from PIL import Image
img = Image.open("icon.png")  # Replace with your original image
img.save("icon.ico", format="ICO")