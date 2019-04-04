import argparse
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('folder', metavar='d', type=str, help='folder')
parser.add_argument('file', metavar='d', type=str, help='File')


args = parser.parse_args()

g1=[]
g2=[]
score=[]
names=[]

firstLine = True
with open(args.folder+args.file) as f:
    lines = f.readlines()
    for l in lines:
        if firstLine:
            firstLine=False
        else:
            g1.append(l.split(",")[0])
            g2.append(l.split(",")[1])
            score.append(l.split(',')[2])
            names.append(l.split(",")[0]+" (interacts with) "+l.split(",")[1])
        
df = pd.DataFrame(
    {
        "name":names,
        "Gene1":g1,
        "Gene2":g2,
        "Score":score
    }
)

df.to_csv(args.folder+"/table.csv") 