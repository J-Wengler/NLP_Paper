from bs4 import BeautifulSoup
import datetime
import json
import numpy as np
import os
from pathlib import Path
import pke
import re
import requests
from scipy.spatial.distance import cosine
from gensim.models.fasttext import FastText as FT_gensim
from tester import tester
import math

def printTimestamp(message):
    print(f"{message} - {datetime.datetime.now()}")

def cleanText(text):
    text = BeautifulSoup(text, "lxml").text
    text = re.sub(r'\W', ' ', str(text))
    text = re.sub(r'\s+[a-zA-Z]\s+', ' ', text)
    text = re.sub(r'\^[a-zA-Z]\s+', ' ', text)
    text = re.sub(r'\s+', ' ', text, flags=re.I)
    text = re.sub(r'^b\s+', '', text)
    text = text.lower()
    text = re.sub(r'\|\|\|', r' ', text)
    text = re.sub(r'http\S+', r'<URL>', text)
    text = text.lower()
    text = text.replace('x', '')
    text = text.replace(',', ' ')
    text = re.sub('\n', ' ', text)
    text = re.sub('[n|N]o\.', 'number', text)

    return text

def getCandidateArticles(limit):
    cacheFilePath = f"/Data/CandidateArticles_{limit}.json"
    series_to_summary = {}

    if os.path.exists(cacheFilePath):
        with open(cacheFilePath) as cacheFile:
            series_to_summary = json.loads(cacheFile.read())
    else:
        rq = requests.get(f'http://stargeo.org/api/v2/series/?limit={limit}').json()

        for row in rq['results']:
            temp_dict = row['attrs']
            name = row['gse_name']
            summary = temp_dict['summary']
            title = temp_dict['title']

            full_text = summary + title
            full_text = cleanText(full_text)
            series_to_summary[name] = full_text

        with open(cacheFilePath, 'w') as cacheFile:
            cacheFile.write(json.dumps(series_to_summary))

    return series_to_summary

def getNamesToQuery(queryNumber):
    filePath = f'/Data/Queries/q{queryNumber}/names_to_query.txt'

    files = []

    with open(filePath, 'r+') as in_file:
        for line in in_file:
            names = line.split(' ')
            for name in names:
                files.append(name.upper().strip())

    return (files[0:len(files)-1])

def getKeywordEmbedding(keywords, model, numWords, vectorSize, failedFilePath, modelName):
    doc_vec = np.zeros((vectorSize,))
    #This will throw an error later in the program unless the default model option is changed to match the vector size
    #FastTextWiki is locked into 300 dimensions
    #BioWordVec is locked into 200 dimensions
    #Currently both the FastTextCBOW and FastTextSkipgram we trained with 300 dimensions. To change this we would have
    # to edit the trainFastTextSKIPGRAM.py script
    #Spacy and SciSpacy have a .resize function that would allow them to resize their default vectors (300)
    #Maybe we could trick spaCy into resizing the BioWordVec vectors?

    with open(failedFilePath, 'a+') as failed_file:
        for i, word in enumerate(keywords):
            if type(word) is tuple:
                word = word[0]

            word_list = word.split()
            if len(word_list) > 1:
                new_vec = getKeywordEmbedding(word_list, model, numWords, vectorSize, failedFilePath, modelName)
                if new_vec is not None:
                    numWords += 1
                    doc_vec = np.add(doc_vec, new_vec)
            else:
                error = False
                if(modelName == "SciSpaCy" or modelName == "SpaCy"):
                    try:
                        new_vec = model.vocab[word_list[0]].vector
                    except KeyError or ValueError:
                        failed_file.write(word_list[0])
                        error = True
                        break
                else:
                    try:
                        new_vec = model[word_list[0]]
                    except KeyError or ValueError:
                        failed_file.write(word_list[0])
                        error = True
                        break
                if new_vec is not None and error is False:
                    numWords += 1
                    doc_vec = np.add(doc_vec, new_vec)

        if (numWords != 0):
            doc_vec = doc_vec / numWords

        return doc_vec

def findSimilarity(keyphraseExtractor, modelName, model, candidateArticles, query, numKeywords, vectorSize):
    resultsDirPath = f"/Data/Results/{modelName}/q{query}/{keyphraseExtractor}/{numKeywords}"
    Path(resultsDirPath).mkdir(parents=True, exist_ok=True)

    failedFilePath = f'{resultsDirPath}/failed_words.txt'
    if os.path.exists(failedFilePath):
        os.remove(failedFilePath)

    with open(f'{resultsDirPath}/similarity.txt', 'w+') as out_file:
        embeddings = []
        sim_to_name = {}

        printTimestamp(f"Processed query articles for q{query}, {keyphraseExtractor}, {numKeywords} keywords")
        for queryFileName in getNamesToQuery(query):
            method = getKeyphraseExtractor(keyphraseExtractor)
            method.load_document(input=f'/Data/Queries/q{query}/{queryFileName}.txt', language='en')
            method.candidate_selection()
            method.candidate_weighting()

            keyphrases = method.get_n_best(n=numKeywords)
            embeddings.append(getKeywordEmbedding(keyphrases, model, 0, vectorSize, failedFilePath, modelName))

        for i, article in enumerate(candidateArticles):
            #if i % 1000 == 0:
            if i % 2 == 0:
                printTimestamp(f"Processed {i} candidate articles for q{query}, {keyphraseExtractor}, {numKeywords} keywords")
                if i > 0:
                    break

            method = getKeyphraseExtractor(keyphraseExtractor)
            method.load_document(input=candidateArticles[article], language='en')
            method.candidate_selection()

            error = False

            try:
                method.candidate_weighting()
            except ValueError:
                print("Method was unable to find keyphrases for identification. Setting similarity to 0%")
                sim_to_name[article] = 0
                error = True

            if not error:
                keyphrases = method.get_n_best(n=numKeywords)
                cur_vec = getKeywordEmbedding(keyphrases, model, 0, vectorSize, failedFilePath, keyphraseExtractor, modelName)
                avg_sim = 0
                num_embeddings = 0

                for f in embeddings:
                    sim = 1 - cosine(cur_vec, f)
                    avg_sim += sim
                    num_embeddings += 1

                sim_to_name[article] = avg_sim / num_embeddings

        for name in sim_to_name:
            out_file.write("{}\t{}\n".format(name, sim_to_name[name]))

