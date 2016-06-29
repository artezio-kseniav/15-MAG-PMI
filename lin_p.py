import lxml.html as html
import re
from selenium import webdriver
import time
from collections import defaultdict

news_url = 'http://www.telegraph.co.uk/news/'
news_topics = ['politics', 'uk', 'world', 'science', 'entertainment']



chrome_driver = webdriver.Chrome("./chromedriver.exe")

news_corpus = defaultdict(list) #словарь новостей, собранных по разделам

for news_topic in news_topics:
    topic_page = news_url + news_topic + '/'  # получаем ссылку на раздел с новостями

    # открываем в webdriver
    chrome_driver.get(topic_page)

    # кликаем кнопку `Load More` для загрузки большего списка новостей
    for iteration in range(0, 30):
        # статус
        print("Clicks: %d out of %d " % (iteration, 30), end = '\r' )

        time.sleep(5)  # даем время на открытие страницы
        elems = chrome_driver.find_elements_by_xpath(
            '//a[@class="load-more__button js-load-more__button"]')  # ищем кнопку
        if len(elems) != 0:  # обработка случая, когда искомой кнопки нет
            elems[0].click()  # Load More
        else:
            break  # соответственно, если кнопки нет, полный список загружен
        time.sleep(5)

    # берем все ссылки на новости со страницы после нажатий кнопки Load More
    found_urls = chrome_driver.find_elements_by_xpath('//div[@class="list-of-entities__item-link"]/a')
    news_urls = []  # список ссылок
    for url in found_urls:
        href = url.get_attribute('href')
        news_urls.append(href)

    # парсинг текста новости и заголовка с каждой полученной страницы
    count = 0
    news_count = len(news_urls)
    for news_page in news_urls:
        # с помощью lxml парсим страницу с новостью
        news_html = html.parse(news_page)

        # данный сайт часто отдельно выделяет первую букву новости, парсим ее для дальнейшей конкатенации с текстом новости
        letters = news_html.getroot().xpath('//span[@class="m_first-letter"]')
        news_first_letter = ''
        if len(letters) != 0:  # обработка случая, когда такого выделения не было
            news_first_letter = ''.join(letters[0].itertext())  # берем первую букву из найденных

        # получаем заголовок новости
        header = news_html.getroot().xpath('//h1[@itemprop="headline name"]/text()')
        # убираем из заголовка лишние '\n'
        news_header = re.sub('\n', '', ''.join(header))

        # получаем текст новости
        text = news_html.getroot().xpath('//div[@class="component-content"]/p/text()')
        text = ''.join(text)
        news_text = text

        # убираем © Telegraph Media Group Limited 2016, если спарсился вместе с текстом новости
        index = text.find('©')
        if index != -1:
            news_text = text[0:text.index('©')]

        # составляем полный текст новости
        news = news_header + '\n' + news_first_letter + ''.join(news_text)

        # добавляем в корпус
        news_corpus[news_topic].append(news)

        # статус
        count += 1
        print("Topic: %s, Parsing progress: %d out of %d " % (news_topic, count, news_count), end = '\r' )


chrome_driver.close()  # Размер корпуса
    news_corpus_size = 0
    for news_topic in news_topics:
        print(news_topic, ": ", len(news_corpus[news_topic]))
        news_corpus_size += len(news_corpus[news_topic])
    print("News Corpus Size : ", news_corpus_size)


# Запись в файл
#with open('./news.txt', 'w', encoding='utf-8') as f:
#       for news_topic in news_topics:
#           f.write(news_topic + '\n')
#           for news in news_corpus[news_topic]:
#               f.write(str(news) + '\n')