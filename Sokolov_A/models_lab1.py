#!/usr/bin/python3

# script for loading news from telegraph on themes:
# "politics", "science", "world", "entertainment", "uk"
# 4793 documents
# theme: uk 1761
# Authors: Dm.Zhelonkin, A.Sokolov

import lxml.html as html
from pandas import DataFrame
from urllib.request import urlopen
import sys, nltk, re
import pickle

all_count = 0
base_url = "http://www.telegraph.co.uk/"
themes = ["politics", "science", "world", "entertainment", "uk"]

for theme in themes:
    # list of tuples: (theme, href, text)
    data = []

    if "science" not in theme:
        actual_path = "news/"+theme
    else:
        actual_path = theme
    counter = 0
    for num in range(1,100):
        try:
            main_page = html.parse(base_url+actual_path+"/loadmore"+str(num)+"/")
            tags = main_page.getroot().xpath('//*[@class="list-of-entities__item-body-headline"]//a')
            for tag1 in tags:
                news = ''

                # sum all subtexts into news
                for text in html.parse(base_url+tag1.attrib['href'][1:]).getroot().xpath('//*[@class="articleBodyText section"]'):
                    news += text.text_content()

                # filter out empty text (text which contains only spaces is also empty text)
                # assumption: news must contains point
                if "." not in news:
                    continue

                # delete forbidden symbols
                news = re.sub('[âÂ©Ã§¦]', '', news)
                news = re.sub('[\xa0\n\x80\x9d]', ' ', news)

                # append text of news as a string to data list
                data.append((theme, tag1.attrib['href'][1:], news))
                print (theme, num, tag1.attrib['href'][1:], news)
                counter += 1
                all_count += 1
        except:
            pass
            # print("problem number is", num)
    print ("theme:", theme, counter)
    with open('data_'+theme+'.pickle', 'wb') as f:
        pickle.dump(data, f)
print ("all text counter:", all_count)
