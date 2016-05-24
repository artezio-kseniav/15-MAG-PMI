from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import word_tokenize
from nltk import WordNetLemmatizer
from sklearn import decomposition
import numpy as np
from sklearn.cluster import KMeans, DBSCAN, MiniBatchKMeans
import matplotlib.pyplot as plt

class LemmaTokenizer(object):
     def __init__(self):
         self.wnl = WordNetLemmatizer()
     def __call__(self, doc):
         return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

"""
Для удобства дальнейшего отображения резульатов считаем только часть выборки
Также сохраним правильные классы для объектов.

"""
print("data reading")
cats=['alt.atheism', 'sci.space', 'talk.politics.guns', "rec.autos", "sci.med", "comp.sys.ibm.pc.hardware"]
newsgroups = fetch_20newsgroups(categories=cats)
true_labels = newsgroups.target

"""
Представим нашу изначальную выборку, используя TFIDF метрику.
Кроме того, исключим стоп слова, проведем лемматизацию слов, приведем все слова к нижнему регистру,
исключим из выборки очень редкие и частые слова. Последнее значительно ускорит кластеризацию
"""
print("processing")
vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words='english', tokenizer=LemmaTokenizer(), lowercase=True)
X = vectorizer.fit_transform(newsgroups.data)

"""
Кластеризуем нашу предобработанную выборку при помощи kmeans.
Искать будем столько же кластеров, сколько и в изначальной выборке.
"""
print("clustering")
#km = KMeans(n_clusters=len(true_labels), init='k-means++', n_init=1, max_iter=100)
km = KMeans(n_clusters=len(set(true_labels)), init='k-means++', n_init=1)
km.fit(X)

"""
Сократим рамерность выборки до 2.
Нарисуем объекты с координатами из нового пространства признаков.
Объекты из разных предсказанных классов раскаршены в разные цвета.
Объекты из разных классов, согласно изначальным меткам, отображены различными геометрическими фигурами.
"""
print("painting")
X = decomposition.TruncatedSVD(n_components=2).fit_transform(X)
colors = plt.cm.Spectral(np.linspace(0, 1, len(set(true_labels))))
markers = ('o', 'v', '^', '<', '>',  '1', '2', '3', '4', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', '+' , ',' , '.')
counter = 0
for i in range(len(true_labels)):
    plt.plot(X[i][0], X[i][1], markers[true_labels[i]], markersize=6, alpha = 0.7, color=colors[km.labels_[i]])
plt.show()
print("end")