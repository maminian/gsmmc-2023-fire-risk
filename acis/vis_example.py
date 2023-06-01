
# so that I don't have to re-download.
# Note that the simplified_load.py script needs to 
# be changed to change the focus.
import simplified_load

data = simplified_load.data

    
from matplotlib import pyplot as plt
import numpy as np
#mycm = plt.cm.inferno.copy()
#mycm.set_under([0,0,0,0])

fig,ax = plt.subplots(2,4, figsize=(8,4),sharex=True, sharey=True, gridspec_kw={'wspace':0.04, 'hspace':0.04}, constrained_layout=True)
for i in range(ax.shape[0]):
    for j in range(ax.shape[1]):
        idx = j + ax.shape[1]*i
        
        arr = np.array(data['data'][idx][1], dtype=float)
        arr[arr<0] = np.nan
        ax[i,j].pcolor(arr, vmin=0, vmax=2, cmap=plt.cm.plasma)
        ax[i,j].text(0,1,data['data'][idx][0], color='w', fontsize=11, ha='left', va='top', transform=ax[i,j].transAxes, bbox={'facecolor':'k'})
        
fig.show()