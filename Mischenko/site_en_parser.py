import lxml.html as html
import newspaper
from newspaper import Article
from grab import Grab

output_file = 'parser.txt'
file = open(output_file, 'a')
url_file = open('url_file.txt', 'a')
topics_file = open('topics.txt', 'a')

number_of_articles = 0

site = 'http://cnn.com'
topics = ['regions', 'politics', 'INTERNATIONAL/', 'entertainment', 'tech', 'sport', 'travel', 'style', 'specials',
          'world']

cnn_paper = newspaper.build(u'http://cnn.com')
corpus = {}
for article in cnn_paper.articles:
    url_file.write(article.url)
    article.download()
    article.parse()
    article.nlp()
    file.write(article.title + '\n' + article.text + '\n')
    number_of_articles += 1
for category in cnn_paper.category_urls():
    topics_file.write(category)

print(number_of_articles)
