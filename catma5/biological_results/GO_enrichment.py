import glob
import argparse
import os
import pandas as pd
import networkx as nx
from networkx import Graph,spring_layout
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('folder', metavar='f', type=str, help='data folder')
parser.add_argument('nLinks', metavar='f', type=str, help='number of links')


args = parser.parse_args()

dir_path=os.path.dirname(os.path.realpath(__file__))

graph = Graph()

for file in glob.glob(dir_path + "/" + args.folder + "/*list_link_*" + args.nLinks + "_*"):
    df = pd.read_csv(file,sep=',')
    for idx_i, row in df.iterrows():
        graph.add_edge(row["Gene1"], row["Gene2"], weight=row["Score"])


options={
    'node_color':'black',
    'node_size':10,
    'width':1,
    'font_size':8,
    'font_color':'red'
}
pos=nx.spring_layout(graph)
nx.draw_networkx(graph,pos=pos, **options)
plt.show()
