from fipy import Variable, FaceVariable, CellVariable, Grid1D, ExplicitDiffusionTerm, TransientTerm, DiffusionTerm, Viewer
from fipy.tools import numerix

nx = 50
dx = 1.
mesh = Grid1D(nx=nx, dx=dx)
phi = CellVariable(name="solution variable",
                   mesh=mesh,
                   value=0.)
D=1
eqX = TransientTerm() == ExplicitDiffusionTerm(coeff=D)

#timeStepDuration = 0.9 * dx**2 / (2 * D)
#steps = 100

L=10
x = mesh.cellCenters[0]
steps=100
timeStepDuration = 0.9 * dx**2 / (2 * D)

phi.setValue(1., where=(x > L/2. - L/10.) & (x < L/2. + L/10.))
if __name__ == '__main__':
    viewer = Viewer(vars=phi, datamin=-0.1, datamax=1.1)
    
from builtins import range
for step in range(steps):
    eqX.solve(var=phi,
              dt=timeStepDuration)
    if __name__ == '__main__':
        viewer.plot()
    
