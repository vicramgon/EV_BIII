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
from ASCEVBIII import EOP2, MOEAD
import numpy as np                 # Math library
import os
import shutil
import matplotlib as mpl
import matplotlib.pyplot as plt    # Plot library                  

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
    if  os.path.isdir(completePath + "outputs"):
        shutil.rmtree(completePath + "outputs")
    os.mkdir(completePath + "outputs")
    
    # if  os.path.isdir(completePath + "plots"):
    #     shutil.rmtree(completePath + "plots")
    # os.mkdir(completePath + "plots")
    return completePath + "outputs" #completePath + "plots"

#%%
'''
#######################################
# PROOF 1.1: MOEA/D + EOP2 (N100G100) #
#######################################
'''

# MOEA PARAMETERS
N =80; G =50; T=12; eop=EOP2

# Color gradient for plots
colors = plt.get_cmap('jet',G)

# FILES 
outputDirPath = prepareDir(f'MOEA_D_{eop.__name__}/ZDT3/EVAL4000/N{N}_G{G}_T{T}')
plotsDirPath = f"EV_BIII_ASC_doc/figures/ZDT3_{eop.__name__}_N{N}_G{G}_T{T}"

if os.path.isdir(plotsDirPath):
    shutil.rmtree(plotsDirPath)
os.mkdir(plotsDirPath)


        
    
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
    plt.scatter(ZDT3_PF_x, ZDT3_PF_y, s=1, c='darkgray')
    
    # We plot the the population of each generation to check the development
    for generation in range(G):
        data = np.genfromtxt(f"{outputDirPath}/s{seed}_gen{generation}.out", delimiter='\t')  
        plt.scatter(data[:,0], data[:,1], s=1, c=[colors(generation) for _ in range(N)])
   
    norm = mpl.colors.Normalize(vmin=0,vmax=G)
    sm = plt.cm.ScalarMappable(cmap=colors, norm=norm)
    sm.set_array([])
    cbar= plt.colorbar(sm, ticks=np.linspace(0,G,5), 
             boundaries=np.arange(0,G+1,5), orientation='vertical', format='%1i')
    cbar.set_label('number of generation', rotation=90, fontsize=8)
    # Plot title, axis labels and grid
    plt.title(f"Development ZDT3_{eop.__name__}_N{N}_G{G}_T{T}_s{seed}\n")
    plt.xlabel('$f_1$', fontsize=11)
    plt.ylabel('$f_2$', fontsize=11)
    plt.grid()
    plt.savefig(f"{plotsDirPath}/s{seed}_dev.png", dpi=200)
    plt.clf()
    
    ################################
    # PLOT NON DOMINATED SOLUTIONS #
    ################################
    
    # PLOT ZDT3 REAL PARETO FRONT
    plt.scatter(ZDT3_PF_x, ZDT3_PF_y, s=1, c='darkgray', label='Real PF')
    
    # MOEA NDS
    data = np.genfromtxt(f"{outputDirPath}/s{seed}_nds.out", delimiter='\t')
    plt.scatter(data[:,0], data[:,1], s=1, c='red', label='NDS Set')
    
    
    #  Plot title, axis labels and grid
    plt.legend()
    plt.title(f"NDS ZDT3_{eop.__name__}_N{N}_G{G}_T{T}_s{seed}\n")
    plt.xlabel('$f_1$', fontsize=11)
    plt.ylabel('$f_2$', fontsize=11)
    plt.grid()
    plt.savefig(f"{plotsDirPath}/s{seed}_nds.png", dpi=200)
    plt.clf()
    
    #############################################
    # PLOT MOVEA/D FINAL GEN VS SGAII FINAL GEN #
    #############################################
    
    # PLOT ZDT3 REAL PARETO FRONT
    plt.scatter(ZDT3_PF_x, ZDT3_PF_y, s=1, c='darkgray', label='Real PF')
    
    # MOEA/D LAST GENERATION
    data = np.genfromtxt(f"{outputDirPath}/s{seed}_gen{G-1}.out", delimiter='\t')
    plt.scatter(data[:,0], data[:,1], s=1, c='red', label="MOVEA/D")
    
    # SGAII final solutions
    data2 = np.genfromtxt(f"NSGAII/EVAL4000/P{N}G{G}/zdt3_final_popp{N}g{G}_seed{'0' + str(seed)}.out", delimiter='\t')
    plt.scatter(data2[:,0], data2[:,1], s=1, c='blue', label="NSGAII")
    
    