def trainFastTextModel(vectorSize, trainingModel):
    model = FT_gensim(size=vectorSize)
    model.build_vocab(corpus_file='Data/starGEO.txt')
    model.train(
        corpus_file='Data/starGEO.txt', epochs=model.epochs, model=trainingModel,
        total_examples=model.corpus_count, total_words=model.corpus_total_words
    )
    return model

def findAvgPercent(series_to_score):
    avg_per = 0
    num_keys = 0
    for key in series_to_score:
        if series_to_score[key] != '':
            temp_per = float(series_to_score[key])
            if(math.isnan(temp_per) is False):
                avg_per += float(series_to_score[key])
            num_keys += 1
    avg_to_return = avg_per / num_keys
    return avg_to_return

def getXTopResults(x, series_to_score):
    copy_of_keys = series_to_score.keys()
    sorted_keys = sorted(copy_of_keys, reverse = True)
    to_return = []
    if len(sorted_keys) < 100:
        return [0,0,0,0,0]
    else:
        for per in range(0,x):
            to_return.append(series_to_score[sorted_keys[per]])

        return to_return

def getScore(filePath):
    score_to_series = {}
    with open(filePath, "r+") as in_file:
        for line in in_file:
            line_list = line.split('-')
            try:
                score_to_series[line_list[1].strip()] = line_list[0].strip()
            except:
                print("Line List : {}".format(line_list))
                print("Error was found in {}".format(filePath))
    scores = []
    toTest = [1,10,100,1000,10000]
    for topNum in toTest:
        topResults = getXTopResults(topNum, score_to_series)
        myTester = tester()
        filePathList = filePath.split('/')
        queryNum = int(filePathList[4][0])
        myTester.whichQuery(queryNum)
        score = myTester.returnPercent(topResults)
        scores.append(score)
    return scores

def generateResults (resultPath, modelName, bestCombo):
    outputFile = open('/Results/{}}Output.txt'.format(modelName), 'w+')
    outputFile.write("{} Results\n".format(modelName))
    outputFile.write("MODEL\tQUERY\t#\tSCORE\n")
    for name in resultPath:
        path = "/Results/{}}/{}".format( modelName,name)
        top_nums = [1, 10, 100, 1000, 10000]
        for fileName in os.listdir(path):
            scores = getScore(path + "/" + fileName)
            for i, score in enumerate(scores):
                query = fileName[0]
                if (top_nums[i] == 100):
                    bestCombo.write("{}}\t{}\t{}\t{}\t{}\n".format(modelName, str(name).strip(), str(query).strip(), str(top_nums[i]).strip(), str(score).strip()))
                strForFile = "{}\t{}\t{}\t{}\n".format(str(name).strip(), str(query).strip(), str(top_nums[i]).strip(), str(score).strip())
                outputFile.write(strForFile)

def evaluateGEO():
    path_to_GEO_queries = "/Data/GEO_Queries/"
    path_to_queries = "/Data/Queries/"

    geo_results = []
    query_results = []

    query_list = ["q1_metastasis+brain_GEO.txt", "q2_sars_GEO.txt", "q3_h1n1+infection+mouse+lethal_GEO.txt",
                  "q4_acute_leukemia+mll+progression_GEO.txt", "q5_BRCA+Cancer_GEO.txt",
                  "q6_heart_development+age+failure_GEO.txt"]

    starGEO_datasets = (getCandidateArticles(100000)).keys()

    resultsDirPath = f"/Data/GEO_Queries/geo_results.txt"
    with open(resultsDirPath, 'w+') as out_file:
        for top_n in [1,10,100,500]:
            for path in query_list:
                with open(path_to_GEO_queries + path, 'r') as geo_file:
                    for line in geo_file:
                        if line.startswith("Series"):
                            split_sent = line.split()
                            if split_sent[2] in starGEO_datasets:
                                geo_results.append(split_sent[2])

                with open(path_to_queries + f"q{path[1]}/names.txt", 'r') as query_file:
                    for line in query_file:
                        query_results = line.split()

                num_relevant = 0
                for series in geo_results[:top_n]:
                    if series in query_results:
                        num_relevant = num_relevant + 1

                out_file.write(f"q{path[1]} returned {num_relevant} ({round((num_relevant/len(query_results)) * 100)}%) in {top_n}\n")
    print("Finished GEO evaluation")

# We could do this dynamically, but this is okay.
def getKeyphraseExtractor(name):
    if name == "TopicRank":
        return pke.unsupervised.TopicRank()
    if name == "TfIdf":
        return pke.unsupervised.TfIdf()
    if name == "KPMiner":
        return pke.unsupervised.KPMiner()
    if name == "YAKE":
        return pke.unsupervised.YAKE()
    if name == "TextRank":
        return pke.unsupervised.TextRank()
    if name == "SingleRank":
        return pke.unsupervised.SingleRank()
    if name == "TopicalPageRank":
        return pke.unsupervised.TopicalPageRank()
    if name == "PositionRank":
        return pke.unsupervised.PositionRank()
    if name == "MultipartiteRank":
        return pke.unsupervised.MultipartiteRank()
