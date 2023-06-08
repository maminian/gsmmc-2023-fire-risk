
import numpy as np
from matplotlib import pyplot as plt

def Omega(X,Y,p,b):
    Z = X + 1j*Y
    return Z - p + (p-b)**2/(Z-p)
def Phi(X,Y,p,b):
    return (X-p)*( 1 + (p-b)**2/((X-p)**2 + Y**2) )
def Psi(X,Y,p,b):
    return Y*( 1 - (p-b)**2/( (X-p)**2 + Y**2 ) )

def semicircle(p, b):
    '''
    bottom boundary of domain. To be used in combo with ax.fill().
    '''
    th = np.linspace(0, np.pi, 400)
    _x = p + b*np.cos(th)
    _y = 0 + b*np.sin(th)
    return _x,_y

XX,YY = np.meshgrid( np.linspace(-2,4), np.linspace(0,4) )

p = 1.8
b = 1

phi = Phi(XX,YY, p,b)
psi = Psi(XX,YY, p,b)

#

# TODO: confirm this is actually the correct center/radius to use.
mask = ((XX-p)**2 + YY**2 >= b**2)

phimin = phi[mask].min()
phimax = phi[mask].max()
psimin = psi[mask].min()
psimax = psi[mask].max()
# Ignore values from within the obstruction.
# nevermind - opting for another approach.
#phi = phi * mask
#psi = psi * mask

######################
# Visualization

plt.rcParams.update({'font.size': 16})

fig,ax = plt.subplots(1,2, 
                      figsize=(8,4),
                      sharex=True, sharey=True, constrained_layout=True)


# mut the coors for the pcolor.
alpha = 0.8
LEVELS = 13

ax[0].pcolor(XX,YY, phi, cmap=plt.cm.Purples, alpha=alpha, vmin=phimin, vmax=phimax)
ax[0].contour(XX,YY, phi, 
              levels=np.linspace(phimin,phimax, LEVELS), 
              colors='k', linewidths=2)

ax[1].pcolor(XX,YY, psi, cmap=plt.cm.Greens, alpha=alpha, vmin=psimin, vmax=psimax)
ax[1].contour(XX,YY, psi, 
              levels=np.linspace(psimin, psimax, LEVELS), 
              colors='k', linewidths=2)

ax[0].set(aspect='equal', title=r'$\Phi(X,Y)$')
ax[1].set(aspect='equal', title=r'$\Psi(X,Y)$')

for axi in ax:
    axi.grid(ls='--', lw=0.5)
    axi.set(xlabel=r'$X$', ylabel=r'$Y$')
    # mask out the interior of circle at (p,0), radius b.
    xbathy = np.linspace(XX.min(), XX.max(), 500)
    axi.fill(*semicircle(p, b), 
                hatch='////', facecolor=[0,0,0,0], zorder=100, 
                edgecolor='r')
    
    

fig.show()