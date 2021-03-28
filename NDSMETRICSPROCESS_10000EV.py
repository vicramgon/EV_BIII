#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 19:57:46 2021

@author: victor
"""

# import numpy as np
# import pandas as pd


# resData=[]

# for eop in ['EOP1','EOP2','EOP3']:
#     for n,g in [(40,250),(100,100),(200,50)]:
#             data = np.genfromtxt(f"./tmp_zdt3_{eop}/N{n}_G{g}/metric_NDS.out")
#             hvmean, spcmean = np.mean(data, axis=0)
#             hvstd, spcstd = np.std(data, axis=0)
#             resData.append(('MOEA/D ' + eop,n,g,hvmean,hvstd, spcmean, spcstd))

   
# resultsDf = pd.DataFrame(resData, columns=('ALGORITHM','N','G','Hv_mean', 'Hv_std', 'Spc_mean', 'Spc_std'))

# print("==============================================================")  
# print("====================== RESULSTS SUMMARY ======================")    
# print("==============================================================") 
# print()         
# # print(resultsDf)
# print(resultsDf.to_latex(index=False))
    
import numpy as np
import pandas as pd

resData=[]
algs = ['EOP1','EOP2','EOP3']
for i, eop1 in enumerate(algs):
    for eop2 in algs[i+1:]:
        for n,g in [(40,250),(100,100),(200,50)]:
                data = np.genfromtxt(f"./tmp_zdt3_{eop1}/N{n}_G{g}/metric_CS_{eop2}_NDS.out")
                cs21mean, cs12mean = np.mean(data, axis=0)
                cs21std, cs12std = np.std(data, axis=0)
                resData.append((eop1, eop2, n, g, cs21mean, cs21std, cs12mean, cs12std))

    
resultsDf = pd.DataFrame(resData, columns=('ALG1', 'ALG2', 'N','G','c(ALG2, ALG1)_mean', 'c(ALG2, ALG1)_std', 
                                           'c(ALG1, ALG2)_mean', 'c(ALG1, ALG2)_std'))

print("==============================================================")  
print("===================== COVER SET SUMMARY ======================")    
print("==============================================================") 
print()         
# print(resultsDf)
print(resultsDf.to_latex(index=False))
