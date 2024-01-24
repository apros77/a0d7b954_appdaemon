import appdaemon.plugins.hass.hassapi as hass
from matplotlib import pyplot as plt
import cv2
from datetime import datetime, time, timedelta
import os
import pathlib
img = cv2.imread("/config/ssocr-SevenSegment_OCR_c1c_f32216776.png")
plt.imshow(img)

#
# Hellow World App
#
# Args:
#

class HelloWorld(hass.Hass):

  def initialize(self):
     self.run_every(self.lcd_ha, "now", 1 * 360)
     self.log("Hello from AppDaemon")
     self.log("You are now ready to run Apps!")
     self.log("*****  " + dirpath)
     self.log("@@@@. " + filepath)
     