# USAGE
# python detect_barcode.py --image images/barcode_01.jpg

# import the necessary packages
import numpy as np
import argparse
import cv2

# # construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required = True, help = "path to the image file")
# args = vars(ap.parse_args())

# load the image and convert it to grayscale




path ="f:\\008.png"

image = cv2.imread(path)
image1 = cv2.imread(path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#cv2.imshow('grey', gray)
# compute the Scharr gradient magnitude representation of the images
# in both the x and y direction
gradX = cv2.Sobel(gray, ddepth = cv2.CV_64F, dx = 1, dy = 0, ksize = 3)
gradY = cv2.Sobel(gray, ddepth = cv2.CV_64F, dx = 0, dy = 1, ksize = 3)

# subtract the y-gradient from the x-gradient
gradient = cv2.subtract(gradX, gradY)
gradient = cv2.convertScaleAbs(gradient)


# blur and threshold the image
blurred = cv2.blur(gradient, (9,9))
#cv2.imshow('blurred', blurred)
(_, thresh) = cv2.threshold(blurred, 100, 100, cv2.THRESH_BINARY)
#cv2.imshow('thresh', thresh)

# construct a closing kernel and apply it to the thresholded image
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
#cv2.imshow('closed', closed)
# perform a series of erosions and dilations
closed = cv2.erode(closed, None, iterations = 4)
#cv2.imshow('closed1', closed)
closed = cv2.dilate(closed, None, iterations = 4)
#cv2.imshow('closed2', closed)
# find the contours in the thresholded image, then sort the contours
# by their area, keeping only the largest one
(_,cnts,_) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]

# compute the rotated bounding box of the largest contour
rect = cv2.minAreaRect(c)
box = np.int0(cv2.boxPoints(rect))

# draw a bounding box arounded the detected barcode and display the
# image
#cnt = max(cnts, key = lambda x: cv2.contourArea(x))
cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
cv2.imshow("QR", image)
cv2.imshow("QR1", image1)
cv2.waitKey()