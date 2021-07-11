#!/usr/bin/env python
#-*- coding:utf-8 -*-
##
## cat_implication.py
##
##  Created on: April 16, 2021
##  Finds implication relationships between categorical protected and non-protected features of a dataset.
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

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
  
import DataInfo

#==============================================================================
def inputCheck():
    #dataset total-features num-protected protected_1 ... protected_n
    if not path.exists(sys.argv[1]):
        print(sys.argv[1])
        showInfo()
        exit()
    
    #TODO: check #total-features , check #num_protected<#total, check all protected_n exist


#==============================================================================
def showInfo():
    #dataset total-features num-protected protected_1 ... protected_n
    print("How to run: ")
    print("\t dataset_path(.pkl) total-feature-number protected-features-number protected_feature_1 ... protected_feature_n")

#==============================================================================
def detectAbsoluteImp(data_info, proc_num):
    feature_labels  = data_info.data.columns
    proc_feat = data_info.data[feature_labels[proc_num]] #list with all values of the protected feature
    print('Searching proxies for feature '+feature_labels[proc_num])
    
    for j in data_info.non_protected_features:
        print('\t Feature '+feature_labels[j]+ ':')

        cat_relations = dict() # in the form {nproc value1: proc value1, nproc value2, proc value2, ...}
        i = 0
        eq = True
        np_feat = data_info.data[feature_labels[j]] #list with all values of non protected feature #j
        for v in np_feat:
            if v in cat_relations:
                if (cat_relations[v] != proc_feat[i]):
                    #print('\t \t does not imply ' + feature_labels[proc_num])
                    eq = False
                    break
            else: 
                cat_relations[v] = proc_feat[i]
            
            i = i+1

        if( eq ):
            print('\t \t implies ' + feature_labels[proc_num])
        
def detectMarginImp(data_info, proc_num, direction):
    feature_labels  = data_info.data.columns
    proc_feat = data_info.data[feature_labels[proc_num]] #list with all values of the protected feature
   
    print('Searching proxies for feature '+feature_labels[proc_num])
    
    if(direction == "right"):
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

            margin = 0
            for v in cat_relations:
                abs_occurence = cat_relations[v][0]
                max_key = max(cat_relations[v][1], key = cat_relations[v][1].get)
                margin += (cat_relations[v][1][max_key]/abs_occurence)*(abs_occurence/len(data_info.data))
                for proc_v in cat_relations[v][1]:
                    print("\t\t{} implies {} {} of times".format(v, proc_v, round(cat_relations[v][1][proc_v]/abs_occurence, 3) ))

                #print("\t\t{} implies {} {} of times".format(v, max_key, round(cat_relations[v][1][max_key]/abs_occurence, 3) ))

            print("\t\t\t {} implies {} {} of times".format(feature_labels[j], feature_labels[proc_num], margin))

            #data_info.feature_margins[feature_labels[proc_num]][feature_labels[j]] = margin

    elif(direction == "left"):
        for j in data_info.non_protected_features:
            print('\t Feature '+feature_labels[j]+ ':')

            cat_relations = dict() # In the form {proc value: [proc value count, {nproc value1: nproc value1 count, nproc value2, nproc value2 count, ...}]}
            i = 0
            np_feat = data_info.data[feature_labels[j]] #list with all values of non protected feature #j
            for v in proc_feat:
                if v in cat_relations:
                    cat_relations[v][0] +=1 
                    if np_feat[i] in  cat_relations[v][1]:
                        cat_relations[v][1][np_feat[i]] += 1
                    else:
                        cat_relations[v][1][np_feat[i]] = 1
                else: 
                    cat_relations[v] = [1, {np_feat[i]: 1}]
                
                i = i+1

            margin = 0
            for v in cat_relations:
                abs_occurence = cat_relations[v][0]
                max_key = max(cat_relations[v][1], key = cat_relations[v][1].get)
                margin += (cat_relations[v][1][max_key]/abs_occurence)*(abs_occurence/len(data_info.data))
                for np_v in cat_relations[v][1]:
                    print("\t\t{} implies {} {} of times".format(v, np_v, round(cat_relations[v][1][np_v]/abs_occurence, 3) ))

                #print("\t\t{} implies {} {} of times".format(v, max_key, round(cat_relations[v][1][max_key]/abs_occurence, 3) ))

            print("\t\t\t {} implies {} {} of times".format(feature_labels[proc_num], feature_labels[j] , margin))

