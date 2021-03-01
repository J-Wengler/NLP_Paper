library(tibble)
library(ggplot2)
library(ggpubr)

cleanTibble = function(myTib){
   myTib = mutate(myTib, scores = as.numeric(scores))
   query1 = mutate(myTib, numbers = log10(as.numeric(numbers)))
   myTib$Models[myTib$Models=="TFIDF"] <- "TF-IDF"
   myTib$Models[myTib$Models=="KPMINER"] <- "KP-Miner"
   myTib$Models[myTib$Models=="MultipartitieRank"] <- "MultipartiteRank"
   myTib$Models[myTib$Models=="TopicalPageRank"] <- "TopicalRank"
   myTib$Models[myTib$Models=="TopicRankResults"] <- "TopicRank"
   return(myTib)
}

makePlot = function(query){
   cbbPalette <- c("#b35806", "#e08214", "#fdb863", "#fee0b6", "#de77ae", "#d8daeb", "#b2abd2", "#8073ac", "#542788")
   query =  mutate(query, scores = as.numeric(scores))
   query = mutate(query, numbers = as.numeric(numbers))
   print(query)
   tempPlot = ggplot(data = query, aes(x = numbers, y = scores, color = Models)) +
      ylim(0,1) +
      geom_line() +
      geom_point() +
      xlab("Number retrived ") +
      ylab("% of relevant") +
      theme_bw() +
      theme(text = element_text(size=10)) +
      scale_x_log10() +
      scale_colour_manual(values=cbbPalette)
   return(tempPlot)
   
}

#Change me to the appropriate keyword output
setwd("~/NLP_Paper/code/output/text_output/30_keyword_output")

#Change to the specific 
path = "SpacyOutput.txt"

#Change to the title on the graph
title = "Spacy"

data = read_delim(path, delim = "\t", skip = 2, col_names = c('Model', 'Query', 'Number', 'Score' ))

Models = pull(data, Model)
queries = as.numeric(pull(data, Query))
numbers = as.numeric(pull(data, Number))
scores = as.numeric(pull(data, Score))

clean_data = as_tibble(cbind(Models, queries, numbers, scores))

query1 = filter(clean_data, queries == "1")
query2 = filter(clean_data, queries == "2")
query3 = filter(clean_data, queries == "3")
query4 = filter(clean_data, queries == "4")
query5 = filter(clean_data, queries == "5")

query1 = cleanTibble(query1)
query2 = cleanTibble(query2)
query3 = cleanTibble(query3)
query4 = cleanTibble(query4)
query5 = cleanTibble(query5)

g1 = makePlot(query1)
g2 = makePlot(query2)
g3 = makePlot(query3)
g4 = makePlot(query4)
g5 = makePlot(query5)

figure = ggarrange(g1, g2, g3, g4, g5,
                   labels = c("Q1 ", "Q2", "Q3", "Q4", "Q5"),
                   common.legend = TRUE,
                   hjust = 0,
                   ncol = 2, nrow = 3)

figure = annotate_figure(figure,top = text_grob(title, color = "blue", size = 18))
ggsave(filename="/Users/jameswengler/SpacyOutput.png", plot = figure, height = 6.5, width = 6.5)
ggsave(filename="/Users/jameswengler/SpacyOutput.pdf", plot = figure, height = 6.5, width = 6.5)

