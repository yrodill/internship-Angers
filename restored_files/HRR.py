#coding: utf8

import os
import pandas as pd
import argparse
from joblib import Parallel, delayed
from tqdm import tqdm

"""
Bothorel Benoît
15/05/2019 
PCC-HRR adaptation in python (it is the HRR part)
If you are using this for a big dataset be sure to change the max_nbytes setting for
the parallelization. (default is 1M)
Also, if you choose a threshold which is too permissive (like 1000) with a big dataset,
you might run into a memory usage error.
File must be in the same directory as the script.

The data provided must be a square matrix with the gene's names as headers and indexes.
Example:
            AT1G15000	        AT4G01130	        AT1G20690
AT1G15000	0.0	                0.2735387936905061	0.13014157940367135
AT4G01130	0.2735387936905061	0.0	                0.13504720604904427
AT1G20690	0.13014157940367135	0.13504720604904427	0.0
"""

def byValue(array):
    return array[2]

def keep_best_links(df,l):
    result=[]
    with open('tmp_{}.csv'.format(args.data.split('.')[0]),'a') as f:
        for j in range(len(df.index)):
            result.append([df.columns.values[l],df.columns.values[j],df.iat[l,j]])
        result=sorted(result,key=byValue,reverse=True)
        index=0
        for val in result:
            if(index < args.threshold):
                index+=1
                f.write(str(val[0])+','+str(val[1])+','+str(val[2])+','+str(index)+'\n')
            else:
                return

def select_ranks(df,i,liste):
    gene1 = df.at[i,'gene1']
    gene2 = df.at[i,'gene2']
    liste.append([gene1,gene2])
    if([gene2,gene1] in liste[0]):
        return
    for j in range(i+1,len(df.index)):
        if(gene1 == df.at[j,'gene2'] and gene2 == df.at[j,'gene1']):
            maxi=max(df.at[i,'rank'],df.at[j,'rank'])
            df.at[i,'rank']=maxi
            df.at[j,'rank']=maxi
            if(df.at[i,'value']!= 0):
                return [df.at[i,'gene1'],df.at[i,'gene2'],df.at[i,'value'],df.at[i,'rank']]


parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('data', metavar='f', type=str, help='matrix containing the pearson corr results and the genes names in col/row')
parser.add_argument('--threshold', metavar='t',default=10, type=int, help='threshold for the rank filter')
parser.add_argument('--njobs', metavar='j', type=int, help='number of cpus to use for parallel computing',default=1)
parser.add_argument('--bytes', metavar='b', type=str, help='max_nbytes parameter for Parallel',default="1M")
parser.add_argument('--zeros',action='store_true', help='Use this tag if your matrix contains half values',default=False)

args = parser.parse_args()

print('Reading file...')
df = pd.read_csv(args.data,header=0,index_col=0)
df = df.astype('float64') #be sure to have all dataframe with the same type
print("Done...")

if(args.zeros):
    print("Preprocessing...")
    for i in tqdm(range(len(df.columns))):
        for j in range(i+1,len(df.index)):
            if(df.iat[j,i] == 0 or df.iat[j,i] == 0.0):
                df.iat[j,i] = df.iat[i,j]
    print('Done...')

print("Step 1/2...")
Parallel(n_jobs=args.njobs)(delayed(keep_best_links)(df,l) for l in tqdm(range((len(df.columns)))))
print("Done...")
del(df) #free memory

df2 = pd.read_csv('tmp_{}.csv'.format(args.data.split('.')[0]),header=None)
df2.columns=["gene1","gene2","value",'rank']

print("Step 2/2...")
genes=[]
liste = Parallel(n_jobs=args.njobs,max_nbytes=args.bytes)(delayed(select_ranks)(df2,i,genes) for i in tqdm(range(len(df2.index))))
liste = [x for x in liste if x is not None]
df3 = pd.DataFrame(liste,columns=["gene1","gene2","value","rank"])         
df3=df3.sort_values(by='value',ascending=False)
df3.to_csv('link_HRR_{}.csv'.format(args.data.split('.')[0]),index=False)
print("Done...")

print("Delete temporary file...")
os.system("rm -f tmp_{}.csv".format(args.data.split('.')[0]))
print("Done...")