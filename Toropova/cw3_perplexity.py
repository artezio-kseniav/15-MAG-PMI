# coding: utf-8

from lxml import html
import time
import requests
from collections import defaultdict
import re
import nltk
import math
import string 
import io

base_url = 'http://ria.ru/'

def get_news_urls(url):
    tree = html.fromstring(requests.get(url).content)
    urls = []
    for a in tree.xpath('//ul/li/a'):
        href = a.get('href')
        if href and '?rubric' in href:
            urls.append(href)
    return urls
    
def get_content(url):
    tree = html.fromstring(requests.get(url).content)
    lines = [x.text for x in tree.xpath('//div[@class="article-body js-mediator-article"]/*') if x.text]
    return '\n'.join(lines)


news_url = {'http://izvestia.ru/archive/10?type=1&p=':'politics',  'http://izvestia.ru/archive/10?type=1&p=':'sport'}

def get_izvestia_urls():
    news_urls = defaultdict(list)
    for url in news_url:
        for i in range(1, 100):
            news = url + str(i)
            news_html = html.parse(news)
            found_urls = news_html.getroot().xpath('//div[@class="items_list_text"]/h3/a')
            for page_url in found_urls:
                href = page_url.get('href')
                news_urls[news_url[url]].append('http://izvestia.ru' + href)
    return news_urls

news_urls = get_izvestia_urls()

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

def load_ngrams(input_file):
    input_f = io.open(input_file, "r", encoding='utf8')
    n_dict = {}
    for line in input_f:
        line = line.replace('\n', '').split('\t')
        n_dict[tuple(line[0:])] = int(line[0])
    input_f.close()
    return n_dict

bigrams = load_ngrams('2grams-3.txt')
threegrams = load_ngrams('3grams-3.txt')

tokenized_corpus = defaultdict(list)
for key in news_corpus.keys():
    for text in news_corpus[key]:
        text_str = ''.join(text)
        line = nltk.word_tokenize(text_str)
        line = [word.encode("utf-8").decode("utf-8").lower() for word in line if word not in string.punctuation
                        and word not in [u'\u2012', u'\u2013', u'\u2014', u'\u2015', u'``', u"''"]]
        tokenized_corpus[key] += line


def find_perplexity(category, n3_gram, n2_gram):
    sum_probability = 0
    unknown_words = 0
    min_probability = 1
    sum_log = 0
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
            sum_log += math.log(current_probability[i] - probability_to_substract, 2)
        except KeyError:
            sum_log += math.log(min_probability, 2)

    return sum_log

for k, v in tokenized_corpus.iteritems():
    perplexity = find_perplexity(v, bigrams, threegrams)
    perplexity = 2**(-perplexity / len(v))
    print(k, perplexity)