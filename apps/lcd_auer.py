import appdaemon.plugins.hass.hassapi as hass

import cv2
import rect
import numpy as np
import os
import pathlib

from datetime import datetime, time, timedelta

##############################################
# Snap_lcd_auer App
#
# Args:
#############################################

class SnapLcdAuer(hass.Hass):
  def initialize(self):
     self.run_every(self.lcd_ha, "now", 10 * 60)
     self.log("$$$$$$$$$$$$$$$$Hello from AppDaemon")
     self.log("$$$$$$$$$$$$$$$$You are now ready to run Apps!")
     self.log("*****  " + dirpath)
     self.log("@@@@. " + filepath)
    
##############################################



def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    
    # zainicjuj listę współrzędnych, które zostaną uporządkowane
    # taki, że pierwszy wpis na liście znajduje się w lewym górnym rogu,
    # drugi wpis to prawy górny róg, trzeci to the
    # prawy dolny róg, a czwarty lewy dolny róg
    rect = np.zeros((4, 2), dtype = "float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    
    # lewy górny punkt będzie miał najmniejszą sumę, podczas gdy
    # prawy dolny punkt będzie miał największą sumę
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right poi
    # nt will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    
    # teraz oblicz różnicę między punktami, the
    # prawy górny punkt
    # nt będzie miał najmniejszą różnicę,
    # podczas gdy lewy dolny róg będzie miał największą różnicę
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    # zwróć zamówione współrzędne
    return rect

def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    # uzyskaj spójną kolejność punktów i rozpakuj je
    # indywidualnie
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    
    # obliczyć szerokość nowego obrazu, który będzie
    # maksymalna odległość między dolnym prawym a dolnym lewym
    # Współrzędne x lub współrzędne x-prawy górny i lewy górny róg
    
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    
    # obliczyć wysokość nowego obrazu, który będzie
    # maksymalna odległość między górnym prawym a dolnym prawym
    # Współrzędne y lub współrzędne y lewy górny i lewy dolny róg
    
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    
    # teraz, gdy mamy wymiary nowego obrazu, skonstruuj
    # zestaw punktów docelowych, aby uzyskać „widok z lotu ptaka”,
    # (czyli widok z góry na dół) obrazu, ponownie określając punkty
    # w lewym górnym rogu, prawym górnym rogu, prawym dolnym rogu i lewym dolnym rogu
    # zamówienie
    
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")

    # compute the perspective transform matrix and then apply it
    # obliczyć macierz transformacji perspektywy, a następnie zastosować ją
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # return the warped image
    # zwróć wypaczony obraz
    return warped

def lcd_ha():    
    # add image here.
    # We can also use laptop's webcam if the resolution is good enough to capture
    # readable document content
    filepath = os.path.realpath(__file__)
    dirpath = os.getcwd()
    open("/config/www/auer/readme_lcd.txt", "w")

    image = cv2.imread("/config/www/auer/lcd_0.png")
    #   resize image so it can be processed
    # choose optimal dimensions such that important content is not lost
    #image = cv2.resize(image, (1500, 880))

# creating copy of original image
    orig = image.copy()

# convert to grayscale and blur to smooth
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#blurred = cv2.medianBlur(gray, 5)

# apply Canny Edge Detection
    edged = cv2.Canny(blurred, 0, 50)
    orig_edged = edged.copy()

# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
    (contours, _) = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    x,y,w,h = cv2.boundingRect(contours[0])
    cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),0)
    con = np.zeros_like(image)
    for d in contours:
        # Approximate the contour.
        epsilon = 0.02 * cv2.arcLength(d, True)
        corners = cv2.approxPolyDP(d, epsilon, True)
        # If our approximated contour has four points
    
        if len(corners) == 4:
            break
        
        
    img_crop = four_point_transform(orig, corners.reshape(4, 2))

    cv2.imwrite("/config/www/auer/cropped.png", img_crop)

