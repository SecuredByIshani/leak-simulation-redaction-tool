from PIL import Image
import piexif

img = Image.open("sample.jpg")  # Make sure this is a JPEG with EXIF data

# Check if image has EXIF data
if "exif" in img.info:
    exif_data = piexif.load(img.info["exif"])
    print(exif_data)
else:
    print("No EXIF data found in this image.")
