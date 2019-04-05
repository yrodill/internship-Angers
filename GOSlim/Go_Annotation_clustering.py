from copy import deepcopy
import json

"""
Benoît BOTHOREL
GO annotation genes clustering
19/03/2019
"""

dic={}
listGenes=[]
clusters=[]

#parsing GOSLIM annotations to build reference files
with open("ATH_GO_GOSLIM.txt") as annots:
    lines = annots.readlines()

    for l in lines:
        values = l.strip().split("\t")
        if (values[0] not in listGenes):
            listGenes.append(values[0])
        if (values[0] not in dic.keys()):
            dic[values[0]] = []
        if (values[3] == "involved in"):
            dic[values[0]].append([values[4],values[5]])
            if(values[4] not in clusters):
                clusters.append(values[4])


clusts={}
for clust in clusters:
    genes=[]
    for k in dic:
        for GO in dic[k]:
            if(GO[0] == clust and k not in genes):
                genes.append(k)
    
    clusts[clust]=genes

print(clusts)

finalClust={}
for GO in clusters:
    finalClust[GO]={
        "cluster":clusts[k] for k in clusts if(len(clusts[k]) > 5 and len(clusts[k]) < 100)
        }

#print all go annotation and his related genes
# for GO in finalClust:
#     print("{} => {}".format(GO,finalClust[GO]["cluster"]))

#write json files from data
file={}
for gene in listGenes:
    file[gene]={
        "GOTerms":[GO[0] for GO in dic[gene]],
        "GONums":[GO[1] for GO in dic[gene]]
    }

#Remove duplicates
for gene in listGenes:
    for term in file[gene]:
        uniq = []
        for go in file[gene][term]:
            if go not in uniq:
                uniq.append(go)
        file[gene][term]=uniq


with open("genes_list.json","w") as output:
    json.dump(file,output)

with open("clusters.json","w") as outfile:
    json.dump(finalClust,outfile)

print("Len clust raw: ",len(clusts))
print("Len clust filtered : ",len(finalClust))