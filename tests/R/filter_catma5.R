X <- as.matrix(read.table("~/internship-Angers/catma5/catma5_ISampleNorm.txt" ,sep="\t",header=FALSE,row.names=1) ) # tab-delimited data
X2 <- as.matrix(read.table("~/internship-Angers/catma5/catma5_IRefNorm.txt" ,sep="\t",header=FALSE,row.names=1) ) # tab-delimited data

lineToDelete <- c()
lineToDelete10 <- c()

threshold <- ncol(X)*0.1

for(row in 1:nrow(X)){
  for(col in 1:ncol(X)){
    if(X[row,col]==""){
      lineToDelete <- c(lineToDelete,row)
      break
    }
  }
}

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

removedNASample <- X[-lineToDelete,]
removedNANorm <- X2[-lineToDelete,]

removedNASample10 <- X[-lineToDelete,]
removedNANorm10 <- X2[-lineToDelete,]

write.table(removedNASample,file="~/internship-Angers/catma5/filtered_catma5_ISampleNorm.txt",row.names=TRUE, col.names=FALSE,sep="\t")
write.table(removedNANorm,file="~/internship-Angers/catma5/filtered_catma5_IRefNorm.txt",row.names=TRUE, col.names=FALSE,sep="\t")
write.table(removedNASample10,file="~/internship-Angers/catma5/filtered_10_catma5_ISampleNorm.txt",row.names=TRUE, col.names=FALSE,sep="\t")
write.table(removedNANorm10,file="~/internship-Angers/catma5/filtered_10_catma5_IRefNorm.txt",row.names=TRUE, col.names=FALSE,sep="\t")

library("GENIE3")               
#wMat <- GENIE3(removedNASample,nTrees = 10 , K=5,nCores=1)