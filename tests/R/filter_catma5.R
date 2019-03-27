#!/usr/bin/env Rscript

#' Launch GENIE3 on the chosen dataset according to the arguments given
#' @author Benoît Bothorel March 2019
#' @param file Path to the input file.
#' @param json Path to the json file containing the experiences sorted by stress type.
#' @param nCores The number of cores used for parallel computation (default 1).
#' @param threshold Number between 0 and 1. Example : 0.1 means if there is more than 10% missing data for one gene, it is deleted from data. (default 0 = delete all row with at leats 1 missing value)
#' @param stress Name of the stress used to filter your experiences (default "all") possible value => ["development","chemical treatment","abiotic","biotic"]
#' @param ratio Value used for the bootstrap [0:1] (default 0.8)
#' @return Write a csv file containing the matrix of co-expression.
#' @examples
#' Rscript --vanilla /path/to/file /path/to/json
#' Rscript --vanilla /path/to/file /path/to/json 10 0.1 "development"



#Function to filter experiences by type of stress
filter_experiences <- function(df,stress,json){
  
  data <- fromJSON(file = json)
  
  list_exp <- c()
  for(exp in data[stress]){
    list_exp <- c(list_exp,exp)
  }
  
  colToDelete <- c()
  
  if(stress == "all"){
    return (df)
  }
  else{
    index=1
    for(names in gsub("X", "", colnames(df))){
      if(!(names %in% list_exp)){
        colToDelete <- c(colToDelete,index)
      }
      index <- index + 1
    }
  }
  return (df[,-colToDelete])
}

#Function to filter missing values
filter_missing_values <- function(df,threshold){
  
  lineToDelete <- c()
  
  if(threshold == 1){
    return (df)
  }
  else{
    threshold <- ncol(df)*threshold
    
    for(row in 1:nrow(df)){
      nbMiss<-0
      for(col in 1:ncol(df)){
        if(df[row,col]=="" || is.na(df[row,col])){
          nbMiss<-nbMiss+1
        }
        if(nbMiss > threshold){
            lineToDelete <- c(lineToDelete,row)
            break
        }
      }
    }
  }
  return(df[-lineToDelete,])
  
}

#Bootstrap to keep only a few part of the data randomly
bootstrap <- function(df,ratio){
  lineToKeep <- c()
  limit <- nrow(df)*ratio
  
  while(length(lineToKeep)<limit){
    number <- sample(1:nrow(df),1)
    while(number %in% lineToKeep){
      number <- sample(1:nrow(df),1)
    }
    lineToKeep <- c(lineToKeep,number)
  }
  
  return (df[lineToKeep,])
}

#Function to replace missing values by a random value from another experience for the same gene
replace_missing_values <- function(df, threshold) {
  
  if(threshold == 0){
    return (df)
  }
  else{
    newcolumn <- 0
    for(row in 1:nrow(df)){
      for(col in 1:ncol(df)){
        if(df[row,col]=="" || is.na(df[row,col])){
          while(is.na(df[row,col])){
            newcolumn <- sample(1:ncol(df),1)
            df[row,col]=df[row,newcolumn]
          }
        }
      }
    }
  }
  return (df)
}

#Function to replace the genes in the correct order because GENIE3 sorts automaticaaly by name
reorder <- function(original,matrix){
    rowOrder <- row.names(original)
    matrixOrder <- sort(rowOrder)

    newOrder <- c()

    for(x in rowOrder){
        index=1
        for(y in matrixOrder){
            if(x==y){
            newOrder <- c(newOrder,index)
                }
            index<-index+1
        }
    }
    return (matrix[newOrder,newOrder])
}

#MAIN
args = commandArgs(trailingOnly=TRUE)

#Load libraries
library("rjson")
library("GENIE3")

if (length(args)< 2) {
  stop("At least two arguments must be supplied (input file path and json file path)", call.=FALSE)
} else if (length(args)==2) {
  args[3] = 1
  args[4] = 0
  args[5] = "all"
  args[6] = 0.8
}

#Load the file
print("Loading file...")
gen3 <- as.matrix(read.csv(args[1],row.names = 1))
print("Done...")
#gen3 <- as.matrix(read.csv("~/internship-Angers/catma5/changedNames.csv",row.names = 1))

#Filter columns by stress type
print("Filtering column by experience type selected...")
gen3_c_filtered <- filter_experiences(gen3,args[5],args[2])
print("Done...")
#gen3_c_filtered <- filter_experiences(gen3,"development","~/internship-Angers/catma5/sorted_exp_by_stress.json")

#Filter missing values by threshold
print("Filtering rows by missing values threshold...")
gen3_filtered <- filter_missing_values(gen3_c_filtered,as.numeric(args[4]))
print("Done...")
#gen3_filtered <- filter_missing_values(gen3_c_filtered,0.1)
#dim(gen3_filtered)

#Bootstrap à 80% des données
print("Boostraping the data according to the selected ratio...")
gen3_boot <- bootstrap(gen3_filtered,as.numeric(args[6]))
print("Done...")
#gen3_boot <- bootstrap(gen3_filtered,0.8)
#dim(gen3_boot)

#Replace missing values by random value from the gene expression
print("Replacing missing values by a random value from same row but another column...")
gen3_final <- replace_missing_values(gen3_boot,as.numeric(args[4]))
print("Done...")
#gen3_final <- replace_missing_values(gen3_boot,0.1)

#Test sur sous-échantillon
test_gen3 <- gen3_boot[1:200,1:300]
test_gen3 <- replace_missing_values(test_gen3,0.1)



print("Running GENIE3 on the data...")
set.seed(123)
matrix <- GENIE3(test_gen3,nCores=as.numeric(args[3]),verbose=TRUE)
print("Done...")

print("Re-ordering the matrix to fit the original order...")
matrix <- reorder(test_gen3,matrix)
print("Done...")

print("Writing matrix in the current folder...")
write.csv(as.matrix(matrix), file = 'weightedMatrix_Genie3.csv')
print("Done...")

