from sklearn.datasets import fetch_20newsgroups
from nltk import word_tokenize
from gensim.models import Word2Vec

if __name__ == "__main__":
	categories=['comp.os.ms-windows.misc', 'rec.autos','rec.motorcycles', 'sci.space']
	dataset = fetch_20newsgroups(subset='all', categories=categories)
	tokenized = [nltk.word_tokenize(text) for text in dataset.data]
	
	corpus=[]
	for doc in tokenized:
    lemms = []
		for word in doc:
			if word not in string.punctuation:
				lemms.append(word.lower())
		corpus.append(lemms)
		
	w2v = gensim.models.Word2Vec(corpus)
	print (model['car'])
	print ('N of dimesions: %i' % len(w2v['Honda']))

	print (w2v.similarity('bike','Honda'))

	print(w2v.most_similar(positive=['drive', 'Honda'], negative = ['car']))