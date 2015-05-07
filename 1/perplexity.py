import os
import math
import xml.etree.ElementTree as ET
from collections import defaultdict

class Runner():
        def create_test_and_training_sets(self, input):
                test, training = [],[]
                for i in range(0,len(input)):
                    if (i % 10 == 0):
                        test.append(input[i])
                    else:
                        training.append(input[i])
                return test, training

        def get_articles(self, folder):
                articles = []
                for (folder, dirnames, filenames) in os.walk(folder):
                    xmlfiles = [ fi for fi in filenames if fi.endswith(".xml") ]
                    for filename in xmlfiles:
                        filepath = os.path.join(folder, filename)
                        articles.append(GeniusArticle(filepath))
                    break
                return articles

class LanguageModel():
        def __init__(self, training_data):
            self.training_data = training_data
            self.__counted_unigrams = None
            self.__counted_bigrams = None

        def number_of_unique_words(self):
            return len(self.counted_unigrams())


        def likelihood(self, bigram):
            w1 = self.counted_unigrams()[bigram[0]]
            w2_given_w1 = self.counted_bigrams()[bigram]
            p = float(w2_given_w1)/float(w1)
            return p

        def likelihood_laplace(self, bigram):
            w1 = self.counted_unigrams()[bigram[0]]
            w2_given_w1 = self.counted_bigrams()[bigram]
            p = float(w2_given_w1 + 1)/float(w1 + self.number_of_unique_words())
            return p

        def perplexity_per_sentence(self, sentence):
            pps = 1
            bigrams = list(zip(sentence, sentence[1:]))
            exponent = -float(1)/len(bigrams)
            for bigram in bigrams:
                p = self.likelihood_laplace(bigram)
                pps *= math.pow(p, exponent)
            return pps

        def raw_unigrams(self):
            unigrams = []
            for sentence in self.training_data:
                for word in sentence:
                    unigrams.append(word)
            return unigrams

        def counted_unigrams(self):
            if (self.__counted_unigrams == None):
                self.__counted_unigrams = self.__counted(self.raw_unigrams())
            return self.__counted_unigrams

        def raw_bigrams(self):
            raw_bigrams = []
            for sentence in self.training_data:
                raw_bigrams.extend(list(zip(sentence, sentence[1:])))
            return raw_bigrams

        def counted_bigrams(self):
            if (self.__counted_bigrams == None):
                self.__counted_bigrams = self.__counted(self.raw_bigrams())
            return self.__counted_bigrams

        def __counted(self, somelist):
            counted_something = defaultdict(int)
            for something in somelist:
                counted_something[something] += 1
            return counted_something



class GeniusArticle:
        def __init__(self, location):
                self.location = location
                self.__tree   = None

        def tree(self):
            if (self.__tree == None):
                self.__tree  = ET.parse("./{location}".format(location=self.location))
            return self.__tree

        def article(self):
                return self.tree().getroot()[0][0][0][1]

        def abstract(self):
                return self.article()[1][0]

        def title(self):
                return self.article()[0]

        def sentences(self):
                return self.__get_sentences(self.article())

        def __get_sentences(self, xml_branch):
                sentences = []
                for sentence in xml_branch.findall('.//sentence'):
                        words = []
                        for token in sentence.findall('.//tok'):
                            words.append(token.text)
                        sentences.append(words)
                return sentences


if (__name__ == "__main__"):
    mypath = "./GENIA_treebank_v1/"
    runner = Runner()
    test, training = runner.create_test_and_training_sets(runner.get_articles(mypath))
    test_sentences = []
    training_sentences = []
    for article in training:
        training_sentences.extend(article.sentences())
    for article in test:
        test_sentences.extend(article.sentences())
    model = LanguageModel(training_sentences)

    sum = 0
    for sentence in test_sentences:
        sum += model.perplexity_per_sentence(sentence)
    average_perplexity = sum/len(test_sentences)
    print(average_perplexity)


