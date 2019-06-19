import os
import sys
import glob
import argparse
import pandas as pd
import numpy as np
from cdt.independence.stats.numerical import MIRegression
from cdt.independence.stats.numerical import PearsonCorrelation
from tqdm import tqdm
from math import sqrt

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('folder', metavar='f', type=str, help='data folder')
parser.add_argument('model', metavar='m', type=str, help='correlation to be used')


args = parser.parse_args()

dir_path=os.path.dirname(os.path.realpath(__file__))

genesNames = []
matrix = []

if(args.model == "MI"):
    model = MIRegression()
    for file in glob.glob(dir_path + "/*" + args.folder + "_filtered.*"):
        print("Running on file : {} , ...".format(file))
        filename = file.split("/")[-1].replace(".csv","")
        print("Reading file...")
        data = pd.read_csv(file,sep=',')
        print("Done...")
        genesNames = data.columns
        pbar = tqdm(total=len(data.columns))
        for idx_i, i in enumerate(data.columns):
            pbar.update(1)
            results = []  
            for idx_j, j in enumerate(data.columns[idx_i+1:]):
                score = model.predict(data[i].values, data[j].values)
                results.append(score)
            matrix.append(results)
        pbar.close()

else:
    model = PearsonCorrelation()
    for file in glob.glob(dir_path + "/*" + args.folder + "_filtered.*"):
        print("Running on file : {} , ...".format(file))
        filename = file.split("/")[-1].replace(".csv","")
        print("Reading file...")
        data = pd.read_csv(file,sep=',')
        print("Done...")
        genesNames = data.columns
        pbar = tqdm(total=(len(data.index)*len(data.columns))/2)
        for idx_i, i in enumerate(data.columns):
            pbar.update(1)
            results = []  
            for idx_j, j in enumerate(data.columns[idx_i+1:]):
                score = model.predict(data[i].values, data[j].values)
                results.append(score)
            matrix.append(results)
        pbar.close()
            
print(matrix)
df=pd.DataFrame(matrix)
if(args.folder != "MI"):
    args.folder = "Pearson"
df.to_csv(args.folder + "/" + args.folder + "_"+filename+".csv")
print("Done...")