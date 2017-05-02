'''
 ▄████▄  ▄▄▄      ███▄    █ ▄████▄ ▓█████ ██▀███      ▄████▄  ▄▄▄     ▓█████▄ 
▒██▀ ▀█ ▒████▄    ██ ▀█   █▒██▀ ▀█ ▓█   ▀▓██ ▒ ██▒   ▒██▀ ▀█ ▒████▄   ▒██▀ ██▌
▒▓█    ▄▒██  ▀█▄ ▓██  ▀█ ██▒▓█    ▄▒███  ▓██ ░▄█ ▒   ▒▓█    ▄▒██  ▀█▄ ░██   █▌
▒▓▓▄ ▄██░██▄▄▄▄██▓██▒  ▐▌██▒▓▓▄ ▄██▒▓█  ▄▒██▀▀█▄     ▒▓▓▄ ▄██░██▄▄▄▄██░▓█▄   ▌
▒ ▓███▀ ░▓█   ▓██▒██░   ▓██▒ ▓███▀ ░▒████░██▓ ▒██▒   ▒ ▓███▀ ░▓█   ▓██░▒████▓
 ░ ░▒ ▒  ░▒▒   ▓▒█░ ▒░   ▒ ▒░ ░▒ ▒  ░░ ▒░ ░ ▒▓ ░▒▓░   ░ ░▒ ▒  ░▒▒   ▓▒█░▒▒▓  ▒ 
  ░  ▒    ▒   ▒▒ ░ ░░   ░ ▒░ ░  ▒   ░ ░  ░ ░▒ ░ ▒░     ░  ▒    ▒   ▒▒ ░░ ▒  ▒ 
░         ░   ▒     ░   ░ ░░          ░    ░░   ░    ░         ░   ▒   ░ ░  ░ 
░ ░           ░  ░        ░░ ░        ░  ░  ░        ░ ░           ░  ░  ░    
░                          ░                         ░                 ░       
A 15-112 Term Project
Author: Dean Dijour
Mentor: Lukas Peraza
'''

# The code for changing tkinter pages was derived from: 
    #stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/   

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, \
                            NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.tri as mtri
import tkinter.filedialog
from PIL import Image, ImageTk
from stl import mesh
from scipy.spatial import Delaunay
from tkinter import *

#Import python files made for 15-112 Term Project:
import drawingBlobs
import tumorDetector
import autoCAD

LARGE_FONT= ("Verdana", 12) #specify global fonts
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)


