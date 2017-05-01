import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.tri as mtri
import matplotlib.patches as mpatches

def coordinateStats(pointSet):
    newPoints = []
    denominator = len(pointSet)
    xTotal = yTotal = 0
    rTotal = 0
    for i in range(len(pointSet)):
        xTotal += pointSet[i][0]
        yTotal += pointSet[i][1]
        rTotal += pointSet[i][2]
    xMean = xTotal/denominator
    yMean = yTotal/denominator
    rMean = rTotal/denominator
    return (xMean, yMean, rTotal, denominator)

def stdDevs(pointSet):
    xMean, yMean, rMean, denominator = coordinateStats(pointSet) 
    xNums = yNums = rNums = 0
    for i in range(len(pointSet)):
        xNums += (pointSet[i][0]-xMean)**2
        yNums += (pointSet[i][1]-yMean)**2
        rNums += (pointSet[i][2]-rMean)**2
    xVariance = (1/denominator)*xNums
    yVariance = (1/denominator)*yNums
    rVariance = (1/denominator)*rNums
    xStdDev = xVariance**.5
    yStdDev = yVariance**.5
    rStdDev = rVariance**.5
    return (xStdDev, yStdDev, rStdDev)

def filterPointSet(pointSet):
    xStdDev, yStdDev, rStdDev = stdDevs(pointSet)
    allPolygons = []
    for i in range(len(pointSet)):
        if ((pointSet[i][0] > pointSet[i][0] + (2*xStdDev)) or 
            (pointSet[i][0] < pointSet[i][0] - (2*xStdDev)) or
            (pointSet[i][1] > pointSet[i][1] + (2*yStdDev)) or
            (pointSet[i][1] < pointSet[i][1] - (2*yStdDev)) or
            (pointSet[i][2] > pointSet[i][2] + (2*rStdDev)) or
            (pointSet[i][2] < pointSet[i][2] - (2*rStdDev))):
            pass
        else:
            cx = pointSet[i][0] 
            cy = pointSet[i][1]
            r = pointSet[i][2] 
            coordinates = []
            for angle in range (1,360,20):
                newX = cx + np.cos(angle)*r
                newY = cy + np.sin(angle)*r
                coordinates.append((newX,newY))
            allPolygons.append(coordinates)
    return allPolygons 

def autoCAD(pointSet):
    allPolygons = filterPointSet(pointSet)

    fig = plt.figure()

    def center(pointList):
        L = len(pointList)
        xSum = 0
        ySum = 0
        for point in pointList:
            xSum += point[0]
            ySum += point[1]
        return (xSum/L,ySum/L) #returns average of all points, A.K.A. Barycenter

    def getAngle(x,y):
        epsilon = 0.001
        distance = ((x**2)+(y**2))**.5 #normalize first, from zero (origin)
        if distance < epsilon:
            return 0 #too close to center, don't want to use this point
        theta = np.arccos(x/distance) #need to multiply by SIGN of y
        if y<0: theta*= -1 #accounts for sin function, which is odd
        return theta

        
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

    def cancerVolume(allPolygons):
        volume = 0
        for i in allPolygons:
            volume += polyArea(i)
        return volume

    def cancerCAD(allPolygons,sliceThickness = 2):
        #Create 5 lists: x,y,z,u,v
        x = []
        y = []
        z = []
        u = []
        v = []

        for i in range(len(allPolygons)):
            if allPolygons[i] != []:
                cx,cy = center(allPolygons[i]) #feed one allPolygons at a time, find center
                for point in allPolygons[i]:
                    x.append(point[0]) #add coordinates to lists
                    y.append(point[1])
                    z.append(i*sliceThickness)
                    v.append(i*sliceThickness)
                    dx = point[0] - cx #find differences between center and each point
                    dy = point[1] - cy
                    theta = getAngle(dx,dy)
                    u.append(theta)

        # Triangulate parameter space to determine the triangles
        tri = mtri.Triangulation(u, v)

        # Plot the surface.  The triangles in parameter space determine which x, y, z
        # points are connected by an edge.
        ax = fig.add_subplot(1, 1, 1, projection='3d')
        ax.plot_trisurf(x, y, z, triangles=tri.triangles, cmap=plt.cm.Spectral)
        ax.set_xlim(min(x), max(x))
        ax.set_ylim(min(y), max(y))
        ax.set_zlim(min(z), max(z))
        Volume = cancerVolume(allPolygons)
        red_patch = mpatches.Patch(color='red', label='Volume = %s' % (Volume))
        plt.legend(handles=[red_patch])
        plt.show()

    cancerCAD(allPolygons)

if __name__ == "__main__":
    pointSet = [[341.2093200683594, 188.14134216308594, 56.83320999145508], 
                 [505.187255859375, 506.65789794921875, 51.9934196472168],
                 [445.5681457519531, 166.8529815673828, 67.94416809082031], 
                 [482.7690734863281, 481.78021240234375, 57.7081413269043], 
                 [318.03363037109375, 445.75360107421875, 82.49557495117188], 
                 [500.9687805175781, 502.7318115234375, 50.900909423828125], 
                 [502.596923828125, 505.7395324707031, 50.72273254394531], 
                 [442.5135192871094, 170.01329040527344, 79.96908569335938], 
                 [499.2638244628906, 500.2850036621094, 50.27344512939453], 
                 [490.2976379394531, 488.2977600097656, 56.33266067504883], 
                 [314.5223693847656, 432.2388610839844, 72.85964965820312], 
                 [487.6045227050781, 485.37432861328125, 56.45241165161133], 
                 [315.3462219238281, 438.9722900390625, 79.45706939697266], 
                 [485.4549560546875, 484.382568359375, 58.26536560058594], 
                 [317.547119140625, 444.8305358886719, 81.5938720703125], 
                 [481.5622863769531, 478.8992614746094, 59.61460494995117], 
                 [320.1226806640625, 448.9004821777344, 77.68781280517578], 
                 [481.6703186035156, 475.51849365234375, 60.00159454345703], 
                 [318.2685546875, 456.8684997558594, 78.93309020996094], 
                 [469.5013122558594, 325.2032165527344, 62.094520568847656], 
                 [481.2523498535156, 470.3836364746094, 61.747093200683594], 
                 [317.3448791503906, 461.44061279296875, 78.03243255615234], 
                 [470.3708190917969, 327.2347412109375, 66.2372817993164], 
                 [480.852783203125, 463.2069091796875, 62.15095901489258], 
                 [470.8657531738281, 327.71124267578125, 71.20011138916016], 
                 [310.2822265625, 477.999267578125, 59.23594284057617], 
                 [309.2926025390625, 482.533203125, 54.67033004760742], 
                 [416.5625, 256.33843994140625, 70.5586166381836], 
                 [479.2214660644531, 276.13555908203125, 76.56217193603516], 
                 [404.6139831542969, 268.2266845703125, 57.1832160949707], 
                 [383.3925476074219, 293.11993408203125, 70.32743835449219]]

    autoCAD(pointSet)