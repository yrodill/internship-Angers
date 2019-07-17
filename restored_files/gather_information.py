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
Gathering information from clusters (AUROC/AUPR) in each folder
""" 


parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('folder', metavar='d', type=str, help='folder containing the results')

args = parser.parse_args()

for folder in glob.glob(args.folder+"/*"):
    if(folder.split('/')[-1] != 'global'):
        firstLoop = True
        for file in glob.glob(folder+"/*"):
            df = pd.read_csv(file)
            if(file.split('/')[-1] == 'recap.csv'):
                continue
            if(os.path.isfile(folder+"/recap.csv") and firstLoop):
                os.remove(folder+"/recap.csv")
                firstLoop = False              
            with open(folder+"/recap.csv","a") as f:
                f.write(str(file.split('study_')[-1].split('_')[0])+','+str(df.iat[len(df.index)-2,1])+','+str(df.iat[len(df.index)-1,1])+'\n')