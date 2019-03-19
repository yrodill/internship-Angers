library(WGCNA)
options(stringsAsFactors = FALSE);
#enableWGCNAThreads()

df <- as.matrix(read.table("~/internship-Angers/tests/benchmark/genie3_syntren/syntrenHop2_20_0_data.csv" ,sep=",",header=FALSE) ) # tab-delimited data
gene.names=rownames(df)
SubGeneNames=gene.names[1:n]
df <- df[-1,]
df <- as.matrix(apply(df,c(1,2),as.numeric))
adj= adjacency(df,type = "unsigned", power = 7);

TOM=TOMsimilarityFromExpr(df,networkType = "unsigned", TOMType = "unsigned", power = 7)

dissTOM=1-TOM
library(flashClust)
geneTree = flashClust(as.dist(dissTOM),method="average")

plot(geneTree, xlab="", sub="",cex=0.3)
