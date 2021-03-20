#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 
==============================================================================
               APLICACIONES DE SOFT-COMPUTING
==============================================================================

@title : COMPETICIÓN B.III - Algoritmos Evolutivos : MOEA/D
@author: Víctor Ramos González
"""
'''
##############
# LIBRARIES #
#############
'''

import numpy as np                 # Math library
import os                          # Create directories
import shutil                      # Delete directories


'''
#######################
# EOP IMPLEMENTATION #
######################
'''

def EOP1(i, P, VP, Bi, searchSpace, F=0.5, CR=0.5, SIG=20, pm=None, seed=None):
    # 1) DIFFERENTIAL EVOLUTION MUTATION
    p = P.shape[1]
    PM = 1/p if pm is None else pm
    r = P[np.random.choice(Bi, 3, replace=False)]
    yhat = r[0] + F*(r[1]-r[2])
    
    # 2) DIFFERENTIAL EVOLUTION CROSSING
    delta = np.random.randint(0,p)
    M = np.array([True if np.random.random()<=CR else False for _ in range(p)])
    M[delta] = True 
    
    y = M.astype(np.float64)*yhat + (~M).astype(np.float64)*P[i]
    
    # 3) GAUSSIAN MUTATION AND REPARING
    for j, yj in enumerate(y):
        if np.random.random() < PM:
            y[j] = min(max(yj+ np.random.normal(0,(searchSpace[j][1]-searchSpace[j][0])/SIG),searchSpace[j][0]),searchSpace[j][1])
        else:
            y[j] = min(max(yj,searchSpace[j][0]),searchSpace[j][1])
    return y

def EOP2(i, P, VP, Bi, searchSpace, seed=None, F=0.5, CR=0.5, pm=None, ETA=10):
    # 1) DIFFERENTIAL EVOLUTION MUTATION
    p = P.shape[1]
    PM = 1/p if pm is None else pm
    r = P[np.random.choice(Bi, 5, replace=False)]
    yhat = r[0] + F*(r[1]-r[2]) + np.random.random()*(r[3]-r[4])
    
    # 2) DIFFERENTIAL EVOLUTION CROSSING
    delta = np.random.randint(0,p)
    M = np.array([True if np.random.random()<=CR else False for _ in range(p)])
    M[delta] = True 
    
    y = M.astype(np.float64)*yhat + (~M).astype(np.float64)*P[i]
    
    # 3) SBX MUTATION 
    for j, yj in enumerate(y):
        if np.random.random() < PM :
            mu =  np.random.random()
            sigmaj = (2*mu)**(1/(ETA+1)) if mu < 0.5 else 1 - (2 - 2*mu)**(1/(ETA+1))
            y[j] += sigmaj*(searchSpace[j][1] - searchSpace[j][0])
        
        # REPARING
        if y[j] < searchSpace[j][0] or y[j] > searchSpace[j][1]:
            y[j] = min(max(yj,searchSpace[j][0]),searchSpace[j][1])
    return y


def EOP3(i, P, VP, Bi, searchSpace, seed=None, e=4, SIG=20, pm=None):
    p = P.shape[1]
    PM = 1/p if pm is None else pm
    
    # 1) UX CROSSOVER
    r = P[np.random.choice(Bi, e, replace=False)]
    y = np.array([r[np.random.randint(0,e)][j] for j in range(p)])
    
    
    # EOP1.3) GAUSSIAN MUTATION 
    for j, yj in enumerate(y):
        if np.random.random() < PM:
            y[j] = min(max(yj+ np.random.normal(0,(searchSpace[j][1]-searchSpace[j][0])/SIG),searchSpace[j][0]),searchSpace[j][1])
        else:
            y[j] = min(max(yj,searchSpace[j][0]),searchSpace[j][1])
    return y
    

'''
##########################
# MOEA/D IMPLEMENTATION #
#########################
'''
def MOEAD(goals, searchSpace, N, G, T, eop=EOP3, seed=None, lambdaInput={'path':'./input/lambdas.csv', 'delimiter':'j'}, outputDirPath='./results'):

    
    ## SETTINGS & PARAMETERS
    if os.path.isdir(outputDirPath):
        shutil.rmtree(outputDirPath)
    os.mkdir(outputDirPath) 
    
    searchSpace = [sorted(vl) for vl in searchSpace]
    p=len(searchSpace)
    m=len(goals)
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
    # is between the corresponding searchSpace.
    P = np.random.random([N, p]).astype(np.float64)
    #print(P);
    
    for i, bi in enumerate(searchSpace):
        P[:,i] = list(map(lambda x: bi[0] + (bi[1] - bi[0])*x, P[:,i]))
    del i
    
    
    VP = np.array([np.apply_along_axis(fi, 1, P) for fi in goals]).transpose()
    
    ## We initialize z vector with the best value of f1 and f2 in the population.
    z = np.apply_along_axis(np.min, 0, VP)
    
    with open(f"{outputDirPath}/{'' if seed is None else 's' + str(seed) + '_'}gen0.out", "ab") as resFile:
        writeVP = np.zeros([N,m+1])
        writeVP[:,:-1] = VP
        np.savetxt(resFile,writeVP, delimiter="\t", newline='\n', header='', footer='')
    
    for it in range(G-1):     
        order = np.array(range(N))
        np.random.shuffle(order)
        for cur in order:
            # GENERATE CHILD
            y = eop(cur, P, VP, B[cur], searchSpace, seed=seed)
            vy =  np.array([fi(y) for fi in goals])
            
            # UPDATE Z
            z = np.minimum(z, vy)
            
            for j in B[cur]:
                gtey = np.max([L[j][i]*abs(vy[i]-z[i]) for i in range(m)])
                gtex = np.max([L[j][i]*abs(VP[j][i]-z[i]) for i in range(m)])
                if gtey <= gtex:
                    P[j] = y
                    VP[j] = vy
        
        with open(f"{outputDirPath}/{'' if seed is None else 's' + str(seed) + '_'}gen{it+1}.out", "ab") as resFile:
            writeVP = np.zeros([N,m+1])
            writeVP[:,:-1] = VP
            np.savetxt(resFile,writeVP, delimiter="\t", newline='\n', header='', footer='')
