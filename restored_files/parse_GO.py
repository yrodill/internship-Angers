import argparse
import pandas as pd

"""
Bothorel Benoît
19/06/2019
Parser for GO file :
Get the GO_GOSlim file parsed into GOSlim only or even
chose a specific subject (like biotic, others must be implemented)
"""

def write_GO(df,file,terms):
    for i in range(len(df.index)):
        if(df.iat[i,8] in terms.keys()):
            file.write(str(df.iat[i,0]+'\t'+str(terms[df.iat[i,8]])+'\t'+str(df.iat[i,8]+'\t'+str(df.iat[i,7])+'\t'+str(df.iat[i,9])+'\n')))

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('GO', metavar='f', type=str, help='Ref GO file')
parser.add_argument('slim', metavar='p', type=str, help='GO slim terms from TAIR')
parser.add_argument('--biotic', action='store_true',default=False, help='Only use terms linked to biotic interaction')

args = parser.parse_args()

GO = pd.read_csv(args.GO,sep='\t',header=None)
slim = pd.read_csv(args.slim,sep='\t',header=None)

"""
Part 1 :
Get all GO slim terms in a list
"""
if(args.biotic):
    terms = {
        'response to stress':'GO:0006950',
        'response to biotic stimulus':'GO:0009607',
        'response to external stimulus':'GO:0009605'
    }
else:
    terms = { slim.iat[i,1]:slim.iat[i,2] for i in range(len(slim.index)) }

"""
Part 2 :
Filter GO with those terms
"""
if(args.biotic):
    with open('GO_slim_biotic.csv','w') as f:
        write_GO(GO,f,terms)
else:
    with open('GO_slim.csv','w') as f:
        write_GO(GO,f,terms)
