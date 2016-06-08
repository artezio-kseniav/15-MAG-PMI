#*- coding: utf-8 -*
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import TruncatedSVD
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.cross_validation import train_test_split
from sklearn.feature_selection import chi2, SelectKBest
import matplotlib.pyplot as plt
import pandas as pd
import math
import re
import enchant

dataset = fetch_20newsgroups(categories = ['alt.atheism', 'comp.graphics', 'comp.os.ms-windows.misc'])
labels = dataset.target
texts = dataset.data
tfidf = TfidfVectorizer()
X = tfidf.fit_transform(texts)
print(X)
svd = TruncatedSVD(n_components=3)
th = svd.fit_transform(X)
ph = svd.components_

print(th.shape)
print(ph)

X_train, X_test, Y_tain, Y_test = train_test_split (th, labels, test_size=0,3, random_state=10)
clf = SVC(probability=True, kernel = 'linear')
clf.fit(X_train, Y_tain)
y_hat = clf.predict(X_test)

print(classification_report(Y_test, y_hat)

most_popular_words = []
for theme in range(words.shape[0]):
    most_popular_words.append([tfidf.get_feature_names()[words[theme, :].argsort()[i]] for i in range(-1, -6, -1)])
    print(theme, most_popular_words[theme])

