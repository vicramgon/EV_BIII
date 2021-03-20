#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 
==============================================================================
               APLICACIONES DE SOFT-COMPUTING
==============================================================================

@title : COMPETICIÓN B.III - Algoritmos Evolutivos : Pruebas
@author: Víctor Ramos González
"""

#%%
'''
##############
# LIBRARIES #
#############
'''
from ASCEVBIII import EOP1, EOP2, EOP3, MOEAD
import numpy as np                 # Math library
import os
import matplotlib.pyplot as plt    # Plot library
import colour                      # Color library
import shutil

#%%
'''
###############################################
# ZDT3: GOALS, SEARCH SPACE AND PARETO FRONT #
##############################################
'''

# GOALS FUNCTIONS
f1 = lambda x : x[0]

def f2(x):
    g = 1 + 9/(len(x)-1) *sum(x[1:])
    return g*(1 - np.sqrt(x[0]/g)-(x[0]/g)*np.sin(10*np.pi*x[0]))

ZDT3_GOALS = [f1, f2]

# SEARCH SPACE
ZDT3_SS = [(0,1) for _ in range(30)]

# REAL PARETO FRONT
ZDT3_PF_x = np.concatenate((np.linspace(0, 0.0830015349), 
                        np.linspace(0.1822287281, 0.2577623634),
                        np.linspace(0.4093136749,0.45388221041),
                        np.linspace(0.6183967945,0.6525117038),
                        np.linspace(0.8233317984, 0.8518328654))
                      )

ZDT3_PF_y = np.vectorize(lambda x: 1 - np.sqrt(x) - x*np.sin(10*np.pi*x))(ZDT3_PF_x)

#%%
'''
###############################################
# DIRECTORY PREPARING FOR RESULTS AND PLOTS #
##############################################
'''
def prepareDir(path):
    if os.path.isdir(path.split("/")[0]):
        shutil.rmtree(path.split("/")[0])
    
    completePath = ""
    for p in path.split("/"):
        completePath += p + "/"
        os.mkdir(completePath)
    os.mkdir(completePath + "outputs")
    os.mkdir(completePath + "plots")
    return completePath + "outputs", completePath + "plots"

#%%
'''
#############################
# PROOF 1.1: MOEA/D + EOP1 #
#############################
'''

# MOEA PARAMETERS
N = 100; G = 100; T=8; eop=EOP1

# Color gradient for plots
colors = list(colour.Color("blue").range_to(colour.Color("red"),G))

# FILES 
outputDirPath, plotsDirPath = prepareDir(f'results_ZDT3_{eop.__name__}_N{N}_G{G}_T{T}')
        
    
# EXECUTION ALGORITHM. 
# Results are saved in given directory with name:
#   "gen{nº gen}.out"         if no seed is given
#   "s{seed}_gen{nº gen}.out" in other case

for seed in [i+1 for i in range(10)]:

    # EXECUTION ALGORITHM. 
    # Results are saved in given directory with name:
    #   "gen{nº gen}.out"         if no seed is given
    #   "s{seed}_gen{nº gen}.out" in other case
    MOEAD(ZDT3_GOALS, ZDT3_SS, N, G, T, eop=eop, outputDirPath=outputDirPath, seed=seed);
    
    # Results PLOT
    for generation in range(G):
        data = np.genfromtxt(f"{outputDirPath}/s{seed}_gen{generation}.out", delimiter='\t')
        plt.scatter(data[:,0], data[:,1], s=1, c=[colors[generation].rgb for _ in range(N)], cmap='gray')
    
    # PLOT ZDT3 REAL PARETO FRONT
    plt.scatter(ZDT3_PF_x, ZDT3_PF_y, s=1, c='black', alpha=0.3)
    
#  Plot title, axis labels and grid
    plt.title(f"Development ZDT3_{eop.__name__}_N{N}_G{G}_T{T}_s{seed}")
    plt.xlabel('$f_1$')
    plt.ylabel('$f_2$')
    plt.grid()
    plt.savefig(f"{plotsDirPath}/s{seed}_dev.png")
    plt.show()



#%%
'''
#############################
# PROOF 1.2: MOEA/D + EOP2 #
#############################
'''

# MOEA PARAMETERS
N = 200; G = 50; T=20; eop=EOP2

# Color gradient for plots
colors = list(colour.Color("blue").range_to(colour.Color("red"),G))

# FILES 
outputDirPath, plotsDirPath = prepareDir(f'results_ZDT3_{eop.__name__}_N{N}_G{G}_T{T}')
        
    
# EXECUTION ALGORITHM. 
# Results are saved in given directory with name:
#   "gen{nº gen}.out"         if no seed is given
#   "s{seed}_gen{nº gen}.out" in other case

for seed in [i+1 for i in range(10)]:

    # EXECUTION ALGORITHM. 
    # Results are saved in given directory with name:
    #   "gen{nº gen}.out"         if no seed is given
    #   "s{seed}_gen{nº gen}.out" in other case
    MOEAD(ZDT3_GOALS, ZDT3_SS, N, G, T, eop=eop, outputDirPath=outputDirPath, seed=seed);
    
    # Results PLOT
    for generation in range(G):
        data = np.genfromtxt(f"{outputDirPath}/s{seed}_gen{generation}.out", delimiter='\t')
        plt.scatter(data[:,0], data[:,1], s=1, c=[colors[generation].rgb for _ in range(N)], cmap='gray')
    
    # PLOT ZDT3 REAL PARETO FRONT
    plt.scatter(ZDT3_PF_x, ZDT3_PF_y, s=1, c='black', alpha=0.3)
    
#  Plot title, axis labels and grid
    plt.title(f"Development ZDT3_{eop.__name__}_N{N}_G{G}_T{T}_s{seed}")
    plt.xlabel('$f_1$')
    plt.ylabel('$f_2$')
    plt.grid()
    plt.savefig(f"{plotsDirPath}/s{seed}_dev.png")
    plt.show()

#%%
'''
#############################
# PROOF 1.3: MOEA/D + EOP3 #
#############################
'''

# MOEA PARAMETERS
N = 100; G = 100; T=8; eop=EOP3

# Color gradient for plots
colors = list(colour.Color("blue").range_to(colour.Color("red"),G))

# FILES 
outputDirPath, plotsDirPath = prepareDir(f'results_ZDT3_{eop.__name__}_N{N}_G{G}_T{T}')
        
    
# EXECUTION ALGORITHM. 
# Results are saved in given directory with name:
#   "gen{nº gen}.out"         if no seed is given
#   "s{seed}_gen{nº gen}.out" in other case

for seed in [i+1 for i in range(10)]:

    # EXECUTION ALGORITHM. 
    # Results are saved in given directory with name:
    #   "gen{nº gen}.out"         if no seed is given
    #   "s{seed}_gen{nº gen}.out" in other case
    MOEAD(ZDT3_GOALS, ZDT3_SS, N, G, T, eop=eop, outputDirPath=outputDirPath, seed=seed);
    
    # Results PLOT
    for generation in range(G):
        data = np.genfromtxt(f"{outputDirPath}/s{seed}_gen{generation}.out", delimiter='\t')
        plt.scatter(data[:,0], data[:,1], s=1, c=[colors[generation].rgb for _ in range(N)], cmap='gray')
    
    # PLOT ZDT3 REAL PARETO FRONT
    plt.scatter(ZDT3_PF_x, ZDT3_PF_y, s=1, c='black', alpha=0.3)
    
#  Plot title, axis labels and grid
    plt.title(f"Development ZDT3_{eop.__name__}_N{N}_G{G}_T{T}_s{seed}")
    plt.xlabel('$f_1$')
    plt.ylabel('$f_2$')
    plt.grid()
    plt.savefig(f"{plotsDirPath}/s{seed}_dev.png")
    plt.show()
