from copy import deepcopy

"""
Benoît BOTHOREL
GO annotation genes clustering
19/03/2019

Ref::
Liesecke, Franziska, et al. 
"Ranking genome-wide correlation measurements improves microarray and
 RNA-seq based global and targeted co-expression networks."
 Sci. Rep., vol. 8, no. 1, 18 July 2018, p. 10885, 
 doi:10.1038/s41598-018-29077-3.
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


finalClust=[clusts[k] for k in clusts  if(len(clusts[k]) > 5 and len(clusts[k]) < 100) ]

print (finalClust)
print("Len clust raw: ",len(clusts))
print("Len clust filtered : ",len(finalClust))