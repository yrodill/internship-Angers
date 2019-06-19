import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('file', metavar='f', type=str, help='File')

args = parser.parse_args()


genes = []
with open(args.file) as f:
    lines = f.readlines()
    for l in lines:
        if(l.replace('"',"").split(',')[12] == "true"):
            genes.append(l.strip().replace('"',"").split(',')[13])

df = pd.DataFrame(genes)
df.to_csv("list_"+args.file,header=None,index=None)
