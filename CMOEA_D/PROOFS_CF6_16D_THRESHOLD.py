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

from ASCEVBIII_THRESHOLD import CMOEAD
import numpy as np                 # Math library
import os
import shutil
import matplotlib as mpl
import matplotlib.pyplot as plt    # Plot library     
from matplotlib.lines import Line2D

#%%
'''
###############################################
# ZDT3: GOALS, SEARCH SPACE AND PARETO FRONT #
##############################################
'''

# GOALS FUNCTIONS
def f1(x):
    n=len(x)
    res = x[0]
    c = 6*np.pi*x[0]
    for j,xj in enumerate(x[1:]):
        if j%2!=0:
            yj =xj - 0.8*x[0]*np.cos(c + np.pi*(j+2)/n)
            res += yj**2
    return res

def f2(x):
    n=len(x)
    res = (1-x[0])**2
    c = 6*np.pi*x[0]
    for j,xj in enumerate(x[1:]):
        if j%2==0:
            yj =xj - 0.8*x[0]*np.sin(c + (np.pi*(j+2)/n))
            res += yj**2
    return res

C1 = lambda x: x[1] - 0.8*x[0]*np.sin(6*np.pi*x[0] + ((2*np.pi)/(len(x)))) - np.sign(0.5*(1-x[0]) - (1-x[0])**2)*np.sqrt(np.abs(0.5*(1-x[0]) - (1-x[0])**2))
C2 = lambda x: x[3] - 0.8*x[0]*np.sin(6*np.pi*x[0] + ((4*np.pi)/(len(x)))) - np.sign(0.25*np.sqrt(1-x[0]) - 0.5*(1-x[0]))*np.sqrt(np.abs(0.25*np.sqrt(1-x[0]) - 0.5*(1-x[0])))

 
GOALS = [f1, f2]
CONSTRAINTS = [C1, C2]

# SEARCH SPACE
CF616D_SS = [(0,1)]+[(-2,2) for _ in range(15)]

# REAL PARETO FRONT
CF6_PF_x = [np.linspace(0, 0.5, num=1000, endpoint=False), 
                        np.linspace(0.5, 0.75, num=500, endpoint=False),
                        np.linspace(0.75, 1, num=500)]

CF6_PF_y= [np.vectorize(lambda f1: (1-f1)**2)(CF6_PF_x[0]), 
    np.vectorize(lambda f1: 0.5*(1-f1))(CF6_PF_x[1]), 
    np.vectorize(lambda f1: 0.25*np.sqrt(1-f1))(CF6_PF_x[2])]

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
    
    if  os.path.isdir(completePath + "plots"):
        shutil.rmtree(completePath + "plots")
    os.mkdir(completePath + "plots")
    return completePath + "outputs", completePath + "plots"


plotColor1 = np.vectorize(lambda x: 'red' if x else 'green')
plotColor2 = np.vectorize(lambda x: 'purple' if x else 'gold')
plotColor3 = np.vectorize(lambda x: 'fuchsia' if x else 'turquoise')

#%%
'''
#######################################
# PROOF 1.1: MOEA/D + EOP1 (N100G100) #
#######################################
'''

# MOEA PARAMETERS
#N =100; G =100; T=(15*N//100)
#N =40; G =250; T=(15*N//100)
#N =200; G =50; T=(15*N//100)

#N =40; G =100; T=(15*N//100)
#N =80; G =50; T=(15*N//100)
#N =100; G =40; T=(15*N//100)

