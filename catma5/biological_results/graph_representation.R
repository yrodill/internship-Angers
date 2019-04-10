df <- as.matrix(read.csv(file="/home/bothorel/internship-Angers/catma5/biological_results/Ratio/all/list_link_all_1000_0.05.csv"))

library('igraph')
g <- graph_from_data_frame(df,directed = TRUE)
g2 <- graph_from_data_frame(df,directed = FALSE)

net.bg <- sample_pa(1000)
l <- layout_with_fr(net.bg)
plot(g, edge.arrow.size=.4,vertex.size=2,layout=l,vertex.label=NA)

plot(g2, edge.arrow.size=.2,vertex.size=2,layout=l,vertex.label=NA,edge.width=0.2)


g_clust <- cluster_louvain(g2)

g_greed <- cluster_fast_greedy(g2)

g_eigen <- cluster_leading_eigen(g2)

plot(g_greed,g2,edge.arrow.size=.2,vertex.size=2,vertex.label=NA,edge.width=0.2)

par(mfrow=c(2,1))
plot(g_greed, g2, col = membership(g_greed),mark.groups = communities(g_greed),edge.arrow.size=.2,vertex.size=2,vertex.label=NA,edge.width=0.2)

plot(g_clust, g2, col = membership(g_greed),mark.groups = communities(g_greed),edge.arrow.size=.2,vertex.size=2,vertex.label=NA,edge.width=0.2)

plot(g_eigen, g2, col = membership(g_greed),mark.groups = communities(g_greed),edge.arrow.size=.2,vertex.size=2,vertex.label=NA,edge.width=0.2)

#as.dendrogram(g_clust, hang = -1,use.modularity = FALSE)
#as.hclust(g_clust)

modularity(g_clust)
modularity(g_greed)

for(i in 1:412){
  print(g_clust[i])
}