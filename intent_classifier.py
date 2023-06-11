import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import LinearSVC

class IntentClassifier:
    def __init__(self):
        
        self.data = pd.read_csv('C:\\Users\\cagri\\Documents\\proje\\sonlar\\data.csv')
        
        self.count_vect = CountVectorizer()
        self.svm = LinearSVC()

    def train(self):
        
        X_train, y_train = self.data['text'], self.data['intent']
        self.count_vect = CountVectorizer()
        
        X_train_counts = self.count_vect.fit_transform(X_train)
        tfidf_transformer = TfidfTransformer()
        
        X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
        self.svm = LinearSVC().fit(X_train_tfidf, y_train)

    def predict(self, text):
        
        return self.svm.predict(self.count_vect.transform([text]))[0]