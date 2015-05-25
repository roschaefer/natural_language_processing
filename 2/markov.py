from collections import defaultdict
class Model:
    def __init__(self, word_tag_sentences):
        self.word_tag_sentences = word_tag_sentences
        self.__train(word_tag_sentences)

    def __train(self, word_tag_sentences):
        self.context = defaultdict(int)
        self.transition = defaultdict(int)
        self.emit = defaultdict(int)
        self.possible_tags = set([])
        for sentence in word_tag_sentences:
            previous = '<s>'
            self.context[previous] += 1
            for word, tag in sentence:
                self.transition[(previous, tag)] += 1
                self.context[word] += 1
                self.emit[(tag, word)] += 1
                self.possible_tags.add(tag)
                previous = tag
            self.transition[(previous, '</s>')] += 1
