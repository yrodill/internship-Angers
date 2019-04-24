import hdbscan
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn.cluster as cluster
import time

def plot_clusters(data, algorithm, args, kwds):
    start_time = time.time()
    labels = algorithm(*args, **kwds).fit_predict(data)
    end_time = time.time()
    palette = sns.color_palette('deep', np.unique(labels).max() + 1)
    colors = [palette[x] if x >= 0 else (0.0, 0.0, 0.0) for x in labels]
    plt.scatter(data.T[0], data.T[1], c=colors, **plot_kwds)
    frame = plt.gca()
    frame.axes.get_xaxis().set_visible(False)
    frame.axes.get_yaxis().set_visible(False)
    plt.title('Clusters found by {}'.format(str(algorithm.__name__)), fontsize=24)
    plt.text(-0.5, 0.7, 'Clustering took {:.2f} s'.format(end_time - start_time), fontsize=14)
    plt.show()

sns.set_context('poster')
sns.set_color_codes()
plot_kwds = {'alpha' : 0.25, 's' : 80, 'linewidths':0}

print("Loading data...")
data = pd.read_csv("biological_results/Ratio/all/wmat_all.csv",header=None)
#data = pd.read_csv("data/Ratio_filtered_by_exp_by_genes.csv",header=0)
print("Done...")

print(data)

# clusterer = hdbscan.HDBSCAN(min_cluster_size=10,metric='precomputed')
# print("DBSCAN running...")
# tree = clusterer.fit(data)
# print("Done...")
# print(tree)
# for clust in clusterer.labels_ :
#     print(clust)

plot_clusters(data, hdbscan.HDBSCAN, (), {'min_cluster_size':10,'metric':'precomputed'})