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
from copy import deepcopy          # For a real coping of objects
                           
'''
#######################
# EOP IMPLEMENTATION #
######################
'''

def EOP1(i, P, VP, Bi, searchSpace, Fs=[0.5, 0.7], CRs=[0.5], SIG=20, pm=None, seed=None):
    # 1) DIFFERENTIAL EVOLUTION MUTATION
    p = P.shape[1]
    
    PM = 1/p if pm is None else pm
    F = np.random.choice(Fs)
    
    r = P[np.random.choice(Bi, 5, replace=(len(Bi) < 5))]
    yhat = r[0] + F*(r[1]-r[2]) + np.random.random()*(r[3]-r[4])
    
    # 2) DIFFERENTIAL EVOLUTION CROSSING
    delta = np.random.randint(0,p)
    CR = np.random.choice(CRs)
    M = np.array([True if np.random.random()<=CR else False for _ in range(p)])
    M[delta] = True 
    
    y = M.astype(np.float64)*yhat + (~M).astype(np.float64)*P[i]
    
    # 3) GAUSSIAN MUTATION AND REPARING
    for j, yj in enumerate(y):
        if np.random.random() < PM:
            y[j] = yj+ np.random.normal(0,(searchSpace[j][1]-searchSpace[j][0])/SIG)
        
        if y[j] < searchSpace[j][0] or y[j] > searchSpace[j][1]:
            y[j] = min(max(yj,searchSpace[j][0]),searchSpace[j][1])
    return y


