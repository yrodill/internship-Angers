#coding: utf8

import os
import pandas as pd
import argparse
from joblib import Parallel, delayed
from tqdm import tqdm

"""
Bothorel Benoît
04/06/2019 
Preprocessing of the data for the EGAD analysis

EVIDENCE CODES:
    Experimental:
        EXP Inferred from Experiment
        IDA Inferred from Direct Assay
        IPI Inferred from Physical Interaction
        IMP Inferred from Mutant Phenotype
        IGI Inferred from Genetic Interaction
        IEP Inferred from Expression Pattern
    Similarity:
        ISS Inferred from Sequence or structural Similarity
        ISO Inferred from Sequence Orthology
        ISA Inferred from Sequence Alignment
        ISM Inferred from Sequence Model used in manual assertion
        IGC Inferred from Genomic Context
        IBA Inferred from Biological aspect of Ancestor
        IBD Inferred from Biological aspect of Descendant
        IKR Inferred from phylogenetic determination of loss of key residues (manual assertion)
        IRD Inferred from Rapid Divergence from ancestral sequence (manual assertion)
        IMR Phylogenetic determination of loss of key residues in manual assertion
    Combinatorial:
        RCA Inferred from Reviewed Computational Analysis
    High_Throughput:
        HTP Inferred from High Throughput Experimental
        HDA Inferred from High Throughput Direct Assay
        HMP Inferred from High Throughput Mutant Phenotype
        HGI Inferred from High Throughput Genetic Interaction
        HEP Inferred from High Throughput Expression Pattern
    Author:
        TAS Traceable Author Statement used in manual assertion
        NAS Non-traceable Author Statement used in manual assertion
    Curatorial:
         IC Inferred by Curator
    No biological data:
         ND No biological Data available
    Automatic:
        IEA Inferred from Electronic Annotation
"""

def get_adjacency_matrix(df,df2):
    for i in tqdm(range(len(df.index))):
        df2.at[df.at[i,'gene1'],df.at[i,'gene2']] = 1
        df2.at[df.at[i,'gene2'],df.at[i,'gene1']] = 1
    if(df2.equals(df2.transpose())):
        print("SYMETRIC MATRIX!")
    return df2

def test_process(args,df,i):
    if(args.specific):
        index = 3
    else:
        index = 7
    if(df.iat[i,index] == args.process or args.process == 'all'):
        return True
    else:
        return False

def get_allowed_evidence_codes(args):
	if(args.ev_inc != 'all'):
		ev_inc = []
		for ev in args.ev_inc:
			if(ev == "Experimental"):
				ev_inc.extend(("EXP","IDA","IPI","IMP","IGI","IEP"))
			elif(ev == "Similarity"):
				ev_inc.extend(("ISS","ISO","ISA","ISM","IGC","IBA","IBD","IKR","IRD","IMR"))
			elif(ev == "Combinatorial"):
				ev_inc.append("RCA")
			elif(ev == "High_Throughput"):
				ev_inc.extend(("HTP","HDA","HMP","HGI","HEP"))
			elif(ev == "Author"):
				ev_inc.extend(("TAS","NAS"))
			elif(ev == "Curatorial"):
				ev_inc.append("IC")
			elif(ev == "No_biological_data"):
				ev_inc.append("ND")
			elif(ev == "Automatic"):
				ev_inc.append("IEA")
			else:
				ev_inc.append(ev)
		return ev_inc
	else:
		return ["EXP","IDA","IPI","IMP","IGI","IEP","ISS","ISO","ISA","ISM","IGC","IBA","IBD","IKR","IRD","IMR","RCA",
				"HTP","HDA","HMP","HGI","HEP","TAS","NAS","IC","ND","IEA"]

def test_evidence_codes(ev_inc,df,i):
    if(args.specific):
        index = 4
    else:
        index = 9
    if(df.iat[i,index] not in ev_inc):
        return False
    else:
        return True


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('data', metavar='f', type=str, help='file containing the links of the network')
parser.add_argument('GO', metavar='g', type=str, help='file containing the GO file')
parser.add_argument('--process', metavar='p', default='all', help='filter by type of process(P = biological process, C = cellular component,F= molecular function')
parser.add_argument('--ev_inc', metavar='e',nargs='*',type=str, default='all', help='evidence codes to use can be by group name/group names/evidence codes')
# parser.add_argument('--min', metavar='m',type=int, default=3, help='min value to filter under-represented GO Terms')
# parser.add_argument('--max', metavar='x',type=int, default=200, help='max value to filter over-represented GO Terms')
parser.add_argument('--specific', action='store_true', help='If you are using a specific GO file (one given by parse_GO.py)',default=False)

args = parser.parse_args()


if(args.process == "BP"):
	args.process = "P"
elif(args.process == "MF"):
	args.process == "F"
elif(args.process == "CC"):
	args.process = "C"
else:
	args.process == 'all'

allowed_evidence_codes = get_allowed_evidence_codes(args)

"""
Part 1
Building the adjacency matrix of the network
"""

print('Reading file...')
df = pd.read_csv(args.data,header=0)
print("Done...")

genes = []
for i in df['gene1'].values:
    if(i not in genes):
        genes.append(i)
for i in df['gene2'].values:
    if(i not in genes):
        genes.append(i)

adj_matrix = pd.DataFrame(0,columns=genes,index=genes)

adj_matrix = get_adjacency_matrix(df,adj_matrix)

adj_matrix.to_csv('tmp_adj_matrix.csv')

"""
Part 2
Functionnal annotations
Links between Genes and GO Terms
"""
df = pd.read_csv(args.GO,sep='\t',header=None)
if(args.specific):
    index=1
else:
    index=5     

association = {}
for i in tqdm(range(len(df.index))):
    if(df.iat[i,0] in genes and test_process(args,df,i) and test_evidence_codes(allowed_evidence_codes,df,i)):
        if(df.at[i,0] not in association.keys()):
            association[df.iat[i,0]]=[df.iat[i,index]]
        else:
            association[df.iat[i,0]].append(df.iat[i,index])

GOTerms = []
for k,v in association.items():
    for go in v:
        if(go not in GOTerms):
            GOTerms.append(go)

functionnal_annotations = pd.DataFrame(0,columns=GOTerms,index=genes)

for k,v in association.items():
    for go in v:
        functionnal_annotations.at[k,go] = 1


functionnal_annotations.to_csv('tmp_GO_matrix.csv')