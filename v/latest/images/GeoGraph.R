library(tidyverse)
#library(ggplot2)
#library(ggpubr)

setwd("/Users/jameswengler/NLP_Paper/analysis/Data/GEO_Queries")
#setwd("/Users/jameswengler/")
path = "geo_results.txt"

cbbPalette <- c("#b35806", "#e08214", "#fdb863", "#fee0b6", "#de77ae", "#d8daeb", "#b2abd2", "#8073ac", "#542788")
data = read_delim(path, delim="\t", col_names = c("GEO", "Query", "N", "Score"))
data =mutate(data, Score = as.numeric(Score))
data = mutate(data, N = log10(N))
ggplot(data = data, aes(x = N, y = Score, group = Query, color = Query)) +
  geom_line() +
  #xlab("Number retrived (log transformed)") +
  #ylab("% of relevant") +
  labs(title="GEO Performance",
       x ="Number retrived (log transformed))", y = "% of relevant") +
  theme_bw() +
  theme(text = element_text(size=10)) +
  scale_color_brewer(palette= "RdBu")