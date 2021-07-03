#!/usr/bin/env python
#-*- coding:utf-8 -*-
##
## simple_equivalence.py
##
##  Created on: Feb 17, 2021
##  Finds direct and inverse equivalence between protected and non-protected features of a dataset.
#
#
#==============================================================================
import sys
import os.path
from os import path
import pandas as pd
import pickle as pkl
from DataInfo import DataInfo, ProxyType

#==============================================================================
def input_check():
    #dataset total-features num-protected protected_1 ... protected_n
    if not path.exists(sys.argv[1]):
        print(sys.argv[1])
        show_info()
        exit()
    
    #TODO: check #total-features , check #num_protected<#total, check all protected_n exist


#==============================================================================
def show_info():
    #dataset total-features num-protected protected_1 ... protected_n
    print("How to run: ")
    print("\t dataset_path(.pkl) total-feature-number protected-features-number protected_feature_1 ... protected_feature_n")

#==============================================================================
def detect_direct_eq(data_info, proc_num):
    feature_labels  = data_info.data.columns
    proc_feat = data_info.data[feature_labels[proc_num]]
    print('Searching proxies for feature '+feature_labels[proc_num])
    for j in data_info.non_protected_features:
        eq = True 
        i = 0
        np_feat = data_info.data[feature_labels[j]] #list with all values of feature #j
        for v in np_feat.values:
            if( proc_feat[i] != v):
                eq = False
                break
            i += 1
        
        if(eq == True):
            print('\t Feature '+feature_labels[j]+ ':')
            print('\t \t directly equivalent.')
        #else: 
         #   print('\t \t not directly equivalent.')

#==============================================================================
def detect_inverse_eq(data_info, proc_num):
    feature_labels  = data_info.data.columns
    proc_feat = data_info.data[feature_labels[proc_num]]
    print('Searching proxies for feature '+feature_labels[proc_num])

    for j in data_info.non_protected_features:
        eq = True 
        i = 0
        np_feat = data_info.data[feature_labels[j]] #list with all values of feature #j
        for v in np_feat.values:
            if( proc_feat[i] == v):
                eq = False
                break
            i += 1
        if(eq == True):
            print('\t Feature '+feature_labels[j]+ ':')
            print('\t \t inversely equivalent.')
        #else: 
         #   print('\t \t not inversely equivalent.')

#==============================================================================
if __name__ == '__main__':
    input_check()
    data_info = DataInfo(sys.argv)

    print("==================== Searching for Direct Equivalence ==================")
    print()
    for p_feature in data_info.protected_features:
        detect_direct_eq(data_info, p_feature)

    print("==================== Searching for Inverse Equivalence ==================")
    print()
    for p_feature in data_info.protected_features:
        detect_inverse_eq(data_info, p_feature)

    
