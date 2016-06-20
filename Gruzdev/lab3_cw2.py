# Models of corpus linguistics. Task 3.
#
# Perform search of semantically similar texts of 20newsgroup dataset to the input query.
# As measure of semantic similarity consider 2 cases:
# 1) TF/IDF + cosine distance
# 2) BM25 model

import warnings
warnings.simplefilter("ignore")

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import gensim
from gensim import corpora
import math

# Code for BM25 model
class BM25 :
    def __init__(self, fn_docs, delimiter='|') :
        self.dictionary = corpora.Dictionary()
        self.DF = {}
        self.delimiter = delimiter
        self.DocTF = []
        self.DocIDF = {}
        self.N = 0
        self.DocAvgLen = 0
        self.fn_docs = fn_docs
        self.DocLen = []
        self.buildDictionary()
        self.TFIDF_Generator()

    def buildDictionary(self):
        raw_data = []
        for i in range(0, len(self.fn_docs), 1):
            doc = self.fn_docs[i]
            #print doc
            for line in doc.split(' '):
                line = line.lower()
                line = ''.join([i if ord(i) < 128 else '' for i in line])
                line = line.replace('.', '')
                line = line.replace(',', '')
                line = line.replace('-', '')
                line = line.replace('(', '')
                line = line.replace(')', '')
                line = line.replace(']', '')
                line = line.replace('[', '')
                line = line.replace('"', '')
                line = line.replace('<', '')
                line = line.replace('>', '')
                line = line.replace('/', '')
                line = line.replace('\\', '')
                line = line.replace('\n', '')
                line = line.replace('?', '')
                line = line.replace('!', '')
                line = line.replace(':', '')
                line = line.replace('$', '')
                line = line.replace('"', '')
                #print line
                raw_data.append(line.strip().split(self.delimiter))
        self.dictionary.add_documents(raw_data)

    def TFIDF_Generator(self, base=math.e) :
        docTotalLen = 0
        for i in range(0,len(self.fn_docs),1):
            doc = self.fn_docs[i].split(self.delimiter)
            #print doc
        #for line in file(self.fn_docs):
            #doc = line.strip().split(self.delimiter)
            docTotalLen += len(doc)
            self.DocLen.append(len(doc))
            #print self.dictionary.doc2bow(doc)
            bow = dict([(term, freq*1.0/len(doc)) for term, freq in self.dictionary.doc2bow(doc)])
            for term, tf in bow.items() :
                if term not in self.DF :
                    self.DF[term] = 0
                self.DF[term] += 1
            self.DocTF.append(bow)
            self.N = self.N + 1
        for term in self.DF:
            self.DocIDF[term] = math.log((self.N - self.DF[term] +0.5) / (self.DF[term] + 0.5), base)
        self.DocAvgLen = docTotalLen / self.N

    def BM25Score(self, Query=[], k1=1.5, b=0.75):
        print "-----------------------"
        print 'Query for search: ', ' '.join(Query)
        print "-----------------------"
        query_bow = self.dictionary.doc2bow(Query)
        scores = []
        for idx, doc in enumerate(self.DocTF) :
            commonTerms = set(dict(query_bow).keys()) & set(doc.keys())
            tmp_score = []
            doc_terms_len = self.DocLen[idx]
            for term in commonTerms :
                upper = (doc[term] * (k1+1))
                below = ((doc[term]) + k1*(1 - b + b*doc_terms_len/self.DocAvgLen))
                tmp_score.append(self.DocIDF[term] * upper / below)
            scores.append(sum(tmp_score))
        return scores

    def TFIDF(self) :
        tfidf = []
        for doc in self.DocTF :
            doc_tfidf  = [(term, tf*self.DocIDF[term]) for term, tf in doc.items()]
            doc_tfidf.sort()
            tfidf.append(doc_tfidf)
        return tfidf

    def Items(self) :
        # Return a list [(term_idx, term_desc),]
        items = self.dictionary.items()
        items.sort()
        return items


