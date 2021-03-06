from sklearn.datasets import fetch_20newsgroups
from pprint import pprint
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import nltk
from collections import defaultdict
import string
from nltk.stem.porter import PorterStemmer


newsgroups = fetch_20newsgroups(categories=['comp.graphics','comp.os.ms-windows.misc','rec.autos','rec.sport.hockey'],
                                subset='all', shuffle=True, random_state=1)
								
pprint(list(newsgroups.target_names))

print("%d documents" % len(newsgroups.data))
print("%d categories" % len(newsgroups.target_names))

#взято с stackoverflow
stemmer = PorterStemmer()
def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    tokens = [i for i in tokens if i not in string.punctuation]
    stems = stem_tokens(tokens, stemmer)
    return stems

	
vectorizer = TfidfVectorizer(stop_words='english', tokenizer=tokenize)
tfidf_data = vectorizer.fit_transform(newsgroups.data)

query = 'computer vision'
tfidf_query = vectorizer.transform([query])

feature_names = vectorizer.get_feature_names()
for word in tfidf_query.nonzero()[1]:
    print(feature_names[word], ' - ', tfidf_query[0, word])
	
	

	
def query_results(query_string, top_count):
    tfidf_query = vectorizer.transform([query_string])
    cosine_similarities = defaultdict(float) #словарь всех дистанций
    count = 0
    for doc in tfidf_data: #для каждого документа в корпусе находим косинусное расстояние с запросом
        #пользуемся матричным видом для умножения векторов
        #так как TF-IDF нормализует данные, делить на длины векторов не нужно
        cosine_similarity = doc*(tfidf_query[0].transpose()) 
        if not cosine_similarity:
            cosine_similarity = 0.0
        else:
            #при умножении матриц получается матрица размером [1,1], записываем этот элемент
            cosine_similarity = cosine_similarity[0,0]
        #записываем в словарь
        cosine_similarities[newsgroups.data[count]] = cosine_similarity
        count += 1
    #сортируем словарь по значению и выводим заданное значение документов
    for key, value in sorted(cosine_similarities.items(), reverse=True, key=lambda x:x[1])[:top_count]:
        print('Similarity value = ', value, '\n\n', key )
        print('----------------------------------------------------------------------')
		
		
		
		
		
query_results("hockey champion", 3)

query_results("auto speed", 5)