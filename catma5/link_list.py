from GENIE3 import get_link_list as gll
import argparse
import pandas as pd
import numpy as np
import glob

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('folder', metavar='d', type=str, help='Folder containing the data')
parser.add_argument('out', metavar='o', type=str, help='File output')


args = parser.parse_args()

for file in glob.glob(args.folder + "/*filtered*"):
    matrix = np.genfromtxt(file,delimiter=',',skip_header=1)
    gll(matrix,args.out)