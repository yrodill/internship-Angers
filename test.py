import pandas as pd
from matplotlib import pyplot as plt
from cdt.independence.stats.all_types import AdjMI
from networkx import Graph,draw,shell_layout

data = pd.read_csv('../../CausalGen/Syntren/data/results/nn100_nbgr100_hop0.3_bionoise0.1_expnoise0.1_corrnoise0.1_neighAdd_maxExpr1_dataset.txt', sep="\t",engine="python",index_col=0)

data = data.T

print (data)

graph = Graph()

adjMI = AdjMI()
graph = adjMI.predict_undirected_graph(data)

draw(graph,pos=shell_layout(graph),with_labels=True)
plt.show()

print("Creating plot...")

#Construct plot 8 by 8 (max for scatter plot)
count=1
for i,key in enumerate(data.columns):
    for j, key2 in enumerate(data.columns[i+1:]):
        plt.subplot(420+count)
        plt.scatter(data[key], data[key2])
        plt.xlabel(key)
        plt.ylabel(key2)
        count+=1
        if count > 8:
            count=1
            plt.show()


print("Done !")