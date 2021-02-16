from helper import *
import multiprocessing
import sys
import time

numKeywords = int(sys.argv[1])
vectorSize = int(sys.argv[2])
maxCandidateArticles = int(sys.argv[3])

printTimestamp("Getting candidate articles")
candidate_articles = getCandidateArticles(maxCandidateArticles)

printTimestamp("Loading BioWordVec")
model = load_embedding("/Models/concept_model.bin")

start = time.time()

for query in range(1,6):
    for keywordExtractor in ["TopicRank", "TfIdf", "KPMiner", "YAKE", "TextRank", "SingleRank", "TopicalPageRank", "PositionRank", "MultipartiteRank"]:
        mp = multiprocessing.Process(target=findSimilarity, args=(keywordExtractor, "BioWordVec", model, candidate_articles, query, numKeywords, vectorSize))
        mp.start()
        mp.join()

end = time.time()
print('{:.4f} s'.format(end - start))




