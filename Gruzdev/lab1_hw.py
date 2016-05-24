# Models of corpus linguistics. Task 1.
#
# Perform clustering of 20newsgroup dataset.
# As features for that use TF-IDF.
# Visualize results and existing clusters in 2D plot by using any methods for dimension reduction.

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN

import numpy as np
import matplotlib.pyplot as plt


# Download 20newsgroups dataset
dataset = fetch_20newsgroups(subset='all', shuffle=True, random_state=60612)

# TF-IDF vectorization
vectorizer = TfidfVectorizer(max_df=0.5, max_features=12,
                             min_df=4, stop_words='english',
                             use_idf=True)

X = vectorizer.fit_transform(dataset.data)
labels = dataset.target
categories = np.unique(labels).shape[0]

# Show dataset statistics
print("Dataset info: ")
print("Documents: %d, features: %d" % X.shape)
print("Categories number: %d" % categories)
print("\n")
print("Categories:")
for target_name in dataset.target_names:
    print "    " + target_name
print("\n")

# Let's do K-means clustering for cluster task.
kmeans = KMeans(init='random', n_clusters=categories, n_init=5).fit(X)

order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]

feature_names = vectorizer.get_feature_names()
for i in range(categories):
    print("Cluster %d's top 5 words:" % i)
    words = ''
    for ind in order_centroids[i, :5]:
        words = words + feature_names[ind] + ' '
    print words

print("\n")
print("Labels of corresponding points:")
# Get labels of corresponding points
classes = kmeans.labels_
print classes
print("\n")

# Let's do SVD for dimension reduction
svd = TruncatedSVD(n_components=2, random_state=50010)
X_2d = svd.fit_transform(X)

explained_variance = svd.explained_variance_ratio_.sum()
print("Explained variance of the SVD step: {}%".format(
    int(explained_variance * 100)))

# Plotting results
plt.figure(figsize = (10, 10))
plt.scatter(X_2d[:,0], X_2d[:,1], c=classes, alpha=0.6)
plt.show()

# Let's do DBSCAN clustering for cluster task.
# db = DBSCAN(eps=0.5, min_samples=5, metric='euclidean', algorithm='auto', leaf_size=30, )
# db.fit(X)
#
# order_centroids = db.cluster_centers_.argsort()[:, ::-1]
#
# feature_names = vectorizer.get_feature_names()
# for i in range(categories):
#    print("Cluster %d's top 5 words:" % i)
#    words = ''
#    for ind in order_centroids[i, :5]:
#        words = words + feature_names[ind] + ' '
#    print words
#
# print("\n")
# print("Labels of corresponding points:")
# # Get labels of corresponding points
# classes = db.labels_
# print classes
# print("\n")
#
# # Let's do SVD for dimension reduction
# svd = TruncatedSVD(n_components=2, random_state=50010)
# X_2d = svd.fit_transform(X)
#
# explained_variance = svd.explained_variance_ratio_.sum()
# print("Explained variance of the SVD step: {}%".format(
#     int(explained_variance * 100)))
#
# # Plotting results
# plt.figure(figsize = (10, 10))
# plt.scatter(X_2d[:,0], X_2d[:,1], c=classes, alpha=0.6)
# plt.show()