#  Plot title, axis labels and grid
    plt.legend()
    plt.title(f" MOVEAD VS SGAII (FGEN) ZDT3_{eop.__name__}_N{N}_G{G}_s{seed}\n")
    plt.xlabel('$f_1$', fontsize=11)
    plt.ylabel('$f_2$', fontsize=11)
    plt.grid()
    plt.savefig(f"{plotsDirPath}/s{seed}_comp.png", dpi=200)
    plt.clf()

#%%
'''
######################################
# PROOF 1.2: MOEA/D + EOP2 (N40G250) #
######################################
'''

# MOEA PARAMETERS
N =40; G =100; T=6; eop=EOP2
# Color gradient for plots
colors = plt.get_cmap('jet',G)

# FILES 
outputDirPath = prepareDir(f'MOEA_D_{eop.__name__}/ZDT3/EVAL4000/N{N}_G{G}_T{T}')
plotsDirPath = f"EV_BIII_ASC_doc/figures/ZDT3_{eop.__name__}_N{N}_G{G}_T{T}"

if os.path.isdir(plotsDirPath):
    shutil.rmtree(plotsDirPath)
os.mkdir(plotsDirPath)
        
    
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
    plt.scatter(ZDT3_PF_x, ZDT3_PF_y, s=1, c='darkgray')
    
    # We plot the the population of each generation to check the development
    for generation in range(G):
        data = np.genfromtxt(f"{outputDirPath}/s{seed}_gen{generation}.out", delimiter='\t')  
        plt.scatter(data[:,0], data[:,1], s=1, c=[colors(generation) for _ in range(N)])
   
    norm = mpl.colors.Normalize(vmin=0,vmax=G)
    sm = plt.cm.ScalarMappable(cmap=colors, norm=norm)
    sm.set_array([])
    cbar= plt.colorbar(sm, ticks=np.linspace(0,G,5), 
             boundaries=np.arange(0,G+1,5), orientation='vertical', format='%1i')
    cbar.set_label('number of generation', rotation=90, fontsize=8)
    # Plot title, axis labels and grid
    plt.title(f"Development ZDT3_{eop.__name__}_N{N}_G{G}_T{T}_s{seed}\n")
    plt.xlabel('$f_1$', fontsize=11)
    plt.ylabel('$f_2$', fontsize=11)
    plt.grid()
    plt.savefig(f"{plotsDirPath}/s{seed}_dev.png", dpi=200)
    plt.clf()
    
    ################################
    # PLOT NON DOMINATED SOLUTIONS #
    ################################
    
    # PLOT ZDT3 REAL PARETO FRONT
    plt.scatter(ZDT3_PF_x, ZDT3_PF_y, s=1, c='darkgray', label='Real PF')
    
    # MOEA NDS
    data = np.genfromtxt(f"{outputDirPath}/s{seed}_nds.out", delimiter='\t')
    plt.scatter(data[:,0], data[:,1], s=1, c='red', label='NDS Set')
    
    
    #  Plot title, axis labels and grid
    plt.legend()
    plt.title(f"NDS ZDT3_{eop.__name__}_N{N}_G{G}_T{T}_s{seed}\n")
    plt.xlabel('$f_1$', fontsize=11)
    plt.ylabel('$f_2$', fontsize=11)
    plt.grid()
    plt.savefig(f"{plotsDirPath}/s{seed}_nds.png", dpi=200)
    plt.clf()
    
    #############################################
    # PLOT MOVEA/D FINAL GEN VS SGAII FINAL GEN #
    #############################################
    
    # PLOT ZDT3 REAL PARETO FRONT
    plt.scatter(ZDT3_PF_x, ZDT3_PF_y, s=1, c='darkgray', label='Real PF')
    
    # MOEA/D LAST GENERATION
    data = np.genfromtxt(f"{outputDirPath}/s{seed}_gen{G-1}.out", delimiter='\t')
    plt.scatter(data[:,0], data[:,1], s=1, c='red', label="MOVEA/D")
    
    # SGAII final solutions
    data2 = np.genfromtxt(f"NSGAII/EVAL4000/P{N}G{G}/zdt3_final_popp{N}g{G}_seed{'0' + str(seed)}.out", delimiter='\t')
    plt.scatter(data2[:,0], data2[:,1], s=1, c='blue', label="NSGAII")
    
    
