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


def job_function(data, target, gpu=0, **kwargs):

    model = gSAM3d(**kwargs)
    filename = args.log + "/agsam_t_res_" + "_".join(["{}-{}".format(k[:4], l) for k, l
                                          in zip(kwargs.keys(), kwargs.values())])
    if not args.parallel:
        result = model.predict(data, nruns=args.nruns, njobs=args.njobs,
                               gpus=args.gpus, verbose=args.nv)
    else:
        result = model.exec_sam_instance(data, gpus=args.gpus, verbose=args.nv,
                                         gpuno=gpu)


    scores = {leg:sc for leg,sc in zip(score_legend, score_function(result, target))}
    global report
    name_graph = str(parameters["losstype"][0]) + "_" + str(parameters["linear"][0]) + "_" + args.data.split("/")[7]
    np.savetxt(name_graph, result, delimiter=',')
    report = report.append(dict(kwargs, **scores), ignore_index=True)
    report.to_csv(args.log + "/agsam-treport-" + name_graph, index=False)
    return result


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
           'losstype':["mse"],
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
rules_exclusive_custom = {'losstype': ("mse", ['dnh', 'dlr']),
                          "linear": (True, ['nh', 'lambda2'])}

score_legend = ["AUPR"] + ["SHD 0." + str(i) for i in range(1,10)] + ["DAG 0." + str(i) for i in range(1,10)]

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('data', metavar='d', type=str, help='data')
parser.add_argument('target', metavar='t', type=str, help='target')
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


if args.tsv:
    sep = "\t"
else:
    sep = ","
data = pd.read_csv(args.data, sep=sep)
if "Time" in list(data.columns):
    del data["Time"]
# print(args.data)
if args.adjmatrix:
    if args.header:
        target = pd.read_csv(args.target, sep=sep).as_matrix()
    else:
        target = np.loadtxt(args.target, delimiter=sep)
else:
    target = np.zeros((len(data.columns), len(data.columns)))
    lstcols = list(data.columns.values)
    tardata = pd.read_csv(args.target, sep=sep)
    for idx, row in tardata.iterrows():
        if len(row) < 3 or int(row[2]):
            target[lstcols.index(row[0]), lstcols.index(row[1])] = 1

# print(target.shape)

# if args.skeleton is not None:
#     skeleton = np.zeros((len(data.columns), len(data.columns)))
#     for idx, row in pd.read_csv(args.skeleton, sep=sep).iterrows():
#         skeleton[int(row[0][1:]), int(row[1][1:])] = 1
#         skeleton[int(row[1][1:]), int(row[0][1:])] = 1
# else:
#     skeleton = None

paramset = parameter_set(parameters, rules_exclusive, rules_exclusive_custom)

# Exec computations
if not args.parallel:
    results = []
    for p in paramset:
        results.append(job_function(data, target, **p))
else:
    paramset = [v for c in [[(paramset*args.nruns)[k*len(paramset) + i] for k in range(args.nruns)]
                              for i in range(len(paramset))] for v in c]
    results = Parallel(n_jobs=args.njobs)(delayed(job_function)
                                          (data, target,
                                           gpu=idx % args.gpus if bool(args.gpus) else 0, **p)
                                          for idx, p in enumerate(paramset))

# Compute scores:
scores = [score_function(pred, target) for pred in results]
# Create report
order = list(parameters.keys())
freport = pd.DataFrame(format_parameters(paramset, order), columns=order)
for idx, legend in enumerate(score_legend):
    # print(legend)
    freport[legend] = [score[idx] for score in scores]
print(scores)
name_graph = args.data.split("/")[1]
freport.to_csv(args.log + "/agsam3d-freport_" + str(name_graph) + "_" + str(datetime.now().isoformat()) + ".csv", index=False)
