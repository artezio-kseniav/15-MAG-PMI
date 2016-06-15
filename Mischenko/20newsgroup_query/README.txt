A tf-idf-based ranker for simple queries



The 20 newsgroups corpus is converted to a sparse tfidf matrix where the rows 
are the documents and the columns are the terms present in the corpus (using 
scikit-learn's TfidfVectorizer).
  
A given query is converted to a sparse vector based on the tfidf matrix 
previously obtained. This vector will have values of 0 but for the terms 
which match the terms in the matrix. The rows (corresponding to document ids) 
of these non-zero terms are retrieved and ordered by the tfidf weight. The 
top k documents are returned as a result of the query.
Usage



`python newsgroup.py`


To create the conda environment


`conda create -p env --file conda.txt`


`source activate env/`