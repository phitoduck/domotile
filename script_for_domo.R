# install domo package
args <- commandArgs(trailingOnly=TRUE) # get arguments
setwd(args[1])

data <- read.csv(args[2], header=T)
# output.csv <- output.csv[c(2,3,4,5,6)]
data$Peak.Year <- data$Peak.Year + 10
write.table(data, file=args[3], row.names=FALSE, sep=",", col.names=FALSE, quote=FALSE, append=FALSE)