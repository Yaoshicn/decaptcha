__author__ = 'Yaoshi'
from PIL import Image

def openImg():
    im = Image.open('1.png')
    im.show()

openImg()