for N,G in [(100, 100), (40,250),(200,50),(40,100),(80,50),(100,40)]:
    T=(12*N)//100    
    # Color gradient for plots
    colors = plt.get_cmap('jet',G)
    
    # FILES 
    outputDirPath, plotsDirPath = prepareDir(f'CMOEAD_THRES/CF6_16D/EVAL{N*G}/N{N}_G{G}_T{T}')
            
        
    # EXECUTION ALGORITHM. 
    # Results are saved in given directory with name:
    #   "gen{nº gen}.out"         if no seed is given
    #   "s{seed}_gen{nº gen}.out" in other case
    
    for seed in list(range(1,10))+[99]:
    
        # EXECUTION ALGORITHM. 
        # Results are saved in given directory with name:
        #   "gen{nº gen}.out"         if no seed is given
        #   "s{seed}_gen{nº gen}.out" in other case
        CMOEAD(GOALS, CONSTRAINTS, CF616D_SS, N, G, T, updationsNumber=(2*N)//100, outputDirPath=outputDirPath, seed=seed);
        
        
        ####################################
        # PLOT DEVELOPMENT ALL GENERATIONS #
        ####################################
        
        fig, ax1 = plt.subplots()
        
        # PLOT CF6 REAL PARETO FRONT
        ax1.scatter(CF6_PF_x[0], CF6_PF_y[0], s=1, color='black')
        ax1.scatter(CF6_PF_x[1], CF6_PF_y[1], s=1, color='black')
        ax1.scatter(CF6_PF_x[2], CF6_PF_y[2], s=1, color='black')
        
        
        # We plot the the population of each generation to check the development
        for generation in range(G):
            data = np.genfromtxt(f"{outputDirPath}/s{seed}_gen{generation}.out", delimiter='\t')
            ax1.scatter(data[:,0], data[:,1], c=[colors(generation) for _ in range(N)], s=1, marker = '.') 
           
       
        norm = mpl.colors.Normalize(vmin=0,vmax=G)
        sm = plt.cm.ScalarMappable(cmap=colors, norm=norm)
        sm.set_array([])
        cbar= fig.colorbar(sm, ticks=np.linspace(0,G,5), 
                  boundaries=np.arange(0,G+1,5), orientation='vertical', format='%1i')
        cbar.set_label('number of generation', rotation=90, fontsize=8)
        # Plot title, axis labels and grid
        fig.suptitle(f"Development (Conv) CF616D_PENAL_N{N}_G{G}_T{T}_s{seed}\n")
        plt.subplots_adjust(left=0.125,
                        bottom=0.125, 
                        right=0.9, 
                        top=0.9, 
                        wspace=0.35, 
                        hspace=0.35)
        
        ax1.set_xlabel('$f_1$', fontsize=11)
        ax1.set_ylabel('$f_2$', fontsize=11)
        ax1.grid(True)
        fig.savefig(f"{plotsDirPath}/s{seed}_devI.png", dpi=600)
        plt.clf(); plt.close()
        
        fig, ax1 = plt.subplots()
        
        # PLOT CF6 REAL PARETO FRONT
        ax1.scatter(CF6_PF_x[0], CF6_PF_y[0], s=1, color='black')
        ax1.scatter(CF6_PF_x[1], CF6_PF_y[1], s=1, color='black')
        ax1.scatter(CF6_PF_x[2], CF6_PF_y[2], s=1, color='black')
        
        # We plot the the population of each generation to check the development
        for generation in range(G):
            data = np.genfromtxt(f"{outputDirPath}/s{seed}_gen{generation}.out", delimiter='\t')
            ax1.scatter(data[:,0], data[:,1], c=plotColor1(data[:,2]), s=1, marker = '.')
           
       
        # Plot title, axis labels and grid
        fig.suptitle(f"Development (Feas) CF616D_PENAL_N{N}_G{G}_T{T}_s{seed}\n")
        plt.subplots_adjust(left=0.125,
                        bottom=0.125, 
                        right=0.9, 
                        top=0.9, 
                        wspace=0.35, 
                        hspace=0.35)
        
     
        ax1.set_xlabel('$f_1$', fontsize=11)
        ax1.set_ylabel('$f_2$', fontsize=11)
        
        legend_elements_ax1 = [  
             Line2D([0], [0], marker='o', color='w', label='feasible',
                              markerfacecolor='g', markersize=5),
             Line2D([0], [0], marker='o', color='w', label='infeasible',
                              markerfacecolor='r', markersize=5),
            ]
        ax1.legend(handles=legend_elements_ax1)
        ax1.grid(True)
        fig.savefig(f"{plotsDirPath}/s{seed}_devII.png", dpi=600)
        plt.clf(); plt.close()
        
        ################################
        # PLOT NON DOMINATED SOLUTIONS #
        ################################
        
        fig, ax1 = plt.subplots()
        
        # PLOT ZDT3 REAL PARETO FRONT
        ax1.scatter(CF6_PF_x[0], CF6_PF_y[0], s=1, color='black')
        ax1.scatter(CF6_PF_x[1], CF6_PF_y[1], s=1, color='black')
        ax1.scatter(CF6_PF_x[2], CF6_PF_y[2], s=1, color='black')
        
        # MOEA NDS
        data = np.genfromtxt(f"{outputDirPath}/s{seed}_nds.out", delimiter='\t')
        ax1.scatter(data[:,0], data[:,1], s=1, c=plotColor1(data[:,2]))
        
        
        #  Plot title, axis labels and grid
        legend_elements = [  
              Line2D([0], [0], marker='o', color='w', label='feasible',
                              markerfacecolor='g', markersize=5),
              Line2D([0], [0], marker='o', color='w', label='infeasible',
                              markerfacecolor='r', markersize=5),
            ]
        ax1.legend(handles=legend_elements)
        fig.suptitle(f"NDS CF616D_CMOEAD_PENAL_N{N}_G{G}_T{T}_s{seed}\n")
        ax1.set_xlabel('$f_1$', fontsize=11)
        ax1.set_ylabel('$f_2$', fontsize=11)
        ax1.grid(True)
        plt.subplots_adjust(left=0.125,
                        bottom=0.125, 
                        right=0.9, 
                        top=0.9, 
                        wspace=0.35, 
                        hspace=0.35)
        fig.savefig(f"{plotsDirPath}/s{seed}_nds.png", dpi=600)
        plt.clf(); plt.close()
        
        #############################################
        # PLOT MOVEA/D FINAL GEN VS SGAII FINAL GEN #
        ##########################
        ###################
        fig, ax1 = plt.subplots()
        # PLOT ZDT3 REAL PARETO FRONT
        ax1.scatter(CF6_PF_x[0], CF6_PF_y[0], s=1, color='black')
        ax1.scatter(CF6_PF_x[1], CF6_PF_y[1], s=1, color='black')
        ax1.scatter(CF6_PF_x[2], CF6_PF_y[2], s=1, color='black')
        
        # MOEA/D LAST GENERATION
        data = np.genfromtxt(f"{outputDirPath}/s{seed}_gen{G-1}.out", delimiter='\t')
        ax1.scatter(data[:,0], data[:,1], s=1, c=plotColor1(data[:,2]))
        
        # SGAII final solutions
        data2 = np.genfromtxt(f"NSGAII/CF6_16D/EVAL{N*G}/P{N}G{G}/cf6_16d_all_popmp{N}g{G}_seed{'0' + str(seed)}.out", delimiter='\t')
        ax1.scatter(data2[-N:,0], data2[-N:,1], s=1, c=plotColor2(data2[-N:,2]))
        
        
    #  Plot title, axis labels and grid
        legend_elements = [  
             Line2D([0], [0], marker='o', color='w', label='feas. CMOEA/D',
                              markerfacecolor='g', markersize=5),
             Line2D([0], [0], marker='o', color='w', label='infeas. CMOEA/D',
                              markerfacecolor='r', markersize=5),
             Line2D([0], [0], marker='o', color='w', label='feas. NSGAII',
                              markerfacecolor='gold', markersize=5),
             Line2D([0], [0], marker='o', color='w', label='infeas. NSGAII',
                              markerfacecolor='purple', markersize=5)]
        ax1.legend(handles=legend_elements)
        fig.suptitle(f" CMOVEAD_PENAL VS SGAII (FGEN) CF616D_N{N}_G{G}_s{seed}\n")
        ax1.set_xlabel('$f_1$', fontsize=11)
        ax1.set_ylabel('$f_2$', fontsize=11)
        ax1.grid(True)
        plt.subplots_adjust(left=0.125,
                        bottom=0.125, 
                        right=0.9, 
                        top=0.9, 
                        wspace=0.35, 
                        hspace=0.35)
        fig.savefig(f"{plotsDirPath}/s{seed}_comp.png", dpi=600)
        plt.clf(); plt.close()

plotColors= [plotColor1, plotColor2, plotColor3]
# = np.vectorize(lambda x: 'red' if x else 'green')
# plotColor2 = np.vectorize(lambda x: 'purple' if x else 'gold')
# plotColor3 = np.vectorize(lambda x: 'fuchsia' if x else 'turquoise')

PROOFS = [(100, 100), (40,250),(200,50)]

for seed in list(range(9)) + [98]:
    fig, ax1 = plt.subplots()
    ax1.scatter(CF6_PF_x[0], CF6_PF_y[0], s=1, color='black')
    ax1.scatter(CF6_PF_x[1], CF6_PF_y[1], s=1, color='black')
    ax1.scatter(CF6_PF_x[2], CF6_PF_y[2], s=1, color='black')
    for i, (N,G) in enumerate(PROOFS):
        T = T=(10*N)//100
        data = np.genfromtxt(f"CMOEAD_THRES/CF6_16D/EVAL{N*G}/N{N}_G{G}_T{T}/outputs/s{seed+1}_gen{G-1}.out", delimiter='\t')
        ax1.scatter(data[:,0], data[:,1], c=plotColors[i](data[:,2]), s=1, marker = '.')
    
    legend_elements = [  
          Line2D([0], [0], marker='o', color='w', label='feas. N100G100',
                          markerfacecolor='green', markersize=5),
          Line2D([0], [0], marker='o', color='w', label='infeas. N100G100',
                          markerfacecolor='red', markersize=5),
          Line2D([0], [0], marker='o', color='w', label='feas. N40G250',
                          markerfacecolor='gold', markersize=5),
          Line2D([0], [0], marker='o', color='w', label='infeas. N40G250',
                          markerfacecolor='purple', markersize=5),
          Line2D([0], [0], marker='o', color='w', label='feas. N200G50',
                          markerfacecolor='turquoise', markersize=5),
          Line2D([0], [0], marker='o', color='w', label='infeas. N200G50',
                          markerfacecolor='fuchsia', markersize=5)]
    ax1.legend(handles=legend_elements)
    fig.suptitle(f" CMOVEAD COMPARISION FGEN CF6_16D 10000EV s{seed+1}\n")
    ax1.set_xlabel('$f_1$', fontsize=11)
    ax1.set_ylabel('$f_2$', fontsize=11)
    ax1.grid(True)
    plt.subplots_adjust(left=0.125,
                    bottom=0.125, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.35, 
                    hspace=0.35)
    if not(os.path.isdir(f"CMOEAD_THRES/CF6_16D/EVAL10000/COMP_PLOTS")):
        os.mkdir(f"CMOEAD_THRES/CF6_16D/EVAL10000/COMP_PLOTS")
    fig.savefig(f"CMOEAD_THRES/CF6_16D/EVAL10000/COMP_PLOTS/s{seed+1}_FGEN.png", dpi=600)
    plt.clf(); plt.close()
    
    
    fig, ax1 = plt.subplots()
    ax1.scatter(CF6_PF_x[0], CF6_PF_y[0], s=1, color='black')
    ax1.scatter(CF6_PF_x[1], CF6_PF_y[1], s=1, color='black')
    ax1.scatter(CF6_PF_x[2], CF6_PF_y[2], s=1, color='black')
    for i, (N,G) in enumerate(PROOFS):
        T = T=(10*N)//100
        data = np.genfromtxt(f"CMOEAD_THRES/CF6_16D/EVAL{N*G}/N{N}_G{G}_T{T}/outputs/s{seed+1}_nds.out", delimiter='\t')
        ax1.scatter(data[:,0], data[:,1], c=plotColors[i](data[:,2]), s=1, marker = '.', alpha=0.5)
    
    legend_elements = [  
          Line2D([0], [0], marker='o', color='w', label='feas. N100G100',
                          markerfacecolor='green', markersize=5),
          Line2D([0], [0], marker='o', color='w', label='infeas. N100G100',
                          markerfacecolor='red', markersize=5),
          Line2D([0], [0], marker='o', color='w', label='feas. N40G250',
                          markerfacecolor='gold', markersize=5),
          Line2D([0], [0], marker='o', color='w', label='infeas. N40G250',
                          markerfacecolor='purple', markersize=5),
          Line2D([0], [0], marker='o', color='w', label='feas. N200G50',
                          markerfacecolor='turquoise', markersize=5),
          Line2D([0], [0], marker='o', color='w', label='infeas. N200G50',
                          markerfacecolor='fuchsia', markersize=5)]
    ax1.legend(handles=legend_elements)
    fig.suptitle(f" CMOVEAD COMPARISION NDS CF6_16D 10000EV s{seed+1}\n")
    ax1.set_xlabel('$f_1$', fontsize=11)
    ax1.set_ylabel('$f_2$', fontsize=11)
    ax1.grid(True)
    plt.subplots_adjust(left=0.125,
                    bottom=0.125, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.35, 
                    hspace=0.35)
    if not(os.path.isdir(f"CMOEAD_THRES/CF6_16D/EVAL10000/COMP_PLOTS")):
        os.mkdir(f"CMOEAD_THRES/CF6_16D/EVAL10000/COMP_PLOTS")
    fig.savefig(f"CMOEAD_THRES/CF6_16D/EVAL10000/COMP_PLOTS/s{seed+1}_NDS.png", dpi=600)
    plt.clf(); plt.close()