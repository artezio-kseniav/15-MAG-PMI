
import io
import math
import nltk
import string
import lxml.html as html
topics=['business','politics']
all_text=[]
corpus={}
for i in topics:

    page=html.parse('http://www.gazeta.ru/'+i+'/')

    urls = page.getroot().xpath('//div[@class="pl20 pr20"]//a[@href]/@href')

    for j in urls:
        #print ('http://www.gazeta.ru/'+j)
        new_page = html.parse('http://www.gazeta.ru/'+j)




        texts = new_page.getroot().xpath('//p/text()')
        texts = [''.join(t).encode('utf-8', 'ignore').decode('utf-8') for t in texts]
        page_texts = ''.join(texts)


        page_texts = page_texts.replace('\n', ' ').replace('\r', '')
        page_texts = " ".join(page_texts.split())
        all_text.append(page_texts)
    corpus[i]=all_text
    all_text=[]
        #print  page_texts


def tokenize(corpus):
    news_list = corpus
    words = []
    for text in news_list:
        text_str = ''.join(text)
        line = nltk.word_tokenize(text_str)
        line = [word.encode("utf-8").decode("utf-8").lower() for word in line if word not in string.punctuation
                        and word not in [u'\u2012', u'\u2013', u'\u2014', u'\u2015', u'``', u"''"]]
        words += line
    return words
#arr= tokenize(all_text)
#print type(corpus['politics'])
#print (tokenize(corpus['politics']))

def load_ngrams(in_file):
    input_f = io.open(in_file, "r", encoding='utf8')
    n_dict = {}
    for line in input_f:
        line = line.replace('\n', '').split('\t')
        n_dict[tuple(line[0:])] = int(line[0])
    input_f.close()
    return n_dict


def compute_perplexity(category, n3_gram, n2_gram):
    sum_probability = 0
    unknown_words = 0
    min_probability = 1
    sum_log = 0

    current_probability = {}

    for i in range(2, len(category)):
        try:
            current_probability[i] = (n3_gram[(category[i - 2], category[i - 1], category[i])] + 0.0)/ n2_gram[(category[i - 2], category[i - 1])]
            sum_probability += current_probability
            if current_probability[i] < min_probability:
                min_probability = current_probability[i]
        except KeyError:
            unknown_words += 1
    print (unknown_words, len(category), sum_probability)
    known_words = len(category) - unknown_words
    min_probability /= 10.0
    probability_to_substract = (unknown_words * min_probability + 0.0) / known_words
    for i in range(2, len(category)):
        try:
            sum_log += math.log(current_probability[i] - probability_to_substract, 2)
        except KeyError:
            sum_log += math.log(min_probability, 2)

    return sum_log

n_two_gram=load_ngrams("C://valentina//17.07.2016//2grams-3(1)//2grams-3.txt")
#print (len(n_two_gram.keys()))
n_three_gram=load_ngrams("C://valentina//17.07.2016//3grams-3//3grams-3.txt")
#print (len(n_three_gram.keys()))
arr_business=(tokenize(corpus['business']))
arr_politics=tokenize(corpus['politics'])

business_per=compute_perplexity(arr_business, n_three_gram, n_two_gram)
print ("Perplexity for business = ",2**(-business_per / len(arr_business)))
print ("Perplexity for politics = ",2**(-business_per / len(arr_politics)))