#!/usr/bin/python3

# Authors: Dm.Zhelonkin, A.Sokolov

import gensim, logging
import nltk
import itertools
from sklearn.datasets import fetch_20newsgroups
from nltk import word_tokenize
from nltk import WordNetLemmatizer
from gensim.utils import smart_open, simple_preprocess

cats=['sci.space','sci.med','alt.atheism', 'talk.politics.guns', "rec.autos" , "comp.sys.ibm.pc.hardware"]

print("fetching text...")
newsgroups_dataset = fetch_20newsgroups()
correct_format = []

for text in newsgroups_dataset.data:
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    for sentence in tokenizer.tokenize(text):
        tmp=list(gensim.utils.tokenize(sentence, lower=True))
        if len(tmp) != 0:
            # tokenize each message; simply lowercase & match alphabetic chars, for now
            correct_format.append(tmp)

print("making gensym model...")
model = gensim.models.Word2Vec(correct_format, min_count=10, window=3)

print("'earth' - 'moon' + 'pluto':")
print(model.most_similar(positive=['earth','moon'], negative=['pluto']))

print("similarity of 'earth' and 'shuttle:'")
print(model.similarity('earth', 'shuttle'))


print("end")
