import nltk
import gensim
#nltk.download()
import string
from gensim.models import Word2Vec
from nltk.stem import WordNetLemmatizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
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
tok=TfidfVectorizer().build_tokenizer()

test=[]
newsgroups_tokenized = [nltk.word_tokenize(text) for text in dataset.data]

for text in newsgroups_tokenized:
    lemms = []
    for word in text:
        if word not in string.punctuation:
            lemms.append(word.lower())
    test.append(lemms)


model = gensim.models.Word2Vec(test)
print (model['car'])
print ('Dimension',len(model['car']))
#Similarity
#print (model.similarity('car','bycycle'))
print (model.similarity('car','computer'))
print (model.similarity('hair','bear'))
#OPERATIONS with words
print(model.most_similar(positive=['car', 'white']))
print(model.most_similar(positive=['hair', 'bear', 'cat'], negative = ['animals']))
print(model.most_similar(positive=['python', 'java', 'programming']))
