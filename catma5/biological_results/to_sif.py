import argparse
import pandas as pd
import glob
from tqdm import tqdm
import csv

"""Written by Benoît Bothorel 
 -> benbotho@gmail.com for any questions
 03/04/2019
"""


parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('folder', metavar='d', type=str, help='Folder containing the data')

args = parser.parse_args()

for file in glob.glob(args.folder + "/*list_link*"):
    df = pd.read_csv(file)
    with open("{}/links.sif".format(args.folder.split("/")[-1]),"w") as output:
        for i in range(len(df.index)):
            gene1=df.at[i, 'Gene1'].replace('"',"")
            gene2=df.at[i, 'Gene2'].replace('"',"")
            output.write(gene1+'\tcauses\t'+gene2)
            output.write("\n")
