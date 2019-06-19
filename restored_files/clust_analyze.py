#coding: utf8

import argparse
import pandas as pd
from glob import glob
from itertools import chain

"""
Bothorel Benoît
June 2019
Compare clusters composition with one ref cluster
"""

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('ref', metavar='d', type=str, help='Clust of ref (list of genes)')
parser.add_argument('folder', metavar='f', type=str, help='folder containing the clusters to analyze')
parser.add_argument('--v',action='store_true', help='print the genes from the intersection with the best cluster',default=False)

args = parser.parse_args()

ref = []
with open(args.ref) as reference:
    lines = reference.readlines()
    for l in lines:
        val = l.strip().replace("'","")
        ref.append(val)

clust=''
maxi=0
bestmatch = {}
for file in glob(args.folder + '/*cluster*.csv'):
    df = pd.read_csv(file,header=None)
    cluster = (list(chain.from_iterable(df.values)))
    intersection = set(cluster).intersection(ref)
    identity = len(intersection)/float(len(ref))
    if(maxi < identity):
        maxi = identity
        maxi = maxi
        clust=file.split('_')[1]
        bestmatch = intersection  
    # print("{}".format(file.split('_')[1])+'\n'+str(identity*100)+'%')

print("The {} has the highest identity with the reference\n cluster with a score of {:.2f}%".format(clust,maxi*100))

if(args.v):
    print(bestmatch)