def visualizeAttributeImp(data, np_num, p_num):
    feature_labels  = data.columns
    proc_feat = data[feature_labels[p_num]]     #list with all values of the protected feature
    nproc_feat = data[feature_labels[np_num]]   #list with all values of the non-protected feature

    num_examples = len(proc_feat)
    
    right_implication = dict()
    left_implication = dict()

    for i in range(num_examples):
        proc_value = proc_feat[i]
        nproc_value = nproc_feat[i]

        if proc_value in left_implication:
            left_implication[proc_value][0] +=1 
            if nproc_value in  left_implication[proc_value][1]:
                left_implication[proc_value][1][nproc_value] += 1
            else:
                left_implication[proc_value][1][nproc_value] = 1
        else: 
            left_implication[proc_value] = [1, {nproc_value: 1}]

        if nproc_value in right_implication:
            right_implication[nproc_value][0] +=1 
            if proc_value in  right_implication[nproc_value][1]:
                right_implication[nproc_value][1][proc_value] += 1
            else:
                right_implication[nproc_value][1][proc_value] = 1
        else: 
            right_implication[nproc_value] = [1, {proc_value: 1}]

    left_imp_scores = dict()
    for v in left_implication: 
        abs_occurence = left_implication[v][0]
        for nproc_value in left_implication[v][1]:
            if v in left_imp_scores:
                left_imp_scores[v][nproc_value] = round(left_implication[v][1][nproc_value]/abs_occurence, 3)
            else:
                left_imp_scores[v] = {nproc_value: round(left_implication[v][1][nproc_value]/abs_occurence, 3) }

    print(left_imp_scores)

    right_imp_scores = dict()
    for v in right_implication: 
        abs_occurence = right_implication[v][0]
        for proc_value in right_implication[v][1]:
            if v in right_imp_scores:
                right_imp_scores[v][proc_value] = round(right_implication[v][1][proc_value]/abs_occurence, 3)
            else:
                right_imp_scores[v] = {proc_value: round(right_implication[v][1][proc_value]/abs_occurence, 3) }

    print(right_imp_scores)

    left = pd.DataFrame.from_dict(left_imp_scores).transpose()
    right = pd.DataFrame.from_dict(right_imp_scores).transpose()

    f, (ax1, ax2) = plt.subplots(ncols=2)


    sns.heatmap(left, annot=True, fmt = 'g', ax=ax2)
    sns.heatmap(right, annot=True, fmt = 'g', ax=ax1)
 
    ax1.set_title("{} -> {}".format(feature_labels[np_num], feature_labels[p_num]))
    ax2.set_title("{} -> {}".format(feature_labels[p_num], feature_labels[np_num]))
    
    plt.show()

#==============================================================================
if __name__ == '__main__':
    inputCheck()
    print("==================== Searching for Categorical Implication ==================")
    print()

    # To test both directions an output detailed .txt files #
    #data_info = DataInfo(sys.argv)
    #for p_feature in data_info.protected_features:
     #   detectMarginImp(data_info, p_feature, "right")
     #   detectMarginImp(data_info, p_feature, "left")

    # To generate visualizations between two attributes #
    data = pd.read_csv(sys.argv[1])
    np_num = int(sys.argv[2])
    p_num = int(sys.argv[3])
    visualizeAttributeImp(data, np_num, p_num)

    #feat_margins = pd.DataFrame.from_dict(data_info.feature_margins)
    #ax = sns.heatmap(feat_margins, annot=True, fmt="f")
    #plt.show()