#  Plot title, axis labels and grid
    plt.legend()
    plt.title(f" MOVEAD VS SGAII (FGEN) ZDT3_{eop.__name__}_N{N}_G{G}_s{seed}\n")
    plt.xlabel('$f_1$', fontsize=11)
    plt.ylabel('$f_2$', fontsize=11)
    plt.grid()
    plt.savefig(f"{plotsDirPath}/s{seed}_comp.png", dpi=200)
    plt.clf()
    
#%%
'''
######################################
# PROOF 1.3: MOEA/D + EOP2 (N200G50) #
######################################
'''

# MOEA PARAMETERS
N =100; G = 40; T=15; eop=EOP2

# Color gradient for plots
colors = plt.get_cmap('jet',G)

# FILES 
outputDirPath = prepareDir(f'MOEA_D_{eop.__name__}/ZDT3/EVAL4000/N{N}_G{G}_T{T}')
plotsDirPath = f"EV_BIII_ASC_doc/figures/ZDT3_{eop.__name__}_N{N}_G{G}_T{T}"

if os.path.isdir(plotsDirPath):
    shutil.rmtree(plotsDirPath)
os.mkdir(plotsDirPath)
        
    
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
    plt.scatter(ZDT3_PF_x, ZDT3_PF_y, s=1, c='darkgray')
    
    # We plot the the population of each generation to check the development
    for generation in range(G):
        data = np.genfromtxt(f"{outputDirPath}/s{seed}_gen{generation}.out", delimiter='\t')  
        plt.scatter(data[:,0], data[:,1], s=1, c=[colors(generation) for _ in range(N)])
   
    norm = mpl.colors.Normalize(vmin=0,vmax=G)
    sm = plt.cm.ScalarMappable(cmap=colors, norm=norm)
    sm.set_array([])
    cbar= plt.colorbar(sm, ticks=np.linspace(0,G,5), 
             boundaries=np.arange(0,G+1,5), orientation='vertical', format='%1i')
    cbar.set_label('number of generation', rotation=90, fontsize=8)
    # Plot title, axis labels and grid
    plt.title(f"Development ZDT3_{eop.__name__}_N{N}_G{G}_T{T}_s{seed}\n")
    plt.xlabel('$f_1$', fontsize=11)
    plt.ylabel('$f_2$', fontsize=11)
    plt.grid()
    plt.savefig(f"{plotsDirPath}/s{seed}_dev.png", dpi=200)
    plt.clf()
    
    ################################
    # PLOT NON DOMINATED SOLUTIONS #
    ################################
    
    # PLOT ZDT3 REAL PARETO FRONT
    plt.scatter(ZDT3_PF_x, ZDT3_PF_y, s=1, c='darkgray', label='Real PF')
    
    # MOEA NDS
    data = np.genfromtxt(f"{outputDirPath}/s{seed}_nds.out", delimiter='\t')
    plt.scatter(data[:,0], data[:,1], s=1, c='red', label='NDS Set')
    
    
    #  Plot title, axis labels and grid
    plt.legend()
    plt.title(f"NDS ZDT3_{eop.__name__}_N{N}_G{G}_T{T}_s{seed}\n")
    plt.xlabel('$f_1$', fontsize=11)
    plt.ylabel('$f_2$', fontsize=11)
    plt.grid()
    plt.savefig(f"{plotsDirPath}/s{seed}_nds.png", dpi=200)
    plt.clf()
    
    #############################################
    # PLOT MOVEA/D FINAL GEN VS SGAII FINAL GEN #
    #############################################
    
    # PLOT ZDT3 REAL PARETO FRONT
    plt.scatter(ZDT3_PF_x, ZDT3_PF_y, s=1, c='darkgray', label='Real PF')
    
    # MOEA/D LAST GENERATION
    data = np.genfromtxt(f"{outputDirPath}/s{seed}_gen{G-1}.out", delimiter='\t')
    plt.scatter(data[:,0], data[:,1], s=1, c='red', label="MOVEA/D")
    
    # SGAII final solutions
    data2 = np.genfromtxt(f"NSGAII/EVAL4000/P{N}G{G}/zdt3_final_popp{N}g{G}_seed{'0' + str(seed)}.out", delimiter='\t')
    plt.scatter(data2[:,0], data2[:,1], s=1, c='blue', label="NSGAII")
    
    
