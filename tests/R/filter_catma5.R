X <- as.matrix(read.table("~/internship-Angers/catma5/catma5_ISampleNorm.txt" ,sep="\t",header=FALSE) ) # tab-delimited data
X2 <- as.matrix(read.table("~/internship-Angers/catma5/catma5_IRefNorm.txt" ,sep="\t",header=FALSE,row.names=1) ) # tab-delimited data
gen3 <- as.matrix(read.csv("~/internship-Angers/catma5/changedNames.csv",row.names = 1))

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

lineToDelete10 <- c()

threshold <- ncol(X)*0.1

#Remove row with at least 1 missing data
for(row in 1:nrow(X)){
  for(col in 1:ncol(X)){
    if(X[row,col]=="" || X[row,col]=="NA"){
      lineToDelete <- c(lineToDelete,row)
      break
    }
  }
}

removedNASample <- X[-lineToDelete,]
removedNANorm <- X2[-lineToDelete,]


#Remove row if more than 10% missing data for the row
for(row in 1:nrow(X)){
  nbMiss<-0
  for(col in 1:ncol(X)){
    if(X[row,col]==""){
      nbMiss<-nbMiss+1
    }
  }
  if(nbMiss > threshold){
    lineToDelete10 <- c(lineToDelete10,row)
  }
}

removedNASample10 <- X[-lineToDelete10,]
removedNANorm10 <- X2[-lineToDelete10,]

write.table(removedNASample,file="~/internship-Angers/catma5/filtered_catma5_ISampleNorm.txt",row.names=FALSE, col.names=FALSE,sep="\t")
write.table(removedNANorm,file="~/internship-Angers/catma5/filtered_catma5_IRefNorm.txt",row.names=TRUE, col.names=FALSE,sep="\t")
write.table(removedNASample10,file="~/internship-Angers/catma5/filtered_10_catma5_ISampleNorm.txt",row.names=TRUE, col.names=FALSE,sep="\t")
write.table(removedNANorm10,file="~/internship-Angers/catma5/filtered_10_catma5_IRefNorm.txt",row.names=TRUE, col.names=FALSE,sep="\t")

gen3 <- prepare_dataset(gen3)

??GENIE3
library("GENIE3")
set.seed(123)
wMat <- GENIE3(gen3,nTrees = 10 , K=5,nCores=1,verbose=TRUE)

linkList <- getLinkList(wMat)

removedNASample <- t(removedNASample)
genesNames <- removedNASample[1,]
genesNames <- genesNames[-1]

removedNASample <- removedNASample[-1,-1]
removedNASample <- apply(removedNASample,c(1,2),as.numeric)


library("corpcor")


pcr1 <- pcor.shrink(gen3,verbose=TRUE)

write.table(pcr1,file="~/internship-Angers/catma5/pcr.txt",row.names=genesNames, col.names=genesNames,sep="\t")





exprMat <- matrix(sample(1:10, 100, replace=TRUE), nrow=20)
rownames(exprMat) <- paste("Gene", 1:20, sep="")
colnames(exprMat) <- paste("Sample", 1:5, sep="")
