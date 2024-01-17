#import appdaemon.plugins.hass.hassapi as hass
import cv2

import os
import pathlib
import time


class SingleDeformer:

    def getmesh(self, img):
        #Map a target rectangle onto a source quad
        return [(
                # target rectangle
                (0, 0, 730, 320),
                # corresponding source quadrilateral
                (50, 30, 10, 290, 715, 290, 670, 25)
                )]


filepath = os.path.realpath(__file__)
dirpath = os.getcwd()
open("/config/www/auer/readme.txt", "w")

from PIL import Image, ImageOps
from PIL import Image, ImageFilter
# im = Image.open("/config/autosnap.png") 


# for i in range(36):
im = Image.open("/config/ssocr-SevenSegment_OCR_c1c_f32216776.png")
   # im = im.rotate(i * 10)
   
left = 300
top = 180
right = 1030
bottom = 500
 
# Cropped image of above dimension
# (It will not change original image)
imcrop = im.crop((left, top, right, bottom))   
   
imcrop.save("/config/www/auer/lcd_crop_0.png")
edges = im.filter(ImageFilter.FIND_EDGES)

edges.save("/config/www/auer/lcd_edge_0.png")


result_image = ImageOps.deform(imcrop, SingleDeformer())
result_image.save("/config/www/auer/imageops-deform2.png")


#
# Hellow World App
#
# Args:
#

#class HelloWorld(hass.Hass):

 # def initialize(self):
  #   self.log("Hello from AppDaemon")
   #  self.log("You are now ready to run Apps!")
    # self.log("*****  " + dirpath)
     #self.log("@@@@. " + filepath)