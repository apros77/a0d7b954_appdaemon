# import the necessary packages
import time
import cv2
import numpy as np
import os
import pathlib

def run_script():
   # set the template matching and
   # non-maximum suppression thresholds
   thresh = 0.37
   nms_thresh = 0.93

   # load the main image and the template image
   image = cv2.imread("/config/ssocr-SevenSegment_OCR_c1c_f32216776.png")
   template = cv2.imread("/config/www/auer/target5.png")
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

   minX = 1000
   maxX = 0
   minY = 1000
   maxY = 0
   xc = 0
   yc = 0
   for i in indices:
    (x, y, w, h) = boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3]
    cv2.rectangle(image, (x, y), (w, h), (0, 255, 0), 2)
    print("x", x)
    print("y", y)
    xc = int(x+(template_w/2))
    yc = int(y+(template_h/2))
    cv2.circle(image,(xc,yc), 10,(0,0,255),-1)
    if xc < minX:
        minX = xc
    if xc > maxX:
        maxX = xc
    if yc < minY:
        minY = yc
    if yc > maxY:
        maxY = yc

   print("minX", minX)
   print("maxX", maxX)
   print("minY", minY)
   print("maxY", maxY)
   finalImage = image[minY:maxY,minX:maxX]
   cv2.imwrite("/config/www/auer/image2.png", image)
   cv2.imwrite("/config/www/auer/imagecrop2.png", finalImage)

   # Pixel values in original image
   red_point = [147,150]
   green_point = [256,182]
   black_point = [119,453]
   blue_point = [231,460]

   # Create point matrix
   point_matrix = np.float32([red_point,green_point,black_point, blue_point])

   # Output image size
   width, height = 250,350

   # Desired points value in output images
   converted_red_pixel_value = [0,0]
   converted_green_pixel_value = [width,0]
   converted_black_pixel_value = [0,height]
   converted_blue_pixel_value = [width,height]

   # Convert points
   converted_points = np.float32([converted_red_pixel_value,converted_green_pixel_value,
                                  converted_black_pixel_value,converted_blue_pixel_value])

#    perspective transform
   perspective_transform = cv2.getPerspectiveTransform(point_matrix,converted_points)
   img_Output = cv2.warpPerspective(finalImage,perspective_transform,(width,height))

   cv2.imwrite("/config/www/auer/imagetransform2.png", img_Output)

def main():
   while True:
      run_script()
      time.sleep(10)  # Sleep for 5 minutes (300 seconds)

if __name__ == "__main__":
    main()