from helper import *
import sys

maxCandidateArticles = int(sys.argv[1])
printTimestamp("Getting candidate articles")
candidate_articles = getCandidateArticles(maxCandidateArticles)
