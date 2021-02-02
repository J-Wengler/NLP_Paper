library(tidyverse)
library(ggplot2)

base_path_30 = "/Users/jameswengler/NLP_Paper/code_output/output/text_output/30_keyword_output/"
base_path_20 = "/Users/jameswengler/NLP_Paper/code_output/output/text_output/20_keyword_output/"
base_path_10 = "/Users/jameswengler/NLP_Paper/code_output/output/text_output/10_keyword_output/"
names = c("FastTextCBOWOutput.txt","FastTextSKIPGRAMOutput.txt","FastTextWikiOutput.txt", "SciSpacyOutput.txt", "SpacyOutput.txt")

first_tibble = read_tsv("/Users/jameswengler/NLP_Paper/code_output/output/text_output/30_keyword_output/BioWordVecOutput.txt")
at_100 = filter(first_tibble, N == 100)
all_nums_30 = pull(at_100, SCORE)

for (name in names){
  cur_path = paste0(base_path_30,name)
  temp_tibble = read_tsv(cur_path)
  at_100 = filter(temp_tibble, N == 100)
  all_nums_30 = c(all_nums_30, pull(at_100, SCORE))
}

first_tibble = read_tsv("/Users/jameswengler/NLP_Paper/code_output/output/text_output/30_keyword_output/BioWordVecOutput.txt")
at_100 = filter(first_tibble, N == 100)
all_nums_20 = pull(at_100, SCORE)

for (name in names){
  cur_path = paste0(base_path_20,name)
  temp_tibble = read_tsv(cur_path)
  at_100 = filter(temp_tibble, N == 100)
  all_nums_20 = c(all_nums_20, pull(at_100, SCORE))
}

first_tibble = read_tsv("/Users/jameswengler/NLP_Paper/code_output/output/text_output/30_keyword_output/BioWordVecOutput.txt")
at_100 = filter(first_tibble, N == 100)
all_nums_10 = pull(at_100, SCORE)

for (name in names){
  cur_path = paste0(base_path_10,name)
  temp_tibble = read_tsv(cur_path)
  at_100 = filter(temp_tibble, N == 100)
  all_nums_10 = c(all_nums_10, pull(at_100, SCORE))
  
}
final_tibble = tibble(values = c(all_nums_10, all_nums_20, all_nums_30), labels = c(rep("10 Keywords", length(all_nums_10)), rep("20 Keywords", length(all_nums_20)), rep("30 Keywords", length(all_nums_30))))

ggplot(data = final_tibble, aes(x = values, y = labels)) +
  geom_boxplot() +
  theme_bw(base_size = 18) +
  theme(plot.title = element_text(hjust = 0.5)) +
  geom_jitter() + 
  labs( y = "Number of keywords", x ="Percentage of relevant articles returned", title = "Number of Keywords Extracted vs \nPercentage of Relevant Articles Returned")
  

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