# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 12:39:57 2023

@author: maminian
"""

import pandas

from matplotlib import pyplot as plt
import numpy as np

prefix = 'PRISM_ppt_early_4kmD2_20230531_bil'

df = pandas.read_csv(prefix + '/' + prefix + '.stn.csv' , skiprows=1)

fig,ax = plt.subplots()

mask= df['Elevation(m)']<0
df['Elevation(m)'].replace(-9999, np.nan, inplace=True)

ax.scatter(
    df['Longitude'],
    df['Latitude'],
    c=df['Elevation(m)'],
    vmin=0,
    s=1
    )