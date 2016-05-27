""" Parser of news with using selenium. """

__author__ = 'Ksenia Voronaya'

import lxml.html as html
from selenium import webdriver
import time

# Works fine with Firefox for me
driver = webdriver.Firefox()

# Canadian global news
base_url = 'http://globalnews.ca/'

# Found all possible topics on the website:
topics = ['world', 'canada', 'politics', 'money', 'entertainment', 'health',
          'lifestyle', 'tech', 'science', 'sports']

corpus = {}
for topic in topics:
    url = base_url + topic + '/'
    driver.get(url)
    # Need to use selenium action click 10 times in order to load more news
    for x in xrange(0, 10):
        # Wait while page loads
        time.sleep(3)
        # To load more news - clicking on "load more" button
        driver.find_element_by_xpath('//a[@id="lm_id_gnca_category_loadmore"]').click()
        time.sleep(3)

    find_all_urls = driver.find_elements_by_xpath('//div[@class="story story-float-img"]'
                                                  '/article//*[@class="story-h"]//a[@href]')
    hrefs = []
    # Getting urls for each news with specific topic
    for url in find_all_urls:
        href = url.get_attribute('href')
        hrefs.append(href)

    articles_list = []
    try:
        for url in hrefs:
            page = html.parse(url)
            # Getting article header
            page_header = page.getroot().xpath('//article/h1[@class="story-h"]/text()')
            page_header = ''.join(page_header)
            # Getting article text
            page_text = page.getroot().xpath('//div[@class="story-txt"]'
                                             '//span[@itemprop="articleBody"]/p/text()')
            page_text = ''.join(page_text)
            # Full article
            full_article = page_header + page_text
            articles_list.append(full_article)
        corpus.update({topic: articles_list})
    except IOError:
        continue

driver.close()

corpus_size = 0
for topic in corpus.keys():
    topic_size = len(corpus[topic])
    corpus_size += topic_size

print "The size of corpus is {} texts \nfor diffrent {} topics".format(corpus_size, len(corpus.keys()))

for topic in corpus.keys():
    topic_size = len(corpus[topic])
    print "The size of topic '{}' is {} texts".format(topic, topic_size)


# Enter a topic for which you want to see a list of full news articles
my_topic = 'money'
print "List of full news articles for topic '{}'".format(my_topic)
print corpus[my_topic]

# Writing full corpus in file
with open(r'C:\Users\kvoronaya\Desktop\parser_news\corpus_news.txt', 'w') as f:
        for theme in topics:
            try:
                f.write("List of full news articles for topic '{}'\n".format(theme))
                f.write(str(corpus[theme]) + '\n')
            except KeyError:
                continue
