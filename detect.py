import cv2
import numpy as np
import os
import math
import imutils

path = "f:\\008.png"
img = cv2.imread("f:\\008.png")
OUTPUT_DIR = 'f:\\digital'
num = 60
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
img = img[68:-50,30:-100]
grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#cv2.imshow('grey', grey)
converted = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#cv2.imshow('hsv', converted)
grey = cv2.bitwise_not(grey)
#cv2.imshow('1', grey)
value = (5,5)
kernel = np.ones((5,5),np.uint8)
blurred = cv2.GaussianBlur(grey, value, 0)
_, thresh1 = cv2.threshold(blurred,200, 255,
                           cv2.THRESH_BINARY)
#cv2.imshow('thresh1', thresh1)


#thresh1 = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
#thresh1 = cv2.erode(thresh1,kernel,iterations = 1)
thresh1 = cv2.dilate(thresh1,kernel,iterations = 1)
cv2.imshow('2', thresh1)
#thresh1 = cv2.dilate(thresh1,kernel,iterations = 1)
#cv2.imshow('3', thresh1)
#thresh1 = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
#cv2.imshow('4', thresh1)
image, contours, hierarchy = cv2.findContours(thresh1, \
               cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

cnt = max(contours, key = lambda x: cv2.contourArea(x))
rect = cv2.minAreaRect(cnt)
box = np.int0(cv2.boxPoints(rect))
x,y,w,h= box
print(box)
# draw a bounding box arounded the detected barcode and display the
# image
cv2.drawContours(img, [box], -1, (0, 0, 255), 2)
#digtals = img[y:y+h,x:x+w]
#cv2.imwrite(os.path.join(OUTPUT_DIR, str(num) + '.jpg'), digtals)

#cv2.drawContours(img, contours, -1, (0, 255, 0), 1)
#cv2.imshow('5', img)
count = 0
#contours = max(contours, key=lambda x: cv2.contourArea(x))
#print(contours)
#index = cv2.contourArea(contours)
#print(index)
cnts = sorted([(c, cv2.boundingRect(c)[0]) for c in contours], key = lambda x: x[1])
#print(cnts)
for (c, _) in cnts:

    #cnt = max(contours, key=lambda x: cv2.contourArea(x))
    if cv2.contourArea(c)>5000:
        print(cv2.contourArea(c))
        if count <1:
            (x, y, w, h) = cv2.boundingRect(c)
            #print(cv2.boundingRect(c))
            #cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),0)
            digtals = img[y:y+h,x:x+w]
            #cv2.imwrite(os.path.join(OUTPUT_DIR, str(num) + '.jpg'), digtals)
            count = count + 1
            num = num +1
        else:break
cv2.imshow('Thresholded', img)
cv2.imwrite(os.path.join(OUTPUT_DIR, str(num) + '.jpg'), img)
k = cv2.waitKey()
