#!/home/artsokol/anaconda/bin/python
#/usr/bin/python3

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt


def show_top10(classifier, vectorizer, categories):
     feature_names = np.asarray(vectorizer.get_feature_names())
     for i, category in enumerate(categories):
         top10 = np.argsort(classifier.coef_[i])[-10:]
         print("%s: %s" % (category, " ".join(feature_names[top10])))
         
         
         
newsgroups = fetch_20newsgroups()         
newsgroups_train = fetch_20newsgroups(subset='train')
newsgroups_test = fetch_20newsgroups(subset='test')

#pprint(list(newsgroups_train.target_names))
#pprint(list(newsgroups_test.target_names))

vectorizer = TfidfVectorizer()
vectors_train = vectorizer.fit_transform(newsgroups_train.data)
vectors_test = vectorizer.transform(newsgroups_test.data)

pprint("Train data size:")
pprint(vectors_train.shape)

pprint("Test data size:")
pprint(vectors_test.shape)
print("---------------------------------")


clf = MultinomialNB(alpha=.01)
clf.fit(vectors_train, newsgroups_train.target)
pred = clf.predict(vectors_test)

show_top10(clf, vectorizer, newsgroups_train.target_names)



