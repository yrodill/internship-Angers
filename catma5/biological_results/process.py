import argparse
import pandas as pd
import glob
from tqdm import tqdm

"""Written by Benoît Bothorel 
 -> benbotho@gmail.com for any questions
 03/04/2019
"""



parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('folder', metavar='d', type=str, help='Folder containing the data')
parser.add_argument('experience', metavar='d', type=str, help='Experience to process')
parser.add_argument('--nLinks', metavar='l',type=int, default=10000, help='Maximum number of links to show (default 10 000)')
parser.add_argument('--threshold', metavar='l',type=float, default=0.05, help='Threshold percentage of max value (default = 0.05)')

args = parser.parse_args()


with open("./{}/filtered_data_{}_genie3.csv".format(args.folder,args.experience)) as f:
    genesNames = f.readline().strip().split(',')

for file in glob.glob(args.folder + "/" + args.experience + "/*wmat*"):
    print("Reading file...")
    df = pd.read_csv(file)
    print("Done...")


print("Finding max...")
maxi=0
pbar = tqdm(total=len(genesNames))
for i, row in df.iterrows():
    pbar.update(1)
    for j, value in enumerate(row):
        if float(value) > maxi:
            maxi = float(value)

pbar.close()
print("Done...")
print("Max : ",maxi)

gene1 = []
gene2 = []
score = []

threshold = maxi * args.threshold

print("Getting links...")
pbar = tqdm(total=len(genesNames))
for i, row in df.iterrows():
    pbar.update(1)
    for j, value in enumerate(row):
        if(float(value) >= threshold and i != j):
            gene1.append(genesNames[i].replace('"',''))
            gene2.append(genesNames[j].replace('"',''))
            score.append(float(value))
pbar.close()
print("Done")

print("Making the dataframe")
links = pd.DataFrame({
    'Gene1' : gene1,
    'Gene2' : gene2,
    'Score' : score
})
print("Done...")

print("Ordering the values...")
links = links.sort_values(by='Score',ascending=False)
print("Done...")
if args.nLinks < len(links.index):
    links = links.iloc[0:args.nLinks]
else:
    print("The link list has less values than your selected max number of links, select lesser threshold value to increase the number of results")

print("Writing the result...")
links.to_csv("{}/{}/list_link_{}_{}_{}.csv".format(args.folder,args.experience,args.experience,args.nLinks,args.threshold),index=False)
print("Done...")

