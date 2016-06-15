import inverted_index as ii
import vector_space_model as vsm

from sklearn.datasets import fetch_20newsgroups


def query_iindex(query, k, newsgroups):

    '''
    Helper function to query the inverted index

    :param query: the query string
    :param k: number of results to display
    :param newsgroups: corpus
    :return: -
    '''

    result = ii.boolean_search(query, iindex)

    print ('The result of the boolean query: {0}'.format(query))

    if result:
        print ('Obtained {0} results'.format(len(result)))

        print ('A subset of {0} results'.format(k))
        for r in result[:k]:
            print newsgroups.filenames[r]
    else:
        print ('No result for this query: {0}'.format(query))


def query_tfidf_vectors(query, k, vectorizer, tfidf_vectors, newsgroups):

    '''
    Helper function to query using tfidf vectors

    :param query: query string
    :param k: number of top ranked results
    :param vectorizer: vectorizer object
    :param tfidf_vectors: the tfidf weighted vectors
    :param newsgroups: corpus
    :return: -
    '''

    result = vsm.rank_documents(query, k, vectorizer, tfidf_vectors)

    if result:
        print ('Top {0} documents as result of the query: {1}'.format(k, query))

        for r in result:
            print newsgroups.filenames[r]
    else:
        print ('No result for this query: {0}'.format(query))


def do_con_search(query):

    tfidf_query = tfidfVectorizer.transform([query])
    words = query.split()
        

    # Find cosine similarity for query and texts
    similarity = {}
    index = 0
    for document in tfidf_index:
        similarity[texts.data[index]] = cosine_similarity(document, tfidf_query)[0][0]
        index += 1

    result = sorted(similarity.values(), reverse=True)

    # Show top-5 the most relevant results
    for i in range(5):
        text = similarity.keys()[similarity.values().index(result[i])]
        lines = text.split('\n')
        print 'Score: ', result[i], '\n'		

if __name__ == '__main__':

    # fetch the 20newsgroups dataset
    newsgroups = fetch_20newsgroups(subset='all')

    # obtain the documents and the words in the 20 newsgroups corpus
    docs, words = ii.read_newsgroups(newsgroups.data)

    print ("Statistics about the corpus")
    print ('Number of documents {0} and number of words {1}'.format(len(docs),
                                                                   len(words)))

    print ("Creating the inverted index...")
    iindex = ii.inverted_index(docs, words)

    # perform boolean queries
    query_iindex('science', 5, newsgroups)
    query_iindex('science and religion', 5, newsgroups)
    query_iindex('science or religion', 5, newsgroups)

    print ("Creating the tfidf vectors...")

    vectorizer, tfidf_vectors = vsm.create_vectors(newsgroups)

    # perform queries using tfidf vectors
    query_tfidf_vectors("science religion", 5, vectorizer, tfidf_vectors,
                        newsgroups)

	do_con_search('corpus linguistics')
	do_con_search('world champions in hockey')