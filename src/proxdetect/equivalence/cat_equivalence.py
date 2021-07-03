#!/usr/bin/env python
#-*- coding:utf-8 -*-
##
## cat_equivalence.py
##
##  Created on: April 3, 2021
##  Finds equivalence between categorical protected and non-protected features of a dataset.
#
#
#==============================================================================
import sys
import os.path
from os import path
import pandas as pd
import pickle as pkl
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics.cluster import normalized_mutual_info_score
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
def detect_cat_eq(data_info, proc_num):
    feature_labels  = data_info.data.columns
    proc_feat = data_info.data[feature_labels[proc_num]] #list with all values of the protected feature
    print('Searching proxies for feature '+feature_labels[proc_num])
    
    for j in data_info.non_protected_features:
        print('\t Feature '+feature_labels[j]+ ':')

        cat_relations = dict()
        i = 0
        eq = True
        np_feat = data_info.data[feature_labels[j]] #list with all values of non protected feature #j
        for v in np_feat:
            if proc_feat[i] in cat_relations:
                if (cat_relations[proc_feat[i]] != v):
                    print('\t \t not equivalent.')
                    eq = False
                    break
            else:
                cat_relations[proc_feat[i]] = v
            
            i = i+1

        if( eq and (len(set(cat_relations.values)) == len(cat_relations.values)) ): #eq and all values are different
            print('\t \t directly equivalent.')
        
def detect_margin_eq(data_info, proc_num):
    feature_labels  = data_info.data.columns
    proc_feat = data_info.data[feature_labels[proc_num]] #list with all values of the protected feature
    print('Searching proxies for feature '+feature_labels[proc_num])
    
    for j in data_info.non_protected_features:
        print('\t Feature '+feature_labels[j]+ ':')

        cat_relations = dict() # In the form {nproc value: [nproc value count, {proc value1: proc value1 count, proc value2, proc value2 count, ...}]}
        i = 0
        np_feat = data_info.data[feature_labels[j]] #list with all values of non protected feature #j
        for v in np_feat:
            if v in cat_relations:
                cat_relations[v][0] +=1 
                if proc_feat[i] in  cat_relations[v][1]:
                    cat_relations[v][1][proc_feat[i]] += 1
                else:
                    cat_relations[v][1][proc_feat[i]] = 1
            else: 
                cat_relations[v] = [1, {proc_feat[i]: 1}]
            
            i = i+1
        
        for v in cat_relations:
            abs_occurence = cat_relations[v][0]
            max_key = max(cat_relations[v][1], key = cat_relations[v][1].get)
            print(v, max_key, max(cat_relations[v][1].values()) /abs_occurence)

#This applies the Normalized Mutual Information definition of a proxy attribute
def detect_NMI_eq(data_info, proc_num):
    
    feature_labels  = data_info.data.columns
    proc_feat = data_info.data[feature_labels[proc_num]] #list with all values of the protected feature

    for np in data_info.non_protected_features:
        np_feat = data_info.data[feature_labels[np]] #list with all values of non protected feature #j
        data_info.feature_margins[feature_labels[proc_num]][feature_labels[np]] = normalized_mutual_info_score(proc_feat, np_feat)


def generate_pair_count(data_info, proc_num, nproc_num):
    feature_labels  = data_info.data.columns
    proc_feat = data_info.data[feature_labels[proc_num]]    #list with all values of the protected feature
    nproc_feat = data_info.data[feature_labels[nproc_num]]   #list with all values of the non-protected feature

    proc_values = set(proc_feat)
    nproc_values = set(nproc_feat)

    pairs = dict()
    num_examples = len(proc_feat)

    for i in range(num_examples):

        if (proc_feat[i] in pairs) and (nproc_feat[i] in pairs[proc_feat[i]]):
            pairs[proc_feat[i]][nproc_feat[i]] += 1
        else:
            if proc_feat[i] not in pairs:
                pairs[proc_feat[i]] = dict()
            pairs[proc_feat[i]][nproc_feat[i]] = 1
    
    for p in pairs.keys():
        for np in nproc_values:
            if np not in pairs[p]:
                pairs[p][np] = 0

    pair_counts = pd.DataFrame.from_dict(pairs)
    ax = sns.heatmap(pair_counts, annot=True, fmt = 'g')
    
    plt.xlabel(data_info.feature_labels[proc_num])
    plt.ylabel(data_info.feature_labels[nproc_num])

    plt.show()

#==============================================================================
if __name__ == '__main__':
    input_check()
    data_info = DataInfo(sys.argv)
    

    print("==================== Searching for Categorical Equivalence ==================")
    print()
    #for p_feature in data_info.protected_features:
    #    detect_margin_eq(data_info, p_feature)

    #feat_margins = pd.DataFrame.from_dict(data_info.feature_margins)
    #ax = sns.heatmap(feat_margins, annot=True, fmt="f")
    #plt.show()
    p_feature = data_info.protected_features[2]
    for np_feature in data_info.non_protected_features:
        generate_pair_count(data_info, p_feature, np_feature)

        

