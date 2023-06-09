from fipy import Variable, FaceVariable, CellVariable, Grid1D, Grid2D, ExplicitDiffusionTerm, TransientTerm, DiffusionTerm, Viewer
from fipy.tools import numerix
import numpy as np
import math,mpmath
from matplotlib import pyplot as plt

#A function to define the polygonal mesh
def gen_mesh(pts,cellSize):

    import fipy
    
    gmsh_arg = 'cellSize = %.8f; \n '%cellSize    # %.8f could cause truncation issues in edge cases
    idx = 0
    for p in pts:
        idx += 1
        gmsh_arg += 'Point(%i) = {%.8f,%.8f,0,%.8f}; \n '%(idx, p[0], p[1], cellSize)
    #

    line_ptrs = [str(jj+1+idx) for jj in range(len(pts))]
    for j in range(len(pts)):
        idx += 1
        gmsh_arg += 'Line(%i) = {%i,%i};\n'%(idx, 1+(j%len(pts)), 1+((j+1)%len(pts)))
        
#        line_ptrs += str(idx)
    #

    idx += 1
    gmsh_arg += 'Line Polygon(%i) = '%(idx,)
    gmsh_arg += '{' + ','.join(line_ptrs) + '}; \n'

    idx += 1
    gmsh_arg += 'Plane Surface(%i) = {%i};\n'%(idx, idx-1)

    # Call fipy to construct the mesh with the given 
    # input parameters (a plaintext file we constructed procedurally)
    mesh = fipy.Gmsh2D(gmsh_arg)

    return mesh

#Creating the an hexagonal mesh with a downward slope at the bottom
x_max=2
x_min=-0.5*x_max
x_length=x_max-x_min
y_min=0
theta = np.pi/4
y_max=2
h=-x_min
slope_base=h*mpmath.cot(theta)
left_length=(x_length-slope_base)/2
right_length=left_length
pts = [(x_min,h),(left_length+x_min, h), (x_max-right_length, y_min), (x_max,y_min), (x_max,y_max), (x_min, y_max)]

mesh = gen_mesh(pts, 0.01)
#Defining the potential variable
phi = CellVariable(name="Potential",
                   mesh=mesh,
                   value=0.)

#Defining the equation
D=1
eqX = DiffusionTerm(coeff=D)==0

#Setting up boundary conditions. This is the simple case of Neumann Boundary
#condition. The assumption is the normal derivative of phi is a constant at
#top and 0 everywhere else on the boundary.

valueLeft=0
valueRight=0
valueTop=1
valueBottomRight=0
valueBottomLeft=0
valueBottomMiddle=0

X, Y=mesh.faceCenters

facesbottomright=(mesh.exteriorFaces & (X>=x_max-right_length) & (Y==y_min)) 
facesbottomleft=(mesh.exteriorFaces & (X<left_length+x_min) & (Y==h)) 
facesbottommiddle=(mesh.exteriorFaces & (X>=left_length+x_min) & (X<x_max-right_length) & (Y<=h+0.1))
faceslefttop=(mesh.exteriorFaces & (X==x_min))
facesright=(mesh.exteriorFaces & (X==x_max))
facestop=(mesh.exteriorFaces & (Y==y_max))
phi.faceGrad.constrain(valueTop,facestop)
phi.faceGrad.constrain(valueBottomRight,facesbottomright)
phi.faceGrad.constrain(valueBottomMiddle, facesbottommiddle)  
phi.faceGrad.constrain(valueBottomLeft, facesbottomleft)
phi.faceGrad.constrain(valueRight, facesright) 
phi.faceGrad.constrain(valueLeft, faceslefttop) 
#For Neumann BC we need to fix a point in the boundary to prevent the solver
#from choosing constant of solution randomly.
phi.constrain(0, where=(mesh.exteriorFaces & (X<=x_max-right_length+0.01)&(Y<=y_min+0.01))) 

#Plotting the graph
viewer = Viewer(vars=phi)
eqX.solve(var=phi)
viewer.plot()

fig=plt.gcf()
ax=fig.gca()
ax.tricontour(mesh.cellCenters[0],mesh.cellCenters[1],phi.value,40)
plt.xlabel("Ground position")
plt.ylabel("Height")


