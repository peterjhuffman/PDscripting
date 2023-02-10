# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 09:36:00 2022

@author: HUFFMP
"""
# Importing necessary modules
import pandas as pd # for data manipulation
import sys # for exit command
from time import sleep as slp # also for exit command
from matplotlib import pyplot as plt # for data visualizations

"""
stop()
simple function that exits the program if something is incorrect or complete.
"""
def stop():
    print('Exiting mixratio.exe. Thanks for dropping by.')
    slp(2)
    sys.exit()

datasource = input('DATA LOCATION (x to exit): ') # Asking for file location
print('Loading file.')
if datasource.lower()=='x':
    stop()
fdtype = datasource[-3:] # Distinguishing between csv and xlsx files
if fdtype == 'csv':
    df = pd.read_csv(datasource) # Reading file
elif fdtype == 'lsx':
    df = pd.read_excel(datasource) # Reading file
else:
    print('filetype not recognized.')
    stop()
print('File read successfully.\n')

df.dropna(inplace=True, thresh=3) # removing rows with missing values

sav = '.'.join(datasource.split('.')[:-1]).split('\\')[-1] # sav is the name of the file
newpath = f'\\\\amer.pfizer.com\\pfizerfiles\\Research\\LAJ\\oru-tcb\\ChemBio\\MS_Analyses_PD\\tmt mixing' # path to which the result files are saved



THRESH = str(input('THRESHOLD (ex: enter 0.15 for the middle 70%)(x to exit): ')) # asking for the threshold information
if THRESH.lower()=='x':
    stop()
THRESH = float(THRESH) # converting threshold to numeric
if (THRESH > 1) or (THRESH<0.01):
    print('Incorrect threshold notation. Ask Peter.')
    stop()

ab_count = 1
for ab in df.columns:
    print(f"{ab_count}: {ab}")
    ab_count+=1
print()
print('Abundance columns detected.')
ab_select = input('Enter the start and end indices of the desired abundance columns for analysis, separated by a comma.\n'+
                  'Example: if columns 1-18 are desired, input should be: 1,18.\n'+
                  'Type ALL for all columns.\n\nIndices: ')
# prints out all the columns. Asks the user which columns are the columns of interest containing abundance values.

if ab_select.upper() == 'ALL': #if user wants all columns
    abundances = df.columns
elif len(ab_select.split(','))!=2: # error if formatting is incorrect
    print('Incorrect Formatting.')
    stop()
else:
    ab_indc = ab_select.split(',')
    abundances = abundances[int(ab_indc[0])-1:int(ab_indc[1])] # selects requested columns

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------

means = []
for col in abundances: #for each lane, cuts values above and below threshold and calculates mean.
    df_slice = df[col]
    df_slice = df_slice[(df_slice>df_slice.quantile(THRESH))&(df_slice<df_slice.quantile(1-THRESH))] 
    means.append(df_slice.mean())

plt.bar(abundances, means) # creates bar plot
plt.ylabel('Mean Abundance')
plt.xlabel('TMT Lane')
plt.xticks([i for i in range(0, 18)], [str(i) for i in range(1, 19)])
plt.title('TMT Lanes: Mean Abundances')
plt.savefig(newpath+f'/{sav}_bar.png', dpi=1200)
print(f'barplot saved to folder ChemBio\MS_Analyses_PD\TMTtesting/{sav}')
plt.clf()

tmtMXR = pd.DataFrame() # creates table
tmtMXR['means'] = means # adds calculated means to table

meanmin = max(means)
for val in means:
    if (val < meanmin) and (val*4 > max(means)): # calculates minimum value that is within a reasonable range to be considered an active lane
        meanmin = val

tmtMXR['rel. ratio'] = tmtMXR['means'] / meanmin # adds relative ratio to table
tmtMXR['add. percent'] = 1 / tmtMXR['rel. ratio'] # adds new calculated mixratio to table

tmtMXR['add. percent'][tmtMXR['add. percent']>1] = 0 # converts empty lanes to 0
tmtMXR = tmtMXR.round({'add. percent':3, 'rel. ratio':4, 'means':4}) # rounds lanes to 4 digits

tmtMXR.columns = ['Abundance Means', 'Relative Abundance Ratio', 'New Mix Ratio']

tmtMXR.to_csv(newpath+f'/{sav}_values.csv', index=False) # saves table

plt.table(cellText=tmtMXR.values, colLabels=tmtMXR.columns, loc='center', cellLoc='center') # creates picture of table, saves
plt.axis('off')
plt.title('TMT mix ratio calculation', y=1.08)
plt.tight_layout()
plt.xticks([])
plt.yticks([])
print(newpath+f'/{sav}_summary{str(int(THRESH*100))}.png')
plt.savefig(newpath+f'/{sav}_summary{str(int(THRESH*100))}.png', dpi=1200)
print(f'TMT mix ratio table saved to folder ChemBio\MS_Analyses_PD\TMTtesting/{sav}')
plt.clf()
