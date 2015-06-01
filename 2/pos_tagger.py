import os
import markov
import genia
import random
from IPython import embed

__author__ = "Robert Schaefer"

class PosTagger:
    def __init__(self, location):
        self.location = location
        self.__articles = None

    def articles(self):
        if (self.__articles == None):
            self.__articles = []
            for (self.location, dirnames, filenames) in os.walk(self.location):
                xmlfiles = [ fi for fi in filenames if fi.endswith(".xml") ]
                for filename in xmlfiles:
                    filepath = os.path.join(self.location, filename)
                    self.__articles.append(genia.Article(filepath))
                break
        return self.__articles

    def flatten(self, list):
         return [item for sublist in list for item in sublist]

    def run(self, n=10):
        partitions = self.random_partitions(n)
        for test in partitions:
                training = []
                for p in [p for p in partitions if p != test]:
                    training.extend(p)
                all_wt_sentences = [a.word_tag_sentences for a in training]
                wt_sentences = self.flatten(all_wt_sentences)
                model = markov.Model(wt_sentences)
                for test_sentence in self.flatten([a.word_tag_sentences for a in test]):
                    print(model.tag(test_sentence))

    def random_partitions(self, n = 10, input = None):
        partitions = []
        if (input == None):
            input = self.articles()
        random.shuffle(input)
        for i in range(n):
            partitions.append([])

        for i in range(len(input)):
            partitions[i % n].append(input[i])
        return partitions

    def true_positives(self):
        pass

    def false_positives(self):
        pass

    def precision(self):
        pass


if __name__ == "__main__":
    path = "./GENIA_sample/"
    tagger = PosTagger(path)
    tagger.run(10)
