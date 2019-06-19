#!/usr/bin/env Rscript

#' Realize fast_greedy clustering on the data
#' @author Benoît Bothorel March 2019
#' @param file Path to the input file.
#' @param method Clustering method to use.
#' @param output Path to the output file.
#' @return Write a csv file containing the communities after using fast_greedy clustering algorithm.
#' @examples
#' Rscript --vanilla /path/to/file /path/to/output

#cluster methods that could be implemented instead of using fast greedy only
#cluster_edge_betweenness, cluster_fast_greedy, cluster_label_prop
#cluster_leading_eigen, cluster_louvain, cluster_optimal, cluster_spinglass, cluster_walktrap

library('igraph')

args = commandArgs(trailingOnly=TRUE)

if (length(args)< 3) {
  stop("You must provide the path to the file containing the genes links, the method for the clustering and the output file name", call.=FALSE)
}


df <- as.matrix(read.csv(file=args[1],sep=',',skip=1))

g2 <- graph_from_data_frame(df,directed = FALSE)

if (args[2] == "greedy"){
  clusters <- cluster_fast_greedy(g2)
}
if (args[2] == "betweeness"){
  clusters <- cluster_edge_betweenness(g2)
}

write.table(as.matrix(membership(clusters)),file=args[3],col.names=FALSE,sep=',')