'''
##########################
# MOEA/D IMPLEMENTATION #
#########################
'''
def CMOEAD(goals, constraints, searchSpace, N, G, T, eop=EOP1, updationsNumber=None, NDS=True, seed=None, lambdaInput=None, outputDirPath='./results'):
    def dominates(a, va, b, vb):
        nonlocal m
        if va<vb:
            return True
        if vb<va:
            return False
        lessInAnyValue = False
        for j in range(m):
            if not(lessInAnyValue) and (a[j] < b[j]):
                lessInAnyValue = True
            if a[j] > b[j]:
                return False
            
        return  lessInAnyValue
    
    def updateNDS(NDS_P, NDS_F, NDS_V, xi, fi, vi):
        NDS_P_ = deepcopy(NDS_P)
        NDS_F_ = deepcopy(NDS_F)
        NDS_V_ = deepcopy(NDS_V)
        for j in range(len(NDS_P)):
            fj=NDS_F[j]; vj=NDS_V[j]
            if dominates(fj, vj, fi, vi):
                return (NDS_P, NDS_F, NDS_V)
            elif dominates(fi, vi, fj, vj):
                NDS_P_[j] = None
                NDS_F_[j] = None
                NDS_V_[j] = None
       
        NDS_P_ = list(filter(lambda x: x is not None, NDS_P_)) + [xi]
        NDS_F_ = list(filter(lambda x: x is not None, NDS_F_)) + [fi]
        NDS_V_ = list(filter(lambda x: x is not None, NDS_V_)) + [vi]
    
        return (NDS_P_, NDS_F_, NDS_V_)
    
    ## SETTINGS & PARAMETERS
    searchSpace = [sorted(vl) for vl in searchSpace]
    p=len(searchSpace)      # dimension of vectors
    m=len(goals)            # number of goals
    UN = N if updationsNumber is None else updationsNumber
    np.random.seed(seed)
    
    
    # INITIALIZATION
   
    # We generate N lambda vectors one for each subproblem and calculate
    # the distance between each two.
    L = np.zeros((N, m), dtype=np.float64)
    
    if m == 2 and not (lambdaInput):
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
    
    
    FP = np.array([np.apply_along_axis(fi, 1, P) for fi in goals]).transpose()
    VP = np.array([np.apply_along_axis(gi, 1, P) for gi in constraints]).transpose()
    
    posToZero = np.vectorize(lambda x: min(x,0.))
    VP = posToZero(VP)
    VP = np.apply_along_axis(np.sum, 1, (-1)*VP)
    
    ## We initialize z vector with the best value of f1 and f2 in the population.
    z = np.apply_along_axis(np.min, 0, FP)
    
    ## We initialize the non dominated solutions
    if NDS:
        NDS_P= []
        NDS_F= []
        NDS_V= []
        for i in range(N):
            NDS_P, NDS_F, NDS_V = updateNDS(NDS_P, NDS_F, NDS_V, P[i], FP[i], VP[i])
        del i
    
    
   
    with open(f"{outputDirPath}/{'' if seed is None else 's' + str(seed) + '_'}gen0.out", "wb") as resFile:
        with open(f"{outputDirPath}/{'' if seed is None else 's' + str(seed) + '_'}allGen.out", "wb") as allGenFile:
            writeVP = np.zeros([N,m+1])
            writeVP[:,:-1] = FP
            writeVP[:,-1] = (-1)*(VP)
            np.savetxt(resFile,writeVP, delimiter="\t", newline='\n', header='', footer='')
            np.savetxt(allGenFile,writeVP, delimiter="\t", newline='\n', header='', footer='')
     
    for it in range(G-1):     
        order = np.array(range(N))
        np.random.shuffle(order)
       # P_ = deepcopy(P)
      #  VP_ = deepcopy(VP)
        for cur in order:
            # GENERATE CHILD
            y = eop(cur, P, FP, B[cur], searchSpace, seed=seed)
            
            # EVALUATE CHILD AGAINST OBJECTIVES
            fy =  np.array([fi(y) for fi in goals])
            
            # EVALUATE CHILD AGAINST CONSTRAINTS
            vy = (-1)*sum(min(0., gj(y)) for gj in constraints)
            
            # UPDATE Z
            z = np.minimum(z, fy)
            
            if NDS:
            # UPDATE NDS
                NDS_P, NDS_F, NDS_V = updateNDS(NDS_P, NDS_F, NDS_V, y, fy, vy)
            
            updations = 0
            SIGMA = 0.01
            ETA = 20
            
            for j in sorted(B[cur], key=(lambda x: np.random.random())):
                Vmin = np.min(VP[B[j]]) 
                Vmax = np.max(VP[B[j]]) 
                TAU = Vmin + 0.3*(Vmax - Vmin)
                
                gteyap = np.max([L[j][i]*abs(fy[i]-z[i]) for i in range(m)]) + SIGMA*(min(TAU, vy)**2) + ETA*(max(0, vy-TAU))
                gtexap = np.max([L[j][i]*abs(FP[j][i]-z[i]) for i in range(m)]) + SIGMA*(min(TAU, VP[j])**2) + ETA*(max(0, VP[j]-TAU))
                
                
                if gteyap <= gtexap:
                    P[j] = y
                    FP[j] = fy
                    VP[j] = vy
                    updations +=1                      
                
                if updations >= UN:
                    break
            #P = deepcopy(P_); VP= deepcopy(VP_)
        
        with open(f"{outputDirPath}/{'' if seed is None else 's' + str(seed) + '_'}gen{it+1}.out", "wb") as resFile:
            with open(f"{outputDirPath}/{'' if seed is None else 's' + str(seed) + '_'}allGen.out", "ab") as allGenFile:
                writeVP = np.zeros([N,m+1])
                writeVP[:,:-1] = FP
                writeVP[:,-1] = (-1)*(VP)
                np.savetxt(resFile,writeVP, delimiter="\t", newline='\n', header='', footer='')
                np.savetxt(allGenFile,writeVP, delimiter="\t", newline='\n', header='', footer='')
    
    if NDS:
        with open(f"{outputDirPath}/{'' if seed is None else 's' + str(seed) + '_'}nds.out", "wb") as ndsFile:
            writeNDS = np.zeros([len(NDS_P),m+1])
            writeNDS[:,:-1] = np.array(NDS_F)
            writeNDS[:,-1] = (-1)*np.array(NDS_V)
            np.savetxt(ndsFile, writeNDS, delimiter="\t", newline='\n', header='', footer='')
