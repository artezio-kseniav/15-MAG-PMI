import lxml.html as html
from bs4 import BeautifulSoup
from nltk.util import ngrams
import io
import math
import json
import requests
import string
import numpy as np

base_url = "http://www.mk.ru"
topics = ["economics", "politics"]
year = 2016
months = ["03", "04", "05"]
days = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]
for topic in topics:
	for month in months:
		for day in days:
			for url in [base_url + '/' + topic + '/' + year + '/' + month + '/' + day]:
			page = urllib2.urlopen(url)
			soup = BeautifulSoup(page)
			soup_class = soup.findAll('a', attrs={'class': 'mkh2'})
			for article in soup_class.findAll('a', href=True):
				site = urllib2.urlopen(article)
				soup_low = BeautifulSoup(site)
				soup_text = soup_low.findAll('div', attrs={'class': 'content'})
				text = ''
				for el in soup_text[0].contents:
					if el.name == 'p':
					text += el.text + '\n'
	txt = open("texts_" + topic + ".txt", "w")
    for text in texts:
        txt.write(text.encode("utf-8") + "\n\n\n")
    txt.close()

def load_ngrams(input_file):
    input_f = io.open(input_file, "r", encoding='utf8')
    n_dict = {}
    for line in input_f:
        line = line.replace('\n', '').split('\t')
        n_dict[tuple(line[0:])] = int(line[0])
    input_f.close()
    return n_dict

bi_gram = load_ngrams('2grams-3.txt')
tri_gram = load_ngrams('3grams-3.txt')

file_politics = open("texts_politics.txt")
politics = []
for line in file_politics:
    current_line = nltk.word_tokenize(line.decode("utf-8"))
    current_line = [word.encode("utf-8").decode("utf-8").lower() for word in current_line if word not in string.punctuation
                    and word not in [u'\u2012', u'\u2013', u'\u2014', u'\u2015', u'``', u"''"]]
    politics = politics + current_line
file_politics.close()

file_economics = open("texts_economics.txt")
economics = []
for line in file_economics:
    current_line = nltk.word_tokenize(line.decode("utf-8"))
    current_line = [word.encode("utf-8").decode("utf-8").lower() for word in current_line if word not in string.punctuation
                    and word not in [u'\u2012', u'\u2013', u'\u2014', u'\u2015', u'``', u"''"]]
    economics = economics + current_line
file_economics.close()

def find_perplexity(category, n3_gram, n2_gram):
    sum_probability = 0
    unknown_words = 0
    min_probability = 1
    sum_perplexity = 0
    
    current_probability= {}
    
    for i in range(2, len(category)):
        try:
            current_probability[i] = (n3_gram[(category[i-2], category[i-1], category[i])] + 0.0) 
            / n2_gram[(category[i-2],category[i-1])]
            sum_probability += current_probability
            if current_probability[i] < min_probability:
                min_probability = current_probability[i]
        except KeyError:
            unknown_words +=1
    print (unknown_words, len(category), sum_probability)
    known_words = len(category) - unknown_words
    min_probability /= 10.0
    probability_to_substract = (unknown_words * min_probability + 0.0) / known_words
    for i in range(2, len(category)):
        try:
            sum_perplexity += math.log(current_probability[i] - probability_to_substract, 2)
        except KeyError:
            sum_perplexity += math.log(min_probability, 2)

    return sum_perplexity

politics_perplexity = find_perplexity(politics, bi_gram, tri_gram)
economics_perplexity = find_perplexity(economics, bi_gram, tri_gram)

print("Perplexity for topic 'politics' is = ", 2**(-politics_perplexity / len(politics))
print("Perplexity for topic 'economics' is = ", 2**(-economics_perplexity / len(economics))