#!/usr/bin/env python
#-*- coding:utf-8 -*-
##
## p_correlation.py
##
##  Created on: Feb 6, 2021
##  Calculates correlations between non-protected and a protected feature using Pearson correlation

#
#==============================================================================
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import csv


#==============================================================================
def value_to_color(val):
    val_position = float((val - color_min)) / (color_max - color_min) # position of value in the input range, relative to the length of the input range
    ind = int(val_position * (n_colors - 1)) # target index in the color palette
    return palette[ind]

#==============================================================================
if __name__ == '__main__':
    f = open('../../../bench/communities-crime/communities.csv', 'r')
    data = pd.read_csv(f)
    corr = data.corr()

    ax = sns.heatmap(corr, annot=True, fmt="f")
    plt.show()
    #plt.savefig('adult_corr.png')
    
    f.close()