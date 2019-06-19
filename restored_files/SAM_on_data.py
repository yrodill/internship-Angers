import pandas as pd
from gsam.agsam import gSAM3d
import numpy as np
from joblib import Parallel, delayed
import argparse
import networkx as nx
from sklearn.metrics import average_precision_score
from itertools import product
from datetime import datetime
from cdt.utils.metrics import SHD
from copy import deepcopy

report = pd.DataFrame()


def job_function(data, gpu=0, **kwargs):

    model = gSAM3d(**kwargs)
    return(model.predict(data, nruns=args.nruns, njobs=args.njobs,
                               gpus=args.gpus, verbose=args.nv))


def score_function(prediction, target):
    preds = []
    prediction = np.nan_to_num(prediction)
    for threshold in np.arange(.1,1,.1):
        mat = deepcopy(prediction)
        mat[mat < threshold] = 0
        mat[mat > threshold] = 1
        preds.append(mat)
    # print(target, prediction)
    score = [average_precision_score(target.ravel(), prediction.ravel())] + \
            [SHD(m, target) for m in preds] + \
            [nx.is_directed_acyclic_graph(nx.DiGraph(m)) for m in preds]
    return score


def parameter_set(params, ex_rules=None, custom_ex_rules=None):
    full_set = [dict(zip(params, x)) for x in product(*params.values())]
    if ex_rules is not None:
        for param in full_set:
            for rule in ex_rules:
                if not param[rule]:
                    for excluded in ex_rules[rule]:
                      param.pop(excluded)
    if custom_ex_rules is not None:
        for param in full_set:
            for rule in custom_ex_rules:
                if param[rule] == custom_ex_rules[rule][0]:
                    for excluded in custom_ex_rules[rule][1]:
                        param.pop(excluded)

    # Exclude redudant param sets
    full_set = [dict(s) for s in set(frozenset(d.items()) for d in full_set)]
    # full_set = list(np.unique(np.array(full_set)))
    return full_set

def format_parameters(params, order):
    output=[]
    list_param = [[(k, l) for k,l in zip(i.keys(), i.values())] for i in params]
    for param in list_param:
        output.append([]) 
        local = [i[0] for i in param]
        for o in order:
            if not o in local:
                output[-1].append(None)
            else:
                output[-1].append(param[local.index(o)][1])
    return output

parameters={'lr':[0.01],
           'dlr':[0.01],
           'lambda1': [0.01],
           'lambda2':[0.00001],
           'nh':[200],
           'dnh': [200],
           'losstype':["fgan"],
           'sampletype':["sigmoidproba"],
           'train_epochs':[10000],
           'test_epochs':[1000],
           'dagstart':[0.5],
           'dagloss':[True],
           'dagpenalization':[0],
           'dagpenalization_increase':[0.001],
           'use_filter':[False],
           'filter_threshold':[0.5],
           'linear':[False]}

# When key is false, do not consider elements in list.
rules_exclusive = {'dagloss': ['dagpenalization', 'dagstart', 'dagpenalization_increase']}
# When key and value[0] match, exclude the elements in list given in tuple[1]
rules_exclusive_custom = {'losstype': ("mse", ['dnh', 'dlr','numberHiddenLayersD']),
                          "linear": (True, ['nh', 'lambda2'])}

score_legend = ["AUPR"] + ["SHD 0." + str(i) for i in range(1,10)] + ["DAG 0." + str(i) for i in range(1,10)]

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('data', metavar='d', type=str, help='data')
# parser.add_argument('--skeleton', metavar='t', type=str, help='skeleton')
parser.add_argument('--nruns', metavar='j', type=int,
                    help="num of runs", default=-1)
parser.add_argument('--gpus', help="Use gpu", type=int, default=0)
parser.add_argument('--njobs', metavar='j', type=int,
                    help="num of jobs", default=-1)
parser.add_argument('--tsv', help="TSV file", action='store_true')
parser.add_argument('--nv', help="No verbose", action='store_false')
parser.add_argument('--log', metavar='l', type=str,
                    help='Specify a custom log folder', default=".")
parser.add_argument('--adjmatrix', help="Target is an adjacency matrix", action='store_true')
parser.add_argument('--header', help="header target", action='store_true')
parser.add_argument('--parallel', help="Parallelize param sets.", action='store_true')
parser.add_argument('--v100', help="Set lambda1 for 100 vars100.", action='store_true')

args = parser.parse_args()


data = pd.read_csv(args.data, sep=',')


paramset = parameter_set(parameters, rules_exclusive, rules_exclusive_custom)

# Exec computations
paramset = [v for c in [[(paramset*args.nruns)[k*len(paramset) + i] for k in range(args.nruns)]
                              for i in range(len(paramset))] for v in c]
results = Parallel(n_jobs=args.njobs)(delayed(job_function)
                                          (data,
                                           gpu=idx % args.gpus if bool(args.gpus) else 0, **p)
                                          for idx, p in enumerate(paramset))

#print(results)
mat = results[0]
for i in range(1,len(results)):
    mat+=results[i]

mat = mat / len(results)

#print(mat)

with open('/home/bothorel/internship-Angers/catma5/data/link_list_SAM_on_genes_of_interest.csv',"w") as output:
    output.write("Gene1,Gene2,Score\n")
    for i in range(len(mat)):
        for j in range(len(mat)):
            output.write(str(data.columns.values[i])+","+str(data.columns.values[j])+","+str(mat[i][j])+"\n")


df = pd.read_csv('/home/bothorel/internship-Angers/catma5/data/link_list_SAM_on_genes_of_interest.csv',header=0)
#print(df)
df=df.sort_values(by="Score",ascending=False)
df.to_csv('/home/bothorel/internship-Angers/catma5/data/link_list_SAM_on_{}_of_interest.csv'.format(args.data.split('.')[0].split('_')[-1]),index=False,header=True)