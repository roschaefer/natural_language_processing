import os
import markov
import genia
import random
import timeit
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
        self.true_positives = 0
        self.false_positives = 0
        partitions = self.random_partitions(n)
        for test in partitions:
                training = []
                for p in [p for p in partitions if p != test]:
                    training.extend(p)
                self.run_fold(test, training)

    def run_fold(self, test, training):
        training_word_tag_sentences = self.flatten([a.word_tag_sentences for a in training])
        model = markov.Model(training_word_tag_sentences)
        test_word_sentences = self.flatten([a.word_sentences for a in test])
        expected_tagged_sentences = self.flatten([a.word_tag_sentences for a in test])
        for i  in range(len(test_word_sentences)):
            tagged_sentence = model.tag(test_word_sentences[i])
            tp, fp = self.compare(tagged_sentence, expected_tagged_sentences[i])
            self.true_positives += tp
            self.false_positives += fp

    def compare(self, tagged_sentence, expected_sentence):
        tp= 0
        fp= 0
        for i in range(len(tagged_sentence)):
            if (tagged_sentence[i] == expected_sentence[i]):
                tp += 1
            else:
                fp += 1
        return tp, fp


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

    def precision(self):
        return float(self.true_positives)/float(self.true_positives + self.false_positives)


if __name__ == "__main__":
    start = timeit.default_timer()
    path = "./GENIA_treebank_v1/"
    tagger = PosTagger(path)
    tagger.run(2)
    stop = timeit.default_timer()
    print("TP : " , tagger.true_positives)
    print("FP : " , tagger.false_positives)
    print("Precision : ", tagger.precision())
    print("Runtime(sec) : " , stop - start )
