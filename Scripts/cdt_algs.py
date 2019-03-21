#!/usr/bin/env python

import glob, os
import cdt
import argparse
from tqdm import tqdm
import numpy as np
import pandas as pd
import networkx as nx
from cdt.utils.metrics import SHD
from sklearn.metrics import average_precision_score
from sklearn.utils import resample
from copy import deepcopy
from cdt.causality import graph

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('folder', metavar='f', type=str, help='data folder')
parser.add_argument('alg', metavar='a', type=str,
                    help="name of the algorithm", default=-1)
parser.add_argument('--nruns', metavar='j', type=int,
                    help="num of runs", default=16)
parser.add_argument('--njobs', metavar='j', type=int,
                    help="num of jobs", default=6)
parser.add_argument('--tsv', help="TSV file", action='store_true')
parser.add_argument('--nv', help="No verbose", action='store_false')
parser.add_argument('--log', metavar='l', type=str,
                    help='Specify a custom log folder', default=".")
parser.add_argument('--adjmatrix', help="Target is an adjacency matrix", action='store_true')
parser.add_argument('--header', help="header target", action='store_true')

args = parser.parse_args()
cdt.SETTINGS.NB_JOBS = args.njobs
cdt.SETTINGS.verbose = args.nv
if args.tsv:
    sep = "\t"
else:
    sep = ","

report = pd.DataFrame(columns=["File", "Model", "AUPR"] +
                      ["SHD 0." + str(i) for i in range(1,10)] +
                      ["DAG 0." + str(i) for i in range(1,10)])
nfiles = len([0 for _ in glob.glob(args.folder + "/*data*")])

pbar = tqdm(total=nfiles * args.nruns)

def score_function(prediction, target):
    prediction = np.nan_to_num(prediction)
    preds = []
    for threshold in np.arange(.1,1,.1):
        mat = deepcopy(prediction)
        mat[mat < threshold] = 0
        mat[mat > threshold] = 1
        preds.append(mat)
    return (average_precision_score(target.ravel(), prediction.ravel()),
            [SHD(m, target) for m in preds],
            [nx.is_directed_acyclic_graph(nx.DiGraph(m)) for m in preds])


def run_alg(model_c, data, **params):
    m = model_c(**params)
    global pbar
    pbar.update(1)
    return m.predict(data)


def bootstrap_alg(model_c, parameters, data, n=16, ratio=.8):
    return [run_alg(model_c, resample(data, n_samples=int(.8 * len(data))),
                    **parameters) for i in range(n)]


model = {"PC-G": graph.PC,
         "GES": graph.GES,
	    "GENIE3": graph.GENIE3
}

params = {"PC-G": {'CItest': 'gaussian',
                   'method_indep': 'corr',
                   'alpha': 0.01},
          "PC-RCIT": {'CItest': 'randomized',
                   'method_indep': 'rcit',
                   'alpha': 0.01},
          "PC-RCoT": {'CItest': 'randomized',
                   'method_indep': 'rcot',
                   'alpha': 0.01},
          "PC-H": {'CItest': 'hsic',
                    'method_indep': 'hsic_gamma',
                    'alpha': 0.01},
          "GES": {},  # Default params
          "GIES": {},
          "CAM": {'pruning': False},
          "LiNGAM": {},
          "MMPC": {"score": "mi-g-sh"},
          "CCDr":{},
	      "GENIE3":{}
          }



for _file in glob.glob(args.folder + "/*data*"):
    data = pd.read_csv(_file, sep=sep)
    target_file = _file.replace("data", "target")
    if "Time" in list(data.columns):
        del data["Time"]
    # print(args.data)
    if args.adjmatrix:
        if args.header:
            target = pd.read_csv(target_file, sep=sep).as_matrix()
        else:
            target = np.loadtxt(target_file, delimiter=sep)
    else:
        target = np.zeros((len(data.columns), len(data.columns)))
        lstcols = list(data.columns.values)
        tardata = pd.read_csv(target_file, sep=sep)
        for idx, row in tardata.iterrows():
            if len(row) < 3 or int(row[2]):
                target[lstcols.index(row[0]), lstcols.index(row[1])] = 1

    preds = bootstrap_alg(model[args.alg], params[args.alg], data, n=args.nruns)
    avg_pred = sum([np.array(nx.adjacency_matrix(i, nodelist=list(data.columns)).todense()) 
                    for i in preds])/args.nruns

    np.savetxt("{}_matrix.csv".format(_file.split("/")[-1]),avg_pred)

    aupr, shd, dag = score_function(avg_pred, target)
    config_dict = dict({"File": _file.split("/")[-1],
                                 "Model": args.alg,
                                 "AUPR": aupr},
                                **params[args.alg])
    shd_dict = {key:val for val,key in  zip(shd,
                                            ["SHD 0." + str(i) for i in range(1,10)])}
    dag_dict = {key:bool(val) for val,key in  zip(dag,
                                            ["DAG 0." + str(i) for i in range(1,10)])}
    config_dict.update(shd_dict)
    config_dict.update(dag_dict)
    report = report.append(config_dict, ignore_index=True)
    report.to_csv("Report-" + args.alg + "-" + args.folder.replace("/","_") + ".csv", index=False)
pbar.close()
