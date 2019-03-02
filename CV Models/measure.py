#importing the necessary packages
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

def midpoint(ptA,ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)
#parsing of arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help="path to input image")
ap.add_argument("-w", "--width", type=float, required=True, help="width of the object")
args = vars(ap.parse_args())
#Read the image and preprocessing of the image
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7,7), 0)

#Edge Detection performed using edge canny algorithm
#This part can also be carried out using auto edge canny algorithm
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations = 1)
edged = cv2.erode(edged, None, iterations = 1)

#Find contours in the edge map
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
(cnts, _) = contours.sort_contours(cnts)
pixelsPerMetric = None

#Go check each contour
for c in cnts:
    if cv2.contourArea(c) < 10000:
        continue
    orig = image.copy()
    box = cv2.minAreaRect(c)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    box = perspective.order_points(box)
    cv2.drawContours(orig, [box.astype("int")], -1, (0,255,255), 2)
#Loop over the original points and draw them
for (x,y) in box: 
    cv2.circle(orig,(int(x),int(y)), 5, (0,0,255), -1)
#The midpoint is calculated followed by computing the midpoint between top-left and top-right coordinates
(tl, tr, br, bl) = box
(tltrX, tltrY) = midpoint(tl,tr)
(blbrX, blbrY) = midpoint(bl,br)
(tlblX,tlblY) = midpoint(tl,bl)
(trbrX, trbrY) = midpoint(tr,br)

#Draw the midpoints on the image
cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

#intersect the lines between midpoints
cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
		(255,255, 255), 2)
cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
		(255, 255, 255), 2)
#compute the Euclidean distance between midpoints
dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
#We initialize the pixels per metric has not been established 
if pixelsPerMetric is None:
    pixelsPerMetric = dB / args['width']
dimA = dA / pixelsPerMetric
dimB = dB / pixelsPerMetric
#to compute the final object size
cv2.putText(orig, "{:.1f} feet".format(dimA*10),
		(int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (255, 0, 0), 2)
cv2.putText(orig, "{:.1f} feet".format(dimB),
		(int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (255, 0, 0), 2)
area = dimA*dimB
print(area*10)
 
# show the output image
cv2.imshow("Image", orig)
cv2.waitKey(0)


