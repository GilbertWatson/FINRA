# set working directory
setwd("C:/Users/gwatson/Desktop/")

# load packages
library(rjson)
library(plyr)

# load data from python script
BigDataTables <- fromJSON(file = "BigDataTables.json")
DetailDataTables <- fromJSON(file = "DetailDataTables.json")

# function to turn javascript dates in to POSIXct dates
removeJavascript <- function(text) {
  return(as.POSIXct(as.numeric(gsub(")/","",
                         gsub(pattern = "/Date(", 
                              replacement = "", 
                              text, fixed = T),
                         fixed=T))/1000,origin="1970-01-01"))
}

# clean up BigDataTables
BDT <- lapply(X = BigDataTables, FUN = function(x) {
  x <- as.data.frame(x, stringsAsFactors = F)
  return(x)
})
BDT <- rbind.fill(BDT)
BDT <- mutate(BDT, 
              LatestUpdatedDate = removeJavascript(LatestUpdatedDate),
              WeeklyReportDate = removeJavascript(WeeklyReportDate),
              TradeLastUpdatedDate = removeJavascript(TradeLastUpdatedDate),
              LastUpdatedDate = removeJavascript(LastUpdatedDate),
              ShareLastUpdatedDate = removeJavascript(ShareLastUpdatedDate))

# clean up DetailDataTables
DDT <- lapply(X = DetailDataTables, FUN = function(x) {
  x <- x$TradingDetails
  x <- lapply(X = x, FUN = function(x) {
    x <- as.data.frame(x, stringsAsFactors = F)
    return(x)
  })
  return(x)
})
DDT <- lapply(X = DDT, FUN = function(x) {
  return(rbind.fill(x))
})
DDT <- rbind.fill(DDT)
DDT <- mutate(DDT, 
              WeeklyReportDate = removeJavascript(WeeklyReportDate),
              TradeLastUpdatedDate = removeJavascript(TradeLastUpdatedDate),
              LastUpdatedDate = removeJavascript(LastUpdatedDate),
              ShareLastUpdatedDate = removeJavascript(ShareLastUpdatedDate))

# write data files to csv
write.csv(BDT, "BigDataTables.csv", row.names=F)
write.csv(DDT, "DetailDataTables.csv", row.names=F)
