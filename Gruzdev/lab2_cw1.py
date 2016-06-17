# Models of corpus linguistics. Task 2.
#
# Collect dataset of English texts, which contain at least 2 classes.
#

import grab
import time
import os
import pickle

if os.path.exists("texts.pkl"):
    texts = pickle.load(open("texts.pkl", "rb"))
    count = 0
    category_number = 0
    print "-----------------------"
    print "Summary:"
    print "-----------------------"
    for topic in texts:
        count = count + len(texts[topic])
        category_number = category_number + 1
        print topic + ' contains : ' + str(len(texts[topic])) + ' articles.'
    print "-----------------------"
    print 'Totally: ' + str(count) + ' articles.'
    print 'Total categories: ' + str(category_number)
    print "-----------------------"
else:
    g = grab.Grab()
    print "Parsing NY times in progress..."
    root = 'https://www.nytimes.com'
    topics = ['politics', 'business', 'realestate', 'multimedia', 'opinion', 'technology', 'sports', 'dining']
    texts = {}
    for topic in topics:
        articles_list = []
        time.sleep(0.2)
        g.go(root + '/pages/' + topic)
        html_lines = g.response.body.split('\n')
        # Getting url links
        pages = list()
        for line in html_lines:
            if line.startswith('<a href='):
                elements = line.split("\"")
                if elements[1].endswith('?ref=' + topic):
                    pages.append(elements[1])
        for i in range(0, len(pages), 1):
            g.go(pages[i])
            text = []
            splitted_text = g.response.body.split('\n')
            for j in splitted_text:
                if j.startswith('<p class="story-body-text story-content"'):
                    ind1 = j.find('\">')
                    ind2 = j.find('</p>')
                    article = j[ind1+2:ind2]
                    # Let's remove invalid symbols
                    article = article.lower()
                    s = article.split()
                    words_cleaned = list()
                    for word in s:
                        word = ''.join([i if ord(i) < 128 else '' for i in word])
                        word = word.replace('.', '')
                        word = word.replace(',', '')
                        word = word.replace('-', '')
                        word = word.replace('"', '')
                        word = word.replace('<', '')
                        word = word.replace('>', '')
                        word = word.replace('/', '')
                        word = word.replace('"', '')
                        if not (word.startswith('href') or word == ''):
                            words_cleaned.append(word)
                    for word in words_cleaned:
                        text.append(word)
            if len(text) != 0:
                articles_list.append(text)
        texts.update({topic: articles_list})
    pickle.dump(texts, open("texts.pkl", "wb"))
    print "Parsing NY times has ended..."