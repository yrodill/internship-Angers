#!/bin/env Rscript --vanilla

#' Realize fast_greedy clustering on the data
#' @author Benoît Bothorel March 2019
#' @param Links_matrix Binary matrix of genes*genes.
#' @param GO_matrix Binary matrix of genes*GOTerms.
#' @param output1 Filename of the AUROC output.
#' @param output2 Filename of the AUPR output
#' @return Write a csv file containing the GOTerms with an AUC >threshold.
#' @examples
#' Rscript --vanilla GO_enrichment.R genes_links.csv GO_matrix.csv results.csv 0.7

args<-commandArgs(trailingOnly=TRUE)

library(Matrix)
library(data.table)

run_GBA <- function(network, labels, min = 20, max = 1000, nfold = 3, calc = "AUROC") {

  m <- match(rownames(network), rownames(labels))
  f <- !is.na(m)
  g <- m[f]

  network.sub <- network[f, f]
  genes.labels <- filter_network_cols(labels[g, ], min, max)

  roc.sub <- neighbor_voting(labels, network, nfold, output=calc)
  genes <- predictions(labels, network)
  auroc <- mean(roc.sub[, 1], na.rm = TRUE)
  
  results <- list(roc.sub, genes, auroc)
  return(results)
  
} 

filter_network_cols <- function(network, min = 0, max = 1, ids = NA) {
  network <- as.matrix(network)
  if (sum(is.na(ids))) {
    colsums <- colSums(network)
    col.filter <- which((colsums > min & colsums < max))
  } else {
    m = match(colnames(network), ids)
    col.filter = !is.na(m)
    
  }
  network <- network[, col.filter]
  
  return(network)
} 

neighbor_voting <- function(genes.labels, network, nFold = 3, output = "AUROC", FLAG_DRAW = FALSE) {
  genes.labels <- as.matrix(genes.labels)
  
  # Filter for common genes between network and labels
  ord <- order(rownames(network))
  network <- network[ord, ord]
  
  ord <- order(rownames(genes.labels))
  genes.labels <- as.matrix(genes.labels[ord, ])
  
  match.lab <- match(rownames(genes.labels), rownames(network))
  filt.lab <- !is.na(match.lab)
  filt.net <- match.lab[filt.lab]
  network <- network[filt.net, filt.net]
  genes.labels <- as.matrix(genes.labels[filt.lab, ])

  # genes.label : needs to be in 1s and 0s
  l <- dim(genes.labels)[2]
  g <- dim(genes.labels)[1]
  ab <- which(genes.labels != 0, arr.ind = TRUE)
  n <- length(ab[, 1])

  
  # print('Make genes label CV matrix')
  test.genes.labels <- matrix(genes.labels, nrow = g, ncol = nFold * l)

  # For each fold in each GO group, remove 1/nth of the values of the genes.label
  for (j in 1:l) {
    d <- which(ab[, 2] == j)  # Which indices the genes are in this particular GO group
    t <- length(d)  # Total number of genes in the GO group
    r <- sample(1:t, replace = FALSE)
    f <- t/nFold
    for (i in 1:nFold) {
      e <- c((1:f) + f * (i - 1))
      e <- sort(r[e])
      c <- j + l * (i - 1)  # GO group to look at (ie column)
      test.genes.labels[ab[d], c][e] <- 0
    }
  }
  
  # print('Get sums - mat. mul.') sumin = ( t(network) %*% test.genes.labels) sumin <- ((network)
  # %*% test.genes.labels)
  sumin <- crossprod(network, test.genes.labels)
  
  # print('Get sums - calc sumall')
  sumall <- matrix(apply(network, 2, sum), ncol = dim(sumin)[2], nrow = dim(sumin)[1])
  
  # print('Get sums - calc predicts')
  predicts <- sumin/sumall
  
  
  if (output == "AUROC") {
    # print('Hide training data')
    nans <- which(test.genes.labels == 1, arr.ind = TRUE)
    
    predicts[nans] <- NA
    
    # print('Rank test data')
    predicts <- apply(abs(predicts), 2, rank, na.last = "keep", ties.method = "average")
    
    filter <- matrix(genes.labels, nrow = g, ncol = nFold * l)
    negatives <- which(filter == 0, arr.ind = TRUE)
    positives <- which(filter == 1, arr.ind = TRUE)
    
    predicts[negatives] <- 0
    
    # print('Calculate ROC - np')
    np <- colSums(filter) - colSums(test.genes.labels)  # Postives
    
    # print('Calculate ROC - nn')
    nn <- dim(test.genes.labels)[1] - colSums(filter)  # Negatives
    
    # print('Calculate ROC - p')
    p <- apply(predicts, 2, sum, na.rm = TRUE)
    
    # print('Calculate ROC - rocN')
    rocN <- (p/np - (np + 1)/2)/nn
    rocN <- matrix(rocN, ncol = nFold, nrow = l)
    rocN <- rowMeans(rocN)
    
    # print('Calculate node degree')
    node_degree <- rowSums(network)
    colsums <- colSums(genes.labels)
    
    # print('Calculate node degree - sum across gene labels')
    node_degree <- matrix(node_degree)
    temp <- t(node_degree) %*% genes.labels
    
    
    # print('Calculate node degree - average')
    average_node_degree <- t(temp)/colsums
    
    # print('Calculate node degree roc - rank node degree')
    ranks <- apply(abs(node_degree), 2, rank, na.last = "keep", ties.method = "average")
    ranks <- matrix(ranks, nrow = length(ranks), ncol = dim(genes.labels)[2])
    
    # print('Calculate node degree roc - remove negatives')
    negatives <- which(genes.labels == 0, arr.ind = TRUE)
    ranks[negatives] <- 0
    
    # print('Calculate node degree roc - np')
    np <- colSums(genes.labels)
    
    # print('Calculate node degree roc - nn')
    nn <- dim(genes.labels)[1] - np
    
    # print('Calculate node degree roc - p')
    p <- apply(ranks, 2, sum, na.rm = TRUE)
    
    # print('Calculate node degree roc - roc')
    roc <- (p/np - (np + 1)/2)/nn
    
    if (FLAG_DRAW == TRUE) {
      plot_roc_overlay(predicts, test.genes.labels)
    }
    
    scores <- cbind(
      auc=rocN,
      avg_node_degree=matrix(average_node_degree)[, 1],
      degree_null_auc=roc)
  } else if (output == "PR") {
    
    nans <- which(test.genes.labels == 1, arr.ind = TRUE)
    predicts[nans] <- NA
    filter <- matrix(genes.labels, nrow = g, ncol = nFold * l)
    negatives <- which(filter == 0, arr.ind = TRUE)
    positives <- which(filter == 1, arr.ind = TRUE)
    
    # print('Rank test data')
    predicts <- apply(-abs(predicts), 2, rank, na.last = "keep", ties.method = "average")
    predicts[negatives] <- 0
    
    avgprc.s <- lapply(1:(nFold * l), function(i)  
      mean(  ( 1:length(which( sort(predicts[,i]) > 0   )  )
               / sort(predicts[,i])[ which( sort(predicts[,i]) > 0 )]), na.rm = TRUE)   )
    
    n.s <- colSums(test.genes.labels)
    avgprc.null <- lapply(1:(nFold * l), function(i) n.s[i]/g)
    avgprc.null <- rowMeans(matrix(unlist(avgprc.null), ncol = nFold, nrow = l, byrow = FALSE), 
                            na.rm = TRUE)
    
    avgprc <- rowMeans(matrix(unlist(avgprc.s), ncol = nFold, nrow = l, byrow = FALSE), na.rm = TRUE)
    names(avgprc) <- colnames(genes.labels)
    
    # print('Calculate node degree')
    node_degree <- rowSums(network)
    colsums <- colSums(genes.labels)
    
    # print('Calculate node degree - sum across gene labels')
    node_degree <- matrix(node_degree)
    temp <- t(node_degree) %*% genes.labels
    
    
    # print('Calculate node degree - average')
    average_node_degree <- t(temp)/colsums
    
    scores <- cbind(
      avgprc=avgprc,
      avg_node_degree=matrix(average_node_degree)[, 1],
      degree_null_auc=avgprc.null)
  }
  
  
  return(scores)
}

