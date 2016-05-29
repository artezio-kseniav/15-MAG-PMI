from grab import Grab
from lxml.html import fromstring
from weblib.error import DataNotFound

f = open("/home/vladimir/Documents/PyCharmScripts/Parser/parser_result.txt", "a")
number_of_articles = 0

sites = 'http://www.9news.com.au'
slash = '/'
topics = ['national', 'world', 'politics', 'technology', 'good-news']
grab = Grab()

for topic in topics:
    url = sites + slash + topic

    f.write('--------------------------------\n')
    f.write('CATEGORY:    ' + topic + '\n')
    f.write('URL:         ' + url + '\n')
    f.write('--------------------------------\n')

    grab.go(url)
    news = grab.doc.select('//h2[@class="story-block__title"]')

    for article in news:
        try:
            text = article.select("./a").text()
            url_h = article.select("./a").attr("href")

            grab.go(url_h)
            text_of_article = grab.doc.select('//div[@itemprop="articleBody"]')
            number_of_articles += 1

            f.write('[ DESCRIPTION OF ARTICLE ]' + '\n')
            f.write(repr(fromstring(text).text_content()) + '\n')
            f.write('[ URL OF ARTICLE ]' + '\n')
            f.write(url_h + '\n')
            f.write('[ WHOLE ARTICLE ]' + '\n')
            #f.write(repr(fromstring(text_of_article.text()).text_content()) + '\n')
            f.write(text_of_article.text().encode('ascii', 'ignore') + '\n')
        except DataNotFound:
            continue
        f.write('\n')
f.close()
print number_of_articles
