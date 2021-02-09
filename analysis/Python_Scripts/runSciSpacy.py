import fasttext
from helper import *
import multiprocessing
import os
import scispacy
import spacy
import sys
import time
import wikipedia

numKeywords = int(sys.argv[1])
vectorSize = int(sys.argv[2])
maxCandidateArticles = int(sys.argv[3])

printTimestamp("Getting candidate articles")
candidate_articles = getCandidateArticles(maxCandidateArticles)

printTimestamp("Loading SciSpacy")
model = spacy.load("en_ner_bc5cdr_md")

#findSimilarity("TopicRank", "ScispaCy", model, candidate_articles, 1, numKeywords, vectorSize)
#sys.exit()

start = time.time()

for query in range(1,6):
    for keywordExtractor in ["TopicRank", "TfIdf", "KPMiner", "YAKE", "TextRank", "SingleRank", "TopicalPageRank", "PositionRank", "MultipartiteRank"]:
        mp = multiprocessing.Process(target=findSimilarity, args=(keywordExtractor, "ScispaCy", model, candidate_articles, query, numKeywords, vectorSize))
        mp.start()
        mp.join()

end = time.time()
print('{:.4f} s'.format(end - start))
