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
ZDT3_PF_x = np.concatenate((np.linspace(0, 0.0830015349, num=100), 
                        np.linspace(0.1822287281, 0.2577623634, num=100),
                        np.linspace(0.4093136749,0.45388221041, num=100),
                        np.linspace(0.6183967945,0.6525117038, num=100),
                        np.linspace(0.8233317984, 0.8518328654, num=100))
                      )

ZDT3_PF_y = np.vectorize(lambda x: 1 - np.sqrt(x) - x*np.sin(10*np.pi*x))(ZDT3_PF_x)

#%%
'''
###############################################
# DIRECTORY PREPARING FOR RESULTS AND PLOTS #
##############################################
'''
def prepareDir(path):
    completePath = ""
    for p in path.split("/"):
        completePath += p + "/"
        if not(os.path.isdir(completePath)):
            os.mkdir(completePath)
    os.mkdir(completePath + "outputs")
    os.mkdir(completePath + "plots")
    return completePath + "outputs", completePath + "plots"

#%%
'''
#######################################
# PROOF 1.1: MOEA/D + EOP1 (N40G100) #
#######################################
'''

# MOEA PARAMETERS
N =40; G =100; T=6; eop=EOP1

# Color gradient for plots
colors = list(colour.Color("blue").range_to(colour.Color("red"),G))

# FILES 
outputDirPath, plotsDirPath = prepareDir(f'MOEA_D_{eop.__name__}/ZDT3/EVAL4000/N{N}_G{G}_T{T}')
        
    
# EXECUTION ALGORITHM. 
# Results are saved in given directory with name:
#   "gen{nº gen}.out"         if no seed is given
#   "s{seed}_gen{nº gen}.out" in other case

for seed in [i+1 for i in range(9)]+[99]:

    # EXECUTION ALGORITHM. 
    # Results are saved in given directory with name:
    #   "gen{nº gen}.out"         if no seed is given
    #   "s{seed}_gen{nº gen}.out" in other case
    MOEAD(ZDT3_GOALS, ZDT3_SS, N, G, T, eop=eop, outputDirPath=outputDirPath, seed=seed);
    
    
    ####################################
    # PLOT DEVELOPMENT ALL GENERATIONS #
    ####################################
    
    # PLOT ZDT3 REAL PARETO FRONT
    plt.scatter(ZDT3_PF_x, ZDT3_PF_y, s=1, c='black')
    
    # Results PLOT
    for generation in range(G):
        data = np.genfromtxt(f"{outputDirPath}/s{seed}_gen{generation}.out", delimiter='\t')
        plt.scatter(data[:,0], data[:,1], s=1, c=[colors[generation].rgb for _ in range(N)])
    
    # Plot title, axis labels and grid
    plt.title(f"Development ZDT3_{eop.__name__}_N{N}_G{G}_T{T}_s{seed}")
    plt.xlabel('$f_1$')
    plt.ylabel('$f_2$')
    plt.grid()
    plt.savefig(f"{plotsDirPath}/s{seed}_dev.png")
    plt.show()
    
    ################################
    # PLOT NON DOMINATED SOLUTIONS #
    ################################
    
     # PLOT ZDT3 REAL PARETO FRONT
    plt.scatter(ZDT3_PF_x, ZDT3_PF_y, s=1, c='black')
    
    # MOEA NDS
    data = np.genfromtxt(f"{outputDirPath}/s{seed}_nds.out", delimiter='\t')
    plt.scatter(data[:,0], data[:,1], s=1, c='red')
    
    
#  Plot title, axis labels and grid
    plt.title(f"NDS ZDT3_{eop.__name__}_N{N}_G{G}_T{T}_s{seed}")
    plt.xlabel('$f_1$')
    plt.ylabel('$f_2$')
    plt.grid()
    plt.savefig(f"{plotsDirPath}/s{seed}_nds.png")
    plt.show()
    
    #############################################
    # PLOT MOVEA/D FINAL GEN VS SGAII FINAL GEN #
    #############################################
    
      # PLOT ZDT3 REAL PARETO FRONT
    plt.scatter(ZDT3_PF_x, ZDT3_PF_y, s=1, c='black')
    
    # MOEA NDS
    data = np.genfromtxt(f"{outputDirPath}/s{seed}_gen{G-1}.out", delimiter='\t')
    plt.scatter(data[:,0], data[:,1], s=1, c='red')
    
    # SGAII final solutions
    data2 = np.genfromtxt(f"NSGAII/EVAL4000/P{N}G{G}/zdt3_final_popp{N}g{G}_seed{'0' + str(seed)}.out", delimiter='\t')
    plt.scatter(data2[:,0], data2[:,1], s=1, c='blue')
    
    
#  Plot title, axis labels and grid
    plt.title(f" MOVEAD VS SGAII (FGEN) ZDT3_{eop.__name__}_N{N}_G{G}_s{seed}")
    plt.xlabel('$f_1$')
    plt.ylabel('$f_2$')
    plt.grid()
    plt.savefig(f"{plotsDirPath}/s{seed}_comp.png")
    plt.show()

