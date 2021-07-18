#!/usr/bin/env python
#-*- coding:utf-8 -*-
##
## DataInfo.py
##
##  Created on: Feb 22, 2021
##
#==============================================================================
import sys
from enum import Enum
import pandas as pd
import numpy as np
import pickle as pkl
#==============================================================================

class ProxyType(Enum):
    EQUIVALENCE = 1
    IMPLICATION = 2

#==============================================================================

class DataInfo(object):
    """
        Class for representing a dataset, its protected and non-protected features, and possible proxies
    """
    def __init__(self, commands):
        self.data = pd.read_csv(commands[2])
        self.num_features = int(commands[3])
        self.num_protected_features = int(commands[4])

        self.protected_features = [int(commands[i]) for i in range(5, len(commands))]
        self.non_protected_features = np.setdiff1d([range(self.num_features - 1)],self.protected_features)

        self.feature_labels  = self.data.columns
        print('Non-Protected Features: ')
        for f_num in self.non_protected_features:
            print("\t" + self.feature_labels[f_num])
        print('Protected Features: ')
        for f_num in self.protected_features:
            print("\t" + self.feature_labels[f_num])
        

        self.left_margins = {}
        for proc in self.protected_features:
            self.left_margins[self.feature_labels[proc]] = {}

        self.right_margins = {}
        for nproc in self.non_protected_features:
            self.right_margins[self.feature_labels[nproc]] = {}

        self.potential_proxies = {}
        for proc in self.protected_features:
            self.potential_proxies[proc] = {}


    def add_proxy(proxy_num, proc_num, proxy_type):
        """
            Adds a new proxy (feature #proxy_num) of a protected feature (feature #proc_num)
        """
        self.potential_proxies[proc_num] += (proxy_num, proxy_type)


    def pickle_load_file(self, filename):
        try:
            f =  open(filename, "rb")
            data = pkl.load(f)
            f.close()
            return data
        except:
            print("Cannot load from file", filename)
            exit()

    