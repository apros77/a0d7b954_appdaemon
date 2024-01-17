# import the necessary packages
import cv2
import numpy as np
import os
import pathlib

# set the template matching and
# non-maximum suppression thresholds
thresh = 0.5
nms_thresh = 0.7

# load the main image and the template image
image = cv2.imread("/config/ssocr-SevenSegment_OCR_c1c_f32216776.png")
template = cv2.imread("/config/www/auer/target2.png")
# make a copy of the image
image_copy = image.copy()

# convert the images to grayscale
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

# get the width and height of the template image
template_h, template_w = template.shape[:-1]

# perform template matching using the normalized cross-correlation method
result = cv2.matchTemplate(image_gray, template_gray, cv2.TM_CCOEFF_NORMED)

# get the coordinates of the matches that are above the threshold
y_coords, x_coords = np.where(result >= thresh)

print("Number of matches found:", len(x_coords))

# loop over the coordinates and draw a rectangle around the matches
for x, y in zip(x_coords, y_coords):
    cv2.rectangle(image_copy, (x, y), (x + template_w,
                  y + template_h), (0, 255, 0), 2)

# show the images
#cv2.imshow("Template", template)
#cv2.imshow("Multi-Template Matching", image_copy)

######################################################################
# Apply Non-Maximum Suppression
######################################################################

# create a list of bounding boxes
boxes = np.array([[x, y, x + template_w, y + template_h]
                 for (x, y) in zip(x_coords, y_coords)])

# apply non-maximum suppression to the bounding boxes
indices = cv2.dnn.NMSBoxes(
    boxes, result[y_coords, x_coords], thresh, nms_thresh)

print("Number of matches found after NMS:", len(indices))

for i in indices:
    (x, y, w, h) = boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3]
    cv2.rectangle(image, (x, y), (w, h), (0, 255, 0), 2)
   # print("x", x)

cv2.imwrite("/config/www/auer/image2.png", image)
#image.save("/config/www/auer/image2.png")
#cv2.waitKey(0)
