from collections import defaultdict
class Model:
    def __init__(self, word_tag_sentences):
        self.word_tag_sentences = word_tag_sentences
        self.__train(word_tag_sentences)

    def __train(self, word_tag_sentences):
        self.context = defaultdict(int)
        for sentence in word_tag_sentences:
            for word, tag in sentence:
                self.context[word] += 1


