#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 19:12:22 2021

@author: trialctor
"""

""" 
==============================================================================
               APLICACIONES DE SOFT-COMPUTING
==============================================================================


"""

import numpy as np                 # Math library
import matplotlib.pyplot as plt    # Plot library
import os                          # Create directories
import shutil                      # Delete directories
import colour

def EOP1(cur, P, VP, Bcur, bounds, seed=None, F=0.5, CR=0.5, SIG=20, pm=None):
    np.random.seed(seed)
    # 1) DIFFERENTIAL EVOLUTION MUTATION
    p = P.shape[1]
    PM = 1/p if pm is None else pm
    r = P[np.random.choice(Bcur, 3, replace=False)]
    trial = r[0] + F*(r[1]-r[2])
    
    # 2) DIFFERENTIAL EVOLUTION CROSSING
    delta = np.random.randint(0,p)
    M = np.array([True if np.random.random()<=CR else False for i in range(p)])
    M[delta] = True 
    
    y = M.astype(np.float64)*trial + (~M).astype(np.float64)*P[cur]
    
    # EOP1.3) GAUSSIAN MUTATION 
    for j, yj in enumerate(y):
        if np.random.random() < PM:
            y[j] = min(max(yj+ np.random.normal(0,(bounds[j][1]-bounds[j][0])/SIG),bounds[j][0]),bounds[j][1])
        else:
            y[j] = min(max(yj,bounds[j][0]),bounds[j][1])
    return y

def EOP2(cur, P, VP, Bcur, bounds, seed=None, F=0.5, CR=0.5, pm=None, ETA=10):
    np.random.seed(seed)
    # 1) DIFFERENTIAL EVOLUTION MUTATION
    p = P.shape[1]
    PM = 1/p if pm is None else pm
    r = P[np.random.choice(Bcur, 5, replace=False)]
    trial = r[0] + F*(r[1]-r[2]) + np.random.random()*(r[3]-r[4])
    
    # 2) DIFFERENTIAL EVOLUTION CROSSING
    delta = np.random.randint(0,p)
    M = np.array([True if np.random.random()<=CR else False for i in range(p)])
    M[delta] = True 
    
    y = M.astype(np.float64)*trial + (~M).astype(np.float64)*P[cur]
    
    # SBX MUTATION 
    for j, yj in enumerate(y):
        if np.random.random() < PM :
            mu =  np.random.random()
            sigmaj = (2*mu)**(1/(ETA+1)) if mu < 0.5 else 1 - (2 - 2*mu)**(1/(ETA+1))
            y[j] += sigmaj*(bounds[j][1] - bounds[j][0])
        
        if y[j] < bounds[j][0] or y[j] > bounds[j][1]:
            y[j] = min(max(yj,bounds[j][0]),bounds[j][1])
    return y


def EOP3(cur, P, VP, Bcur, bounds, seed=None, e=2, CR=1, SIG=20, pm=None):
    np.random.seed(seed)
    # 1) DIFFERENTIAL EVOLUTION MUTATION
    
    p = P.shape[1]
    PM = 1/p if pm is None else pm
    r = P[np.random.choice(Bcur, e, replace=False)]
    y = np.array([ r[np.random.randint(0,e)][j] for j in range(p)])
    
    
    # EOP1.3) GAUSSIAN MUTATION 
    for j, yj in enumerate(y):
        if np.random.random() < PM:
            y[j] = min(max(yj+ np.random.normal(0,(bounds[j][1]-bounds[j][0])/SIG),bounds[j][0]),bounds[j][1])
        else:
            y[j] = min(max(yj,bounds[j][0]),bounds[j][1])
    return y
    

def ASCEVBIII(Fgoals, vars_limits, N, G, T, eop=EOP1, seed=None, lambdaInput={'path':'./input/lambdas.csv', 'delimiter':'j'}, outputDirPath='./results'):

    
    ## SETTINGS & PARAMETERS
    if os.path.isdir(outputDirPath):
        shutil.rmtree(outputDirPath)
    os.mkdir(outputDirPath) 
    
    bounds = [sorted(vl) for vl in vars_limits]
    p=len(bounds)
    m=len(Fgoals)
    np.random.seed(seed)
    
    # INITIALIZATION
   
    # We generate N lambda vectors one for each subproblem and calculate
    # the distance between each two.
    L = np.zeros((N, m), dtype=np.float64)
    
    if m == 2:
        for i in range(N):
            L[i] = (1-i/(N-1), i/(N-1))
        del i
    else:
        readedL = np.genfromtxt(lambdaInput['path'], delimiter=lambdaInput['delimiter'])
        L[:,:]= readedL[:N, :m]
        del readedL
        
        
    # We calculates the distances between each pair of lambda vectors
    # and save in into a distance matrix D
    D = np.zeros((N,N), dtype=np.float64)
    for i in range(N):
        for j in range(i):
            dij = np.linalg.norm(L[i]-L[j])
            D[i][j] = dij
            D[j][i] = dij
    del i
    del j
             
    # We calculate the vicinity for each subproblem taking the T nearest
    # lambda vectors to lambda_i
    B = [np.argpartition(D[i], T)[:T] for i in range(N)]
    
    del D
    
    # We generate a random population in which each component of each individual
    # is between the corresponding bounds.
    P = np.random.random([N, p]).astype(np.float64)
    #print(P);
    
    for i, bi in enumerate(bounds):
        P[:,i] = list(map(lambda x: bi[0] + (bi[1] - bi[0])*x, P[:,i]))
    del i
    
    
    VP = np.array([np.apply_along_axis(fi, 1, P) for fi in Fgoals]).transpose()
    
    ## We initialize z vector with the best value of f1 and f2 in the population.
    z = np.apply_along_axis(np.min, 0, VP)
    
    with open(f"{outputDirPath}/gen0.out", "ab") as resFile:
        writeVP = np.zeros([N,m+1])
        writeVP[:,:-1] = VP
        np.savetxt(resFile,writeVP, delimiter="\t", newline='\n', header='', footer='')
    
    for it in range(G-1):     
        order = np.array(range(N))
        np.random.shuffle(order)
        for cur in order:
            # GENERATE CHILD
            y = eop(cur, P, VP, B[cur], bounds, seed)
            vy =  np.array([fi(y) for fi in Fgoals])
            
            # UPDATE Z
            z = np.minimum(z, vy)
            
            for j in B[cur]:
                gtey = np.max([L[j][i]*abs(vy[i]-z[i]) for i in range(m)])
                gtex = np.max([L[j][i]*abs(VP[j][i]-z[i]) for i in range(m)])
                if gtey <= gtex:
                    P[j] = y
                    VP[j] = vy
        
        with open(f"{outputDirPath}/gen{it+1}.out", "ab") as resFile:
            writeVP = np.zeros([N,m+1])
            writeVP[:,:-1] = VP
            np.savetxt(resFile,writeVP, delimiter="\t", newline='\n', header='', footer='')

"""
###############
# PARAMETERS #
##############
"""
N = 100
G = 100
T = 5

f1 = lambda x : x[0]

def f2(x):
    g = 1 + 9/(len(x)-1) *sum(x[1:])
    return g*(1 - np.sqrt(x[0]/g)-(x[0]/g)*np.sin(10*np.pi*x[0]))

vars_limits = [(0,1) for _ in range(30)]



"""
##############################
#   REAL ZDT3 PARETO FRONT  #
#############################
"""
ZDT3_pareto_front_x = np.concatenate((np.linspace(0, 0.0830015349), 
                        np.linspace(0.1822287281, 0.2577623634),
                        np.linspace(0.4093136749,0.45388221041),
                        np.linspace(0.6183967945,0.6525117038),
                        np.linspace(0.8233317984, 0.8518328654))
                      )

ZDT3_pareto_front_y = np.vectorize(lambda x: 1 - np.sqrt(x) - x*np.sin(10*np.pi*x))(ZDT3_pareto_front_x)

"""
##############################
# ONE EXECUTION DEVELOPMENT #
#############################
"""

outputDirPath = './results'

# Executes algorithm one time. Results are saved in ./results directory
ASCEVBIII([f1, f2], vars_limits, N, G, T,  outputDirPath=outputDirPath);


colors = list(colour.Color("blue").range_to(colour.Color("red"),G))
# Plot an execution development 
for generation in range(G):
    my_data = np.genfromtxt(f"{outputDirPath}/gen{generation}.out", delimiter='\t')
    plt.scatter(my_data[:,0], my_data[:,1], s=1, c=[colors[generation].rgb for _ in range(N)], cmap='gray')
    
#  Plot real front
plt.scatter(ZDT3_pareto_front_x, ZDT3_pareto_front_y, s=1, c='black', alpha=0.3)






