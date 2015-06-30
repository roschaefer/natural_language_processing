import os
from IPython import embed



class DataSet:
    def __init__(self, folder, subset="training"):
        self.folder = folder
        self.data  = list()
        self.target = list()
        subset_folder = self.folder + "/" + subset + "/"
        self.target_names = sorted(next(os.walk(subset_folder))[1])

        for i,n in enumerate(self.target_names):
                folder = subset_folder + "/" + n + "/"
                for subdir, dirs, files in os.walk(folder):
                    for file in files:
                        with open(os.path.join(subdir,file),'r') as my_file:
                            self.data.append(my_file.read())
                        self.target.append(i)



if __name__ == "__main__":
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.feature_extraction.text import TfidfTransformer
    from sklearn.pipeline import Pipeline
    from sklearn import metrics
    import stopwords


    training = DataSet("../ohsumed-first-20000-docs/")
    text_clf = Pipeline([('vect', CountVectorizer(stop_words = stopwords.LIST)), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB()) ])
    text_clf = text_clf.fit(training.data, training.target)

    test = DataSet("../ohsumed-first-20000-docs/", subset="test")
    predicted = text_clf.predict(test.data)
    print(metrics.classification_report(test.target, predicted, target_names=test.target_names))
