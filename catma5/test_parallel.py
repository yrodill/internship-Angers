import pandas as pd
import numpy as np
from joblib import Parallel, delayed
import argparse
from cdt.independence.stats.numerical import MIRegression
from cdt.independence.stats.numerical import PearsonCorrelation
from sklearn.feature_selection import mutual_info_regression
from tqdm import tqdm
import time
import sys

"""
Bothorel Benoît
May 2019
Launch MI or PC on data
"""

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('data', metavar='f', type=str, help='data')
parser.add_argument('model', metavar='m', type=str, help='correlation to be used')
parser.add_argument('--njobs', metavar='j', type=int, help='number of jobs for parralel computation',default=1)
parser.add_argument('--header', help='use if your data contains headers',default=False,action='store_true')


args = parser.parse_args()

with open(args.data) as f:
    genes=f.readline().strip().replace('"','').split(',')

print('Reading file...')
if(args.header):
    data = pd.read_csv(args.data, sep=',',header=None,skiprows=1)
else:
    data = pd.read_csv(args.data, sep=',',header=None)
print("Done...")

def mi_job(data,model,l):
    result=[]
    for j in range(len((data.columns))):
        if(j <= l):
            result.append(0)
        else:
            result.append(model.predict(data[l].values, data[j].values)[0])
    return result

def pc_job(data,model,l):
    result=[]
    for j in range(len((data.columns))):
        if(j <= l):
            result.append(0)
        else:
            result.append(model.predict(data[l].values, data[j].values))
    return result
  


# Exec computations
print("Launch parallelization...")
if(args.model == "MI"):
    model = MIRegression()
    results = Parallel(n_jobs=args.njobs)(delayed(mi_job)(data,model,l) for l in tqdm(range(len(data.columns))))
else:
    model = PearsonCorrelation()
    results = Parallel(n_jobs=args.njobs)(delayed(pc_job)(data,model,l) for l in tqdm(range(len(data.columns))))
print("Done..")

if(args.header):
    report = pd.DataFrame(results,columns=genes,index=genes)
    report.to_csv("{}_{}.csv".format(args.data.split('/')[-1].split('.')[0],args.model),index=True,header=True)
else:
    report = pd.DataFrame(results)
    report.to_csv("{}_{}.csv".format(args.data.split('/')[-1].split('.')[0],args.model),index=False,header=False)

