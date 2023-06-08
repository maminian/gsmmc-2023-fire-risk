import us_boundaries as usb
from matplotlib import pyplot as plt

fig,ax = plt.subplots()

usb.draw_state(ax, 'Massachusetts', edgecolor='#333')

# you can do this more than once...
usb.draw_state(ax, 'Maine', edgecolor='b')
usb.draw_state(ax, 'New York', edgecolor='#808')
usb.draw_state(ax, 'Vermont')
usb.draw_state(ax, 'New Hampshire')
fig.show()

