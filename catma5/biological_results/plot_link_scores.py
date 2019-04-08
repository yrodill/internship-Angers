import argparse
import pandas as pd
import glob
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('folder', metavar='d', type=str, help='Folder containing the data')
parser.add_argument('experience', metavar='d', type=str, help='Experience to process')

args = parser.parse_args()


with open("./{}/filtered_data_{}_genie3.csv".format(args.folder,args.experience)) as f:
    genesNames = f.readline().strip().split(',')

for file in glob.glob(args.folder + "/" + args.experience + "/*wmat*"):
    print("Reading file...")
    df = pd.read_csv(file)
    print("Done...")

x= []
y = []

print("Getting values...")
pbar = tqdm(total=len(genesNames))
for i, row in df.iterrows():
    pbar.update(1)
    for j, value in enumerate(row):
        if(i+j % 4 == 0):
            x.append(i+j)
            y.append(float(value))
pbar.close()
print("Done")

y = sorted(y,reverse=True)

print("Plotting...")
plt.scatter(x,y,norm=True)
print('Done...')
plt.show()