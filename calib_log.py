# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 09:36:00 2022

@author: HUFFMP
"""

import sys # for reading PD parameters
import json # for reading PD output
import os # for determining user
import pandas as pd # for data manipulation
import datetime # for determining date

BSAcode = 'A0A140T897' # ID for the protein of interest, BSA
json_loc = sys.argv[1] # parameter passed: outputs
ms_machine = sys.argv[2] # parameter passed: machine
ms_standard = sys.argv[3] # parameter passed: standard (bsa/hela)

with open(json_loc, encoding="utf-8") as g:
    lines = json.load(g) # loads information of outputs

infoloc1 = lines['Tables'][0]['DataFile'] # first output table location
infoloc2 = lines['Tables'][1]['DataFile'] # second output table location

cols = ['initial', 'date', 'standard', 'gradient', 'injection,ng/fm', 'protein', 'peptides', 'PSMs', 'MS2', 'sequence coverage for BSA', 'TIC intensity'] # columns of log file

df1 = pd.read_excel('\\\\amer.pfizer.com\\pfizerfiles\\Research\\LAJ\\oru-tcb\\ChemBio\\Standards on Lumos and Eclipse.xlsx', 'Lumos') # reads lumos log
df2 = pd.read_excel('\\\\amer.pfizer.com\\pfizerfiles\\Research\\LAJ\\oru-tcb\\ChemBio\\Standards on Lumos and Eclipse.xlsx', 'Eclipse') # reads eclipse log

df = pd.read_csv(infoloc1, sep='\t') # reads first table request : proteins
sdf = pd.read_csv(infoloc2, sep='\t') # reads second table request : summary statistics
user = os.getlogin() # gets user information
date = str(datetime.date.today()) # gets date information

t_col_coverage = ''
for b in df.columns:
    if b.lower().count('coverage')>0:
        t_col_coverage = b
# the above is kind of a convoluted way to find the coverage column -- I wasn't sure what the actual column name was at the time and then I never bothered to
# change this when I found it out. Awkward, but still works and it's not going to be computationally slow anyways. Also checks to make sure the table is
# pulled down successfully.

if ms_standard.lower() == 'bsa' and t_col_coverage: # standard is bsa and table is correct
    bsa_cov = df[df['Accession']==BSAcode].reset_index().loc[0][t_col_coverage] # accesses BSA coverage. BSA sometimes has multiple isoforms so this also always pulls 
    # down the main one.
    gradient = '0.5h' # same in every line
    injection = '60fm' # same in every line
    additive = pd.Series([user, date, 'BSA', gradient, injection, '', '', '', '', bsa_cov, ''], index=cols) # the new line to be written into file

elif ms_standard.lower() == 'hela': # standard is hela
    gradient = '2h' #same in every line
    injection = '200ng' # same in every line
    prot=sdf[sdf['Name']=='Protein Groups - # Peptides'].reset_index().loc[0]['Count'] # value of proteins - I don't remember why I made these call statements so
    # awkward--  I think I was having issues with regular .loc commands at the time and these worked. Never went back to simplify.
    pep=sdf[sdf['Name']=='Peptide Groups - # Proteins'].reset_index().loc[0]['Count'] # value of peptides
    psm=sdf[sdf['Name']=='PSMs - # Proteins'].reset_index().loc[0]['Count'] # value of PSMs
    ms2=sdf[sdf['Name']=='MS/MS Spectrum Info - # Precursors'].reset_index().loc[0]['Count'] # value of MSMS spectra
    additive = pd.Series([user, date, 'Hela', gradient, injection, prot, pep, psm, ms2, '', ''], index=cols) # the new line to be written into file
    t_col_coverage = True # table pulled down successfully - all of these t_col_coverage checks are there because I was having issues with unsuccessful BSA runs adding
    # junk into the log file. Easier to build it like this than filter for those.

if t_col_coverage:
    if ms_machine.lower() == 'lumos':
        df1 = df1.append(additive, ignore_index=True) # writing new line into lumos sheet
    elif ms_machine.lower() == 'eclipse':
        df2 = df2.append(additive, ignore_index=True) # writing new line into eclipse sheet
    
    with pd.ExcelWriter('\\\\amer.pfizer.com\\pfizerfiles\\Research\\LAJ\\oru-tcb\\ChemBio\\Standards on Lumos and Eclipse.xlsx') as writer:
        df1.to_excel(writer, sheet_name='Lumos', index=False) # saving both sheets to file
        df2.to_excel(writer, sheet_name='Eclipse', index=False) # saving both sheets to file
