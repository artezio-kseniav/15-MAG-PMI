from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from pprint import pprint
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
import numpy as np
import matplotlib
import pylab
#from sklearn.naive_bayes import MultinomialNB
#from sklearn import metrics


news = fetch_20newsgroups(subset = 'train')
print (news.filenames.shape)
pprint(list(news.target_names))

n = len(news.target_names)
print n
tf_idf = TfidfVectorizer().fit_transform(news.data)
#print tf_idf.shape
#print tf_idf

clusters = KMeans(n_clusters=n, n_init=1)
km_clustering = clusters.fit(tf_idf)

svd_dim = TruncatedSVD(2).fit_transform(tf_idf)

colors = matplotlib.cm.rainbow(np.linspace(0, 1, 20))


for i in range(0, svd_dim.shape[0]):
    pylab.scatter(svd_dim[i, 0], svd_dim[i, 1], c=colors[clusters.labels_[i]])
pylab.show()
