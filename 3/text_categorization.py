import os
from IPython import embed

from sklearn.feature_extraction.text import CountVectorizer


class DataSet:
    def __init__(self, folder):
        self.folder = folder
        self.data  = list()
        self.target = list()
        training_folder = self.folder + "/training/"
        self.target_names = sorted(next(os.walk(training_folder))[1])

        for i,n in enumerate(self.target_names):
                folder = training_folder + "/" + n + "/"
                for subdir, dirs, files in os.walk(folder):
                    for file in files:
                        with open(os.path.join(subdir,file),'r') as my_file:
                            self.data.append(my_file.read())
                        self.target.append(i)



if __name__ == "__main__":
    count_vect = CountVectorizer()
    input = DataSet("../ohsumed-first-20000-docs/")
    X_train_counts = count_vect.fit_transform(input.data)
    X_train_counts.shape
    embed()
