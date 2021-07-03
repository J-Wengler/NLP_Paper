library(tidyverse)
library(ggplot2)

base_path_30 = "/Users/jameswengler/NLP_Paper/content/images/30_keyword_output/Text_Output/"
base_path_20 = "/Users/jameswengler/NLP_Paper/content/images/20_keyword_output/Text_Output/"
base_path_10 = "/Users/jameswengler/NLP_Paper/content/images/10_keyword_output/Text_Output/"
names = c("BioWordVecOutput.txt","FTCBOWOutput.txt","FTSkipGramOutput.txt", "FTWikiOutput.txt", "SciSpaCyOutput.txt", "SpaCyOutput.txt")

first_tibble = read_delim("/Users/jameswengler/NLP_Paper/content/images/30_keyword_output/Text_Output/30_BioWordVecOutput.txt", delim = "\t", skip = 2, col_names = c('Model', 'Query', 'Number', 'Score' ))
at_100 = filter(first_tibble, Number == 100)
all_nums_30 = pull(at_100, Score)

for (name in names){
  cur_path = paste0(base_path_30,"30_",name)
  print(cur_path)
  temp_tibble = read_delim(cur_path, delim = "\t", skip = 2, col_names = c('Model', 'Query', 'Number', 'Score' ))
  at_100 = filter(temp_tibble, Number == 100)
  all_nums_30 = c(all_nums_30, pull(at_100, Score))
}

first_tibble = read_delim("/Users/jameswengler/NLP_Paper/content/images/20_keyword_output/Text_Output/20_BioWordVecOutput.txt", delim = "\t", skip = 2, col_names = c('Model', 'Query', 'Number', 'Score' ))
at_100 = filter(first_tibble, Number == 100)
all_nums_20 = pull(at_100, Score)

for (name in names){
  cur_path = paste0(base_path_20,"20_",name)
  temp_tibble = read_delim(cur_path, delim = "\t", skip = 2, col_names = c('Model', 'Query', 'Number', 'Score' ))
  at_100 = filter(temp_tibble, Number == 100)
  all_nums_20 = c(all_nums_20, pull(at_100, Score))
}

first_tibble = read_delim("/Users/jameswengler/NLP_Paper/content/images/10_keyword_output/Text_Output/10_BioWordVecOutput.txt", delim = "\t", skip = 2, col_names = c('Model', 'Query', 'Number', 'Score' ))
at_100 = filter(first_tibble, Number == 100)
all_nums_10 = pull(at_100, Score)

for (name in names){
  cur_path = paste0(base_path_10,"10_",name)
  temp_tibble = read_delim(cur_path, delim = "\t", skip = 2, col_names = c('Model', 'Query', 'Number', 'Score' ))
  at_100 = filter(temp_tibble, Number == 100)
  all_nums_10 = c(all_nums_10, pull(at_100, Score))
  
}
final_tibble = tibble(values = c(all_nums_10, all_nums_20, all_nums_30), labels = c(rep("10 Keywords", length(all_nums_10)), rep("20 Keywords", length(all_nums_20)), rep("30 Keywords", length(all_nums_30))))

wilcox.test(all_nums_10, all_nums_20)
wilcox.test(all_nums_10, all_nums_30)
wilcox.test(all_nums_20, all_nums_30)

sum_plot = ggplot(data = final_tibble, aes(x = values, y = labels)) +
  geom_boxplot() +
  theme_bw(base_size = 18) +
  theme(plot.title = element_text(hjust = 0.5)) +
  geom_jitter() + 
  labs( y = "Number of keywords", x ="Percentage of relevant articles returned", title = "Number of Keywords Extracted vs \nPercentage of Relevant \nArticles Returned")
  
ggsave(filename="/Users/jameswengler/NLP_Paper/content/images/summaryGraph.png"
       , plot = sum_plot, height = 6.5, width = 6.5)
ggsave(filename="/Users/jameswengler/NLP_Paper/content/images/summaryGraph.pdf"
       , plot = sum_plot, height = 6.5, width = 6.5)
#ggplot(data = data.frame(all_nums_10), aes(x = 10,20, y = all_nums_10, all_nums_20))+
#  geom_boxplot() +
#  geom_boxplot(aes(x = "", y = all_nums_30))
# 
# boxplot(all_nums_10, all_nums_20, all_nums_30,
#         main = "Number of Keywords Extracted\n vs \nPercentage of Relevant Articles Returned",
#         names = c("10", "20", "30"),
#         las = 2,
#         border = "brown",
#         horizontal = TRUE,
#         notch = FALSE, 
#         add.points = TRUE,
#         sub = "All Analysis Done at 100 Articles "
# )