# Code for TFIDF + Cosine distance
def print_top_k_results(top_k, top_l, similarity, sorted_results):
    print "-----------------------"
    print 'Results: '
    print "-----------------------"
    # Show top-k articles
    for i in range(top_k):
        article = similarity.keys()[similarity.values().index(sorted_results[i])]
        lines = article.split('\n')
        print 'Cosine similarity: ', "%.2f" % sorted_results[i], '\n'
        for index in range(top_l):
            print "      " + lines[index]
        print "-----------------------"

def search_cosine(query, dataset, vectorizer, data_tf_idf, top_k, top_l):

    # Transform query words to TF/IDF to perform search
    tf_idf_query = vectorizer.transform([query])
    print "-----------------------"
    print 'Query for search: ', query
    print "-----------------------"
    # Find cosine similarity for query and texts
    similarity = {}
    counter = 0
    for article in data_tf_idf:
        similarity[dataset.data[counter]] = cosine_similarity(article, tf_idf_query)[0][0]
        counter += 1
    sorted_results = sorted(similarity.values(), reverse=True)
    # Print to console all needed results
    print_top_k_results(top_k, top_l, similarity, sorted_results)


# Download 20newsgroups dataset
dataset = fetch_20newsgroups(subset='all')

# Print some info
print "-----------------------"
print "Summary:"
print "-----------------------"
print 'Topics:'
for name in dataset.target_names:
    print " " + name
print "-----------------------"
print 'Categories number:', len(dataset.target_names)
print 'Total length:', len(dataset.data)
print "-----------------------"

# Transform data to TF/IDF
tf_idf_vectorizer = TfidfVectorizer(stop_words='english', analyzer='word')
tf_idf_index = tf_idf_vectorizer.fit_transform(dataset.data)

top_articles_value = 3
top_lines_value = 10

# Call this function for searching according cosine similarity & printing results
search_cosine("deep learning", dataset, tf_idf_vectorizer, tf_idf_index, top_articles_value, top_lines_value)
search_cosine("machine learning", dataset, tf_idf_vectorizer, tf_idf_index, top_articles_value, top_lines_value)
search_cosine("computer vision", dataset, tf_idf_vectorizer, tf_idf_index, top_articles_value, top_lines_value)


# Let's play with BM25

# Code for BM25
def print_top_k_results_bm25(top_k, top_l, similarity, data):
    print "-----------------------"
    print 'Results: '
    print "-----------------------"
    sorted_similarity, sorted_data = zip(*sorted(zip(similarity, data)))
    sorted_similarity = sorted_similarity[-top_k:]

    sorted_data = sorted_data[-top_k:]

    # Show top-k articles
    for i in range(0, top_k, 1):
        lines = ''.join(sorted_data[(top_k-1)-i]).split('\n')
        #print lines
        print 'BM25 similarity: ', "%.2f" % sorted_similarity[(top_k-1)-i], '\n'
        for index in range(top_l):
            print "      " + lines[index]
        print "-----------------------"


dataset_small = fetch_20newsgroups(categories=['sci.space', 'comp.graphics', 'comp.sys.ibm.pc.hardware', 'comp.windows.x',
                                               'sci.electronics'], subset='all')

# Print some info
print "-----------------------"
print "Summary:"
print "-----------------------"
print 'Topics:'
for name in dataset_small.target_names:
    print " " + name
print "-----------------------"
print 'Categories number:', len(dataset_small.target_names)
print 'Total length:', len(dataset_small.data)
print "-----------------------"

bm25 = BM25(dataset_small.data, delimiter=' ')

query = 'computer vision'
query = query.split()
scores = bm25.BM25Score(query)

top_articles_value = 5
top_lines_value = 10

print_top_k_results_bm25(top_articles_value, top_lines_value, scores, dataset_small.data)