# Standard imports
import cv2
from cv2 import SimpleBlobDetector_create, SimpleBlobDetector_Params
import numpy as np
import os
 
allKeyPoints = []
allCircles = []

# Read image
def blobber(filename):
    #create a gray scale version of the image, first
    im_gray = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

    #Use the Otsu thresholding method to automatically B/W contrast the images
    (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, 
                                    cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    blur = cv2.medianBlur(im_bw,15)

    detector = cv2.SimpleBlobDetector_create()

    params = cv2.SimpleBlobDetector_Params()

    # Filter by Color
    params.filterByColor = True
    params.blobColor = 0

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 2000 #magic number, but it works

    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.1

    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.1

    #Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.1

    # Create a detector with the parameters
    ver = (cv2.__version__).split('.')
    if int(ver[0]) < 3 :
        detector = cv2.SimpleBlobDetector(params)
    else : 
        detector = cv2.SimpleBlobDetector_create(params)

    # Detect blobs.
    keypoints = detector.detect(blur)

    allKeyPoints.append(keypoints)
    #print(allKeyPoints)
     
    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures circle size = blob size
    im_with_keypoints = cv2.drawKeypoints(blur,keypoints,np.array([]),(0,0,255),
                        cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
     
    # Show keypoints
    cv2.imshow("Keypoints", im_with_keypoints)
    cv2.waitKey(1)
    cv2.destroyAllWindows()

 def flatten(L = None):
    if L == None: L = allKeyPoints
    if L == []:
        return L
    if isinstance(L[0], list):
        return flatten(L[0]) + flatten(L[1:])
    return L[:1] + flatten(L[1:])

def getCoordinates():
    L = flatten()
    for i in L:
        if i == None:
            pass
        else:
            x,y = i.pt
            diameter = i.size
            allCircles.append([x,y,diameter])
    return allCircles

def detector(source):
    images = []
    for item in os.listdir(source):
        if '.jpg' in item: 
            filename = (os.path.join(source, item))
            allKeyPoints.append(blobber(filename))
    allCircles = getCoordinates()
    return allCircles