predictions <- function(genes.labels, network) {
  genes.labels <- as.matrix(genes.labels)
  
  # Filter for common genes between network and labels
  ord <- order(rownames(network))
  network <- network[ord, ord]
  
  ord <- order(rownames(genes.labels))
  genes.labels <- as.matrix(genes.labels[ord, ])
  
  match.lab <- match(rownames(genes.labels), rownames(network))
  filt.lab <- !is.na(match.lab)
  filt.net <- match.lab[filt.lab]
  network <- network[filt.net, filt.net]
  genes.labels <- as.matrix(genes.labels[filt.lab, ])
  
  # genes.label : needs to be in 1s and 0s
  l <- dim(genes.labels)[2]
  g <- dim(genes.labels)[1]
  ab <- which(genes.labels != 0, arr.ind = TRUE)
  n <- length(ab[, 1])
  
  # Get sums - mat. mul.
  sumin <- (t(network) %*% genes.labels)
  
  # Sum of all edge in network
  sumall <- matrix(apply(network, 2, sum), ncol = dim(sumin)[2], nrow = dim(sumin)[1])
  
  # Predictions
  predicts <- sumin/sumall
  return(predicts)
}

#MAIN
adj.matrix <- as.matrix(read.csv(args[1],row.names = 1))

agrigo <- as.matrix(read.csv(args[2],row.names = 1))

#AUROC CALC
GO_groups_voted <-run_GBA(adj.matrix,agrigo, min=20, max=1000, nfold=3,calc="AUROC")
auroc_network<-GO_groups_voted[[3]]
auroc_degree<-mean(GO_groups_voted[[1]][,3])
GO <- list(GO_groups_voted[[1]][,3])

GO_terms <- c()
values <- c()
for(i in 1:length(GO_groups_voted[[1]][,3])){
  #if(GO_groups_voted[[1]][i,3] > 0.6){
    GO_terms <- c(GO_terms,names(GO[[1]][i]))
    values <- c(values,GO_groups_voted[[1]][i,3])
  #}
}
data <- data.table(GO=GO_terms,value=values)
write.csv(data,args[3],row.names=FALSE)

#PR CALC
GO_groups_voted <-run_GBA(adj.matrix,agrigo, min=20, max=1000, nfold=3, calc="PR")
auroc_network<-GO_groups_voted[[3]]
auroc_degree<-mean(GO_groups_voted[[1]][,3])
GO <- list(GO_groups_voted[[1]][,3])

GO_terms <- c()
values <- c()
for(i in 1:length(GO_groups_voted[[1]][,3])){
  #if(GO_groups_voted[[1]][i,3] > 0.6){
    GO_terms <- c(GO_terms,names(GO[[1]][i]))
    values <- c(values,GO_groups_voted[[1]][i,3])
  #}
}
data <- data.table(GO=GO_terms,value=values)
write.csv(data,args[4],row.names=FALSE)