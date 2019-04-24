import pandas as pd
from joblib import Parallel, delayed
import argparse
from cdt.independence.stats.numerical import MIRegression
from cdt.independence.stats.numerical import PearsonCorrelation
from tqdm import tqdm
import time
import sys


parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('data', metavar='f', type=str, help='data')
parser.add_argument('model', metavar='m', type=str, help='correlation to be used')
#parser.add_argument('njobs', metavar='j', type=int, help='nb jobs')


args = parser.parse_args()

print('Reading file...')
data = pd.read_csv(args.data, sep=',',header=None,skiprows=1)
# print(data)
print("Done...")

def job_function(data,args,l):
    result=[]
    if(args.model == "MI"):
        model = MIRegression()
    else:
        model = PearsonCorrelation()

    for idx_i, i in enumerate(data.columns):
            for idx_j, j in enumerate(data.columns[idx_i+1:]):
                result.append([i,j,model.predict(data[i].values, data[j].values)])
    return result
  


# Exec computations
print("Launch parallelization...")
results = Parallel(n_jobs=2)(delayed(job_function)(data,args,l) for l in range(len(data.columns)**2))
print("Done..")
# print(results)
print(len(results))

# final=[]
# for i in range(len(data.columns)**2):
#     final.append(results[i][2])

report = pd.DataFrame(results)
report.to_csv("data/test_parallel3.csv",index=False,header=False)
# # Compute scores:
# scores = []
# for pred in results:
#   scores.append(score_function(pred, target))
  
# # Create report
# order = list(parameters.keys())
# report = pd.DataFrame(format_parameters(paramset, order), columns=order)
# report['Score'] = scores
# print(scores)
# name_graph = args.data.split("/")[1]
# report.to_csv(args.log + "/agsam3d-report_" + str(name_graph) + "_" + str(datetime.now().isoformat()) + ".csv", index=False)
