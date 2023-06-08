
import numpy as np
from matplotlib import pyplot as plt

def Omega(X,Y,p,b):
    Z = X + 1j*Y
    return Z - p + (p-b)**2/(Z-p)
def Phi(X,Y,p,b):
    return (X-p)*( 1 + (p-b)**2/((X-p)**2 + Y**2) )
def Psi(X,Y,p,b): 
    return Y*( 1 - (p-b)**2/( (X-p)**2 + Y**2 ) )

def semicircle():
    '''
    bottom boundary of domain. To be used in combo with ax.fill().
    '''
    th = np.linspace(0, np.pi, 400)
    _x = 0 + 1*np.cos(th)
    _y = 0 + 1*np.sin(th)
    return _x,_y

xx, yy = np.meshgrid( np.linspace(-2,4,300), np.linspace(0,4, 300) )

p = 1.8
b = 1

XX = xx + xx/(xx**2 + yy**2)
YY = yy - yy/(xx**2 + yy*2)

phi = Phi(XX,YY, p,b)
psi = Psi(XX,YY, p,b)

#

# TODO: confirm this is actually the correct center/radius to use.
# NOPE
# p is the doublet location (Z=p + 0i)
# b is the separation point (Z=b + 0i)

####
# TODO: need to map back to physical (x,y) first.
####
mask = (xx**2 + yy**2 >= 1)

#
phimin = phi[mask].min()
phimax = phi[mask].max()
psimin = psi[mask].min()
psimax = psi[mask].max()
# Ignore values from within the obstruction.
# nevermind - opting for another approach.
#phi = phi * mask
#psi = psi * mask

# TODO: are these still valid after transforming to (x,y)?
phix = np.gradient(phi, xx[0,:], axis=0)
phiy = np.gradient(phi, yy[:,0], axis=1)

mag = np.sqrt(phix**2 + phiy**2)
mag[np.logical_not(mask)] = np.nan


######################
# Visualization

plt.rcParams.update({'font.size': 16})

fig,ax = plt.subplots(1,3, 
                      figsize=(12,4),
                      sharex=True, sharey=True, constrained_layout=True)


# mut the coors for the pcolor.
alpha = 0.8
LEVELS = 13


ax[0].pcolor(xx,yy, phi, cmap=plt.cm.Purples, alpha=alpha, vmin=phimin, vmax=phimax)
ax[0].contour(xx,yy, phi, 
              levels=np.linspace(phimin,phimax, LEVELS), 
              colors='k', linewidths=2)

ax[1].pcolor(xx,yy, psi, cmap=plt.cm.Greens, alpha=alpha, vmin=psimin, vmax=psimax)
ax[1].contour(xx,yy, psi, 
              levels=np.linspace(psimin, psimax, LEVELS), 
              colors='k', linewidths=2)

ax[2].pcolor(xx, yy, mag, cmap=plt.cm.plasma)

ax[0].set(aspect='equal', title=r'$\Phi(X,Y)$')
ax[1].set(aspect='equal', title=r'$\Psi(X,Y)$')


ax[2].set(aspect='equal', title=r'$||\nabla \Phi||$')

for axi in ax:
    axi.grid(ls='--', lw=0.5)
    axi.set(xlabel=r'$X$', ylabel=r'$Y$', xlim=[-2,4], ylim=[0,4])
    # mask out the interior of circle at (p,0), radius b.
    xbathy = np.linspace(XX.min(), XX.max(), 500)
    axi.fill(*semicircle(), 
                hatch='////', facecolor='k', zorder=100, 
                edgecolor='r')
    
    

fig.show()