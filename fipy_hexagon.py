from fipy import Variable, FaceVariable, CellVariable, Grid1D, Grid2D, ExplicitDiffusionTerm, TransientTerm, DiffusionTerm, Viewer
from fipy.tools import numerix

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

#pts = [(-0.5,0.5),(0, 0.5), (0.5, 0), (1,0), (1., 1.), (-0.5, 1)]
x_max=2
x_min=-0.5*x_max
x_length=x_max-x_min
y_min=0
y_max=2
h=-x_min
pts = [(x_min,h),(x_length/3+x_min, h), (2*x_length/3+x_min, y_min), (x_max,y_min), (x_max,y_max), (x_min, y_max)]

mesh = gen_mesh(pts, 0.01)
phi = CellVariable(name="solution variable",
                   mesh=mesh,
                   value=0.)
phi_1 = CellVariable(name="solution variable",
                   mesh=mesh,
                   value=2)

D=1
eqX = DiffusionTerm(coeff=D)==-2

L=1.
valueLeft=2
valueRight=2
valueTop=2
valueBottomRight=0
valueBottomLeft=0
valueBottomMiddle=0

X, Y=mesh.faceCenters

facesbottomright=(mesh.exteriorFaces & (X>=2*x_length+x_min) & (Y==y_min)) 
facesbottomleft=(mesh.exteriorFaces & (X<x_length/3+x_min) & (Y==h)) 
facesbottommiddle=(mesh.exteriorFaces & (X>=x_length/3+x_min) & (X<2*x_length+x_min) & (Y<=h+0.1))
faceslefttop=(mesh.exteriorFaces & (X==x_min))
facesright=(mesh.exteriorFaces & (X==x_max))
facestop=(mesh.exteriorFaces & (Y==y_max))
phi.constrain(valueTop,facestop)
phi.constrain(valueBottomRight,facesbottomright)
phi.constrain(valueBottomMiddle, facesbottommiddle)  
phi.constrain(valueBottomLeft, facesbottomleft)
phi.constrain(valueRight, facesright) 
phi.constrain(valueLeft, faceslefttop)  

#exterior_faces=mesh.exteriorFaces
#phi.constrain(0,exterior_faces)
viewer = Viewer(vars=phi)
eqX.solve(var=phi)
viewer.plot()



#x = mesh.cellCenters[0]
#steps=100
#timeStepDuration = 0.9 * dx**2 / (2 * D)
#phi.value = 0.

#phi.setValue(1., where=(x > L/2. - L/10.) & (x < L/2. + L/10.))
#if __name__ == '__main__':
 #   viewer = Viewer(vars=phi, datamin=-0.1, datamax=1.1)
    
#from builtins import range
#for step in range(steps):
 #   eqX.solve(var=phi)
  #  if __name__ == '__main__':
   #     viewer.plot()
    
