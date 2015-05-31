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
        self.possible_tags = set()
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



    def prob_t(self, tag, previous_tag):
        vocabulary_size = len(self.tag_unigrams)
        return float(self.transition[(previous_tag, tag)] + 1) / float(self.tag_unigrams[tag] + vocabulary_size)

    def prob_e(self, word, tag):
        vocabulary_size = len(self.context)
        return float(self.emit[(tag, word)] + 1) / float(self.context[word] + vocabulary_size)

    def forward_step(self, sentence):
        sentence = ['<s>'] + sentence
        best_score = {}
        best_edge = {}
        best_score[(sentence[0], '<s>')] = 0
        tags_to_start = ['<s>']
        tags_to_start.extend(self.possible_tags)
        for word, next_word in zip(sentence[0::1], sentence[1::1]):
            for prev in tags_to_start:
                for next in self.possible_tags:
                    print(word, next_word, prev, next)
                    if (((word, prev) in best_score) and ((prev, next) in self.transition)):
                        score = best_score[(word, prev)] - math.log(self.prob_t(next,prev)) - math.log(self.prob_e(word, next))
                        if (((next_word, next) not in best_score) or (best_score[(next_word, next)] > score)):
                                best_score[(next_word, next)] = score
                                best_edge[(next_word, next)] = (word, prev)
        return best_score, best_edge
