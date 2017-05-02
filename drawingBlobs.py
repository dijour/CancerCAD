#High level structure from Open CV Tutorials and:
#http://stackoverflow.com/questions/37099262/drawing-
#filled-polygon-using-mouse-events-in-open-cv-using-python

import numpy as np
import cv2
import os
import tkinter
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfile
import copy
import cancerCAD

################################################################################

FINAL_LINE_COLOR = (0, 255, 0) #set the color of the final line
WORKING_LINE_COLOR = (0, 0, 255) #set the color of the working line

################################################################################
class PolygonDrawer(object):
    def __init__(self, source):
        self.window_name = "Blob Drawer" # Name for our window
        self.allDone = False # Flag signaling all voxels are done
        self.runDone = False # Flag signaling one voxel is done
        self.current = (0, 0) # Current position, draw the line-in-progress
        self.points = [] # List of points defining our polygon
        self.allPoints = [] #List of 2d Lists of all polygons
        self.filenames = []
        self.source = source


    def contrastFiles(self, filename): 
        im_gray = cv2.imread(filename, cv2.IMREAD_GRAYSCALE) #convert to g-scale

        thresh = 90 #set up threshold (this just happened to work)
        im_bw = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]

        cv2.imshow('im_bw',im_bw) #show the contrasted image

    def loopThroughFiles(self):
        images = []
        for item in os.listdir(self.source):
            if '.jpg' in item: 
                filename = (os.path.join(self.source, item))
                self.filenames.append(filename)

    def on_mouse(self, event, x, y, buttons, user_param):
        # Mouse callback that gets called for every mouse event

        if self.allDone: # Nothing more to do
            return

        if event == cv2.EVENT_MOUSEMOVE:
            # Draw the line in real time, so update current mouse position
            self.current = (x, y)
        elif event == cv2.EVENT_LBUTTONDOWN:
            # Left click means adding a point at current position to the list 
            print("Adding point #%d with position(%d,%d)" % (len(self.points), 
                                                                        x, y))
            self.points.append((x, y))

    def run(self):
        # Create working window and set a mouse callback to handle events
        self.loopThroughFiles()
        cv2.namedWindow(self.window_name, flags=cv2.WINDOW_AUTOSIZE)
        cv2.waitKey(1)
        cv2.setMouseCallback(self.window_name, self.on_mouse)

        for filename in self.filenames:
            self.runDone = False
            self.points = []
            self.undoList = []
            while(not self.runDone):
                # This is our drawing loop, we just continuously draw new images
                # and show them in the named window
                canvas = cv2.imread(filename)
                font = cv2.FONT_HERSHEY_SIMPLEX #set font
                text1 = "1. In at least 2 MRI slices, click around the tumor"
                text2 = " to extract points"
                text3 = text1+text2
                cv2.putText(canvas,text3,
                                    (25,25),font,.75,(255,0,255),2,cv2.LINE_AA)
                
                cv2.putText(canvas,"2. Hit the (esc) key when done with a slice"
                                    ,(25,60),font,.75,(255,0,255),2,cv2.LINE_AA)

                cv2.putText(canvas,"3. Hit 'u' to undo a point selection"
                                    ,(25,95),font,.75,(255,0,255),2,cv2.LINE_AA)

                cv2.putText(canvas,"4. Hit 'r' to redo a point selection"
                                   ,(25,130),font,.75,(255,0,255),2,cv2.LINE_AA)

                if (len(self.points) > 0):
                    # Draw all the current polygon segments
                    cv2.polylines(canvas, np.array([self.points]), False, 
                                        FINAL_LINE_COLOR, 1)
                    # And  also show what the current segment would look like
                    cv2.line(canvas, self.points[-1], self.current, 
                                        WORKING_LINE_COLOR)
                # Update the window
                cv2.imshow(self.window_name, canvas)
                
                cv2.setMouseCallback(self.window_name, self.on_mouse)

                # Wait 50ms before next iteration 
                if cv2.waitKey(50) == 27: # ESC hit == 27 
                    self.runDone = True
                    polygon = copy.deepcopy(self.points)
                    self.allPoints.append(polygon)
                if cv2.waitKey(50) == ord('u'):
                   print("Pressed undo")
                   if self.points == []:
                       pass
                   else: self.undoList.append(self.points.pop())
                elif cv2.waitKey(50) == ord('r'):
                    print("Pressed redo")
                    if self.undoList == []:
                        pass
                    else: self.points.append(self.undoList.pop())

            # User finised entering the points --> make the final drawing
            canvas = cv2.imread(filename)
            # of a filled polygon
            if (len(self.points) > 0):
                cv2.fillPoly(canvas, np.array([self.points]), FINAL_LINE_COLOR)
            # show the Polgyon
            cv2.imshow(self.window_name, canvas)
            # reset points list
            # Waiting for the user to press any key
            cv2.waitKey()

            cv2.destroyWindow(self.window_name)
        self.allDone = True
        return canvas

################################################################################

def start(source):
    pd = PolygonDrawer(source)
    image = pd.run()
    #cv2.imwrite("polygon.png", image)
    #print("All Polygons = %s" % pd.allPoints)
    #cancerCAD.cancerCAD(pd.allPoints,pd.sliceThickness)
    return pd.allPoints

#start(r"C:\Users\ddijo\Google Drive\Carnegie Mellon First Year 2016-2017\2nd Semester\15-112\Term Project\TP Proposal\BigFlairJPG")