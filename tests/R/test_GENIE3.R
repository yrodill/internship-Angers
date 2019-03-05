#! /usr/bin/Rscript --vanilla --default-packages=utils

library(GENIE3)
#browseVignettes("GENIE3")

data <- read.table(file = "~/CausalGen/Syntren/data/results/nn100_nbgr100_hop0.3_bionoise0.1_expnoise0.1_corrnoise0.1_neighAdd_maxExpr1_dataset.txt",sep = "\t",header = TRUE , row.names = 1)
data <- as.matrix(data,dimnames = row.names(data))

regulators <- c()

data_regulators <- read.table(file="~/CausalGen/Syntren/data/results/nn100_nbgr100_hop0.3_bionoise0.1_expnoise0.1_corrnoise0.1_neighAdd_external.txt",sep = "\t",header = TRUE)
for(reg in data_regulators[,1])
  regulators <- c(regulators,reg)

set.seed(123) # For reproducibility of results
weightMat <- GENIE3(data,regulators = regulators,nTrees = 50,K=7,treeMethod="ET")

linkList <- getLinkList(weightMat)
#View(linkList)

write.table(linkList, file="~/internship-Angers/tests/results/linkList.txt", row.names=FALSE, col.names=TRUE,sep="\t")
