# Models of corpus linguistics. Task 4.
#
# Play with Word2vec model & its functionality for 20newsgroup dataset
#
#

from sklearn.datasets import fetch_20newsgroups
import nltk
import string
import gensim
import os

# Download 20newsgroup dataset
dataset_small = fetch_20newsgroups(categories=['sci.space'])

#dataset_small = fetch_20newsgroups(categories=['sci.space', 'comp.graphics',
# 'comp.sys.ibm.pc.hardware', 'comp.windows.x', 'sci.electronics'], subset='all')

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

# Data preparation for word2vec model
if os.path.exists("word2vec.dump"):
    word2vec_model = gensim.models.Word2Vec.load("word2vec.dump")
else:
    # Tokenization
    dataset_small_tokenized = [nltk.word_tokenize(article) for article in dataset_small.data]

    corpus_prepared = []
    for text in dataset_small_tokenized:
        lemmas = []
        for word in text:
            if word not in string.punctuation:
                lemmas.append(word.lower())
            corpus_prepared.append(lemmas)

    print 'Training of Word2Vec model is in progress...'
    # Run Word2Vec on processed data
    word2vec_model = gensim.models.Word2Vec(corpus_prepared, workers=4, min_count=5)
    print 'Training of Word2Vec model has ended...'
    word2vec_model.save('word2vec.dump')

# Let's use some useful functions from word2vec
example = 'car'

print 'Vector representation of ' + example
print word2vec_model['car']
print "-----------------------"
print('Vector dimension: ', len(word2vec_model['car']))
print "-----------------------"

# Let's play with similarity function
print 'Similarity measure between head & hand: ' + str(word2vec_model.similarity('hand', 'head'))
print 'Similarity measure between computer & mobile: ' + str(word2vec_model.similarity('computer', 'mobile'))
print 'Similarity measure between ship & car: ' + str(word2vec_model.similarity('ship', 'car'))
print "-----------------------"

# Let's remove mismatched word
mismatched = word2vec_model.doesnt_match(['bus', 'bar', 'bicycle'])
print 'Mismatched word among bus, bar, bicycle: ' + mismatched

mismatched = word2vec_model.doesnt_match(['car', 'motorcycle', 'bicycle'])
print 'Mismatched word among car, motorcycle, bicycle: ' + mismatched

mismatched = word2vec_model.doesnt_match(['pen', 'pencil', 'writer'])
print 'Mismatched word among pen, pencil, writer: ' + mismatched
print "-----------------------"

# Let's play with most_similar function of word2vec

words = word2vec_model.most_similar(positive=['man', 'woman'])
print 'Most similar to man & woman are:'
for word in words:
    print "    " + word[0], word[1]
print "-----------------------"
words = word2vec_model.most_similar(positive=['chair', 'table'], negative=['air'])
print 'Most similar to computer & phone are:'
for word in words:
    print "    " + word[0], word[1]
print "-----------------------"