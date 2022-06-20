# Librerias para la pantalla Oled
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
import socket
from PIL import ImageFont, ImageDraw, Image

#Para la pantalla
serial = i2c(port=1, address=0x3c)
#device = ssd1306(serial, rotate=0)
device = sh1106(serial, width=128, height=64, rotate=0)
#device.capabilities(width=128, height=64, rotate=0)
print("size: " , device.bounding_box)
device.clear()

with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
    #font = ImageFont.load_default(size=12)
    #font = ImageFont.truetype(, size=12)
        draw.text((30, 20), "Código IoT", fill="white")
        draw.text((10, 30),"Hola mundo", fill="white")

