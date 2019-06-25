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

def compute_results(file,method,egad):
    tot_gen = 0
    score = 0.0
    if(file.split('_')[1].replace('cluster','') == args.auroc.split('/')[-1].split('_')[1]):
        df = pd.read_excel(file,index_col=None)
        df[method] = 0.0
        for i in tqdm(range(len(df.index))):
            for j in range(len(egad.index)):
                if(df.at[i,'GO'] == egad.at[j,'GO'].replace(".",":")):
                    df.at[i,method] = egad.at[j,'value']
                    tot_gen += df.at[i,'study_count']
                    score += float(df.at[i,method]*df.at[i,'study_count'])
                    break
        score /= tot_gen
        df=df.sort_values(by='p_uncorrected',ascending=True)
        if(method == 'PR'):
            df.loc[-1]=[method+" score",score,'','','','','','','','','','','']
            # index = []
            # for i in range(len(df.index)):
            #     if(df.at[i,method] == 0.0):
            #         index.append(i)
            # df=df.drop(index)
            df.to_csv(file,index=False)
        else:
            df.loc[-1]=[method+" score",score,'','','','','','','','','','']
            df.to_excel(file,index=False)


#MAIN
parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('auroc', metavar='d', type=str, help='EGAD file with GO terms that are enriched with AUROC values')
parser.add_argument('pr', metavar='d', type=str, help='EGAD file with GO terms that are enriched with PR values')

args = parser.parse_args()

auroc = pd.read_csv(args.auroc,sep=',',header=0)
pr = pd.read_csv(args.pr,sep=',',header=0)


for file in glob(os.getcwd()+"/xls/*"):
    compute_results(file,'AUROC',auroc)
    compute_results(file,'PR',pr)
