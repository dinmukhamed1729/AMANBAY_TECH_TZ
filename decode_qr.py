from PIL import Image
from pyzbar.pyzbar import decode

image = Image.open("qr.png")
decoded_objects = decode(image)

for obj in decoded_objects:
    print("Data:", obj.data.decode("utf-8"))
