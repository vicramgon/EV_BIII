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
import sys

#%%
'''
###############################
# PLOT HYPERVOLUME ALL SEEDS #
##############################

'''

N = int(sys.argv[1])
G = int(sys.argv[2]) 
EOP = str(sys.argv[3])
dataFile = str(sys.argv[4])

print(N, G, EOP, dataFile)
colors = plt.get_cmap('jet', 10)
data = np.genfromtxt(dataFile, delimiter='\t')

if not(os.path.isdir(f'../MOEA_D_{EOP}/ZDT3/EVAL{N*G}/METRICS_PLOTS/')):
    os.mkdir(f'../MOEA_D_{EOP}/ZDT3/EVAL{N*G}/METRICS_PLOTS')
    

for i,s in enumerate([1,2,3,4,5,6,7,8,9,99]):
    plt.plot(np.arange(1, G+1), data[G*i:G*(i+1),1], label=f"seed {s}", c=colors(i))
    
plt.title(f'Hyervolume MOEA/D + {EOP} N{N} G{G}\n')
plt.xlabel('Generation', fontsize=11)
plt.ylabel('Hypervolume', fontsize=11)
plt.legend()
plt.grid(True)

plt.savefig(f'../MOEA_D_{EOP}/ZDT3/EVAL{N*G}/METRICS_PLOTS/Hypervol_N{N}_G{G}.png', dpi=200)
plt.clf()