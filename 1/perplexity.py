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

        def number_of_unique_words(self):
            return len(self.counted_unigrams())

        def likelihood(self, bigram):
            w1 = self.counted_unigrams()[bigram[0]]
            w2_given_w1 = self.counted_bigrams()[bigram]
            p = float(w2_given_w1)/float(w1)
            return p


        def raw_unigrams(self):
            unigrams = []
            for sentence in self.training_data:
                for word in sentence:
                    unigrams.append(word)
            return unigrams

        def counted_unigrams(self):
            return self.__counted(self.raw_unigrams())

        def raw_bigrams(self):
            raw_bigrams = []
            for sentence in self.training_data:
                raw_bigrams.extend( list(zip(sentence, sentence[1:])))
            return raw_bigrams

        def counted_bigrams(self):
            return self.__counted(self.raw_bigrams())

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


class Bigram:
        def __init__(self, articles):
                self.words = []
                self.bigrams = []
                for article in articles:
                    for sentence in article.sentences():
                        self.words.extend(sentence)
                        self.bigrams.extend((list(zip(sentence, sentence[1:]))))
                self.__word_dict = dict()
                self.__bigram_dict = dict()

        def count_bigram(self, bigram):
                if not ( bigram in self.__bigram_dict):
                        self.__bigram_dict[bigram] = self.bigrams.count(bigram) + 1 # laplace smoothing
                return self.__bigram_dict[bigram]

        def count_word(self, word):
                if not ( word in self.__word_dict):
                        self.__word_dict[word] = self.words.count(word) + 1
                return self.__word_dict[word]

        def probability(self, bigram):
                return (self.count_bigram(bigram)/self.count_word(bigram[1]))

        def perplexity(self, otherBigram):
                perplexity = 0
                for bigram in otherBigram.bigrams:
                        perplexity += math.log(self.probability(bigram))
                return perplexity

def ten_chunks(array):
    chunks = []
    for i in range(0, len(array), 10):
        chunks.append(array[i:i+10])
    return chunks

if (__name__ == "__main__"):
    mypath = "./GENIA_treebank_v1/"

    articles = []
    for (mypath, dirnames, filenames) in os.walk(mypath):
        xmlfiles = [ fi for fi in filenames if fi.endswith(".xml") ]
        for filename in xmlfiles:
            filepath = os.path.join(mypath, filename)
            articles.append(GeniusArticle(filepath))
        break

    chunks = ten_chunks(articles)
    test = chunks[0]
    training = []
    for chunk in chunks[1:]:
        training.extend(chunk)


    #articles = [GeniusArticle("./GENIA_treebank_v1/10022435.xml")]
    test_bigram = Bigram(test)
    training_bigram = Bigram(training)

    output = training_bigram.perplexity(test_bigram)
    print(output)

