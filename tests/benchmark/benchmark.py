import glob
import pandas as pd
import sys
import os
import numpy as np
from itertools import product
from joblib import Parallel, delayed
import torch as th
import argparse
import datetime
import cdt
from cdt.utils.metrics import precision_recall
from gsam.gsam import gSAM
import networkx as nx


def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)


def exec_cgg_instance(data, gpuno, run=1, path=""):
    model = gSAM(lr=0.1, dlr=0.1, l1=0.1, nh=200, dnh=200,
                 train_epochs=args.train, test_epochs=args.test, batchsize=-1,
                 gumble_by_sample=False, temperature=False, KLpenalization=True, drawhard=True)

    return model.predict()


parser = argparse.ArgumentParser(description='Benchmark a method on graphs.')
parser.add_argument('datafolder', metavar='d', type=str, help='data')
parser.add_argument('--filext', metavar='m', type=str,
                    help="file regexp",
                    default='G20')
parser.add_argument('--dataext', metavar='m', type=str,
                    help="datafile regexp",
                    default='numdata')
parser.add_argument('--train', metavar='tr', type=int,
                    help="num of train epochs", default=1000)
parser.add_argument('--test', metavar='te', type=int,
                    help="num of test epochs", default=1000)
parser.add_argument('--nruns', metavar='n', type=int,
                    help="num of runs", default=1)
parser.add_argument('--njobs', metavar='j', type=int,
                    help="num of jobs", default=-1)
parser.add_argument('--gpu', help="Use gpu", action='store_true')
parser.add_argument('--plot', help="Plot losses", action='store_true')
parser.add_argument('--tsv', help="CSV file", action='store_true')
parser.add_argument('--adjmatrix', help="target is an adjacency matrix", action='store_true')
parser.add_argument('--nv', help="No verbose", action='store_false')
parser.add_argument('--log', metavar='l', type=str,
                    help='Specify a custom log folder', default=".")

args = parser.parse_args()

print(args)
if args.tsv:
    sep = "\t"
else:
    sep = ","

graph_names = []
graph_data = []
graph_target = []
os.chdir('./graph_datasets/' + args.datafolder)

for f in glob.glob('*{}*{}*'.format(args.filext, args.dataext)):
    print(f)
    graph_names.append(f.replace(args.dataext, ''))
    graph_data.append(pd.read_csv(f, sep=sep))
    graph_target.append(cdt.utils.read_list_edges(
        pd.read_csv(f.replace(args.dataext, 'target'), sep=sep)))
    if os.path.exists('{}-{}.done'.format(graph_names[-1], args.nruns)):
        graph_names.pop()
        graph_data.pop()
        graph_target.pop()

if args.skel:
    raise NotImplementedError('ToDo')

# '1500', '2000', 'res', 'res2', 'res3'
out_freq = ['res']  # '0', '500', '1000', '1500',
cdt.SETTINGS.GPU = True
# with torch cpu it is wiser to not parallel computation
# it parallelizes automatically

dataset = product(graph_data, range(1, args.nruns+1))

# Exec computations
# list_out = Parallel(n_jobs=cdt_private.SETTINGS.NB_JOBS)(
#     delayed(exec_cgg_instance)(data, idx % len(cdt_private.SETTINGS.GPU_LIST), run, "./graph_datasets/{}/{}".format(args.datafolder, graph_names[graph_data.index(data)]))
#     for idx, (data, run) in enumerate(dataset))
list_out = []
for idx, (data, run) in enumerate(dataset):
    list_out.append(exec_cgg_instance(data, idx % len(cdt.SETTINGS.GPU_LIST), run, graph_names[idx//args.nruns]))
# Regroup graphs execs w/ same graph
list_out = [list_out[i * args.nruns:(i + 1) * args.nruns]
            for i in range(int(len(list_out) / args.nruns))]
graphs_scores = []

for candidates, target, name, data in zip(list_out, graph_target, graph_names, graph_data):
    W = candidates[0]
    for w in candidates[1:]:
        W += w
    W /= args.nruns
    np.savetxt('{}/mat_CGG_{}.csv'.format(args.log, name),
               W, delimiter=",")
    g0 = nx.DiGraph(pd.DataFrame(W, columns=data.columns, index=data.columns))
    ll = g0.list_edges()
    pd.DataFrame(ll, columns=['Cause', 'Effect', 'Weight']).to_csv(
        '{}/adv_CGGraw-{}.csv'.format(args.log, name), index=False)
    graphs_scores.append(g0, target)
    # print(g)

report = pd.DataFrame()
# print(report, aupr_scores)
print(graphs_scores, len(graphs_scores))
report["Graph"] = graph_names
report["AUPR"] = graphs_scores
report.to_csv("{}/gSAM-report-{}-{}.csv".format(args.log, args.datafolder,
                                                datetime.datetime.now().isoformat()),
              index=False)

print(graphs_scores)