class CancerCAD(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Cancer CAD")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage,PageOne,PageTwo,PageThree,PageFour, PageFive ):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky ="nsew")



            
        self.show_frame(StartPage) #iterate through pages to set them up

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self,parent)

        label = tk.Label(self, text="Cancer CAD", font=LARGE_FONT)
        
        label.pack(pady=40,padx=10)

        button1 = ttk.Button(self, text="Manually Identify Glioblastoma",
                            command=lambda: controller.show_frame(PageOne))

        button1.pack(pady=40,padx=10)

        button2 = ttk.Button(self, text="Intelligently Identify Glioblastoma",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack(pady=40,padx=10)

        button3 = ttk.Button(self, text="Help",
                            command=lambda: controller.show_frame(PageFive))
        button3.pack(pady=40,padx=10)


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        self.source = None
        self.allPolygons = None
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Manual Glioblastoma Imaging",
                                                font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text = "Browse for JPG Directory",
                                        command = self.findSource)

        button1.pack(pady=10,padx=10)

        button2 = ttk.Button(self, text = "Select Glioblastoma Slices",
                                        command = lambda: self.drawBlobs())

        button2.pack(pady=10,padx=10)

        button3 = ttk.Button(self, text = "Print Polygons", 
                                        command = self.printPolygons)

        button3.pack(pady=10,padx=10)

        button4 = ttk.Button(self, text="Manually Constructed 3D Mesh",
                            command=lambda: controller.show_frame(PageThree))
        
        button4.pack(pady=10,padx=10)


        button5 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button5.pack(pady=10,padx=10)

        
        label = tk.Label(self, 
            text="Instructions", 
            font=LARGE_FONT)

        label.pack(pady=10,padx=10)


        label = tk.Label(self, 
            text="1. Browse for JPGs from which you will select tumor slices", 
            font=NORM_FONT)

        label.pack(pady=10,padx=10)

        label = tk.Label(self, 
            text="2. Hit 'Select Glioblastoma Slices' & follow the steps", 
            font=NORM_FONT)

        label.pack(pady=10,padx=10)

        label = tk.Label(self, 
            text="3. Print the polygons to ensure they have been transferred", 
            font=NORM_FONT)

        label.pack(pady=10,padx=10)

        label = tk.Label(self, 
            text="4. Click 'Manually Constructed 3D Mesh' to generate a model", 
            font=NORM_FONT)

        label.pack(pady=5,padx=10)

    def printPolygons(self): #confirm all Polygons have been updated
        print(self.allPolygons)

    def findSource(self):
        self.source = tkinter.filedialog.askdirectory()
        if self.source != None:
            self.alert("Directory selected!")

    def drawBlobs(self):
        source = self.source
        if source == None:
            self.popupMsg("No directory was selected!")
        else: self.allPolygons = drawingBlobs.start(source)

    def getAllPolygons(self): #function called later so variable is not modified
        return self.allPolygons

    #from: https://pythonprogramming.net/tkinter-popup-message-window/
    def popupMsg(self, msg):
        popup = tk.Tk() 
        popup.wm_title("Error!")
        label = ttk.Label(popup, text=msg, font=NORM_FONT)
        label.pack(side="top", fill="x", padx=40, pady=10)
        B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
        B1.pack()
        popup.mainloop()      

    def alert(self, msg):
        popup = tk.Tk() 
        popup.wm_title("Cancer CAD")
        label = ttk.Label(popup, text=msg, font=NORM_FONT)
        label.pack(side="top", fill="x", padx=70, pady=10)
        B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
        B1.pack()
        popup.mainloop()     

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        self.source = None
        self.allPolygons = None
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Intelligently Identify Glioblastoma", 
                                            font=LARGE_FONT)
        
        label.pack(pady=10,padx=10)

        
        button1 = ttk.Button(self, text = "Browse for JPG Directory",
                                        command = self.findSource)

        button1.pack(pady=10,padx=10)

        button2 = ttk.Button(self, text = "Extract Glioblastoma Coordinates",
                                        command = self.extractCoordinates)        

        button2.pack(pady=10,padx=10)

        button3 = ttk.Button(self, text="Construct 3D Mesh",
                            command=lambda: controller.show_frame(PageFour))
        button3.pack(pady=10,padx=10)


        button4 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button4.pack(pady=10,padx=10)

        label = tk.Label(self, 
            text="Instructions", 
            font=LARGE_FONT)

        label.pack(pady=10,padx=10)

        label = tk.Label(self, 
            text="1. Browse for JPGs from which you will select tumor slices", 
            font=NORM_FONT)

        label.pack(pady=10,padx=10)

        label = tk.Label(self, 
            text="2. Hit 'Extract Glioblastoma Coordinates' & follow the steps", 
            font=NORM_FONT)

        label.pack(pady=10,padx=10)

        label = tk.Label(self, 
            text="3. Construct the 3D Mesh to go to the tumor modeling page", 
            font=NORM_FONT)

        label.pack(pady=5,padx=10)

    #from: https://pythonprogramming.net/tkinter-popup-message-window/
    def popupMsg(self, msg):
        popup = tk.Tk()
        popup.wm_title("Error!")
        label = ttk.Label(popup, text=msg, font=NORM_FONT)
        label.pack(side="top", fill="x", padx=40, pady=10)
        B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
        B1.pack()
        popup.mainloop()

    def extractCoordinates(self):
        source = self.source
        if source == None:
            self.popupMsg("No directory was selected!")
        else:
            pointSet = tumorDetector.detector(source)
            self.allPolygons = autoCAD.filterPointSet(pointSet)

    def findSource(self):
        self.source = tkinter.filedialog.askdirectory()
        if self.source != None:
            self.alert("Directory selected!")

    def getAllPolygons(self): #function called later so variable is not modified
        return self.allPolygons

    def alert(self, msg):
        popup = tk.Tk() 
        popup.wm_title("Cancer CAD")
        label = ttk.Label(popup, text=msg, font=NORM_FONT)
        label.pack(side="top", fill="x", padx=70, pady=10)
        B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
        B1.pack()
        popup.mainloop()    

