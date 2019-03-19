from copy import deepcopy

"""
Benoît BOTHOREL
GO annotation genes clustering
19/03/2019
"""

dic={}
clusters=[]

with open("ATH_GO_GOSLIM.txt") as annots:
    lines = annots.readlines()

    for l in lines:
        values = l.strip().split("\t")
        if (values[0] not in dic.keys()):
            dic[values[0]] = []
        if (values[3] == "involved in"):
            dic[values[0]].append([values[4],values[5]])
            if(values[4] not in clusters):
                clusters.append(values[4])

print(len(clusters))

clusts={}
for clust in clusters:
    genes=[]
    for k in dic:
        for GO in dic[k]:
            if(GO[0] == clust and k not in genes):
                genes.append(k)
    
    clusts[clust]=genes

print("Len clust raw: ",len(clusts))

finalClust=[clusts[k] for k in clusts  if(len(clusts[k]) > 10 and len(clusts[k]) < 40) ]

print (finalClust)
print("Len clust filtered : ",len(finalClust))