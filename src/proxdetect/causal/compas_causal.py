#!/usr/bin/env python
#-*- coding:utf-8 -*-
##
## compas_causal.py
##
##  Created on: Feb 15, 2021
##  Generates a causal model from the COMPAS dataset
#
#==============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import dowhy
from dowhy import CausalModel
import dowhy.plotter
from IPython.display import Image, display



def generate_causal_model():
    f = pd.read_csv('../../../bench/compas/compas.csv')

    model= CausalModel(
        data=f,
        treatment='Age_Below_TwentyFive',
        outcome='Female',
        instruments=["Number_of_Priors","score_factor","Age_Above_FourtyFive","Female","African_American","Asian","Hispanic","Native_American","Other"],
    )
    
    model.view_model(layout="dot")
    display(Image(filename="causal_model.png"))
    return model



#==============================================================================
if __name__ == '__main__':
    model = generate_causal_model() 
    identified_estimand = model.identify_effect()
    print(identified_estimand)    
 