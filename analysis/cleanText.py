import pke 
import fasttext
from bs4 import BeautifulSoup
import os
from nltk.tokenize import word_tokenize
import numpy as np
from sklearn.decomposition import PCA 
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import cosine
import io
import wikipedia
from nltk.stem import WordNetLemmatizer
import nltk
import matplotlib.pyplot as plt 
from TextRank import TextRank4Keyword
import pke 
import os
import requests
from gensim.models import KeyedVectors
import pandas as pd
import re
from joblib import Parallel, delayed
import time
import multiprocessing
from multiprocessing import Pool


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


sample_text = "	We obtained peripheral blood samples for women from Utah (USA) and Ontario (Canada) who had a family history of breast cancer (or did not), who carried a BRCA1/2 mutation (or did not), and who had developed breast cancer (or had not). We classified the women into two groups: [1] those who had a family history of breast cancer (irrespective of BRCA1/2 mutation status) and had developed an early-onset breast tumor and [2] those who had a family history of breast cancer but had not developed a breast tumor or who did not have a family history of breast cancer (some of whom had developed sporadic breast cancer and and others who had not). We then used machine-learning methods to assess how well we could classify these women into either group. The Utah samples served as a training set, and the Ontario samples served as an independent validation set from a geographically distinct population."
print("RAW TEXT : {}\n\n\n".format(sample_text))
print("CLEANED TEXT : {}\n".format(cleanText(sample_text)))
