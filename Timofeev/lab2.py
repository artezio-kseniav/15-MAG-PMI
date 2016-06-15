import feedparser
import json
import lxml.html as html

rss_topics = ['cnn_world', 'cnn_us', 'cnn_allpolitics', 'cnn_tech', 'cnn_health',
              'cnn_showbiz', 'cnn_travel', 'cnn_living',
              'edition_sport']

jsonDict = dict()

for topic in rss_topics:
    d = feedparser.parse('http://rss.cnn.com/rss/' + topic + '.rss')
    topicDict = dict()
    for e in d.entries:
        print "link: " + e.link
        page = html.parse(e.link)
        topicDict[e.title] = '\n'.join(page.getroot().xpath("//div[@class='l-container'] \
                                                            //div[@class='zn-body__paragraph']//text()"))
    jsonDict[topic] = topicDict

with open('result.json', 'w') as fp:
    json.dump(jsonDict, fp)
