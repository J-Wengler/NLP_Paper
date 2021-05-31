from helper import *

resultPath = ["MultipartitieRank", "PositionRank", "SingleRank", "TFIDF", "TextRank", "TopicalRank", "YAKE", "KPMINER", "TopicRankResults"]
models = ["FastTextSkipGram", "FastTextCBOW", "FastTextWiki", "BIOWORDVEC", "SpacyWebLG", "SciSpacy"]
numKeywords = [10,20,30]
bestCombo = open('/home/jwengler/NLP_Paper/analysis/Data/Results/bestCombo.txt', 'w+')

for model in models:
    for numKeyword in numKeywords:
        generateResults(resultPath, model, bestCombo, numKeyword)

