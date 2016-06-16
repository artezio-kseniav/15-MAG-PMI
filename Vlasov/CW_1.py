import collections.defaultdict as dd
from lxml import html
import json
import requests

url = 'http://www.independent.co.uk'
papers = dd(list)

def getArticlesByDay(url):
    tree = html.fromstring(requests.get(url).content)
        for el in tree.xpath('//ol[@class="margin archive-news-list"]/li/a'):
            link = el.get('href')
                print link
                    topic = '/'.join(link.split('/')[1:-1])
                    papers[topic].append(get_article(base_url + link))

def getArticle(url):
    tree = html.fromstring(requests.get(url).content)
        xpath = tree.xpath('//div[@class="text-wrapper"]/p')
        return '\n'.join(p.text.encode('utf8') for p in xpath if p.text)

if __name__ == "__main__":
    
    for date in xrange(10,15):
        get_articles_by_day('%s/archive/2016-05-%s'% (url, date))

    with open('news.json', 'w') as out:
        json.dump(papers, out)