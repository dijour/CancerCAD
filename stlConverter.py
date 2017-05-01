import numpy as np
from stl import mesh
from scipy.spatial import Delaunay

def stlConverter(allPoints):
    # Define the vertices of the tumor
    vertices = np.array(allPoints)
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
    tumor.save('cancerCAD.stl')