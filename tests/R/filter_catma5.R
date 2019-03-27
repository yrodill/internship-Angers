#!/usr/bin/env Rscript

#' Launch GENIE3 on the chosen dataset according to the arguments given
#' 
#' @param file Path to the input file.
#' @param json Path to the json file containing the experiences sorted by stress type.
#' @param nCores The number of cores used for parallel computation (default 1).
#' @param threshold Number between 0 and 1. Example : 0.1 means if there is more than 10% missing data for one gene, it is deleted from data(default 1)
#' @param stress Name of the stress used to filter your experiences (default "all") ["development","chemical treatment","abiotic","biotic"]
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
      }
      if(nbMiss > threshold){
        lineToDelete <- c(lineToDelete,row)
      }
    }
  }
  
}

#Bootstrap to keep only a few part of the data randomly
bootstrap <- function(df,ratio){
  lineToKeep <- c()
  limit <- round(nrow(df)*ratio)
  
  while(length(lineToKeep)<limit){
    print(length(lineToKeep))
    print(limit)
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
    nb_missing_values_changed <-0
    newcolumn <- 0
    for(row in 1:nrow(df)){
      for(col in 1:ncol(df)){
        if(df[row,col]=="" || is.na(df[row,col])){
          while(is.na(df[row,col])){
            newcolumn <- sample(1:ncol(df),1)
            df[row,col]=df[row,newcolumn]
          }
          nb_missing_values_changed <- nb_missing_values_changed +1
          print(nb_missing_values_changed)
        }
      }
    }
  }
  return (df)
}


#MAIN
args = commandArgs(trailingOnly=TRUE)

#Load libraries
library("rjson")
library("boot")
library("GENIE3")

if (length(args)< 2) {
  stop("At least two arguments must be supplied (input file path and json file path)", call.=FALSE)
} else if (length(args)==2) {
  args[3] = 1
  args[4] = 1
  args[5] = "all"
  args[6] = 0.8
}

#Load the file
gen3 <- as.matrix(read.csv(args[1],row.names = 1))
gen3 <- as.matrix(read.csv("~/internship-Angers/catma5/changedNames.csv",row.names = 1))
#Filter columns by stress type
gen3_c_filtered <- filter_experiences(gen3,args[5],args[2])
gen3_c_filtered <- filter_experiences(gen3,"all","~/internship-Angers/catma5/sorted_exp_by_stress.json")
#Filter missing values by threshold
gen3_filtered <- filter_missing_values(gen3_c_filtered,strtoi(args[4]))
gen3_filtered <- filter_missing_values(gen3_c_filtered,1)

#write.csv(as.matrix(gen3_filtered), file = 'test.csv')

#Bootstrap à 80% des données
gen3_boot <- bootstrap(gen3_filtered,strtoi(args[6]))
gen3_boot <- bootstrap(gen3_filtered,0.8)

#Replace missing values by random value from the gene expression
test <- replace_missing_values(gen3_boot,1)


write.csv(as.matrix(test), file = 'test2.csv')