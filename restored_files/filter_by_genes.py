import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('file', metavar='f', type=str, help='File')
parser.add_argument('genes', metavar='g', type=str, help='Genes of interest')


args = parser.parse_args()


data = pd.read_csv(args.file,header=0)
ref_gen = pd.read_csv(args.genes,header=None,names=["gene"])

genes=[]
for idx_i, row in ref_gen.iterrows():
    genes.append(row.values[0])

df = data.loc[:,data.columns.isin(genes)]
df.to_csv(args.file.split('.')[0]+"_by_{}.csv".format(args.genes.split('.')[0]),index=False)
print(df.shape)
