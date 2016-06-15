from __future__ import print_function

from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn import metrics
from sklearn.externals import joblib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from matplotlib import colors

from sklearn.cluster import KMeans, MiniBatchKMeans
import logging
from optparse import OptionParser
import sys
from time import time

import numpy as np


# Load some categories from the training set
categories = [
    'alt.atheism',
    'talk.religion.misc',
    'comp.graphics',
    'sci.space',
]
# Uncomment the following to do the analysis on all the categories
#categories = None

print("Loading 20 newsgroups dataset for categories:")
print(categories)

dataset = fetch_20newsgroups(subset='all', categories=categories,
                             shuffle=True, random_state=42)

print("%d documents" % len(dataset.data))
print("%d categories" % len(dataset.target_names))
print()

labels = dataset.target
true_k = np.unique(labels).shape[0]
print ('k'), (true_k)

#define vectorizer parameters
tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.2, stop_words='english',
                                 use_idf=True)

tfidf_matrix = tfidf_vectorizer.fit_transform(dataset.data) #fit the vectorizer to synopses
print (tfidf_matrix.shape)
#print (len(dataset.data))
num_clusters = 20

km = KMeans(n_clusters=num_clusters).fit(tfidf_matrix)

#time km.fit(tfidf_matrix)

clusters = km.labels_.tolist()
print (len(clusters))

svd2 = TruncatedSVD(2).fit_transform(tfidf_matrix)
#print (svd2[1,1])
print ('class')
#print (clusters[0])
print (km.labels_)
COLOR=['green','red','blue','black','yellow','grey', 'cyan','orange_4a','dark_olive_green_3b','dark_slate_gray_3',
       ' medium_orchid_3','misty_rose_3','indian_red_1c','chartreuse_1 ','aquamarine_3','medium_purple_3a',
       'light_slate_blue','sky_blue_1','chartreuse_1','deep_pink_4c']
col_map=dict(zip(set(km.labels_),COLOR))
label_color = [col_map[l] for l in labels]
print ('colours')
#print (len(label_color))
for i in range(0, svd2.shape[0]):
    plt.scatter(svd2[i,0], svd2[i,1], c=label_color[i])
plt.show()
