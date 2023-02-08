# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 09:36:00 2022

@author: HUFFMP
"""

import pandas as pd
import sys
from time import sleep as slp
from matplotlib import pyplot as plt
import json

def stop():
    print('Exiting mixratio.exe. Thanks for dropping by.')
    slp(2)
    sys.exit()

json_loc = sys.argv[1]
THRESH = float(sys.argv[2])

with open(json_loc, encoding="utf-8") as g:
    lines = json.load(g)

infoloc1 = lines['Tables'][0]['DataFile']
df = pd.read_csv(infoloc1, sep='\t')

sav = lines['CurrentWorkflowID']
#df = pd.read_excel('\\\\amer.pfizer.com\\pfizerfiles\\Research\\LAJ\\oru-tcb\\ChemBio\\HUFFMP\\python scripts\\incomplete psms.xlsx')
#THRESH = 0.15

abundances = list(pd.Series(df.columns)[pd.Series(df.columns).str.contains('Abundance:')].values)
if len(abundances)==0:
    abundances = list(pd.Series(df.columns)[pd.Series(df.columns).str.contains('Abundances:')].values)
if len(abundances)==0:
    abundances = list(pd.Series(df.columns)[pd.Series(df.columns).str.contains('Abundances')].values)
if len(abundances)==0:
    abundances = list(pd.Series(df.columns)[pd.Series(df.columns).str.contains('Abundance')].values)

srs_middle = pd.Series(index=abundances)

means = []
for col in abundances:
    df_slice = df[col].astype('float64')
    df_slice = df_slice[(df_slice>df_slice.quantile(THRESH))&(df_slice<df_slice.quantile(1-THRESH))]
    means.append(df_slice.mean())

plt.bar(abundances, means)
plt.ylabel('Mean Abundance')
plt.xlabel('TMT Lane')
plt.xticks([i for i in range(0, 17)], [str(i) for i in range(1, 18)])
plt.title('TMT Lanes: Mean Abundances')
plt.savefig('D:\\tmt mixing\\'+f'{sav}_bar.png', dpi=1200)
plt.clf()

tmtMXR = pd.DataFrame()
tmtMXR['means'] = means

meanmin = max(means)
for val in means:
    if (val < meanmin) and (val*4 > max(means)):
        meanmin = val


tmtMXR['rel. ratio'] = tmtMXR['means'] / meanmin
tmtMXR['add. percent'] = 1 / tmtMXR['rel. ratio']

tmtMXR['add. percent'][tmtMXR['add. percent']>1] = 0
tmtMXR = tmtMXR.round({'add. percent':3, 'rel. ratio':4, 'means':4})

tmtMXR.columns = ['Abundance Means', 'Relative Abundance Ratio', 'New Mix Ratio']

tmtMXR.to_csv('D:\\tmt mixing\\'+f'/{sav}_values.csv', index=False)

plt.table(cellText=tmtMXR.values, colLabels=tmtMXR.columns, loc='center', cellLoc='center')
plt.axis('off')
plt.title(sav, y=1.08)
plt.tight_layout()
plt.xticks([])
plt.yticks([])
plt.savefig('D:\\tmt mixing\\'+f'{sav}_tmtstats.png', dpi=1200)
plt.clf()