#  Plot title, axis labels and grid
    plt.legend()
    plt.title(f" MOVEAD VS SGAII (FGEN) ZDT3_{eop.__name__}_N{N}_G{G}_s{seed}\n")
    plt.xlabel('$f_1$', fontsize=11)
    plt.ylabel('$f_2$', fontsize=11)
    plt.grid()
    plt.savefig(f"{plotsDirPath}/s{seed}_comp.png", dpi=200)
    plt.clf()
    
#%%
'''
###############################
# PROOF 1.4: COMPARISION ALL #
##############################

'''
# Pi = (N, G, T)
PROOFS = [(80,50,12), (40,100,6), (100,40,15)]

colors =  plt.get_cmap('jet',len(PROOFS))
if not(os.path.isdir(f'MOEA_D_{eop.__name__}/ZDT3/EVAL4000/COMPARISION_PLOTS/')):
    os.mkdir(f'MOEA_D_{eop.__name__}/ZDT3/EVAL4000/COMPARISION_PLOTS/')

for seed in [i+1 for i in range(9)] + [99]:
    
    # Uncomment if you have not done the tests previously
    # for N,G,T in PROOFS:
    #     outputDirPath = prepareDir(f'MOEA_D_EOP2/ZDT3/EVAL4000/N{N}_G{G}_T{T}')[0]
    #     MOEAD(ZDT3_GOALS, ZDT3_SS, N, G, T, eop=eop, outputDirPath=outputDirPath, seed=seed);
    
    ################################
    # PLOT NON DOMINATED SOLUTIONS #
    ################################
    
    
    # PLOT ZDT3 REAL PARETO FRONT
    plt.scatter(ZDT3_PF_x, ZDT3_PF_y, s=1, c='darkgray', label='Real PF', alpha=0.4)
    
    for i, (N,G,T) in enumerate(PROOFS):
        data = np.genfromtxt(f"MOEA_D_{eop.__name__}/ZDT3/EVAL4000/N{N}_G{G}_T{T}/outputs/s{seed}_nds.out", delimiter='\t')
        plt.scatter(data[:,0], data[:,1], s=1, c=[colors(i) for _ in range(data.shape[0])] , label=f'N{N}_G{G}_T{T}')

    plt.title(f'COMPARISION N & G s{seed}\n')
    plt.xlabel('$f_1$', fontsize=11)
    plt.ylabel('$f_2$', fontsize=11)
    plt.legend()
    plt.grid(True)
    
    plt.savefig(f'MOEA_D_{eop.__name__}/ZDT3/EVAL4000/COMPARISION_PLOTS/GCOMP_s{seed}.png', dpi=200)
    plt.clf()