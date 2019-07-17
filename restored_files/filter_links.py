#coding: utf8

import os
import pandas as pd
import argparse
from joblib import Parallel, delayed
from tqdm import tqdm

"""
Bothorel Benoît
15/05/2019 
Filter_links.py allows you to chose the best values either by rank (--HRR) or by value(default)
If you are using this for a big dataset be sure to change the max_nbytes setting for
the parallelization. (default is 10M)
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
            result.append([df.columns.values[l],df.columns.values[j],abs(df.iat[l,j])])
        result=sorted(result,key=byValue,reverse=True)
        index=0
        for val in result:
            if(index < args.threshold):
                index+=1
                f.write(str(val[0])+','+str(val[1])+','+str(val[2])+','+str(index)+'\n')
            else:
                return

def select_ranks(df1,df2,i,liste):
    gene1 = df2.at[i,'gene1']
    gene2 = df2.at[i,'gene2']
    liste.append([gene1,gene2])
    if([gene2,gene1] in liste[0]):
        return
    for j in range(i+1,len(df2.index)):
        if(gene1 == df2.at[j,'gene2'] and gene2 == df2.at[j,'gene1']):
            maxi=max(df2.at[i,'rank'],df2.at[j,'rank'])
            df2.at[i,'rank']=maxi
            df2.at[j,'rank']=maxi
            if(df2.at[i,'value']!= 0):
                return [gene1,gene2,df1.at[gene1,gene2],df2.at[i,'rank']]

def select_ranks_V2(df1,df2,i):
    gene1 = df2.at[i,'gene1']
    gene2 = df2.at[i,'gene2']
    with open('tmp_V2_{}.csv'.format(args.data.split('.')[0]),'a') as f:
        for j in range(i+1,len(df2.index)):
            if(gene1 == df2.at[j,'gene2'] and gene2 == df2.at[j,'gene1']):
                maxi=max(df2.at[i,'rank'],df2.at[j,'rank'])
                df2.at[i,'rank'] = maxi
                df2.at[j,'rank'] = maxi
                if(df2.at[i,'value']!= 0):
                    f.write(str(gene1)+','+str(gene2)+','+str(df1.at[gene1,gene2])+','+str(df2.at[i,'rank'])+'\n')

def keep_best_values(df,l):
    result=[]
    with open('tmp_{}.csv'.format(args.data.split('.')[0]),'a') as f:
        for j in range(len(df.index)):
            if(df.iat[l,j] < 0):
                result.append([df.columns.values[l],df.columns.values[j],abs(df.iat[l,j]),"-"])
            else:
                result.append([df.columns.values[l],df.columns.values[j],abs(df.iat[l,j]),"+"])
        result=sorted(result,key=byValue,reverse=True)
        index=0
        for val in result:
            if(index < 100):
                index+=1
                f.write(str(val[0])+','+str(val[1])+','+str(val[2])+','+str(val[3])+'\n')
            else:
                return

def delete_duplications(df2,i):
    gene1 = df2.iat[i,0]
    gene2 = df2.iat[i,1]
    for j in range(i+1,len(df2.index)):
        if(gene1 == df2.iat[j,1] and gene2 == df2.iat[j,0]):
            if(df2.iat[i,2] == df2.iat[j,2]):
                return j
            else: 
                return

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('data', metavar='f', type=str, help='matrix containing the pearson corr results and the genes names in col/row')
parser.add_argument('--POBL', metavar='p',default=5000, type=int, help='Number of best links to keep in the end')
parser.add_argument('--threshold', metavar='t',default=5, type=int, help='Number of ranks to keep by genes (can hugely lower computation time with small value for big dataset) ')
parser.add_argument('--HRR', action='store_true', default=False, help='if you want to use HRR to sort by rank')
parser.add_argument('--njobs', metavar='j', type=int, help='number of cpus to use for parallel computing',default=1)
parser.add_argument('--bytes', metavar='b', type=str, help='max_nbytes parameter for Parallel',default="10M")
parser.add_argument('--fill', action='store_true', default=False, help='use if your matrix is halved')


args = parser.parse_args()


print('Reading file...')
df = pd.read_csv(args.data, header=0, index_col=0)
df = df.astype('float64') #be sure to have all dataframe with the same type
print("Done...")

print("Using {} cores.".format(args.njobs))

if(args.threshold == -1):
    args.threshold = len(df.index)

#NB_OF_LINKS_TO_KEEP = int(round(args.POBL/100 * (len(df.index)**2)))

if(args.fill):
    print("Completing the matrix...")
    df2 = df.T
    df = df + df2
    print('Done...')

if(args.HRR):
    print("Step 1/2...")
    Parallel(n_jobs=args.njobs, max_nbytes=args.bytes)(delayed(keep_best_links)(df,l) for l in tqdm(range((len(df.columns)))))
    print("Done...")

    df2 = pd.read_csv('tmp_{}.csv'.format(args.data.split('.')[0]),header=None)
    df2.columns=["gene1","gene2","value",'rank']

    print("Step 2/2...")
    Parallel(n_jobs=args.njobs, max_nbytes=args.bytes)(delayed(select_ranks_V2)(df,df2,i) for i in tqdm(range(len(df2.index))))    
    df3 = pd.read_csv('tmp_V2_{}.csv'.format(args.data.split('.')[0]),header=None)
    df3.columns=["gene1","gene2","value",'rank']
    df3 = df3.sort_values(by='rank',ascending=True)
    df3 = df3.head(args.POBL)
    df3.to_csv('tmp_{}'.format(args.data),index=False)
else:
    Parallel(n_jobs=args.njobs,max_nbytes=args.bytes)(delayed(keep_best_values)(df,l) for l in tqdm(range((len(df.columns)))))
    df2 = pd.read_csv('tmp_{}.csv'.format(args.data.split('.')[0]),header=None)
    df2.columns=["gene1","gene2","value","signe"]
    df2 = df2.sort_values(by='value',ascending=False)
    #eliminate duplications and recover real value of correlation
    # if MI or PC
    df2 = df2.head(args.POBL*2)
    indexes = Parallel(n_jobs=args.njobs,max_nbytes=args.bytes)(delayed(delete_duplications)(df2,l) for l in tqdm(range((len(df2.index)))))
    indexes = [x for x in indexes if x is not None]
    indexes = list(set(indexes)) #unique indices
    for i in tqdm(range(len(df2.index))):
        if(df2.iat[i,3] == '-'):
            df2.iat[i,2] = -1 * df2.iat[i,2]
    df2.drop(df2.index[indexes],inplace=True)
    df2.drop(columns=['signe'],inplace=True)
    df2 = df2.head(args.POBL)
    df2.to_csv('tmp_{}'.format(args.data),index=False)


print("Done...")