class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        self.pageOne = controller.frames[PageOne]
        self.allPolygons = self.pageOne.getAllPolygons() #reference page one
        self.sliceThickness = 5 #set default slice thickness
        #create lists to store x,y,z and u,v values
        self.allPoints = []
        self.x = []
        self.y = []
        self.z = []

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Glioblastoma 3D Mesh Construction", 
                                    font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Update Polygon Mesh",
                            command=lambda:self.updatePolygons(parent,
                                                                    controller))

        button1.pack(pady=10,padx=10)

        button2 = ttk.Button(self, text="Create Triangularized Mesh",
                            command=self.createMesh)

        button2.pack(pady=10,padx=10)

        button3 = ttk.Button(self, text="Save as STL",
                            command = self.stlConverter)
        button3.pack(pady=10,padx=10)

        button4 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button4.pack(pady=10,padx=10)

        label = tk.Label(self, 
            text="Instructions", 
            font=LARGE_FONT)

        label.pack(pady=10,padx=10)

        label = tk.Label(self, 
            text="1. Update the polygon mesh by clicking 'Update Polygon Mesh'", 
            font=NORM_FONT)

        label.pack(pady=10,padx=10)

        label = tk.Label(self, 
            text="2. Construct a mesh by clicking 'Create Triangularized Mesh'", 
            font=NORM_FONT)

        label.pack(pady=10,padx=10)

        text1 = "3. Click 'Save as STL' to save the model as 3D printable STL" 
        text2 = " called 'manualCancerCAD.stl'"
        text3 = text1 + text2

        label = tk.Label(self, 
            text=text3, 
            font=NORM_FONT)

        label.pack(pady=0,padx=10)

    def updatePolygons(self,parent,controller):
        self.allPolygons = self.pageOne.getAllPolygons()
        if self.allPolygons == None:
            self.popupMsg("No coordinates were passed through!")

    #from: https://pythonprogramming.net/tkinter-popup-message-window/        
    def popupMsg(self, msg):
        popup = tk.Tk()
        popup.wm_title("Error!")
        label = ttk.Label(popup, text=msg, font=NORM_FONT)
        label.pack(side="top", fill="x", padx=40, pady=10)
        B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
        B1.pack()
        popup.mainloop() 

    def createMesh(self):
        allPolygons = self.allPolygons       
        u = []
        v = []

        if self.allPolygons == None:
            self.popupMsg("No coordinates were passed through!")

        fig = plt.figure()

        # Area of Polygon using Shoelace formula
        # http://en.wikipedia.org/wiki/Shoelace_formula
        # FB - 20120218
        # corners must be ordered in clockwise or counter-clockwise direction
        def polyArea(polygon):
            n = len(polygon) # of corners
            area = 0.0
            for i in range(n):
                j = (i + 1) % n
                area += polygon[i][0] * polygon[j][1]
                area -= polygon[j][0] * polygon[i][1]
            area = abs(area) / 2.0
            return area

        def cancerVolume(self): #stack areas to assemble volume
            volume = 0
            for i in allPolygons:
                volume += polyArea(i)
            return volume

        def center(pointList):
            L = len(pointList)
            xSum = 0
            ySum = 0
            for point in pointList:
                xSum += point[0]
                ySum += point[1]
            return (xSum/L,ySum/L) #returns average of all points = Barycenter
        
        def getAngle(x,y):
            epsilon = 0.001
            distance = ((x**2)+(y**2))**.5 #normalize first, from zero (origin)
            if distance < epsilon:
                return 0 #too close to center, don't want to use this point
            theta = np.arccos(x/distance) #need to multiply by SIGN of y
            if y<0: theta*= -1 #accounts for sin function, which is odd
            return theta

        for i in range(len(self.allPolygons)):
            if self.allPolygons[i] != []:
                cx,cy = center(self.allPolygons[i]) #find center of polygon
                for point in self.allPolygons[i]:
                    self.x.append(point[0]) #add coordinates to lists
                    self.y.append(point[1])
                    self.z.append(i*self.sliceThickness)
                    v.append(i*self.sliceThickness)
                    dx = point[0] - cx #find difference between centerX & pointX
                    dy = point[1] - cy #find difference between centerY & pointY
                    theta = getAngle(dx,dy)
                    u.append(theta)

        for i in range(len(self.x)):
            list = [self.x[i],self.y[i],self.z[i]]
            self.allPoints.append(list)

        print("all points =", self.allPoints)

        # Triangulate parameter space to determine the triangles
        tri = mtri.Triangulation(u, v)

        #pack canvas
        canvas = FigureCanvasTkAgg(fig, self)
        #canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        ax = fig.add_subplot(1, 1, 1, projection='3d')
        ax.plot_trisurf(self.x, self.y, self.z, triangles=tri.triangles, 
                                        cmap=plt.cm.Spectral)
        ax.set_xlim(min(self.x), max(self.x)) #set up x min and max
        ax.set_ylim(min(self.y), max(self.y)) #set up y min and max
        ax.set_zlim(min(self.z), max(self.z)) #set up z min and max
        Volume = cancerVolume(self.allPolygons) #print volume as label
        red_patch = mpatches.Patch(color='red', label='Volume = %s' % (Volume))
        plt.legend(handles=[red_patch])

        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, 
                                    fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()

    def getAllPoints(self): #function called later so variable is not modified
        return self.allPoints

    def stlConverter(self):
        if self.allPoints == []: 
            self.popupMsg("No coordinates were passed through!")
        else:
            # Define the vertices of the tumor
            vertices = np.array(self.allPoints)
            # Define the triangles composing the tumor
            tri = Delaunay(vertices)
            #tri.simplices returns list of all triangles
            faces = np.array(tri.simplices)

            # Create the mesh
            tumor = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
            for i, f in enumerate(faces):
                for j in range(3):
                    tumor.vectors[i][j] = vertices[f[j],:]

            # Write the mesh to file "cancerCAD.stl"
            tumor.save('manualCancerCAD.stl')



