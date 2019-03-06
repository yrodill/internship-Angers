#! /usr/bin/Rscript --vanilla --default-packages=utils

library(GENIE3)
#browseVignettes("GENIE3")

data <- read.table(file = "~/internship-Angers/tests/Syntren/nn20_nbgr0_hop0.1_bionoise0.3_expnoise0.1_corrnoise0.1_neighAdd_maxExpr1_dataset.txt",sep = "\t",header = TRUE , row.names = 1)
data <- as.matrix(data,dimnames = row.names(data))

regulators <- c()

#Finding regulators from the result file obtained with the Syntren generator
data_regulators <- read.table(file="~/internship-Angers/tests/Syntren/nn20_nbgr0_hop0.1_bionoise0.3_expnoise0.1_corrnoise0.1_neighAdd_external.txt",sep = "\t",header = TRUE)
for(reg in data_regulators[,1])
  regulators <- c(regulators,reg)

set.seed(123) # For reproducibility of results
weightMat <- GENIE3(data,nTrees = 100)

linkList <- getLinkList(weightMat)
#View(linkList)
write.csv(weightMat, file="~/internship-Angers/tests/results/weightMat.csv")
write.table(linkList, file="~/internship-Angers/tests/results/linkList.txt", row.names=FALSE, col.names=TRUE,sep="\t")
