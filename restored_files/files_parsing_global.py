# coding: utf8

import pandas as pd
import argparse
from copy import deepcopy
from tqdm import tqdm
import sys

"""
Bothorel Benoît
July 2019
Formating files for the enrichment analysis for global (without clustering)
with GOATOOLS https://github.com/tanghaibao/goatools/
""" 

def format_GO_file(df,genes,index):
    for i in range(len(df.index)):
        if(df.iat[i,0] not in genes):
            genes[df.iat[i,0]] = [df.iat[i,index]]
        else:
            genes[df.iat[i,0]].append(df.iat[i,index])

    with open('tmp_{}'.format(args.GO.split('/')[-1]),'w') as f:
        for k,v in genes.items():
            string = str(k)+"\t"
            for i in range(len(v)):
                if(i != len(v)-1):
                    string+=str(v[i])+';'
                else:
                    string+=str(v[i])+'\n'
            f.write(string)


parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('original', metavar='d', type=str, help='file containing the original matrix')
parser.add_argument('data', metavar='d', type=str, help='file containing the genes links')
parser.add_argument('GO', metavar='g', type=str, help='file from TAIR database for the GO association')
parser.add_argument('--threshold', metavar='t', type=int, help='threshold for the cluster`s size',default=100)
parser.add_argument('--specific', action='store_true', help='If you are using a specific GO file (one given by parse_GO.py)',default=False)

args = parser.parse_args()

"""
Part 1 :
Parsing the GO file
"""

df = pd.read_csv(args.GO,sep='\t',header=None)
genes = {}

if(args.specific):
    format_GO_file(df,genes,1)
else:
    format_GO_file(df,genes,5)

"""
Part 2 :
Population file
"""
df = pd.read_csv(args.original,header=0)
with open('population_{}'.format(args.original),'w') as f:
    for gene in df.columns.values:
        f.write(str(gene)+'\n')

"""
Part 3 :
Study file
File containing all the genes from the selected pairs
"""

df = pd.read_csv(args.data, header=0)

genes = []
with open('study_{}'.format(args.data),'w') as f:
    for i in range(len(df.index)):
        if(df.iat[i,0] not in genes):
            f.write(str(df.iat[i,0])+'\n')
            genes.append(df.iat[i,0]) 
        if(df.iat[i,1] not in genes):
            f.write(str(df.iat[i,1])+'\n')
            genes.append(df.iat[i,1])