class PageFour(tk.Frame):
    def __init__(self, parent, controller):
        self.pageTwo = controller.frames[PageTwo]
        self.allPolygons = self.pageTwo.getAllPolygons()
        self.sliceThickness = 5
        self.allPoints = []
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Auto Glioblastoma 3D Mesh Construction", 
                                    font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Update Polygon Mesh",
                            command=lambda:self.updatePolygons(parent,
                                                                    controller))

        button1.pack(pady=10,padx=10)

        button2 = ttk.Button(self, text = "Print Polygons", 
                                        command = self.printPolygons)

        button2.pack(pady=10,padx=10)

        button3 = ttk.Button(self, text="Create Triangularized Mesh",
                            command=self.createMesh)

        button3.pack(pady=10,padx=10)

        button4 = ttk.Button(self, text="Save as STL",
                            command = self.stlConverter)
        button4.pack(pady=10,padx=10)
   
        button5 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button5.pack(pady=10,padx=10)

        label = tk.Label(self, 
            text="Instructions", 
            font=LARGE_FONT)

        label.pack(pady=10,padx=10)

        label = tk.Label(self, 
            text="1. Update the polygon mesh by clicking 'Update Polygon Mesh'", 
            font=NORM_FONT)

        label.pack(pady=10,padx=10)

        label = tk.Label(self, 
            text="2. Print coordinates to ensure they have been transferred", 
            font=NORM_FONT)

        label.pack(pady=10,padx=10)

        label = tk.Label(self, 
            text="3. Click 'Create Triangularized Mesh' to view the 3D model", 
            font=NORM_FONT)

        label.pack(pady=10,padx=10)

        text1 = "3. Click 'Save as STL' to save the model as 3D printable STL" 
        text2 = " called 'autoCancerCAD.stl'"
        text3 = text1 + text2

        label = tk.Label(self, 
            text=text3, 
            font=NORM_FONT)

        label.pack(pady=0,padx=10)

    def printPolygons(self): #confirm all Polygons have been updated
        print(self.allPolygons)

    def updatePolygons(self,parent,controller):
        self.allPolygons = self.pageTwo.getAllPolygons()
        if self.allPolygons == None:
            self.popupMsg("No coordinates were passed through!")

    #from: https://pythonprogramming.net/tkinter-popup-message-window/
    def popupMsg(self, msg):
        popup = tk.Tk()
        popup.wm_title("Error!")
        label = ttk.Label(popup, text=msg, font=NORM_FONT)
        label.pack(side="top", fill="x", padx=40, pady=10)
        B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
        B1.pack()
        popup.mainloop() 

    def createMesh(self):
        allPolygons = self.allPolygons

        if self.allPolygons == None:
            self.popupMsg("No coordinates were passed through!")

        fig = plt.figure()

        # Area of Polygon using Shoelace formula
        # http://en.wikipedia.org/wiki/Shoelace_formula
        # FB - 20120218
        # corners must be ordered in clockwise or counter-clockwise direction
        def polyArea(polygon):
            n = len(polygon) # of corners
            area = 0.0
            for i in range(n):
                j = (i + 1) % n
                area += polygon[i][0] * polygon[j][1]
                area -= polygon[j][0] * polygon[i][1]
            area = abs(area) / 2.0
            return area

        def cancerVolume(self): #stack areas to assemble volume
            volume = 0
            for i in allPolygons:
                volume += polyArea(i)
            return volume

        def center(pointList):
            L = len(pointList)
            xSum = 0
            ySum = 0
            for point in pointList:
                xSum += point[0]
                ySum += point[1]
            return (xSum/L,ySum/L) #returns average of all points = Barycenter
        
        def getAngle(x,y):
            epsilon = 0.001
            distance = ((x**2)+(y**2))**.5 #normalize first, from zero (origin)
            if distance < epsilon:
                return 0 #too close to center, don't want to use this point
            theta = np.arccos(x/distance) #need to multiply by SIGN of y
            if y<0: theta*= -1 #accounts for sin function, which is odd
            return theta

        x = []
        y = []
        z = []
        u = []
        v = []

        for i in range(len(self.allPolygons)):
            if self.allPolygons[i] != []:
                cx,cy = center(self.allPolygons[i]) #find center of polygon
                for point in self.allPolygons[i]:
                    x.append(point[0]) #add coordinates to lists
                    y.append(point[1])
                    z.append(i*self.sliceThickness)
                    v.append(i*self.sliceThickness)
                    dx = point[0] - cx #find difference between centerX & pointX
                    dy = point[1] - cy #find difference between centerY & pointY
                    theta = getAngle(dx,dy)
                    u.append(theta)

        for i in range(len(x)):
            list = [x[i],y[i],z[i]]
            self.allPoints.append(list)

        # Triangulate parameter space to determine the triangles
        tri = mtri.Triangulation(u, v)

        #pack canvas
        canvas = FigureCanvasTkAgg(fig, self)
        #canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        ax = fig.add_subplot(1, 1, 1, projection='3d')
        ax.plot_trisurf(x, y, z, triangles=tri.triangles, 
                                        cmap=plt.cm.Spectral)
        ax.set_xlim(min(x), max(x)) #set up x min and max
        ax.set_ylim(min(y), max(y)) #set up y min and max
        ax.set_zlim(min(z), max(z)) #set up z min and max
        Volume = cancerVolume(self.allPolygons) #print volume as label
        red_patch = mpatches.Patch(color='red', label='Volume = %s' % (Volume))
        plt.legend(handles=[red_patch])

        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, 
                                    fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update() 


    def getAllPoints(self): #function called later so variable is not modified
        return self.allPoints

    def stlConverter(self):
        if self.allPoints == []: 
            self.popupMsg("No coordinates were passed through!")
        else:
            # Define the vertices of the tumor
            vertices = np.array(self.allPoints)
            # Define the triangles composing the tumor
            tri = Delaunay(vertices)
            #tri.simplices returns list of all triangles
            faces = np.array(tri.simplices)

            # Create the mesh
            tumor = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
            for i, f in enumerate(faces):
                for j in range(3):
                    tumor.vectors[i][j] = vertices[f[j],:]

            # Write the mesh to file "cancerCAD.stl"
            tumor.save('autoCancerCAD.stl')

