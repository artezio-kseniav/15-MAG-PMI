# Models of corpus linguistics. Task 6.
#
# Collect dataset of Russian texts, which contain at least 2 classes.
# Compute perplexity for all classes separately by using parameters of language model estimated on NKRYA.

import nltk
import string
import math
import os
import io
import pickle
import grab
import regex
import re

def load_ngrams_from_file(filename):
    d = {}
    dump_filename = filename[:-4] + ".pkl"
    if os.path.exists(dump_filename):
        print "Loading from " + dump_filename + " file."
        d = pickle.load(open(dump_filename, "rb"))
    else:
        print "Loading from " + filename + " file."
        f = io.open(filename, "r", encoding='utf8')
        # Use pretty standard way to read n_grams
        for line in f:
            line = line.replace('\n', '').split('\t')
            d[tuple(line[0:])] = int(line[0])
        f.close()
        pickle.dump(d, open(dump_filename, "wb"))
    print "Length: " + str(len(d)) + " elements."
    return d

if not os.path.exists("2grams-3.txt") or not os.path.exists("3grams-3.txt"):
    print "You must download 2grams-3.txt and 3grams-3.txt files and place it with this script!"
    exit()

print "-----------------------"
bi_grams = load_ngrams_from_file("2grams-3.txt")
print "-----------------------"
three_grams = load_ngrams_from_file("3grams-3.txt")
print "-----------------------"

corpus = {}
# Loading from file
if os.path.exists("corpus.pkl"):
     count = 0
     category_number = 0
     print "-----------------------"
     print "Summary:"
     print "-----------------------"
     corpus = pickle.load(open("corpus.pkl", "rb"))
     for theme in corpus:
        count = count + len(corpus[theme])
        category_number = category_number + 1
        print "    Category: " + theme + ", length: " + str(len(corpus[theme]))
     print "-----------------------"
     print 'Totally: ' + str(count) + ' words.'
     print 'Total categories: ' + str(category_number)
     print "-----------------------"
else:
    g = grab.Grab()
    print "Parsing AIF in progress..."
    root = 'http://www.aif.ru'
    themes = ['politics', 'society', 'money']

    for theme in themes:
        url = root + '/' + theme
        g.go(url)
        html_lines = g.response.body.split('\n')
        pages = list()
        for line in html_lines:
            line = line.replace(' ','')
            expr = '		<ahref=\"' + url + '/'
            if line.startswith(expr):
                elements = line.split('\"')
                pages.append(elements[1])
        pages = list(set(pages))
        cleaned_corpus_words = list()
        for i in range(0, len(pages), 1):
            g.go(pages[i])
            text = []
            ind1 = g.response.body.find('<article class="material_content increase_text">')
            ind2 = g.response.body.find('</article>')
            text = g.response.body[ind1:ind2]
            text = unicode(text, 'utf8', 'replace')
            tokenize = text.split()
            for tok in tokenize:
                tok = tok.replace('.', '')
                tok = tok.replace(',', '')
                tok = tok.replace('-', '')
                tok = tok.replace('"', '')
                tok = tok.replace('<', '')
                tok = tok.replace(';', '')
                tok = tok.replace('>', '')
                tok = tok.replace('/', '')
                tok = tok.replace('"', '')
                tok = tok.lower()
                word = ''.join(['' if ord(i) < 128 else i for i in tok])
                if not (word == '' or word == '\n'):
                    cleaned_corpus_words.append(word)
        print 'Length for ' + theme + ' topic: ' + str(len(cleaned_corpus_words))
        corpus.update({theme: cleaned_corpus_words})
    pickle.dump(corpus, open("corpus.pkl", "wb"))
    print "Parsing AIF has ended..."

# Function for computing perplexity
def find_perplexity(category, n3_gram, n2_gram):
    sum_probability = 0
    unknown_words = 0
    min_probability = 1
    sum_log = 0
    current_probability = {}
    for i in range(2, len(category)):
        try:
            current_probability[i] = (n3_gram[(category[i - 2], category[i - 1], category[i])] + 0.0) / n2_gram[(category[i - 2], category[i - 1])]
            sum_probability += current_probability
            if current_probability[i] < min_probability:
                min_probability = current_probability[i]
        except KeyError:
            unknown_words += 1
    known_words = len(category) - unknown_words
    min_probability /= 10.0
    probability_to_substract = (unknown_words * min_probability + 0.0) / known_words
    for i in range(2, len(category)):
        try:
            sum_log += math.log(current_probability[i] - probability_to_substract, 2)
        except KeyError:
            sum_log += math.log(min_probability, 2)
    return 2**(-sum_log/len(category))

print "-----------------------"
print "Computing perplexity:"

for theme in corpus:
    perplexity = find_perplexity(corpus[theme], bi_grams, three_grams)
    print "Perplexity for " + theme + " : " + str(perplexity)
print "-----------------------"