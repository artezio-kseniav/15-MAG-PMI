from grab import Grab
import time

def parse():

    g = Grab()
    base_url = 'https://www.buzzfeed.com'
    appendix_1 = '/?p='
    topics = ['world', 'politics', 'business', 'lgbt', 'tech', 'science', 'music', 'animals', 'travel', 'style', 'sports']

    data = {}
    for topic in topics:
        articles_list = []
        for page in range(1, 10):
            time.sleep(0.2)
            g.go(base_url + '/' + topic + appendix_1 + str(page))
            urls = getPageUrls(g.response.body)
            for url in urls:
                g.go(base_url + url)
                article = getArticle(g.response.body)
                if len(article) > 1:
                    articles_list.append(article)
        data.update({topic: articles_list})

    data_size = 0
    for topic in data.keys():
        data_size += len(data[topic])
    print "{} articles in {} topics".format(data_size, len(data))

def getPageUrls(mainPage):
    result = []
    i = 0
    for item in mainPage.split("<a class='lede__link' href='"):
        if (i > 0 and i%2 == 0):
            result.append(item.split("'")[0])
        i += 1

    return result

def getArticle(mainPage):
    result = []
    i = 0

    if "buzz_superlist_item_text" in mainPage:
        for item in mainPage.split("buzz_superlist_item_text")[1].split("<div>")[0].split("<p>"):
            if (i > 0 and "<div" not in item):
                result.append(item)
            i += 1

    return ' '.join(result)


parse()
##RESULT: 763 articles in 11 topics
## We need to increase number of pages to get more articles

