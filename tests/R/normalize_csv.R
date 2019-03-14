data <- read.table(file = "~/internship-Angers/tests/Syntren/syntrenHop1_20_0_data.csv",sep = "\t")
data <- t(data)
View(data)
data <- data[,-1]

write.table(data, file = "~/internship-Angers/tests/Syntren/syntrenHop2_20_0_data.csv",row.names = FALSE,col.names=FALSE,sep=",")

data2 <- read.table(file = "~/internship-Angers/tests/Syntren/nn20_nbgr0_hop0.1_bionoise0.3_expnoise0.1_corrnoise0.1_neighAdd_network.sif")
data2 <- data2[-2]
a <- "Cause"
b <- "Effect"

add <- cbind(a,b)
colnames(add) <- c("V1", "V3")

data2 <- rbind(add,data2)

write.table(data2, file = "~/internship-Angers/tests/Syntren/syntrenHop2_20_0_target.csv",row.names = FALSE,col.names=FALSE,sep=",")
