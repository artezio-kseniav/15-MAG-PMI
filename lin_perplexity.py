
import io
import nltk
import math
import string
from collections import defaultdict
import lxml.html as html
import re
import time


topics = ['politics', 'sport']
news_url = {'http://izvestia.ru/archive/15?type=1&p=':'politics',  'http://izvestia.ru/archive/21?type=1&p=':'sport'}
basic_url = 'http://izvestia.ru'

news_urls = defaultdict(list)
for url in news_url:
    for i in range(1,150):
        news = url + str(i)
        news_html = html.parse(news)
        found_urls = news_html.getroot().xpath('//div[@class="items_list_text"]/h3/a')
        for page_url in found_urls:
            href = page_url.get('href')
            news_urls[news_url[url]].append(basic_url + href)

print(len(news_urls['politics']))
print(len(news_urls['sport']))

news_corpus = defaultdict(list)
for topic in topics:
    count = 0
    for news_page in  news_urls[topic]:
        page_html = html.parse(news_page)
        text = page_html.getroot().xpath('//div[@class="text_block"]/p/text()')
        head = page_html.getroot().xpath('//h1[@itemprop="headline"]/text()')
        if not text:
            continue
        news_text = ''.join(head) + ''.join(text)
        news_corpus[topic].append(news_text)
        count += 1
        #print("Topic: %s Parsing progress: %d out of %d " % (topic, count, len(news_urls[topic])), end = '\r' )

print(len(news_corpus['politics']))
print(len(news_corpus['sport']))


def load_ngrams(input_file):
        input_f = io.open(input_file, "r", encoding='utf8')
        n_dict = {}
        for line in input_f:
            line = line.replace('\n', '').split('\t')
            n_dict[tuple(line[0:])] = int(line[0])
        input_f.close()
        return n_dict


bigrams = load_ngrams('2grams-3.txt')
print('2grams count: ', len(bigrams.keys()))

threegrams = load_ngrams('3grams-3.txt')
print('3grams count: ', len(threegrams.keys()))

tokenized_corpus = defaultdict(list)
for key in news_corpus.keys():
    for text in news_corpus[key]:
        text_str = ''.join(text)
        line = nltk.word_tokenize(text_str)
        line = [word.encode("utf-8").decode("utf-8").lower() for word in line if word not in string.punctuation
                        and word not in [u'\u2012', u'\u2013', u'\u2014', u'\u2015', u'``', u"''"]]
        tokenized_corpus[key] += line

for key in tokenized_corpus.keys():
    print(key, len(tokenized_corpus[key]))


def find_perplexity(category, n3_gram, n2_gram):
    sum_probability = 0
    unknown_words = 0
    min_probability = 1
    sum_log = 0


    current_probability = {}
    for i in range(2, len(category)):
        try:
            current_probability[i] = (n3_gram[(category[i - 2], category[i - 1], category[i])] + 0.0)/ n2_gram[(category[i - 2], category[i - 1])]
            sum_probability += current_probability
            if current_probability[i] < min_probability:
                min_probability = current_probability[i]
        except KeyError:
            unknown_words += 1
    print (unknown_words, len(category), sum_probability)
    known_words = len(category) - unknown_words
    min_probability /= 10.0
    probability_to_substract = (unknown_words * min_probability + 0.0) / known_words
    for i in range(2, len(category)):
        try:
            sum_log += math.log(current_probability[i] - probability_to_substract, 2)
        except KeyError:
            sum_log += math.log(min_probability, 2)
    return sum_log


for key in tokenized_corpus.keys():
    perplexity = find_perplexity(tokenized_corpus[key], bigrams, threegrams)
    perplexity = 2**(-perplexity / len(tokenized_corpus[key]))
    print(key,' perplexity: ', perplexity, '\n')