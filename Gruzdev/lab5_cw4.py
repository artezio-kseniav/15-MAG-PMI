# Models of corpus linguistics. Task 5.
#
# Perform SVD & apply some algorithms from scikit-learn for 20newsgroup dataset
#

from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import TruncatedSVD
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import cross_validation
from sklearn import ensemble
from sklearn.grid_search import GridSearchCV
import matplotlib.pyplot as plt
import numpy as np

import warnings
warnings.simplefilter("ignore")

# Download 20newsgroups dataset
dataset_small = fetch_20newsgroups(
    categories=['sci.space', 'comp.graphics', 'comp.sys.ibm.pc.hardware', 'comp.windows.x',
                'sci.electronics'], subset='all')

# Print some info
print "-----------------------"
print "Summary:"
print "-----------------------"
print 'Topics:'
for name in dataset_small.target_names:
    print " " + name
print "-----------------------"
print 'Categories number:', len(dataset_small.target_names)
print 'Total length:', len(dataset_small.data)
print "-----------------------"


# Transform data to TF/IDF
tf_idf_vectorizer = TfidfVectorizer(stop_words='english', analyzer='word')
tf_idf_index = tf_idf_vectorizer.fit_transform(dataset_small.data)
print "Matrix's shape: ", tf_idf_index.shape
top_k = 200
svd = TruncatedSVD(n_components=top_k, random_state=50010)
transformed_svd = svd.fit_transform(tf_idf_index)
explained_variance = svd.explained_variance_ratio_.sum()
print("Explained variance of the SVD step: {}%".format(int(explained_variance * 100)))

# Split randomly dataset
X_train, X_test, y_train, y_test = train_test_split(transformed_svd, dataset_small.target, test_size = 0.3)
print("Length of train data : {}".format(len(X_train)))
print("Length of test data: {}".format(len(X_test)))

# Let's try Random Forest
tree_number = [10, 20]
max_depthes = [8, 10]
max_features = [10, 20]
criters = ['gini', 'entropy']
rf = ensemble.RandomForestClassifier(n_jobs=4)
grid = GridSearchCV(rf, param_grid={'n_estimators': tree_number, 'max_depth': max_depthes,
                                    'criterion': criters, 'bootstrap': [True], 'max_features': max_features}, cv=3)
grid.fit(X_train, y_train)
print 'CV Accuracy of Random Forest: ', grid.best_score_

# Let's try GBT
gbm_grid = GridSearchCV(
    estimator = ensemble.GradientBoostingClassifier(warm_start=True, random_state=10),
    param_grid = {'n_estimators': [10, 20], 'max_depth': [2, 3, 4], 'max_features': [10, 15, 20],
                  'learning_rate': [1e-1, 1] }, cv = 3, n_jobs = 4)

gbm_grid.fit(X_train, y_train)
print 'CV Accuracy of GBT: ', gbm_grid.best_score_

top_l_words = 3
# Words which characterized hidden topics
for j, component in enumerate(svd.components_):
    print("Component {}, top {} words:".format(j+1, top_l_words))
    p = np.argsort(component)
    words = np.asarray(tf_idf_vectorizer.get_feature_names())[p[-(top_l_words+1):-1]][:]
    for word in words:
        print "    " + word