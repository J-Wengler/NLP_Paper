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
                #Here we'll need a if/else statement that will allow the usage of different syntax for each model
                # Spacy = model.vocab[word_list[0]].vector
                # FastText = = model[word_list[0]
                # This are the only two syntax changes we'll need
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
    model.build_vocab(corpus_file='Models/starGEO.txt')
    model.train(
        corpus_file='Models/starGEO.txt', epochs=model.epochs, model=trainingModel,
        total_examples=model.corpus_count, total_words=model.corpus_total_words
    )
    return model
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
