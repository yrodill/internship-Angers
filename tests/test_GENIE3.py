import os


#RUN the R script on the data obtained from Syntren
os.system("Rscript R/test_GENIE3.R")

#Get data from the file created through the R script
with open(file="results/linkList.txt") as f:
    lines=f.readlines()

for l in lines:
    word=l.split("\t")
    print("Gene : {} has effects on Gene : {} ; Score : {}".format(word[0],word[1],word[2]))