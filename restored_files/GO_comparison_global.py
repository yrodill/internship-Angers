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

def compute_results(file,method,egad,folder):
    tot_gen = 0
    score = 0.0
    if(method == 'PR'):
        df = pd.read_excel("results/global/"+folder+"/"+args.goatools.split("/")[-1],index_col=None)
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
        df.loc[len(df.index)+1] = [method+" score",score,'','','','','','','','','','','']
        df.to_csv("results/global/"+folder+"/"+args.goatools.split("/")[-1],index=False)
    else:
        df = pd.read_excel(args.goatools,index_col=None)
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

        df.loc[len(df.index)+1] = [method+" score",score,'','','','','','','','','','']
        if(os.path.isdir("results/global/"+folder)):
            print("File existing...Next step !")
        else:
            os.mkdir("results/global/"+folder)
        df.to_excel("results/global/"+folder+"/"+file.split("/")[-1],index=False)


#MAIN
parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('auroc', metavar='a', type=str, help='EGAD file with GO terms that are enriched with AUROC values')
parser.add_argument('pr', metavar='p', type=str, help='EGAD file with GO terms that are enriched with PR values')
parser.add_argument('goatools', metavar='d', type=str, help='file given by the GOATOOLS analysis')
parser.add_argument('method', metavar='m', type=str, help='method used')
parser.add_argument('data', metavar='d', type=str, help='data type')
parser.add_argument('exp', metavar='e', type=str, help='exp type')
parser.add_argument('threshold', metavar='t', type=str, help='threshold used for link selection')
parser.add_argument('--HRR',action='store_true', help='if HRR used', default=False)

args = parser.parse_args()

auroc = pd.read_csv(args.auroc,sep=',',header=0)
pr = pd.read_csv(args.pr,sep=',',header=0)

if(args.HRR):
    folder = args.method+'_'+args.data.split('.')[0]+'_'+args.exp+'_'+args.threshold+'_HRR'
else:
    folder = args.method+'_'+args.data.split('.')[0]+'_'+args.exp+'_'+args.threshold


compute_results(args.goatools,'AUROC',auroc,folder)
compute_results(args.goatools,'PR',pr,folder)
