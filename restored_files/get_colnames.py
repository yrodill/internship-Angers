import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('data', metavar='f', type=str, help='data containing the colnames')
parser.add_argument('table', metavar='m', type=str, help='table')

args = parser.parse_args()

with open(args.data) as f:
    colnames=f.readline().strip().replace('"',"").split(',')

df=pd.read_csv(args.table,header=None)
df.columns=colnames
df.index=colnames

df.to_csv(args.table.split('.')[0] + "_with_genes_names.csv")