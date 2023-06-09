
import numpy as np
from matplotlib import pyplot as plt

# for the colorbar...
# following https://matplotlib.org/stable/gallery/axes_grid1/simple_colorbar.html#sphx-glr-gallery-axes-grid1-simple-colorbar-py
from mpl_toolkits.axes_grid1 import make_axes_locatable


####

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

xx, yy = np.meshgrid( np.linspace(-2,4,300), np.linspace(0,4,300) )

for p in np.arange(0.2, 3.1, 0.2):
    #p = 1.8
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
    phix = np.gradient(phi, xx[0,:], axis=1)
    phiy = np.gradient(phi, yy[:,0], axis=0)
    psix = np.gradient(psi, xx[0,:], axis=1)
    psiy = np.gradient(psi, yy[:,0], axis=0)
    
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
    
    
    ax[0].contourf(xx,yy, phi, cmap=plt.cm.Purples, alpha=alpha, vmin=phimin, vmax=phimax, levels=np.linspace(phimin,phimax, LEVELS))
    ax[0].contour(xx,yy, phi, 
                  levels=np.linspace(phimin,phimax, LEVELS), 
                  colors='k', linewidths=2)
    
    ax[1].contourf(xx,yy, psi, cmap=plt.cm.Greens, alpha=alpha, vmin=psimin, vmax=psimax, levels=np.linspace(psimin, psimax, LEVELS))
    ax[1].contour(xx,yy, psi, 
                  levels=np.linspace(psimin, psimax, LEVELS), 
                  colors='k', linewidths=2)
    
    im = ax[2].contourf(xx, yy, mag, levels=LEVELS, cmap=plt.cm.plasma)
    
    ax[0].set(aspect='equal', title=r'$\Phi(X,Y)$')
    ax[1].set(aspect='equal', title=r'$\Psi(X,Y)$')
    
    
    ax[2].set(aspect='equal', title=r'$||\nabla \Phi||$')
    
    divider = make_axes_locatable(ax[2])
    cax = divider.append_axes("right", size="5%", pad=0.05)
    
    fig.colorbar(im, cax=cax)
    
    for axi in ax:
        axi.grid(ls='--', lw=0.5)
        axi.set(xlabel=r'$x$', ylabel=r'$y$', xlim=[-2,4], ylim=[0,4])
        # mask out the interior of circle at (p,0), radius b.
        xbathy = np.linspace(XX.min(), XX.max(), 500)
        axi.fill(*semicircle(), 
                    hatch='////', facecolor='k', zorder=100, 
                    edgecolor='r')
    ##
    
    
    fig.savefig('potential_flow_verhoff_2010' + "p%.2f_b%.2f.pdf"%(p,b), bbox_inches='tight')
    fig.savefig('potential_flow_verhoff_2010' + "p%.2f_b%.2f.png"%(p,b), bbox_inches='tight')
    #fig.show()
    
    # where is the max? What is the max relative to the "far field"?
    
    speed_farfied = mag[0,0]
    speed_idx_flat = np.nanargmax(mag)
    speed_idx = np.unravel_index(speed_idx_flat, mag.shape)
    
    print("MAX SPEED RELATIVE TO UPSTREAM SPEED:")
    print("%.2f"%mag[speed_idx])
    
    phix_m = phix*mask/mag
    phiy_m = phiy*mask/mag
    ax[2].streamplot(
        xx,
        yy,
        phix_m, # yeah - supposed to be (-phiy, phix); not sure what I flipped.
        phiy_m, 
        color='w',
        density=0.5, 
        zorder=1000)
