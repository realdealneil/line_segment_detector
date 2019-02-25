#!/usr/bin/env python3

# Initially grabbed from publically available tutorial found here:
# https://www.pyimagesearch.com/2016/03/28/measuring-size-of-objects-in-an-image-with-opencv/

## Import the necessary packages:
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

#def find_marker(image):
#	# convert the image to grayscale, blur, and detect edges (canny)
#	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#	gray = cv2.GaussianBlur(gray, (5,5), 0)
#	edged = cv2.Canny(gray, 35, 125);

def midpoint(ptA, ptB): 
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)
    
# contrcut the argument parse and parse args:
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input img")
ap.add_argument("-w", "--width", type=float, required=True, help="width of object to measure")
args = vars(ap.parse_args())

# load image, convert to gray, blur:
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7,7), 0)

# Perform edge detection, then perform a dilation + erosion:
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

# Try finding lines use OpenCV's line segment detector:
lsd = cv2.createLineSegmentDetector(0)

#cv2.createLineSegmentDetector.detect(_image[, _lines[, width[, prec[, nfa]]]]) → _lines, width, prec, nfa
lines = lsd.detect(gray)[0]

lineImg = lsd.drawSegments(image, lines)

cv2.imshow("Line Segments", lineImg)
cv2.waitKey(0)

drawImg = cv2.cvtColor(edged, cv2.COLOR_GRAY2BGR);

# Find Contours in the edge image:
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
print("Number of contours found: ", len(cnts) )

# Sort the contours from left to right and initialize the 'pixels per meter' calibration
(cnts, _) = contours.sort_contours(cnts)
pixelsPerMeter = None

# Loop over the contours individually:
for c in cnts:
    # If the contour is not very big, ignore it:
    if cv2.contourArea(c) < 100:
        continue
    
    # Compute the rotated bounding box of the contour:
    orig = drawImg.copy()
    box = cv2.minAreaRect(c)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    
    # Order the points in the contour such that they appear in to-left, top-right, bottom-right,
    # bottom-left order.  Then, draw the outline of the rotated bounding box:
    box = perspective.order_points(box)
    cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
    
    # loop over the original points and draw them:
    for (x,y) in box:
        cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)
        
    # unpack the ordered bounding box, then compute the midpoint
    # between top-left and top-right coordinates, followed by
    # the midpoint between bottom-left and bottom-right coordinates:
    (tl, tr, br, bl) = box
    (tltrX, tltrY) = midpoint(tl, tr)
    (blbrX, blbrY) = midpoint(bl, br)
    
    # Compute the remaining midpoints:
    (tlblX, tlblY) = midpoint(tl, bl)
    (trbrX, trbrY) = midpoint(tr, br)
    
    # draw the midpoints on the image:
    cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255,0,0), -1)
    cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255,0,0), -1)
    cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255,0,0), -1)
    cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255,0,0), -1)   
        
    

    cv2.imshow("Image", orig);
    #cv2.imshow("Edges", edged);
    cv2.waitKey(0)
	

	
