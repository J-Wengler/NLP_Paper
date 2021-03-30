library(tidyverse)
#library(ggplot2)
#library(ggpubr)

#setwd("/Users/jameswengler/NLP_Paper/analysis/Data/GEO_Queries")
setwd("/Users/jameswengler/")
path = "geo_results.txt"

data = read_delim(path, delim=" ")