#%%
'''
######################################
# PROOF 1.2: MOEA/D + EOP1 (N80G50) #
######################################
'''

# MOEA PARAMETERS
N =80; G =50; T=12; eop=EOP1

# Color gradient for plots
colors = list(colour.Color("blue").range_to(colour.Color("red"),G))

# FILES 
outputDirPath, plotsDirPath = prepareDir(f'MOEA_D_{eop.__name__}/ZDT3/EVAL4000/N{N}_G{G}_T{T}')
        
    
# EXECUTION ALGORITHM. 
# Results are saved in given directory with name:
#   "gen{nº gen}.out"         if no seed is given
#   "s{seed}_gen{nº gen}.out" in other case

for seed in [i+1 for i in range(9)] + [99]:

    # EXECUTION ALGORITHM. 
    # Results are saved in given directory with name:
    #   "gen{nº gen}.out"         if no seed is given
    #   "s{seed}_gen{nº gen}.out" in other case
    MOEAD(ZDT3_GOALS, ZDT3_SS, N, G, T, eop=eop, outputDirPath=outputDirPath, seed=seed);
    
    
    ####################################
    # PLOT DEVELOPMENT ALL GENERATIONS #
    ####################################
    
    # PLOT ZDT3 REAL PARETO FRONT
    plt.scatter(ZDT3_PF_x, ZDT3_PF_y, s=1, c='black')
    
    # Results PLOT
    for generation in range(G):
        data = np.genfromtxt(f"{outputDirPath}/s{seed}_gen{generation}.out", delimiter='\t')
        plt.scatter(data[:,0], data[:,1], s=1, c=[colors[generation].rgb for _ in range(N)])
    
    # Plot title, axis labels and grid
    plt.title(f"Development ZDT3_{eop.__name__}_N{N}_G{G}_T{T}_s{seed}")
    plt.xlabel('$f_1$')
    plt.ylabel('$f_2$')
    plt.grid()
    plt.savefig(f"{plotsDirPath}/s{seed}_dev.png")
    plt.show()
    
    ################################
    # PLOT NON DOMINATED SOLUTIONS #
    ################################
    
     # PLOT ZDT3 REAL PARETO FRONT
    plt.scatter(ZDT3_PF_x, ZDT3_PF_y, s=1, c='black')
    
    # MOEA NDS
    data = np.genfromtxt(f"{outputDirPath}/s{seed}_nds.out", delimiter='\t')
    plt.scatter(data[:,0], data[:,1], s=1, c='red')
    
    
#  Plot title, axis labels and grid
    plt.title(f"NDS ZDT3_{eop.__name__}_N{N}_G{G}_T{T}_s{seed}")
    plt.xlabel('$f_1$')
    plt.ylabel('$f_2$')
    plt.grid()
    plt.savefig(f"{plotsDirPath}/s{seed}_nds.png")
    plt.show()
    
    #############################################
    # PLOT MOVEA/D FINAL GEN VS SGAII FINAL GEN #
    #############################################
    
      # PLOT ZDT3 REAL PARETO FRONT
    plt.scatter(ZDT3_PF_x, ZDT3_PF_y, s=1, c='black')
    
    # MOEA NDS
    data = np.genfromtxt(f"{outputDirPath}/s{seed}_gen{G-1}.out", delimiter='\t')
    plt.scatter(data[:,0], data[:,1], s=1, c='red')
    
    # SGAII final solutions
    data2 = np.genfromtxt(f"NSGAII/EVAL4000/P{N}G{G}/zdt3_final_popp{N}g{G}_seed{'0' + str(seed)}.out", delimiter='\t')
    plt.scatter(data2[:,0], data2[:,1], s=1, c='blue')
    
    
#  Plot title, axis labels and grid
    plt.title(f" MOVEAD VS SGAII (FGEN) ZDT3_{eop.__name__}_N{N}_G{G}_s{seed}")
    plt.xlabel('$f_1$')
    plt.ylabel('$f_2$')
    plt.grid()
    plt.savefig(f"{plotsDirPath}/s{seed}_comp.png")
    plt.show()
    
#%%
'''
######################################
# PROOF 1.3: MOEA/D + EOP1 (N100G40) #
######################################
'''

# MOEA PARAMETERS
N =100; G = 40; T=15; eop=EOP1

# Color gradient for plots
colors = list(colour.Color("blue").range_to(colour.Color("red"),G))

# FILES 
outputDirPath, plotsDirPath = prepareDir(f'MOEA_D_{eop.__name__}/ZDT3/EVAL4000/N{N}_G{G}_T{T}')
        
    
# EXECUTION ALGORITHM. 
# Results are saved in given directory with name:
#   "gen{nº gen}.out"         if no seed is given
#   "s{seed}_gen{nº gen}.out" in other case

