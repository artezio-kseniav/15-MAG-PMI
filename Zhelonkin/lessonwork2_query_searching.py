#!/usr/bin/python3

# Written by Sokolov Artem and Zhelonkin Dmitry

import numpy as np
import scipy
import nltk

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import word_tokenize
from nltk import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems
    
def cosine_similarity(vector1, vector2):
    dot_product = sum(p*q for p,q in zip(vector1, vector2))
    magnitude = np.sqrt(sum([val**2 for val in vector1])) * np.sqrt(sum([val**2 for val in vector2]))
    if not magnitude:
        return 0
    return dot_product/magnitude


newsgroups_dataset = fetch_20newsgroups(categories=['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med'])
#newsgroups_dataset = fetch_20newsgroups()


sklearn_tfidf=TfidfVectorizer(stop_words='english',
                                tokenizer=tokenize,
                                 use_idf=True)

sklearn_representation = sklearn_tfidf.fit_transform(newsgroups_dataset.data)

inputString = input("Enter your query:")

query = (inputString,)
tfidf_query = sklearn_tfidf.transform(query)

skl_tfidf_comparisons = []

for count_0, doc_0 in enumerate(sklearn_representation.toarray()):
    for count_1, doc_1 in enumerate(tfidf_query.toarray()):
        skl_tfidf_comparisons.append((cosine_similarity(doc_0, doc_1), newsgroups_dataset.data[count_0].split("\n")[1]))

for x in sorted(skl_tfidf_comparisons, reverse = True)[:10]:
    print (x)

