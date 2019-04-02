import os
import sys
import glob
import argparse
import pandas as pd
import numpy as np
from cdt.independence.stats.numerical import MIRegression
from cdt.independence.stats.numerical import PearsonCorrelation

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('folder', metavar='f', type=str, help='data folder')
parser.add_argument('out', metavar='o', type=str, help='extension name')

args = parser.parse_args()

dir_path=os.path.dirname(os.path.realpath(__file__))+"/"+args.folder
print(dir_path)

model = MIRegression()
# model = PearsonCorrelation()


results = []

# for directory in glob.glob(dir_path + "/*"):
#     for file in glob.glob(directory + "/matrix/*matrix*"):
#         print("Running on file : {} , ...".format(file))
#         filename = file.split("/")[-1].replace(".csv","")
#         data = pd.read_csv(file,sep=' ')
#         for idx_i, i in enumerate(data.columns):
#             for idx_j, j in enumerate(data.columns[idx_i+1:]):
#                 score = model.predict(data[i].values, data[j].values)
#                 results.append(score)

#         data.to_csv(directory+"/MI/"+"MI"+filename+"_"+args.out)
#         print("Done...")

# for directory in glob.glob(dir_path + "/*"):
#     for file in glob.glob(directory + "/matrix/*matrix*"):
#         print("Running on file : {} , ...".format(file))
#         filename = file.split("/")[-1].replace(".csv","")
#         data = pd.read_csv(file,sep=' ')
#         for idx_i, i in enumerate(data.columns):
#             for idx_j, j in enumerate(data.columns[idx_i+1:]):
#                 score = model.predict(data[i].values, data[j].values)
#                 results.append(score)

#         data.to_csv(directory+"/Pearson/"+"Pearson_"+filename+"_"+args.out)
#         print("Done...")

for directory in glob.glob(dir_path + "/*"):
    if(directory.split("/")[-1] == "syntren"):
        for file in glob.glob(directory + "/*"):
                for f in glob.glob(file + "/matrix/*matrix*"):
                    print("Running on file : {} , ...".format(f))
                    filename = f.split("/")[-1].replace(".csv","")
                    data = pd.read_csv(f,sep=' ')
                    for idx_i, i in enumerate(data.columns):
                        for idx_j, j in enumerate(data.columns[idx_i+1:]):
                            score = model.predict(data[i].values, data[j].values)
                            results.append(score)

                data.to_csv(file+"/MI/"+"MI"+filename+"_"+args.out)
                print("Done...")
    else:
        for file in glob.glob(directory + "/matrix/*matrix*"):
            print("Running on file : {} , ...".format(file))
            filename = file.split("/")[-1].replace(".csv","")
            data = pd.read_csv(file,sep=' ')
            for idx_i, i in enumerate(data.columns):
                for idx_j, j in enumerate(data.columns[idx_i+1:]):
                    score = model.predict(data[i].values, data[j].values)
                    results.append(score)

            data.to_csv(directory+"/MI/"+"MI"+filename+"_"+args.out)
            print("Done...")

# for directory in glob.glob(dir_path + "/*"):
#     if(directory.split("/")[-1] == "syntren"):
#         for file in glob.glob(directory + "/*"):
#                 for f in glob.glob(file + "/matrix/*matrix*"):
#                     print("Running on file : {} , ...".format(f))
#                     filename = f.split("/")[-1].replace(".csv","")
#                     data = pd.read_csv(f,sep=' ')
#                     for idx_i, i in enumerate(data.columns):
#                         for idx_j, j in enumerate(data.columns[idx_i+1:]):
#                             score = model.predict(data[i].values, data[j].values)
#                             results.append(score)

#                 data.to_csv(file+"/Pearson/"+"Pearson_"+filename+"_"+args.out)
#                 print("Done...")
#     else:
#         for file in glob.glob(directory + "/matrix/*matrix*"):
#             print("Running on file : {} , ...".format(file))
#             filename = file.split("/")[-1].replace(".csv","")
#             data = pd.read_csv(file,sep=' ')
#             for idx_i, i in enumerate(data.columns):
#                 for idx_j, j in enumerate(data.columns[idx_i+1:]):
#                     score = model.predict(data[i].values, data[j].values)
#                     results.append(score)

#             data.to_csv(directory+"/Pearson/"+"Pearson_"+filename+"_"+args.out)
#             print("Done...")