import cdt
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import networkx as nx
from cdt.independence.stats.numerical import MIRegression
import time

"""
Find the matrice of co-expression from biological data
"""

data = pd.read_csv("/home/bothorel/internship-Angers/catma5/catma5_ISampleNorm.txt",sep="\t")

data = data.fillna(0)

model = MIRegression()
print(time.ctime())
print("Prediction running...")
graph=model.predict_undirected_graph(data)
print(time.ctime())


nx.draw_networkx(graph, font_size=8)
plt.show()
