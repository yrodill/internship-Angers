# coding: utf8

import pandas as pd
import argparse
from copy import deepcopy
from tqdm import tqdm
import sys
import glob
import os

"""
Bothorel Benoît
July 2019
Regroup all recaps in one file
""" 


parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('folder', metavar='d', type=str, help='folder containing the results')

args = parser.parse_args()

"""
First step :
Delete file is it already exists
"""
if(os.path.isfile("recap_final.csv")):
    os.remove("recap_final.csv")

"""
Second step :
Write every recap file after each others
"""

for folder in glob.glob(args.folder+"/*"):
    if(folder.split('/')[-1] != 'global'):
        for file in glob.glob(folder+"/*"):
            if(file.split('/')[-1] == 'recap.csv'):
                df = pd.read_csv(file)
                with open("recap_final.csv","a") as f:
                    f.write(str(folder.split('/')[-1])+','+'Cluster'+','+'AUROC'+','+'AUPR'+'\n')
                    
                    
                df.insert(0,'Folder','')
                df2 = pd.read_csv('recap_final.csv',header=None)
                df.columns=['Folder','Cluster','AUROC','AUPR']
                df.sort_values(by='AUROC',ascending=False,inplace=True)
                df2.columns=['Folder','Cluster','AUROC','AUPR']
                df3 = pd.concat([df2,df],ignore_index=True,axis=0)
                df3.fillna(' ',inplace=True)
                df3.to_csv('recap_final.csv',header=False,index=False)

os.remove('recap.csv')