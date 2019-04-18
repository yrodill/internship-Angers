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

args = parser.parse_args()

print('Reading file...')
data = pd.read_csv(args.data, sep=',',header=None,skiprows=1)
# print(data)
print("Done...")

def job_function(data,args,l):
    if(args.model == "MI"):
        model = MIRegression()
    else:
        model = PearsonCorrelation()
    print("Avancement : {:.2f}%".format(l/(len(data.index)*len(data.columns))*100))
    i = l//len(data.index)
    j = l%len(data.columns)
    if(i == j):
        return 1
    elif(i > j):
        return 0
    else:
        return(model.predict(data[i].values, data[j].values))
    
  


# Exec computations
results = Parallel(n_jobs=4)(delayed(job_function)(data,args,l) for l in range(len(data.index)*len(data.columns)))
# print(results)

report = pd.DataFrame(results)
report.to_csv("test_parallel.csv",index=False,header=False)
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
