import pandas as pd

data = pd.read_csv("biological_results/Ratio/biotic/list_link_biotic_10000000_0.05.csv")
print(len(data.index))

countGenes = {}

for i, row in data.iterrows():
    if(row["Gene1"] not in countGenes.keys()):
        countGenes[row["Gene1"]]=1
    else:
        countGenes[row["Gene1"]]+=1 

    if(row["Gene2"] not in countGenes.keys()):
        countGenes[row["Gene2"]]=1
    else:
        countGenes[row["Gene2"]]+=1 

print(len(countGenes.keys()))

genes = [gene for gene in countGenes if countGenes[gene]<2]
print(len(genes))

#Remove isolated genes
indexes=[]
for i, row in data.iterrows():
    if(row["Gene1"] in genes and row["Gene2"] in genes):
        indexes.append(i)

data=data.drop(data.index[indexes])
print(len(data.index))

data.to_csv("biological_results/Ratio/biotic/list_link_biotic_filtered_0.05.csv")