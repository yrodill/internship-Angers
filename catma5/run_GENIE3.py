from GENIE3 import *
import argparse
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('data', metavar='d', type=str, help='data')
parser.add_argument('nCores', metavar='c', type=int, help='number of cores for parallel computing')
parser.add_argument('out', metavar='o', type=str, help='File output')


args = parser.parse_args()

print("Reading file...")
matrix = np.matrix(pd.read_csv(args.data))
print("Done...")

print("Launching GENIE3...")
VIM = GENIE3(matrix,nthreads=args.nCores)
print("Done...")

print("Writing result...")
np.savetxt(fname=args.out,delimiter=',',X=VIM)
print("Done")