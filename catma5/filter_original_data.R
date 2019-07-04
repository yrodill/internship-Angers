#!/usr/bin/env Rscript --vanilla

#' Launch GENIE3 on the chosen dataset according to the arguments given
#' @author Benoît Bothorel March 2019
#' @param file Path to the input file.
#' @param json Path to the json file containing the experiences sorted by stress type.
#' @param threshold Number between 0 and 1. Example : 0.1 means if there is more than 10% missing data for one gene, it is deleted from data. (default 0 = delete all row with at leats 1 missing value)
#' @param stress Name of the stress used to filter your experiences (default "all") possible value => ["development","chemical","abiotic","biotic"]
#' @param output Output file name (default "./weightedMatrix_Genie3.csv")
#' @return Write a csv file containing the data filtered
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

#Function to replace missing values by a random value from another experience for the same gene
replace_missing_values <- function(df, threshold) {
  
  total <- nrow(df)
  
  if(threshold == 0){
    return (df)
  }
  else{
    pb <- txtProgressBar(min = 0, max = total, style = 3)
    newcolumn <- 0
    for(row in 1:nrow(df)){
      setTxtProgressBar(pb, row)
      for(col in 1:ncol(df)){
        if(df[row,col]=="" || is.na(df[row,col])){
          while(is.na(df[row,col])){
            newcolumn <- sample(1:ncol(df),1)
            df[row,col]=df[row,newcolumn]
          }
        }
      }
    }
  close(pb)
  }
  return (df)
}


#MAIN
args = commandArgs(trailingOnly=TRUE)

#Load libraries
library("rjson")

if (length(args)< 2) {
  stop("At least two arguments must be supplied (input file path and json file path)", call.=FALSE)
} else if (length(args)==2) {
  args[3] = 0.1
  args[4] = "all"
  args[5] = "tmp_filtered_data.csv"
}else if (length(args)>2 && length(args)<5){
    stop("When you give more than 2 arguments you must provide all the others arguments", call.=FALSE)
}

#Load the file
print("Loading file...")
data <- as.matrix(read.csv(args[1],row.names = 1))
print("Done...")

#Filter columns by stress type
print("Filtering column by experience type selected...")
data_c_filtered <- filter_experiences(data,args[4],args[2])
print("Done...")

#Filter missing values by threshold
print("Filtering rows by missing values threshold...")
data_filtered <- filter_missing_values(data_c_filtered,as.numeric(args[4]))
print("Done...")


#Replace missing values by random value from the gene expression
print("Replacing missing values by a random value from same row but another column...")
data_final <- replace_missing_values(data_filtered,as.numeric(args[3]))
print("Done...")

print("Writing matrix in the current folder...")
write.csv(as.matrix(t(data_final)), file = args[5],row.names = FALSE)
print("Done...")

quit(save = "default", status = 0, runLast = FALSE)

