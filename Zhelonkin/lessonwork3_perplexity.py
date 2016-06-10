#!/usr/bin/python3

# Written by Sokolov Artem and Zhelonkin Dmitry

# theme: politics 1185
# theme: society 1184
# all text counter: 2369

import lxml.html as html
import re, pickle, datetime, urllib.request
from bs4 import BeautifulSoup
from nltk.util import ngrams
import math

def get_texts():

    all_count = 0
    base_url = "http://www.novayagazeta.ru/"
    themes = ["politics", "society"]

    # create a list of dates
    start = datetime.datetime.strptime("06-01-2016", "%d-%m-%Y")
    end = datetime.datetime.strptime("06-06-2016", "%d-%m-%Y")
    dates = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

    for theme in themes:
        # list of tuples: (theme, href, text)
        data = []
        counter = 0
        for page_num in range(1,80):
            try:
                main_page = html.parse(base_url+theme+"/?p="+str(page_num))
                tags = main_page.getroot().xpath('//*[@class="b-feed-item-head-title"]//a')
                for tag1 in tags:
                    news = ''

                    page = urllib.request.urlopen(base_url+tag1.attrib['href'][1:]+"?print=1")
                    soup = BeautifulSoup(page.read(), "lxml")
                    news = soup.text[:soup.text.find("Автор:")]
                    news = soup.text[:soup.text.find("Постоянный адрес страницы:")]
                    text_flag = False
                    clean_news = ""
                    for line in news.split('\n'):
                        if text_flag:
                            clean_news += line+" "
                            continue
                        if re.search(r'(\d+-\d+-\d+)',line):
                            text_flag = True
                    news = clean_news

                    # filter out empty text (text which contains only spaces is also empty text)
                    # assumption: news must contains point
                    if "." not in news:
                        continue

                    # delete forbidden symbols
                    news = re.sub('[âÂ©Ã§¦«»:,—()%/]', '', news)
                    news = re.sub('[\xa0\n\x80\x9d.!?…]', ' ', news)
                    news = re.sub(' +', ' ', news)

                    # append text of news as a string to data list
                    data.append((theme, tag1.attrib['href'][1:], news))
                    # print (theme, tag1.attrib['href'][1:], news)
                    counter += 1
                    all_count += 1
            except:
                pass
        print ("theme:", theme, counter)
        with open('ng_'+theme+'.pickle', 'wb') as f:
            pickle.dump(data, f)
    print ("all text counter:", all_count)


# load data or execute get_texts()
# get_texts()
with open('ng_politics.pickle', 'rb') as f:
    data_politics = pickle.load(f)
with open('ng_society.pickle', 'rb') as f:
    data_society = pickle.load(f)

# find all 3grams
politics_3grams = []
society_3grams = []
nkrya_3grams = {}
for text in data_politics:
    politics_3grams.extend(ngrams(text[2].split(" "), 3))
for text in data_society:
    society_3grams.extend(ngrams(text[2].split(" "), 3))

# find all unique 3grams and some other staff
set_politics = set(politics_3grams)
set_society = set(society_3grams)
print(len(list(set_politics)), len(list(set_society))) # 1195642 1248795
part = []
politics = {}
society = {}
politics_3grams = []
society_3grams = []

# try to find frequencies for all 3grams in nkrya file
with open("3grams-3.txt", "r", encoding="utf8") as f:
    file = f.read().split("\n")
    for line in file:
        try:
            part = line.split("\t")
            if (part[1], part[3], part[5]) in set_politics:
                politics[(part[1], part[3], part[5])] = part[0]
            if (part[1], part[3], part[5]) in set_society:
                society[(part[1], part[3], part[5])] = part[0]
        except:
            pass # for the last line

# from 1195642 and 1248795 unique words in political and social dictionaries found only 148009 162065 words respectively
print(len(politics.keys()), len(society.keys())) # 148009 162065
#
# with open('nkrya_politics.pickle', 'wb') as f:
#     pickle.dump(politics, f)
#
# with open('nkrya_society.pickle', 'wb') as f:
#     pickle.dump(society, f)

# with open('nkrya_politics.pickle', 'rb') as f:
#     politics = pickle.load(f)
#
# with open('nkrya_society.pickle', 'rb') as f:
#     society = pickle.load(f)


# count perplexity for every dictionary
words_in_pol = len(politics.keys())
pol_most_freq = int(max(politics.items(), key=lambda item: int(item[1]))[1])
sum_pol = 0
for ngram, freq in politics.items():
    sum_pol += math.log10(int(freq) / pol_most_freq)
perplexity_pol = (1 / pol_most_freq) * (-1) * sum_pol
print("perplexity for political news:", perplexity_pol)
# perplexity for political news: 25.732344230392563

words_in_soc = len(society.keys())
soc_most_freq = int(max(society.items(), key=lambda item: int(item[1]))[1])
sum_pol = 0
for ngram, freq in society.items():
    sum_pol += math.log10(int(freq) / soc_most_freq)
perplexity_pol = (1 / soc_most_freq) * (-1) * sum_pol
print("perplexity for social news:", perplexity_pol)
# perplexity for social news: 28.111066052832374