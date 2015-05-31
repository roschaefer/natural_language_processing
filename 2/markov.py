from collections import defaultdict
import math

class Model:
    def __init__(self, word_tag_sentences):
        self.word_tag_sentences = word_tag_sentences
        self.__train(word_tag_sentences)

    def __train(self, word_tag_sentences):
        self.tag_unigrams = defaultdict(int)
        self.context = defaultdict(int)
        self.transition = defaultdict(int)
        self.emit = defaultdict(int)
        self.possible_tags = set([])
        for sentence in word_tag_sentences:
            previous = '<s>'
            self.context[previous] += 1
            for word, tag in sentence:
                self.tag_unigrams[tag] += 1
                self.transition[(previous, tag)] += 1
                self.context[word] += 1
                self.emit[(tag, word)] += 1
                self.possible_tags.add(tag)
                previous = tag
            self.transition[(previous, '</s>')] += 1


    def test(self, sentence):
        self.current_sentence = sentence
        return None

    def prob_t(self, tag, previous_tag):
        # TODO: smoothing
        return float(self.transition[(previous_tag, tag)]) / float(self.tag_unigrams[tag])

    def prob_e(self, word, tag):
        return float(self.emit[(tag, word)]) / float(self.context[word])

    def best_score(self, index, tag):
        scores = []
        if (index == 0):
            return 0
        word = self.current_sentence[index]
        for previous_tag in self.possible_tags:
                score = self.best_score(index - 1, previous_tag) + math.log(self.prob_t(tag,previous_tag)) + math.log(self.prob_e(word, previous_tag))
                scores.append(score)
        return 1
