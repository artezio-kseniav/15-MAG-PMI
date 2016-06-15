import gensim.models import Word2Vec
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import TruncatedSVD
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.cross_validation import train_test_split

dataset = fetch_20newsgroups(subset="all")

# tokenization
for text in corpus_data.data:
	tokenized_data = nltk.word_tokenize(text)

lemms = []
texts = []
lem = WordNetLemmatizer()


for text in tokenized_data:
	for token in text:
		lemms.append(token.lower())
	texts.append(lemms)

model = Word2Vec(texts)
model.save('w2v.dat')

# similarity of words
sim1 = model.similarity("guy","woman")
print(sim1)

sim2 = model.similarity("town", "city")
print(sim2)

sim3 = model.similarity("car", "computer")
print(sim3)

sim4 = model.similarity("motocycle","car")
print(sim4)

sim5 = model.similarity("guy","boy")
print(sim5)

# addition and subtraction of words
msim1 = model.most_similar(positive=["city", "europa"], negative=["turan"])
print(msim1)

msim2 = model.most_similar(positive=["actor", "job"], negative=["man"])
print (msim2)

# word doesn't match the list
dntm = model.doesnt_match("russia italy azerbaijan britain car")
print(dntm)

dntm1 = model.doesnt_match("boy man woman baby guy town")
print(dntm1)