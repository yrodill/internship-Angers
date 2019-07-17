#coding: utf8

from GENIE3 import *
import argparse
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('data', metavar='d', type=str, help='data')
parser.add_argument('nCores', metavar='c', type=int, help='number of cores for parralel computing')
parser.add_argument('out', metavar='o', type=str, help='File output')


args = parser.parse_args()

data = pd.read_csv(args.data)
genes = data.columns

print("Reading file...")
matrix = np.matrix(data)
print("Done...")
print(matrix)

print("Launching GENIE3...")
VIM = GENIE3(matrix,nthreads=args.nCores)
print("Done...")

res = pd.DataFrame(VIM,index=genes,columns=genes)
print(res)

print("Writing result...")
res.to_csv(args.out,sep=',')
print("Done")