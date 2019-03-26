#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

if (length(args)==0) {
  stop("At least one argument must be supplied (input file path)", call.=FALSE)
} else if (length(args)==1) {
  args[2]=1
}

gen3 <- as.matrix(read.csv(args[1],row.names = 1))

prepare_dataset <- function(df){
  
lineToDelete <- c()
  
  for(row in 1:nrow(df)){
    for(col in 1:ncol(df)){
      if(df[row,col]=="" || is.na(df[row,col])){
        lineToDelete <- c(lineToDelete,row)
        break
      }
    }
  }
  return (df[-lineToDelete,])
}

print("Preparing the data...removing all missing values")
gen3 <- prepare_dataset(gen3)

library("GENIE3")
set.seed(123)
print("Done...Launching GENIE3 on the dataset...")
wMat <- GENIE3(gen3,nCores=strtoi(args[2]), verbose=TRUE)
print("Done...")

#linkList <- getLinkList(wMat,threshold=0.2)

print("Changing order from GENIE3 result to original order...")
rowOrder <- row.names(gen3)
matriceOrder <- sort(rowOrder)

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

wMat <- wMat[newOrder,newOrder]
print("Done...")

print("Write file to csv...")
write.csv(wMat, file = '~/weightMat.csv',row.names=FALSE)
print("Done...")
