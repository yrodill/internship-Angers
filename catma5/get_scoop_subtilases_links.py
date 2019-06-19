# coding: utf8

import pandas as pd
import argparse

"""
Récupération des liens entre AT4G44585 et les subtilases
"""

parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('data', metavar='f', type=str, help='list of links')

args = parser.parse_args()

subtilases = ["AT1G01900","AT1G04110","AT1G20150","AT1G20160","AT1G30600","AT1G32940","AT1G32950","AT1G32960","AT1G32970","AT1G62340","AT1G66210","AT1G66220","AT2G04160","AT2G05920","AT2G19170","AT2G39850","AT3G14067","AT3G14240","AT3G46840","AT3G46850","AT4G00230","AT4G10510","AT4G10520","AT4G10530","AT4G10540","AT4G10550","AT4G15040","AT4G20430","AT4G20850","AT4G21323","AT4G21326","AT4G21630","AT4G21640","AT4G21650","AT4G26330","AT4G30020","AT4G34980","AT5G03620","AT5G11940","AT5G19660","AT5G44530","AT5G45640","AT5G45650","AT5G51750","AT5G58810","AT5G58820","AT5G58830","AT5G58840","AT5G59090","AT5G59100","AT5G59120","AT5G59130","AT5G59190","AT5G59810","AT5G67090","AT5G67360","AT2G06050","AT1G09400","AT1G17990","AT1G18020","AT1G76680","AT1G76690","AT1G71950","AT2G39851"]

df = pd.read_csv(args.data,header=0)

with open(args.data.split('/')[-1].split('.')[0]+'_SCOOP.csv','w') as f:
    for i in range(len(df.index)):
        if(df.iat[i,0] == 'AT5G44585' and df.iat[i,1] in subtilases and df.iat[i,2] != 0):
            f.write(str(df.iat[i,0])+','+str(df.iat[i,1])+','+str(df.iat[i,2])+'\n')
        if(df.iat[i,1] == 'AT5G44585' and df.iat[i,0] in subtilases and df.iat[i,2] != 0):
            f.write(str(df.iat[i,0])+','+str(df.iat[i,1])+','+str(df.iat[i,2])+'\n')
