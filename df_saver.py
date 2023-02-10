# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 10:08:25 2023

@author: HUFFMP
"""

import pandas as pd # for data manipulation
import json # for reading output json file from PD
import sys # for reading parameters from PD

json_loc = sys.argv[1] # reads one(1) parameter from PD

with open(json_loc, encoding="utf-8") as g:
    lines = json.load(g) # loads output json file from PD

infoloc1 = lines['Tables'][0]['DataFile'] # reads location of table datafile from PD output
df = pd.read_csv(infoloc1, sep='\t') # reads table datafile from PD output

sav = lines['CurrentWorkflowID'] # reads workflow ID from PD output json
newpath = 'D:\\huffmp\\fileviewing\\' # new path to save information
df.to_csv(newpath+f'/{sav}_pulldown.csv', index=False) # saves requested table output
