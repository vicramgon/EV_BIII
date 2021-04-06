#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 12:48:30 2021

@author: victor
"""
#%%
'''
##############
# LIBRARIES #
#############
'''

import numpy as np                 # Math library
import os
import shutil
import matplotlib as mpl
import matplotlib.pyplot as plt    # Plot library     
import matplotlib.patches as mpatches  
import sys

#%%
'''
###############################
# PLOT HYPERVOLUME ALL SEEDS #
##############################

'''

N1 = int(sys.argv[1])
G1 = int(sys.argv[2]) 
ALG1 = str(sys.argv[3])
dataFile1 = str(sys.argv[4])

N2 = int(sys.argv[5])
G2 = int(sys.argv[6]) 
ALG2 = str(sys.argv[7])
dataFile2 = str(sys.argv[8])
problem =  str(sys.argv[9])

print(N1, G1, ALG1, dataFile1)
print(N2, G2, ALG2, dataFile2)

colors = plt.get_cmap('jet', 2)

data1 = np.genfromtxt(dataFile1, delimiter='\t')
data2 = np.genfromtxt(dataFile2, delimiter='\t')


for i,s in enumerate([1,2,3,4,5,6,7,8,9,99]):
    plt.plot(np.arange(1, G1+1), data1[G1*i:G1*(i+1),1], c=colors(0))
    plt.plot(np.arange(1, G2+1), data2[G2*i:G2*(i+1),1], c=colors(1))
    
patch1 = mpatches.Patch(color=colors(0), label=f'{ALG1} N{N1} G{G1}')
patch2 = mpatches.Patch(color=colors(1), label=f'{ALG2} N{N2} G{G2}')
plt.title(f'Spacing Comp. {problem} {ALG1} N{N1} G{G1} vs {ALG2} N{N2} G{G2}\n', fontsize=10)
plt.xlabel('Generation', fontsize=11)
plt.ylabel('Spacing', fontsize=11)
plt.legend(handles=[patch1, patch2])
plt.grid(True)

if not(os.path.isdir('../METRICS_PLOTS')):
    os.mkdir('../METRICS_PLOTS')
    
if not(os.path.isdir(f'../METRICS_PLOTS/{problem}')):
    os.mkdir(f'../METRICS_PLOTS/{problem}')

plt.savefig(f'../METRICS_PLOTS/{problem}/Spacing_COMP_{problem}_{ALG1}N{N1}G{G1}_{ALG2}N{N2}G{G2}.png', dpi=200)
plt.clf()