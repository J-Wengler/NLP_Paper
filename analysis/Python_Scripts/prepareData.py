from helper import *


maxCandidateArticles = int(sys.argv[1])
printTimestamp("Getting candidate articles")
candidate_articles = getCandidateArticles(maxCandidateArticles)