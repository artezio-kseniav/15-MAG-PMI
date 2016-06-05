import json
from collections import defaultdict

from lxml import html
import requests

base_url = 'http://www.independent.co.uk'
papers = defaultdict(list)

def get_article(url):
	tree = html.fromstring(requests.get(url).content)
	xpath = tree.xpath('//div[@class="text-wrapper"]/p')
	return '\n'.join(p.text.encode('utf8') for p in xpath if p.text)

def get_articles_by_day(url):
	try:
		tree = html.fromstring(requests.get(url).content)
		for el in tree.xpath('//ol[@class="margin archive-news-list"]/li/a'):
			link = el.get('href')
			print link
			topic = '/'.join(link.split('/')[1:-1])
			papers[topic].append(get_article(base_url + link))
	except Exception as e:
		pass

# set date range here
for date in xrange(10,15):
	get_articles_by_day('%s/archive/2016-05-%s'% (base_url, date))

with open('news.json', 'w') as out:
	json.dump(papers, out)