for seed in [i+1 for i in range(9)] + [99]:

    # EXECUTION ALGORITHM. 
    # Results are saved in given directory with name:
    #   "gen{nº gen}.out"         if no seed is given
    #   "s{seed}_gen{nº gen}.out" in other case
    MOEAD(ZDT3_GOALS, ZDT3_SS, N, G, T, eop=eop, outputDirPath=outputDirPath, seed=seed);
    
    
    ####################################
    # PLOT DEVELOPMENT ALL GENERATIONS #
    ####################################
    
    # PLOT ZDT3 REAL PARETO FRONT
    plt.scatter(ZDT3_PF_x, ZDT3_PF_y, s=1, c='black')
    
    # Results PLOT
    for generation in range(G):
        data = np.genfromtxt(f"{outputDirPath}/s{seed}_gen{generation}.out", delimiter='\t')
        plt.scatter(data[:,0], data[:,1], s=1, c=[colors[generation].rgb for _ in range(N)])
    
    # Plot title, axis labels and grid
    plt.title(f"Development ZDT3_{eop.__name__}_N{N}_G{G}_T{T}_s{seed}")
    plt.xlabel('$f_1$')
    plt.ylabel('$f_2$')
    plt.grid()
    plt.savefig(f"{plotsDirPath}/s{seed}_dev.png")
    plt.show()
    
    ################################
    # PLOT NON DOMINATED SOLUTIONS #
    ################################
    
     # PLOT ZDT3 REAL PARETO FRONT
    plt.scatter(ZDT3_PF_x, ZDT3_PF_y, s=1, c='black')
    
    # MOEA NDS
    data = np.genfromtxt(f"{outputDirPath}/s{seed}_nds.out", delimiter='\t')
    plt.scatter(data[:,0], data[:,1], s=1, c='red')
    
    
#  Plot title, axis labels and grid
    plt.title(f"NDS ZDT3_{eop.__name__}_N{N}_G{G}_T{T}_s{seed}")
    plt.xlabel('$f_1$')
    plt.ylabel('$f_2$')
    plt.grid()
    plt.savefig(f"{plotsDirPath}/s{seed}_nds.png")
    plt.show()
    
    #############################################
    # PLOT MOVEA/D FINAL GEN VS SGAII FINAL GEN #
    #############################################
    
      # PLOT ZDT3 REAL PARETO FRONT
    plt.scatter(ZDT3_PF_x, ZDT3_PF_y, s=1, c='black')
    
    # MOEA NDS
    data = np.genfromtxt(f"{outputDirPath}/s{seed}_gen{G-1}.out", delimiter='\t')
    plt.scatter(data[:,0], data[:,1], s=1, c='red')
    
    # SGAII final solutions
    data2 = np.genfromtxt(f"NSGAII/EVAL4000/P{N}G{G}/zdt3_final_popp{N}g{G}_seed{'0' + str(seed)}.out", delimiter='\t')
    plt.scatter(data2[:,0], data2[:,1], s=1, c='blue')
    
    
#  Plot title, axis labels and grid
    plt.title(f" MOVEAD VS SGAII (FGEN) ZDT3_{eop.__name__}_N{N}_G{G}_s{seed}")
    plt.xlabel('$f_1$')
    plt.ylabel('$f_2$')
    plt.grid()
    plt.savefig(f"{plotsDirPath}/s{seed}_comp.png")
    plt.show()
    
#%%
'''
###############################
# PROOF 1.4: COMPARISION ALL #
##############################

'''
# Pi = (N, G, T)
PROOFS = [(40,100,6), (80,50,12), (100,40,15)]

colors = list(colour.Color("blue").range_to(colour.Color("red"), len(PROOFS)))

os.mkdir(f'MOEA_D_{eop.__name__}/ZDT3/EVAL4000/COMPARISION_PLOTS/')

for seed in [i+1 for i in range(9)] + [99]:
    
    # Uncomment if you have not done the tests previously
    # for N,G,T in PROOFS:
    #     outputDirPath = prepareDir(f'MOEA_D_EOP1/ZDT3/EVAL4000/N{N}_G{G}_T{T}')[0]
    #     MOEAD(ZDT3_GOALS, ZDT3_SS, N, G, T, eop=eop, outputDirPath=outputDirPath, seed=seed);
    
    ################################
    # PLOT NON DOMINATED SOLUTIONS #
    ################################
    
    fig, ax = plt.subplots()
    # PLOT ZDT3 REAL PARETO FRONT
    ax.scatter(ZDT3_PF_x, ZDT3_PF_y, s=1, c='black', label='Real PF')
    
    for i, (N,G,T) in enumerate(PROOFS):
        data = np.genfromtxt(f"MOEA_D_{eop.__name__}/ZDT3/EVAL4000/N{N}_G{G}_T{T}/outputs/s{seed}_nds.out", delimiter='\t')
        plt.scatter(data[:,0], data[:,1], s=1, c=[colors[i].rgb for _ in range(data.shape[0])] , label=f'N{N}_G{G}_T{T}')

    ax.set_title(f'COMPARISION N & G s{seed}')
    ax.set_xlabel('$f_1$')
    ax.set_ylabel('$f_2$')
    ax.legend()
    ax.grid(True)
    
    plt.savefig(f'MOEA_D_{eop.__name__}/ZDT3/EVAL4000/COMPARISION_PLOTS/GCOMP_s{seed}.png')
    plt.show()