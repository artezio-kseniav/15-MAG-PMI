#!/usr/bin/env python

import re
import requests
import urllib2
from bs4 import BeautifulSoup
if __name__ == '__main__':
    base_url = 'https://cyberleninka.ru/article/c/%s/%i'
    categories = ['informatika', 'istoriya-istoricheskie-nauki']

    urls_by_categories = {}
    for category in categories:
        tmpurls = []
        s = requests.Session()
        
        for i in xrange(1, 100):  # range of pages
            page = s.get(base_url % (category, i), verify=False)
            soup = BeautifulSoup(page.text, 'html.parser')
            articles = soup.find_all('div', {'class': 'col-right'})
            # print articles
            for art in articles:
                if art.span.a.has_attr('href'):
                    tmpurl = 'https://cyberleninka.ru' + art.span.a.get('href')#.strip()
                    tmpurls.append(tmpurl)
        urls_by_categories[category] = tmpurls

    corpus = []
    regex = re.compile('[a-zA-Z]')
    for cat, urls in urls_by_categories.iteritems():
        for url in urls:
            page = s.get(url, verify=False)
            soup = BeautifulSoup(page.text, 'html.parser')

            title = soup.find('span', attrs={'itemprop': 'headline'}).text.strip()
            if regex.search(title):
                continue
            text = soup.find('p', attrs={'itemprop': 'articleBody'}).text.strip('<br/>')#.findAll('br')

            ready_article = (cat, title, text)
            corpus.append(ready_article)

    print len(corpus)

    f = open('corpus.csv', 'w')
    for article in corpus:
        f.write('%s;%s;t: %s\r\n' % (article[0].encode('utf8'), article[1].encode('utf8'), article[2].encode('utf8')))

    f.close()
