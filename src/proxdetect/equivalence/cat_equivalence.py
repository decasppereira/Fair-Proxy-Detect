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
import argparse
import pandas as pd
import pickle as pkl
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics.cluster import normalized_mutual_info_score

from DataInfo import *

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
def detectAbsEq(data_info, proc_num):
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
        
def detectMarginEq(data_info, proc_num):
    feature_labels  = data_info.data.columns
    proc_feat = data_info.data[feature_labels[proc_num]] #list with all values of the protected feature
    print('Searching proxies for feature '+feature_labels[proc_num])
    

    for j in data_info.non_protected_features:
        print('\t Feature '+feature_labels[j]+ ':')

        right_relations = dict() # In the form {nproc value: [nproc value count, {proc value1: proc value1 count, proc value2, proc value2 count, ...}]}
        left_relations = dict() # In the form {proc value: [proc value count, {nproc value1: nproc value1 count, nproc value2, nproc value2 count, ...}]}
        i = 0
        np_feat = data_info.data[feature_labels[j]] #list with all values of non protected feature #j
        for np_v in np_feat:
            p_v = proc_feat[i]
            if np_v in right_relations:
                right_relations[np_v][0] +=1 
                if p_v in  right_relations[np_v][1]:
                    right_relations[np_v][1][p_v] += 1
                else:
                    right_relations[np_v][1][p_v] = 1
            else:  
                right_relations[np_v] = [1, {p_v: 1}]

            if p_v in left_relations:
                left_relations[p_v][0] +=1 
                if np_v in  left_relations[p_v][1]:
                    left_relations[p_v][1][np_v] += 1
                else:
                    left_relations[p_v][1][np_v] = 1
            else:  
                left_relations[p_v] = [1, {np_v: 1}]
            
            i = i+1
        
        margin = 0
        for v in right_relations:
            abs_occurence = right_relations[v][0]
            max_right = max(right_relations[v][1], key = right_relations[v][1].get)
            print("\t\t", v, "->", max_right, max(right_relations[v][1].values()) /abs_occurence)
            margin += right_relations[v][1][max_right]
        data_info.right_margins[feature_labels[j]][feature_labels[proc_num]] = np.round(margin/len(data_info.data), 2)


        margin = 0
        for v in left_relations:
            abs_occurence = left_relations[v][0]
            max_left = max(left_relations[v][1], key = left_relations[v][1].get)
            print("\t\t", v, "->", max_left, max(left_relations[v][1].values()) /abs_occurence)
            margin += (left_relations[v][1][max_left])

        data_info.left_margins[feature_labels[proc_num]][feature_labels[j]] = np.round(margin/len(data_info.data), 2)

      

#This applies the Normalized Mutual Information definition of a proxy attribute
def detectNMIEq(data_info, proc_num):
    
    feature_labels  = data_info.data.columns
    proc_feat = data_info.data[feature_labels[proc_num]] #list with all values of the protected feature

    for np in data_info.non_protected_features:
        np_feat = data_info.data[feature_labels[np]] #list with all values of non protected feature #j
        data_info.feature_margins[feature_labels[proc_num]][feature_labels[np]] = normalized_mutual_info_score(proc_feat, np_feat)


def generatePairCount(data_info, proc_num, nproc_num):
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

    parser = argparse.ArgumentParser()
    parser.add_argument('-vis', action='store_true')
    parser.add_argument('-nmi', action='store_true')
    parser.add_argument('-counts', action='store_true')
    parser.add_argument('-abs', action='store_true')
    parser.add_argument('dataset', nargs=1)
    parser.add_argument('attributes', type=int, nargs='*')
    args = parser.parse_args()

    data_info = DataInfo(sys.argv)
    feature_labels  = data_info.data.columns

    print("==================== Searching for Categorical Equivalence ==================")
    print()

    if args.vis:
        attribute_margins = dict()
        for p in data_info.protected_features:
            detectMarginEq(data_info, p)
            attribute_margins[feature_labels[p]] = {}

        for p in data_info.protected_features:
            for np in data_info.non_protected_features:
                p_name = feature_labels[p]
                np_name = feature_labels[np]
                attribute_margins[p_name][np_name] = min(data_info.left_margins[p_name][np_name], data_info.right_margins[np_name][p_name])
        
        left = pd.DataFrame.from_dict(data_info.left_margins).transpose()
        right = pd.DataFrame.from_dict(data_info.right_margins).transpose()
        feat_margins = pd.DataFrame.from_dict(attribute_margins)

        f, (ax1, ax2, ax3) = plt.subplots(ncols=3)

        sns.heatmap(left, annot=True, fmt = 'g', ax=ax2)
        sns.heatmap(right, annot=True, fmt = 'g', ax=ax1)
        sns.heatmap(feat_margins, annot=True, fmt="g", ax=ax3)

        ax1.set_title("Non Protected -> Protected")
        ax2.set_title("Protected -> Non Protected")
        ax3.set_title("Equivalence")

        plt.show()

    elif args.nmi:
        for p_feature in data_info.protected_features:
            detectNMIEq(data_info, p_feature)

        feat_margins = pd.DataFrame.from_dict(data_info.feature_margins)
        ax = sns.heatmap(feat_margins, annot=True, fmt="f")
        plt.show()

    elif args.counts:
        p_feature = data_info.protected_features[2]
        for np_feature in data_info.non_protected_features:
            generatePairCount(data_info, p_feature, np_feature)

    elif args.abs:
        for p_feature in data_info.protected_features:
            detectAbsEq(data_info, p_feature)

        

