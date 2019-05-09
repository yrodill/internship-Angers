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
parser.add_argument('--njobs', metavar='m', type=int, help='number of jobs for parralel computation',default=1)


args = parser.parse_args()

print('Reading file...')
data = pd.read_csv(args.data, sep=',',header=None,skiprows=1)
print("Done...")

def job_function(data,args,l):
    result=[]
    if(args.model == "MI"):
        model = MIRegression()
    else:
        model = PearsonCorrelation()

    for idx_j, j in enumerate(data.columns):
        if(l == j):
            result.append(0)
        else:
            if(args.model =="MI"):
                result.append(model.predict(data[l].values, data[j].values)[0])
            else:
                result.append(model.predict(data[l].values, data[j].values))
    return result
  


# Exec computations
start_time = time.time()
print("Launch parallelization...")
results = Parallel(n_jobs=args.njobs)(delayed(job_function)(data,args,l) for l in range(len(data.columns)))
print("Done..")
print("Execution time : {}".format(time.time() - start_time))


report = pd.DataFrame(results)
report.to_csv("data/test_parallel3.csv",index=False,header=False)
