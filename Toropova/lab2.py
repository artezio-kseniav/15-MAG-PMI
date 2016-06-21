import json
from collections import defaultdict

from lxml import html
import requests

base_url = 'http://www.euronews.com/sport'
papers = defaultdict(list)


def get_text(url):
    tree = html.fromstring(requests.get(url).content)
    xpath = tree.xpath('//div[@class="article-text"]/p')
    return '\n'.join(p.text.encode('utf8') for p in xpath if p.text)


def get_articles(url):
	try:
		tree = html.fromstring(requests.get(url).content)
		for el in tree.xpath('//div[@class="themeArtTitle"]/a'):
			link = el.get('href')
			print link
			topic = '/'.join(link.split('/')[1:-1])
			papers[topic].append(get_text(base_url + link))
	except Exception as e:
		pass

for date in xrange(10,15):
	get_articles(base_url, date)

with open('sport.json', 'w') as out:
	json.dump(papers, out)