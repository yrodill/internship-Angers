import argparse
import pandas as pd
import json
from copy import deepcopy
from tqdm import tqdm
import sys
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities
from scipy.stats import hypergeom 

"""
Bothorel Benoît
22/05/2019
Script for the GO terms analysis and comparison
(deprecated : use launch_GO_analyze.sh)
"""

def byValue(array):
    return array[1]

def GO_freq(ref,clust):
    freq = {}
    for gene in clust:
        if(gene in ref.keys()):
            for go in ref[gene]['GONums']:
                if(go not in freq.keys()):
                    freq[go] = 1
                else:
                    freq[go] +=1
    return(freq)

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('data', metavar='m', type=str, help='file containing the genes with their cluster attribute (obtained through clustering.R)')
parser.add_argument('--GO', metavar='f', type=str, help='file containing the GO terms')
parser.add_argument('--njobs', metavar='j', type=int, help='number of jobs for parralel computation',default=1)
parser.add_argument('--threshold', type=int, help='minimum size of the clusters to be used for the comparison',default=3)
parser.add_argument('--csv', help='use it if GO file is a comma-delimited file',action='store_true',default=False)
parser.add_argument('--skip', help='allow to skip the parsing part if you already have a json file containing all the genes annotations',action='store_true',default=False)
parser.add_argument('--json', help='json file containing all the annotations for each genes',type=str)

args = parser.parse_args()

if(args.csv):
    sep=','
else:
    sep='\t'

"""
Part 1 : GO parsing
"""
if(args.skip):
    if(args.json is None):
        print("ERROR !!! You must provide a JSON file when you're using the skip option")
        sys.exit(1)
    else:
        with open(args.json) as f:
            ref = json.load(f)
else:
    pairs = []

    with open(args.GO) as annots:
        lines = annots.readlines()

    print("Normalizing TAIR GO...")
    with open("{}_normalized.csv".format(args.GO.split('/')[-1].split('.')[0]),"w")as output:
        for l in lines:
            values = l.strip().split("\t")
            if(values[7] == "P"):
                #avoid same pairs
                if([values[0],values[5]] not in pairs):
                    pairs.append([values[0],values[5]])
                    output.write("{}\t{}\t{}\n".format(values[13],values[0],values[5]))
    print("Done...")

    dic={}
    listGenes=[]
    clusters=[]

    #parsing GOSLIM annotations to build reference files
    with open(args.GO) as annots:
        lines = annots.readlines()

        for l in lines:
            values = l.strip().split("\t")
            if (values[0] not in listGenes):
                listGenes.append(values[0])
            if (values[0] not in dic.keys()):
                dic[values[0]] = []
            if (values[7] == "P"):
                dic[values[0]].append([values[4],values[5]])
                if(values[4] not in clusters):
                    clusters.append(values[4])


    clusts={}
    for clust in clusters:
        genes=[]
        for k in dic:
            for GO in dic[k]:
                if(GO[0] == clust and k not in genes):
                    genes.append(k)
        
        clusts[clust]=genes

    finalClust={}
    for GO in clusters:
        finalClust[GO]={
            "cluster":clusts[k] for k in clusts if(len(clusts[k]) > 5 and len(clusts[k]) < 100)
            }

    #write json files from data
    file={}
    for gene in listGenes:
        file[gene]={
            "GOTerms":[GO[0] for GO in dic[gene]],
            "GONums":[GO[1] for GO in dic[gene]]
        }

    #Remove duplicates
    for gene in listGenes:
        for term in file[gene]:
            uniq = []
            for go in file[gene][term]:
                if go not in uniq:
                    uniq.append(go)
            file[gene][term]=uniq


    ref=file

"""
Part 2 : Load clusters from file
"""
df = pd.read_csv(args.data,header=None,index_col=None,skiprows=1)
df.columns=['gene','value']
df.sort_values(by='value',inplace=True)
df = df.reset_index(drop=True)

clusters = []
index=0
for i in range(1,max(df['value'])):
    genes = []
    for j in range(index,len(df.index)):
        if(df.at[j,'value'] == i):
            genes.append(df.at[j,"gene"])
        else:
            index=j
            clusters.append(genes)
            break

filtered_clusters = deepcopy(clusters)
#remove clusters with length < threshold
j=0
for i,clust in enumerate(clusters):
    if(len(clust) < args.threshold):
        filtered_clusters.pop(i-j)
        j+=1

"""
Part 3 : Find overrepresented GO term for each cluster
"""
#Calcul of the frequency for each GO terms in the 
GOfreq = {}
GOSlim = pd.read_csv("../../GOSlim/ATH_GO_normalized.csv",sep='\t',header=None)
GOSlim.columns = ["DB","Gene","GO"]

for i in range(len(GOSlim.index)):
    if(GOSlim.at[i,'GO'] not in GOfreq.keys()):
        GOfreq[GOSlim.at[i,"GO"]] = 1
    else:
        GOfreq[GOSlim.at[i,"GO"]] +=1

total = len(GOSlim.index)
GOfreq = {k: v / total for k, v in GOfreq.items()}

#Calcul of the frequency in each cluster
results = []
for clust in filtered_clusters:
    results.append(GO_freq(ref,clust))

print(results)
