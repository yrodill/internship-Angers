import cdt
from cdt.causality.pairwise import Jarfo
from cdt import SETTINGS
SETTINGS.verbose=False
SETTINGS.NB_JOBS=4
import time
import networkx as nx
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

jarf=Jarfo()

start_time = time.time()
data_train = pd.read_csv('/home/bothorel/internship-Angers/catma5/catma5_IRefNorm.txt')
data = pd.read_csv("/home/bothorel/internship-Angers/catma5/catma5_ISampleNorm.txt")
jarf.fit(data_train,data)
ugraph = jarf.predict_dataset(data)
print("--- Execution time : %4.4s seconds ---" % (time.time() - start_time))

nx.draw_networkx(ugraph, font_size=8)
plt.show()

