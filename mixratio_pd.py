# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 09:36:00 2022

@author: HUFFMP
"""

import pandas as pd # for data manipulation
import sys # for exit command and PD parameters
from time import sleep as slp # also for exit command
from matplotlib import pyplot as plt # for data visualizations
import json # for PD output 

"""
stop()
simple function that exits the program if something is incorrect or complete.
"""
def stop():
    print('Exiting mixratio.exe. Thanks for dropping by.')
    slp(2)
    sys.exit()

json_loc = sys.argv[1] # reading parameter 1: pd output info
THRESH = float(sys.argv[2]) # reading parameter output 2: threshold --> numerical

with open(json_loc, encoding="utf-8") as g: # reading pd output info
    lines = json.load(g)

infoloc1 = lines['Tables'][0]['DataFile'] # determining table output location
df = pd.read_csv(infoloc1, sep='\t') # reading table output

sav = lines['CurrentWorkflowID'] # determining workflow id

# below is an extravagant way to pull down abundance columns. I'm going to fix this, actually. Note to self.
abundances = list(pd.Series(df.columns)[pd.Series(df.columns).str.contains('Abundance:')].values)
if len(abundances)==0:
    abundances = list(pd.Series(df.columns)[pd.Series(df.columns).str.contains('Abundances:')].values)
if len(abundances)==0:
    abundances = list(pd.Series(df.columns)[pd.Series(df.columns).str.contains('Abundances')].values)
if len(abundances)==0:
    abundances = list(pd.Series(df.columns)[pd.Series(df.columns).str.contains('Abundance')].values)

means = []
for col in abundances: #for each lane, cuts values above and below threshold and calculates mean.
    df_slice = df[col].astype('float64')
    df_slice = df_slice[(df_slice>df_slice.quantile(THRESH))&(df_slice<df_slice.quantile(1-THRESH))]
    means.append(df_slice.mean())

plt.bar(abundances, means) # creates bar plot
plt.ylabel('Mean Abundance')
plt.xlabel('TMT Lane')
plt.xticks([i for i in range(0, 17)], [str(i) for i in range(1, 18)])
plt.title('TMT Lanes: Mean Abundances')
plt.savefig('D:\\tmt mixing\\'+f'{sav}_bar.png', dpi=1200)
plt.clf()

tmtMXR = pd.DataFrame() # creates table
tmtMXR['means'] = means # adds calculated means to table

# below: calculates minimum value that is within a reasonable range to be considered an active lane
meanmin = max(means)
for val in means:
    if (val < meanmin) and (val*4 > max(means)):
        meanmin = val


tmtMXR['rel. ratio'] = tmtMXR['means'] / meanmin # adds relative ratio to table
tmtMXR['add. percent'] = 1 / tmtMXR['rel. ratio'] # adds new calculated mixratio to table

tmtMXR['add. percent'][tmtMXR['add. percent']>1] = 0 # converts empty lanes to 0
tmtMXR = tmtMXR.round({'add. percent':3, 'rel. ratio':4, 'means':4}) # rounds lanes to 4 digits

tmtMXR.columns = ['Abundance Means', 'Relative Abundance Ratio', 'New Mix Ratio']

tmtMXR.to_csv('D:\\tmt mixing\\'+f'/{sav}_values.csv', index=False) # saves table

plt.table(cellText=tmtMXR.values, colLabels=tmtMXR.columns, loc='center', cellLoc='center') # creates picture of table, saves
plt.axis('off')
plt.title(f"{sav} TMT mix ratio", y=1.08)
plt.tight_layout()
plt.xticks([])
plt.yticks([])
plt.savefig('D:\\tmt mixing\\'+f'{sav}_tmtstats.png', dpi=1200)
plt.clf()
