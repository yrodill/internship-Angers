#coding: utf8

import os
import pandas as pd
import argparse
from joblib import Parallel, delayed
from tqdm import tqdm
from glob import glob

"""
Bothorel Benoît
04/06/2019 
Find the GO terms signification in the original GO file
"""

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('EGAD', metavar='d', type=str, help='EGAD file with GO terms that are enriched')
parser.add_argument('GO', metavar='f', type=str, help='Original GO file used')

args = parser.parse_args()

egad = pd.read_csv(args.EGAD,sep=',',header=0)
egad['function']='0'
go = pd.read_csv(args.GO,sep='\t',header=None)

for i in tqdm(range(len(egad.index))):
    for j in range(len(go.index)):
        if(egad.at[i,'GO'].replace('.',':') == go.at[j,5]):
            egad.at[i,'function'] = go.at[j,4]
            break

egad=egad.sort_values(by='value',ascending=False)
egad.to_csv(args.EGAD)

for file in glob("./study/*"):
    if(file.split('_')[1].replace('cluster','') == args.EGAD.split('_')[1]):
        #after finding the matching files compare !
        goatools = pd.read_csv(file)
        print(goatools)