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

gen3 <- prepare_dataset(gen3)

library("GENIE3")
set.seed(123)
wMat <- GENIE3(gen3, verbose=TRUE)

#linkList <- getLinkList(wMat,threshold=0.2)

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
write.csv(wMat, file = '~/weightMat.csv',row.names=FALSE)
