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
        # some auxiliary variables
        self.vocabulary_size_t = len(self.tag_unigrams)
        self.vocabulary_size_e = len(self.context)
        self.tags_to_start = ['<s>']
        self.tags_to_start.extend(self.possible_tags)



    def prob_t(self, tag, previous_tag):
        return float(self.transition[(previous_tag, tag)] + 1) / float(self.tag_unigrams[tag] + self.vocabulary_size_t)

    def prob_e(self, word, tag):
        return float(self.emit[(tag, word)] + 1) / float(self.context[word] + self.vocabulary_size_e)

    def forward_step(self, sentence):
        sentence = ['<s>'] + sentence + ['</s>']
        best_score = {}
        best_edge = {}
        best_score[(0, '<s>')] = 0
        for i in range(0, len(sentence)-2):
            for prev in self.tags_to_start:
                for next in self.possible_tags:
                    if (((i, prev) in best_score) and ((prev, next) in self.transition)):
                        score = best_score[(i, prev)] - math.log(self.prob_t(next,prev)) - math.log(self.prob_e(sentence[i+1], next))
                        if (((i+1, next) not in best_score) or (best_score[(i+1, next)] > score)):
                                best_score[(i+1, next)] = score
                                best_edge[(i+1, next)] = (i, prev)
        # end tag
        for prev in self.possible_tags:
            i = len(sentence)-2
            next = '</s>'
            if (((i, prev) in best_score) and ((prev, next) in self.transition)):
                score = best_score[(i, prev)] - math.log(self.prob_t(next,prev)) - math.log(self.prob_e(sentence[i+1], next))
                if (((i+1, next) not in best_score) or (best_score[(i+1, next)] > score)):
                        best_score[(i+1, next)] = score
                        best_edge[(i+1, next)] = (i, prev)
        return best_score, best_edge

    def backward_step(self, sentence, best_edge):
        current_edge = best_edge[(len(sentence) + 1 , "</s>")] # +2 for <s> and </s> tags
        result = []
        while (current_edge != (0, "<s>")):
            word = sentence[current_edge[0] - 1]
            tag = current_edge[1]
            result.append((word, tag))
            current_edge = best_edge[current_edge]
        result = list(reversed(result))
        return result


    def tag(self, sentence):
        best_score, best_edge = self.forward_step(sentence)
        return self.backward_step(sentence, best_edge)
