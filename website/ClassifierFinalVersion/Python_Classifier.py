from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
from sklearn.model_selection import GridSearchCV
import pickle

def run(fileName):
    dataframe = pd.read_csv("ClassifierFinalVersion/emails.csv")
    x = dataframe["text"]
    y = dataframe["spam"]
    x_train,y_train = x[0:5724],y[0:5724]

    cv = CountVectorizer()
    features = cv.fit_transform(x_train)

    tuned_parameters = {'kernel': ['rbf','linear'], 'gamma': [1e-3, 1e-4],
                     'C': [1, 10, 100, 1000]}

    model = GridSearchCV(svm.SVC(), tuned_parameters)

    with open('ClassifierFinalVersion/1_modelPickle', 'rb') as modelku:
        model = pickle.load(modelku)

    X = pd.read_csv(fileName)
    return model.predict(cv.transform(X))
