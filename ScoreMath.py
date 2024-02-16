# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 23:32:37 2024

@author: lukej
"""
import math
import numpy as np

def getMean( stat_category, data ):
    return np.mean(data[stat_category])

def getStdDev( stat_category, data ):
    return np.std(data[stat_category])

def zptile(z_score):
    return .5 * (math.erf(z_score / 2 ** .5) + 1)

def calculate_percentile(score, average, std_dev):
    if(average == None or std_dev == None): return 0
    z_score = ( score - average ) / std_dev
    return zptile(z_score)