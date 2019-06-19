# coding: utf8

import pandas as pd
import argparse
import goatools
from copy import deepcopy
from tqdm import tqdm
import sys

"""
Bothorel Benoît
May 2019
Formating files for the enrichment analysis
with GOATOOLS https://github.com/tanghaibao/goatools/
Before using this script, create two folders called "study" & "cluster_links"
in which clusters will be stored for further analysis
"""            

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('original', metavar='d', type=str, help='file containing the genes links')
parser.add_argument('data', metavar='d', type=str, help='file containing the genes with their cluster attribute (obtained through clustering.R)')
parser.add_argument('GO', metavar='g', type=str, help='file from TAIR database for the GO association')
parser.add_argument('--threshold', metavar='t', type=int, help='threshold for the cluster`s size',default=100)

args = parser.parse_args()

"""
Part 1 :
Parsing the GO file
"""

df = pd.read_csv(args.GO,sep='\t',header=None)
genes = {}

for i in range(len(df.index)):
    if(df.at[i,0] not in genes):
        genes[df.at[i,0]] = [df.at[i,5]]
    else:
        genes[df.at[i,0]].append(df.at[i,5])

with open('tmp_{}'.format(args.GO.split('/')[-1]),'w') as f:
    for k,v in genes.items():
        string = str(k)+"\t"
        for i in range(len(v)):
            if(i != len(v)-1):
                string+=str(v[i])+';'
            else:
                string+=str(v[i])+'\n'
        f.write(string)

"""
Part 2 :
Population file
File obtained with R script but without the 2nd column
"""
df = pd.read_csv(args.data,sep=',',skiprows=1,header=None)
with open('population_{}'.format(args.data),'w') as f:
    for i in range(len(df.index)):
        f.write(str(df.at[i,0])+'\n')

"""
Part 3 :
Study files
Here we need to write all the clusters genes into different files
"""

df = pd.read_csv(args.data,sep=',',skiprows=1,header=None)
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

if(len(filtered_clusters) == 0):
    raise ValueError("\nThere is no clusters.\nEither your threshold is too high, either your file\ndoesn't contain enough links between genes\n")

for i in range(len(filtered_clusters)):
    with open('study/study_cluster{}_{}'.format(str(i),args.data),'w') as f:
        print("Writing file n°{}".format(str(i)))
        for gene in filtered_clusters[i]:
            f.write(str(gene)+'\n')

"""
Part 4 :
For each cluster create a file that will contain
the genes links according to the original file
"""

df = pd.read_csv(args.original,header=0)

for i in tqdm(range(len(filtered_clusters))):
    couples = []
    with open('cluster_links/cluster_{}_{}'.format(str(i),args.data),'w') as f:
        f.write('gene1,gene2\n')
        for gene in filtered_clusters[i]:
            for j in range(len(df.index)):
                if([gene,df.at[j,'gene2']] in couples):
                    continue
                elif(df.at[j,'gene1'] == gene and df.at[j,'gene2'] in filtered_clusters[i]):
                    couples.append([gene,df.at[j,'gene2']])
                    f.write(str(gene)+","+str(df.at[j,'gene2']+'\n'))
                
