#! usr/bin/python

import json
import pandas as pd

newFile=[]

with open("catma5_probes.json") as json_file:
    data= json.load(json_file)

with open("catma5_ratio.txt") as f:
    lines = f.readlines()
    
    for l in lines:
        res=l.strip().split("\t")
        if(res[0]!="GENES"):
            res[0]=data[res[0]]["atg"]
        newFile.append(res)

df = pd.DataFrame(newFile)
df.to_csv("changedNamesRatio.csv",index=False,header=False)
