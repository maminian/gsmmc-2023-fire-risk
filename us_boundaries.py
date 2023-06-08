'''
# ATTN: assumes folder structure

./ 
./us_boundaries.py
./us_boundaries/rows.json

This assums you have file rows.json downloaded off 
of the proper website in that folder.

I'm using: 
https://eric.clst.org/tech/usgeojson/

with "US States", 
file gz_2010_us_040_00_5m.json, 
that's the "5m" column.

-Manuch
'''


import geopandas
import os
import json

abspath = os.path.abspath(__file__)
parent_dir = os.path.abspath( os.path.join(abspath, os.path.pardir ) )

shape_file = os.path.join(parent_dir, 'us_boundaries', 'gz_2010_us_040_00_5m.json')

gdf = geopandas.read_file(shape_file)


# for example..
def draw_state(myax, statename, facecolor=[0,0,0,0], edgecolor='r', linewidth=2):
    '''
    Input: state name, full name, capitalized first letter (TODO: simplify)
    Output: lon coords (x), lat coords (y) as a pair of arrays.
    '''
    #statename = statename.lower()
    subset = gdf[gdf['NAME']==statename]
    subset.plot(ax=ax, facecolor=facecolor, edgecolor=edgecolor, linewidth=linewidth)
    
    
if __name__=="__main__":
    # for example...
    from matplotlib import pyplot as plt
    fig,ax = plt.subplots()
    
    draw_state(ax, 'California')
    # you can do this more than once...
    draw_state(ax, 'Nevada', edgecolor='b')
    draw_state(ax, 'New Mexico', edgecolor='g')
    fig.show()
    
    # in another file: just import "us_boundaries" 
    # and call us_boundaries.draw_state(...)