class PageFive(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Help", font=LARGE_FONT)
        
        label.pack(pady=10,padx=10)

        label = tk.Label(self, 
                    text="Cancer CAD is a medical imaging tool to help doctors", 
                    font=NORM_FONT)

        label.pack(pady=10,padx=10)

        label = tk.Label(self, 
                    text="and patients understand the three-dimensional", 
                    font=NORM_FONT)

        label.pack(pady=10,padx=10)

        label = tk.Label(self, 
                   text="characteristics of tumors, using only two-dimensional", 
                    font=NORM_FONT)

        label.pack(pady=10,padx=10)

        label = tk.Label(self, 
                   text="tumor data (magnetic resonance images).",
                    font=NORM_FONT)

        label.pack(pady=10,padx=10)

        label = tk.Label(self, 
                    text="Just follow the instructions on each page!",
                    font=LARGE_FONT)
        
        label.pack(pady=10,padx=10)

        label = tk.Label(self, 
                   text="Either manually upload and analyze glioblastoma MRIs",
                    font=NORM_FONT)

        label.pack(pady=10,padx=10)

        label = tk.Label(self, 
                   text="OR let Cancer CAD 'intelligently' find the tumors.",
                    font=NORM_FONT)

        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=10,padx=10)

app = CancerCAD()
app.mainloop()