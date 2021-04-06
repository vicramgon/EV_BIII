#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 19:57:46 2021

@author: victor
"""

import numpy as np
import pandas as pd


resData=[]

for eop in ['CMOEAD_ADAPT', 'CMOEAD_THRES', 'NSGAII']:
    for n,g in [(40,250),(100,100),(200,50)]:
            data = np.genfromtxt(f"./tmp_cf616d_{eop}/N{n}_G{g}/metric_FGEN.out")
            hvmean, spcmean = np.mean(data, axis=0)
            hvstd, spcstd = np.std(data, axis=0)
            resData.append((eop,n,g,hvmean,hvstd, spcmean, spcstd))

    
resultsDf = pd.DataFrame(resData, columns=('ALGORITHM','N','G','Hv_mean', 'Hv_std', 'Spc_mean', 'Spc_std'))

print("==============================================================")  
print("====================== RESULSTS SUMMARY ======================")    
print("==============================================================") 
print()         
# print(resultsDf)
print(resultsDf.to_latex(index=False))