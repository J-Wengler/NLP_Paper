from helper import *

resultPath = ["MultipartitieRank", "PositionRank", "SingleRank", "TFIDF", "TextRank", "TopicalRank", "YAKE", "KPMINER", "TopicRankResults"]
models = ["FastTextSkipGram", "FastTextCBOW", "FastTextWiki", "BIOWORDVEC", "SpacyWebLG", "SciSpacy"]
bestCombo = open('/Models/bestCombo.txt', 'w+')

for model in models:
    generateResults(resultPath, model, bestCombo)

