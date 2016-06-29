from sklearn.datasets import fetch_20newsgroups
import numpy as np
import nltk
from pprint import pprint
from collections import defaultdict
import string
import gensim


newsgroups = fetch_20newsgroups(categories=['comp.graphics',
                                            'comp.os.ms-windows.misc',
                                            'comp.sys.ibm.pc.hardware',
                                            'comp.sys.mac.hardware',
                                            'comp.windows.x',
                                            'rec.autos',
                                            'rec.motorcycles',
                                            'rec.sport.baseball',
                                            'rec.sport.hockey',
                                            'sci.electronics',
                                            'sci.space', ],
                                subset='all', shuffle=True, random_state=1)

pprint(list(newsgroups.target_names))

print("%d documents" % len(newsgroups.data))
print("%d categories" % len(newsgroups.target_names))

newsgroups_tokenized = [nltk.word_tokenize(text) for text in newsgroups.data]

news_corpus = []
for text in newsgroups_tokenized:
    lemms = []
    for word in text:
        if word not in string.punctuation:
            lemms.append(word.lower())
    news_corpus.append(lemms)

news_model = gensim.models.Word2Vec(news_corpus)
print(news_model['car'], '\n')
print('Vector dimension: ', len(news_model['car']))

news_model.similarity('windows', 'mac')

news_model.similarity('car', 'motorcycle')

news_model.similarity('baseball', 'hockey')

news_model.doesnt_match(['car', 'motorcycle', 'bicycle'])

news_model.doesnt_match(['baseball', 'hockey', 'telephone', 'basketball', 'athletics'])

news_model.doesnt_match(['earth', 'jupyter', 'mars', 'sun'])

news_model.most_similar(positive=['man', 'crown'])

news_model.most_similar(positive=['earth', 'pluto', 'mars'], negative=['planet'])

news_model.most_similar(positive=['seat', 'wheels', 'steer'])
