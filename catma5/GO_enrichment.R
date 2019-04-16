library(igraph)
#library(EGAD)
library(data.table)
library(parallel)
library(reshape2)
library(Matrix)

run_GBA <- function(network, labels, min = 20, max = 1000, nfold = 3) {
  
  m <- match(rownames(network), rownames(labels))
  f <- !is.na(m)
  g <- m[f]
  
  network.sub <- network[f, f]
  genes.labels <- filter_network_cols(labels[g, ], min, max)
  
  roc.sub <- neighbor_voting(genes.labels, network.sub, nfold)
  genes <- predictions(genes.labels, network.sub)
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



df <- as.matrix(read.csv(file="/home/bothorel/internship-Angers/catma5/biological_results/ISample/all/list_link_all_5000_0.05.csv"))
g <- simplify(graph_from_data_frame(df,directed=F))
vertex.number<-length(V(g)$name)
edge.number<-length(E(g))
mean.degree<-mean(degree(g))

agrigo<-read.table("/home/bothorel/internship-Angers/catma5/data/GOagri_term_Arabidopsis_thaliana", sep="", header=F)
#agrigo<-read.csv("/home/bothorel/internship-Angers/GOSlim/ATH_GO_normalized.csv", sep="\t")

agrigo<-subset(agrigo, agrigo[,2] %in% V(g)$name)
GO.eff<-table(agrigo[,3])
GO.eff<-names(which(GO.eff>2 & GO.eff<501))
agrigo<-droplevels(subset(agrigo, agrigo[,3] %in% GO.eff))


goterms<-names(table(agrigo[,3]))
go.list<-vector(mode="list", length(goterms))
names(go.list)<-goterms
for (i in goterms){
  tmp<-subset(agrigo, agrigo[,3]==i)
  go.list[[i]]<-t(combn(as.vector(tmp[,2]),2))
}

go.table<-do.call("rbind", go.list)
go.tag<-unlist(lapply(go.list, nrow))
genome.effectif<-go.tag
go.tag<-unlist(sapply(1:length(go.tag), function(x)rep(names(go.tag)[x],go.tag[x])))
go.table<-cbind.data.frame(go.table,go.tag)
go.table<-rbind(cbind(paste(go.table[,1], go.table[,2], sep="_"), as.vector(go.table[,3])), cbind(paste(go.table[,2], go.table[,1], sep="_"),  as.vector(go.table[,3])))


#GO enrichment
universe=choose(length(table(agrigo[,2])),2)
g.edgelist<-as_edgelist(g)
g.edgelist<-paste(g.edgelist[,1], g.edgelist[,2], sep="_")
go.table.local<-subset(go.table, go.table[,1] %in% g.edgelist)
table.hyper<-cbind(table(go.table.local[,2]), table(go.table[,2])[names(table(go.table.local[,2]))]/2)
k<-length(E(g))
pval<-apply(table.hyper, 1, function(x){
  q<-as.numeric(x[1])
  m<-as.numeric(x[2])
  n<- universe - m
  phyper(q, m, n, k, lower.tail=F)
})

pvaladjust<-p.adjust(pval, method="BH")
go.list.table<-cbind(table.hyper, pvaladjust)
go.list.table<-go.list.table[go.list.table[,3]<0.05,,drop=F]
number.enriched.go.global<-nrow(go.list.table)


#AUROC
g.go<-simplify(graph_from_data_frame(agrigo[,2:3], directed=F))
go.table.auroc<-as_adjacency_matrix(g.go)
go.table.auroc<-as.matrix(go.table.auroc[grep("GO:", colnames(go.table.auroc), invert=T),grep("GO:", colnames(go.table.auroc))])
cs.go<-colSums(go.table.auroc)
go.table.auroc<-go.table.auroc[,cs.go>2 & cs.go<301]
go.table.auroc<-as(go.table.auroc, "sparseMatrix")


mat.adj<-as_adjacency_matrix(g)
mat.adj<-mat.adj[rownames(go.table.auroc), rownames(go.table.auroc)]
GO_groups_voted <-run_GBA(mat.adj, go.table.auroc, min=20, max=1000)
auroc_network<-GO_groups_voted[[3]]
auroc_degree<-mean(GO_groups_voted[[1]][,3])
#print(GO_groups_voted[[1]][,3])

par(mfrow=c(2,1))
plot(g, edge.arrow.size=.2,vertex.size=2,vertex.label=NA,edge.width=0.2)
plot(g.go, edge.arrow.size=.2,vertex.size=2,vertex.label=NA,edge.width=0.2)
