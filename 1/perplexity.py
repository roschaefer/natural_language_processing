import xml.etree.ElementTree as ET

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

        def count_bigram(self, bigram):
            return self.bigrams.count(bigram) + 1 # laplace smoothing

        def count_word(self, word):
            return self.words.count(word)

        def probability(self, bigram):
                return (self.count_bigram(bigram)/self.count_word(bigram[1]))

        def probabilities(self):
                probabilities = []
                for bigram in self.bigrams:
                        probabilities.append(self.probability(bigram))
                return probabilities
        def perplexity(self):
                perplexity = 1
                for p in self.probabilities():
                        perplexity *= p
                return perplexity


article = GeniusArticle('./GENIA_treebank_v1/10022435.xml')
bigram = Bigram([article])
output = bigram.perplexity()
print(output)

