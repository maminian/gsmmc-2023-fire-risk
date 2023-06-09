# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 07:58:26 2023

@author: maminian
"""

import pandas

df = pandas.read_csv('erc.csv')

# "select by" the code being 4.

list = [4, 6, 10, 12] # manually created or automatically defined
for code in list:
    mask= df['US_L3CODE']==code
    df_subset = df[mask]
    
    answer = df_subset['slope of trend'][0]
    