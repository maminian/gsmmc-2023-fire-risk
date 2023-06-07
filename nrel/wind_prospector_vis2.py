# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 12:39:57 2023

@author: maminian
"""

import pandas

from matplotlib import pyplot as plt
import numpy as np

# manually mined from wind-prospector 1.3G zipped folder;
# Wind_Speed_Annual/Wind_Speed_Annual.csv

import geopandas

fig,ax = plt.subplots(figsize=(8,6), constrained_layout=True)

# world map
world_gdf = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
world_gdf = world_gdf[world_gdf['continent'] == 'North America']

world_gdf.plot(ax=ax, facecolor=[0,0,0,0], edgecolor='k')

gdf = geopandas.read_file('Western_Wind_Dataset')

gdf.plot(column='CAPACITY F', ax=ax, s=1)

ax.set(xlabel='Longitude', ylabel='Latitude', xlim=[-130,-100], ylim=[25, 50])
ax.set()
fig.savefig("wind_thingy.png")
fig.show()
