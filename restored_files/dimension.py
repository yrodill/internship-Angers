import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('data', metavar='d', type=str, help='data')

args = parser.parse_args()

df = pd.read_csv(args.data,header=0)
print(len(df.columns))