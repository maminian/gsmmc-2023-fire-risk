
import numpy as np
from matplotlib import pyplot as plt

def Omega(X,Y,p,b):
    Z = X + 1j*Y
    return Z - p + (p-b)**2/(Z-p)
def Phi(X,Y,p,b):
    return (X-p)*( 1 + (p-b)**2/((X-p)**2 + Y**2) )
def Psi(X,Y,p,b):
    return Y*( 1 - (p-b)**2/( (X-p)**2 + Y**2 ) )

XX,YY = np.meshgrid( np.linspace(-4,4), np.linspace(0,4) )

p = 1.8
b = 1

phi = Phi(XX,YY, p,b)
psi = Psi(XX,YY, p,b)

fig,ax = plt.subplots(2,1)

ax[0].pcolor(XX,YY, phi)
ax[0].contour(XX,YY, phi, c='w')
ax[1].pcolor(XX,YY, psi)

fig.show()