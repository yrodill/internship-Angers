#! /usr/bin/Rscript --vanilla --default-packages=utils

library(GENIE3)
#browseVignettes("GENIE3")

data <- read.table(file = "~/internship-Angers/tests/benchmark/genie3_syntren/syntrenHop2_20_0_data.csv",sep = ",",header=TRUE)
data <- as.matrix(data,dimnames = row.names(data))
data <- t(data)

rowOrder <- row.names(data)
matriceOrder <- sort(rowOrder)
#View(rowOrder)

newOrder <- c()

for(x in rowOrder){
  index=1
  for(y in matriceOrder){
    if(x==y){
      newOrder <- c(newOrder,index)
    }
    index<-index+1
  }
}

#View(newOrder)
print(newOrder)
  

regulators <- c()

#Finding regulators from the result file obtained with the Syntren generator
data_regulators <- read.table(file="~/internship-Angers/tests/Syntren/nn20_nbgr0_hop0.1_bionoise0.3_expnoise0.1_corrnoise0.1_neighAdd_external.txt",sep = "\t",header = TRUE)
for(reg in data_regulators[,1])
  regulators <- c(regulators,reg)

set.seed(123) # For reproducibility of results
weightMat <- GENIE3(data,nTrees = 1000)

weightMat <- weightMat[newOrder,newOrder]

linkList <- getLinkList(weightMat)
#View(linkList)
write.csv(weightMat, file="/home/ua24906/internship-Angers/tests/results/weightMatCLUST.csv")
#write.table(linkList, file="~/internship-Angers/tests/results/linkList.txt", row.names=FALSE, col.names=TRUE,sep=",")
