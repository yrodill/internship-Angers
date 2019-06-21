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

args = parser.parse_args()

egad = pd.read_csv(args.EGAD,sep=',',header=0)

for file in glob(os.getcwd()+"/xls/*"):
    tot_gen = 0
    score = 0.0
    if(file.split('_')[1].replace('cluster','') == args.EGAD.split('/')[-1].split('_')[1]):
        df = pd.read_excel(file,index_col=None)
        df['AUC'] = 0.0
        for i in tqdm(range(len(df.index))):
            for j in range(len(egad.index)):
                if(df.at[i,'GO'] == egad.at[j,'GO'].replace(".",":")):
                    df.at[i,'AUC'] = egad.at[j,'value']
                    tot_gen += df.at[i,'study_count']
                    score += float(df.at[i,'AUC']*df.at[i,'study_count'])
                    break
        # index = []
        # for i in range(len(df.index)):
        #     if(df.at[i,'AUC'] == 0.0):
        #         index.append(i)
        # df=df.drop(index)
        score /= tot_gen
        df=df.sort_values(by='p_uncorrected',ascending=True)
        df.loc[-1]=["AUC score",score,'','','','','','','','','','']
        df.to_csv(file,index=False)