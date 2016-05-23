#!/home/artsokol/anaconda/bin/python
#/usr/bin/python3

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt
import numpy as np
                
newsgroups = fetch_20newsgroups()         

tf_vect = TfidfVectorizer(min_df=3, max_df=.95, stop_words='english')
word_freq = tf_vect.fit_transform(newsgroups.data)

lsa = TruncatedSVD(n_components=10)
km = KMeans(n_clusters=3)
word_freq = tf_vect.fit_transform(newsgroups.data)
word_freq_lsa = lsa.fit_transform(word_freq)
km.fit(word_freq_lsa)

print(word_freq.shape)
print(lsa.components_.shape)
print(km.cluster_centers_.shape)
weights = np.dot(km.cluster_centers_, lsa.components_)
print(weights.shape)

features = tf_vect.get_feature_names()
weights = np.abs(weights)

for i in range(km.n_clusters):
  top5 = np.argsort(weights[i])[-5:]
#  print top5
  print(zip([features[j] for j in top5], weights[i, top5]))


plt.figure()
colors = ['red', 'green', 'blue']
centroids = km.cluster_centers_
plt.scatter(centroids[:, 0], centroids[:, 1],
            marker='x', s=100, linewidths=3,c=colors)
#plt.title('K-means clustering on the digits dataset (PCA-reduced data)\n')
#for i, ((x,y), kls) in enumerate(zip(values, 3)):
#    plt.annotate(str(i), xy=(x,y), xytext=(0,0), textcoords='offset points',
#                 color=colors[kls])
plt.show()  
      
