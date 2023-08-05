#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#version fichier py

import pandas as pd

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt

import unittest
import numpy as np


import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt

import imageio
import moviepy

from moviepy.editor import ImageSequenceClip

#fonction pour voir les dechets en France selon les annees voulues

def plot_geo_time_value(x, y, df, lim_metropole = [-5, 10, 41, 52], years=[2003,2005,2007,2009], filename = None):
    
    fig, axs = plt.subplots(2, 2, figsize=(20,15), subplot_kw={'projection': ccrs.PlateCarree()})
        
    i = 0
    j = 0
    
    for k in years :
        colonne = 'Quantite' + str(k)
        axs[i,j].plot()
        axs[i,j].set_extent(lim_metropole)
        axs[i,j].add_feature(cfeature.OCEAN.with_scale('50m'))
        axs[i,j].add_feature(cfeature.COASTLINE.with_scale('50m'))
        axs[i,j].add_feature(cfeature.RIVERS.with_scale('50m'))
        axs[i,j].add_feature(cfeature.BORDERS.with_scale('50m'), linestyle=':')
        axs[i,j].scatter(x, y,
                   s=df[colonne] ** 0.5 / 5, alpha=0.5)
        axs[i,j].set_title('France ' + str(k) + '\nproduction de produits dangereux');
        if i == 0:
            i += 1
        elif i == 1 and j == 0 :
            (i,j) = (j,i)
        else : 
            i = 1
            j = 1
            
    fig.savefig(filename)
    return(i,j)

class Test(unittest.TestCase):
    
    """On teste plot_geo_time_value"""
    
    def test_plot_geo_time_value(self):

    # on regarde les valeurs renvoyees par test_plot_geo_time_value 
    # pour i et j, si elles ne valent pas 1 et 1 il y a un probleme

        (a,b) = plot_geo_time_value(df = pd.read_csv("df_metro.csv", sep=",", encoding = 'latin-1'), x=df['LLX'],y=df['LLY'],lim_metropole = [-5, 10, 41, 52],filename = 'yourfilename.pdf')
        liste = [a,b]
        self.assertEqual(liste,[1,1])
            
#if __name__ == '__main__':
#    unittest.main()

unittest.main(argv=[''], verbosity=2, exit=False)
