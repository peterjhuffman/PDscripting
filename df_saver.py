# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 10:08:25 2023

@author: HUFFMP
"""

import pandas as pd
import json
import sys

json_loc = sys.argv[1]

with open(json_loc, encoding="utf-8") as g:
    lines = json.load(g)

infoloc1 = lines['Tables'][0]['DataFile']
df = pd.read_csv(infoloc1, sep='\t')

sav = lines['CurrentWorkflowID']
newpath = 'D:\\huffmp\\fileviewing\\'
df.to_csv(newpath+f'/{sav}_pulldown.csv', index=False)