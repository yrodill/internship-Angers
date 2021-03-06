import glob
import argparse
import pandas as pd
import re
import csv
import os
import sys

"""
BOTHOREL Benoît
20/03/2019
Script used to calculate means and std dev for all experiences and grouping them
into the specified folder/file

This assumes that you have all the files needed in the selected folder

As to be launched in /CausalGen/gSAM/
"""

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('folder', metavar='f', type=str, help='data folder')
parser.add_argument('out', metavar='o', type=str, help='path to output')

args = parser.parse_args()

def calc_mean(df,colname):
    column = df[colname]
    mean=0
    for v in column:
        mean+=v
    return mean/len(column)

dir_path=os.path.dirname(os.path.realpath(__file__))+"/GENIE3/"

if os.path.isfile("{}{}{}GENIE3_all_results.csv".format(dir_path,args.folder,args.out)):
    if os.stat("{}{}{}GENIE3_all_results.csv".format(dir_path,args.folder,args.out)).st_size != 0:
        open("{}{}{}GENIE3_all_results.csv".format(dir_path,args.folder,args.out),"w").close()

for file_ in glob.glob(dir_path+ args.folder + "*GENIE3*"):
    with open(file_) as f:
        exp=re.match("^.*_(\w+_\w+)_.*$",file_)
        if exp is None:
            exp=re.match("^.*_(\w+)_.*$",file_)
        df = pd.read_csv(f)
        mean=calc_mean(df,"AUPR")
        std_dev=df["AUPR"].std()
        file = file_

        with open("{}{}{}GENIE3_all_results.csv".format(dir_path,args.folder,args.out),mode="a") as csv_file:
            writer = csv.writer(csv_file,delimiter=",",quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([file,exp[1],"Mean :"+str(mean),"Std dev: "+str(std_dev)])

print("Done... File in {}{}{}".format(dir_path,args.folder,args.out))