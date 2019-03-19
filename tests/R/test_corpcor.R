prepare_dataset <- function(df){

  df <- df[-1,]
  df <- as.matrix(apply(df,1, as.numeric))
  
  lineToDelete <- c()
  
  for(row in 1:nrow(df)){
    for(col in 1:ncol(df)){
      if(df[row,col]=="" || is.na(df[row,col])){
        lineToDelete <- c(lineToDelete,row)
        break
      }
    }
  }
  if(length(lineToDelete) > 0){
    df <- df[-lineToDelete,]
  }
  return (df)
}

df <- as.matrix(read.table("~/internship-Angers/tests/benchmark/genie3_syntren/syntrenHop2_20_0_data.csv" ,sep=",",header=FALSE) ) # tab-delimited data

library("corpcor")

matrix <- t(prepare_dataset(df))
pcr1 <- pcor.shrink(matrix,verbose=TRUE)

for(row in 1:nrow(pcr1)){
  for(col in 1:ncol(pcr1)){
    if(pcr1[row,col]==1){
      pcr1[row,col]=0
    }
  }
}

write.table(pcr1,file="~/internship-Angers/tests/results/pcr1.txt",sep="\t",row.names = FALSE,col.names = FALSE)
