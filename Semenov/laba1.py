from sklearn.datasets import fetch_20newsgroups
from pprint import pprint
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np
from sklearn.decomposition import TruncatedSVD
import pylab as pl
import matplotlib

newsgroups = fetch_20newsgroups(subset='all', shuffle=True, random_state=1)

pprint(list(newsgroups.target_names))

print("%d documents" % len(newsgroups.data))
print("%d categories" % len(newsgroups.target_names))

cluster_number = len(newsgroups.target_names)

vectorizer = TfidfVectorizer(stop_words='english')
clustering_data = vectorizer.fit_transform(newsgroups.data)

km = KMeans(n_clusters=cluster_number, n_init = 1)

km.fit(clustering_data)

svd = TruncatedSVD(n_components = 2)
clustering_data_2d = svd.fit_transform(clustering_data)

#цвета для отображения различных кластеров на графике
colors = matplotlib.cm.rainbow(np.linspace(0, 1, 20))

for i in range(0, clustering_data_2d.shape[0]):
    pl.scatter(clustering_data_2d[i,0], clustering_data_2d[i,1], c=colors[km.labels_[i]])
pl.show()