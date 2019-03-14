import os
import sys
import argparse
import csv
import numpy as np
from sklearn.metrics import average_precision_score
from sklearn.metrics import precision_recall_curve
import matplotlib.pyplot as plt
from sklearn.utils.fixes import signature

"""
Bothorel Benoît
March 2019
Launch the script with :
python test_GENIE3.py -nn [int] -nbrg [int] -hop [float] -bionoise [float] -expnoise [float] -corrnoise [float]        
"""

def CSVtoVector(path):
    """Returns the genes list of the network and the array containing weighted predictions made on the data with GENIE3
        Args:
            path (path to csv FILE): expression data file contained in the Syntren repositery.
        Returns:
            list : genes list
            list : weighted predictions flattened
    """

    with open(path) as f:
        lines=f.readlines()

    ignoreLine1 = False
    tmp=[]
    genes=0
    for l in lines:
        weight=l.strip().split(',')
        if(ignoreLine1):
            tmp.append(weight[1:])
        else:
            genes=weight[1:]
            ignoreLine1=True

    weightedPrediction=[]
    for liste in tmp:
        for weight in liste:
            if(weight == "NA"): #replace NA value with 0
                weight=0
            weightedPrediction.append(float(weight))

    return genes,weightedPrediction


def getAdjacencyMatrix(pathToKnownResults,pathToExperimentalResults,genesNames):
    """Compute the adjacency matrix by comparing each genes combinations with the results from the experimental and the known results.
        In the acutal state, it only calculates the adjacency matrix for undirected combinations
        Args:
            pathToKnownResults (path to sif FILE): file contained in the Syntren results repositery containing all the known interaction from the network.
            pathToExperimentalResults (path to txt FILE): file written from the R script using GENIE3 linkList() function.
            genesNames (list): list of the genes from the weighted matrix obtained from GENIE3.
        Returns:
            list: adjacency matrix flattened
    """
    with open(pathToKnownResults) as knownInteractions:
        lines=knownInteractions.readlines()

    truePos=[]
    for l in lines:
        word=l.strip().split()
        truePos.append(word[0]+" "+word[2])

    with open(pathToExperimentalResults) as f:
        lines=f.readlines()

    ignoreLine1 = False
    expPos=[]
    for l in lines:
        genes=l.strip().replace('"',"").split(",")
        if(ignoreLine1):
            expPos.append(genes[0]+" "+genes[1])
        else:
            ignoreLine1=True

    adjMatrix = []
    for gene1 in genesNames:
        for gene2 in genesNames:
            comb = gene1+" "+gene2
            comb=comb.replace('"',"")
            combInv = gene2+" "+gene1
            combInv=combInv.replace('"',"")
            if(comb in truePos and comb in expPos):
                adjMatrix.append(1)
            elif(combInv in truePos and combInv in expPos):
                adjMatrix.append(1)
            else:
                adjMatrix.append(0)

    return adjMatrix

def adjMatrixFromKnown(pathToKnownResults,genesNames):
    dic={}
    for i,gene in enumerate(genesNames):
        dic[gene.replace('"',"")] = i


    with open(pathToKnownResults) as knownInteractions:
        lines=knownInteractions.readlines()
    
    matrix=[]
    for i in range(len(genesNames)):
        matrix.append([])
        for j in range(len(genesNames)):
            matrix[i].append(0)

    for l in lines:
        word=l.strip().split()
        i=dic[word[0]]
        j=dic[word[2]]
        matrix[i][j]=1

    res = []
    for i in matrix:
        for j in i:
            res.append(j)
    return res


###MAIN###
if __name__=="__main__":
    # parser=argparse.ArgumentParser()
    # parser.add_argument('-nn',help="Number of nodes used in the network [int] : default 100")
    # parser.add_argument('-nbgr',help="Number of background nodes [int] : default 100")
    # parser.add_argument('-hop',help="Probability for complex 2-regulator interactions [0..1] : default 0.3")
    # parser.add_argument('-bionoise',help="Biological noise [0..1] : default 0.1")
    # parser.add_argument('-expnoise',help="Experimental noise [0..1] : default 0.1")
    # parser.add_argument('-corrnoise',help="Noise on correlated inputs [0..1] : default 0.1")
    # args=parser.parse_args()

    #if len(sys.argv)<6:
     #   print ("Wrong input args.\nUsage : -nn [int] -nbrg [int] -hop [float] -bionoise [float] -expnoise [float] -corrnoise [float]")               
    #else:
        #RUN the R script on the data obtained from Syntren
        #os.system("Rscript R/test_GENIE3.R")

    genes,weightedPrediction = CSVtoVector("results/weightMat.csv")
    #adjMat = getAdjacencyMatrix("/home/bothorel/CausalGen/Syntren/data/results/nn{}_nbgr{}_hop{}_bionoise{}_expnoise{}_corrnoise{}_neighAdd_network.sif".format(str(args.nn),str(args.nbgr),str(args.hop),str(args.bionoise),str(args.expnoise),str(args.corrnoise)),"results/linkList.txt",genes)
    #adjMat = getAdjacencyMatrix("Syntren/nn20_nbgr0_hop0.1_bionoise0.3_expnoise0.1_corrnoise0.1_neighAdd_network.sif","results/linkList.txt",genes)
    #print(adjMat)
    adjMat = adjMatrixFromKnown("Syntren/nn20_nbgr0_hop0.1_bionoise0.3_expnoise0.1_corrnoise0.1_neighAdd_network.sif",genes)
    average_precision = average_precision_score(adjMat,weightedPrediction)

    precision, recall, _ = precision_recall_curve(adjMat, weightedPrediction)


    # In matplotlib < 1.5, plt.fill_between does not have a 'step' argument
    step_kwargs = ({'step': 'post'}
                if 'step' in signature(plt.fill_between).parameters
                else {})
    plt.step(recall, precision, color='b', alpha=0.2,
            where='post')
    plt.fill_between(recall, precision, alpha=0.2, color='b', **step_kwargs)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.title('2-class Precision-Recall curve: AP={0:0.2f}'.format(
            average_precision))
    plt.show()

